# -*- coding: utf-8 -*-

"""
@author: 猿小天
@contact: QQ:1638245306
@Created on: 2022/1/21 003 0:30
@Remark: 系统配置
"""

import random
import os
import json
import io
import zipfile
import django_filters
from django.db.models import Q
from django_filters.rest_framework import BooleanFilter
from rest_framework import serializers
from rest_framework.views import APIView
import cv2
import numpy as np
from PIL import Image
from django.http import FileResponse, HttpResponse


from application.settings import BASE_DIR
from application import dispatch
from dvadmin.system.models import RecognitionConfig, SystemConfig, FileList, DetectFileList
from dvadmin.utils.json_response import DetailResponse, SuccessResponse, ErrorResponse
from dvadmin.utils.models import get_all_models_objects
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.validator import CustomValidationError
from dvadmin.utils.viewset import CustomModelViewSet
from django.core.files import File
from django.http import StreamingHttpResponse


class SystemConfigCreateSerializer(CustomModelSerializer):
    """
    系统配置-新增时使用-序列化器
    """
    form_item_type_label = serializers.CharField(source='get_form_item_type_display', read_only=True)

    class Meta:
        model = SystemConfig
        fields = "__all__"
        read_only_fields = ["id"]

    def validate_key(self, value):
        """
        验证key是否允许重复
        parent为空时不允许重复,反之允许
        """
        instance = SystemConfig.objects.filter(key=value, parent__isnull=True).exists()
        if instance:
            raise CustomValidationError('已存在相同变量名')
        return value


class RecognitionConfigInitSerializer(CustomModelSerializer):
    """
    初始化获取数信息(用于生成初始化json文件)
    """
    children = serializers.SerializerMethodField()

    def get_children(self, obj: RecognitionConfig):
        data = []
        instance = RecognitionConfig.objects.filter(parent_id=obj.id)
        if instance:
            serializer = RecognitionConfigInitSerializer(instance=instance, many=True)
            data = serializer.data
        return data

    def save(self, **kwargs):
        instance = super().save(**kwargs)
        children = self.initial_data.get('children')
        # 菜单表
        if children:
            for data in children:
                data['parent'] = instance.id
                filter_data = {
                    "key": data['key'],
                    "parent": data['parent']
                }
                instance_obj = RecognitionConfig.objects.filter(**filter_data).first()
                # if instance_obj and not self.initial_data.get('reset'):
                #     continue
                serializer = RecognitionConfigInitSerializer(instance_obj, data=data, request=self.request)
                serializer.is_valid(raise_exception=True)
                serializer.save()
        return instance

    class Meta:
        model = RecognitionConfig
        fields = ['parent', 'title', 'key', 'value', 'sort', 'status', 'data_options', 'form_item_type', 'rule',
                  'placeholder', 'setting', 'creator', 'dept_belong_id', 'children', 'readonly']
        read_only_fields = ["id"]
        extra_kwargs = {
            'creator': {'write_only': True},
            'dept_belong_id': {'write_only': True}
        }


class RecognitionConfigSerializer(CustomModelSerializer):
    """
    系统配置-序列化器
    """
    form_item_type_label = serializers.CharField(source='get_form_item_type_display', read_only=True)

    class Meta:
        model = RecognitionConfig
        fields = "__all__"
        read_only_fields = ["id"]


class RecognitionConfigChildrenSerializer(CustomModelSerializer):
    """
    系统配置子级-序列化器
    """
    children = serializers.SerializerMethodField()
    form_item_type_label = serializers.CharField(source='get_form_item_type_display', read_only=True)

    def get_children(self, instance):
        queryset = RecognitionConfig.objects.filter(parent=instance)
        serializer = RecognitionConfigSerializer(queryset, many=True)
        return serializer.data

    class Meta:
        model = RecognitionConfig
        fields = "__all__"
        read_only_fields = ["id"]


class SystemConfigListSerializer(CustomModelSerializer):
    """
    系统配置下模块的保存-序列化器
    """
    def update(self, instance, validated_data):
        instance_mapping = {obj.id: obj for obj in instance}
        data_mapping = {item['id']: item for item in validated_data}
        for obj_id, data in data_mapping.items():
            instance_obj = instance_mapping.get(obj_id, None)
            if instance_obj is None:
                return SystemConfig.objects.create(**data)
            else:
                return instance_obj.objects.update(**data)

    class Meta:
        model = SystemConfig
        fields = "__all__"
        read_only_fields = ["id"]


class SystemConfigSaveSerializer(serializers.Serializer):
    class Meta:
        read_only_fields = ["id"]
        list_serializer_class = SystemConfigListSerializer


class RecognitionConfigFilter(django_filters.rest_framework.FilterSet):
    """
    过滤器
    """
    parent__isnull = BooleanFilter(field_name='parent', lookup_expr="isnull")

    class Meta:
        model = RecognitionConfig
        fields = ['id', 'parent', 'status', 'parent__isnull']


class RecognitionConfigViewSet(CustomModelViewSet):
    """
    系统配置接口
    """
    queryset = RecognitionConfig.objects.order_by('sort', 'create_datetime')
    serializer_class = RecognitionConfigChildrenSerializer
    # create_serializer_class = SystemConfigCreateSerializer
    retrieve_serializer_class = RecognitionConfigChildrenSerializer
    filter_fields = ['id','parent']
    filter_class = RecognitionConfigFilter

    def save_content(self, request):
        body = request.data
        data_mapping = {item['id']: item for item in body}
        file_info = dict()
        patient_id = 0
        for item in body:
            if item['key'] == "cell_picture":
                file_list = item['value']
                if len(file_list) == 0:
                    return DetailResponse(msg="请上传图片")
                file_info = file_list[0]
            elif item['key'] == 'patient_id':
                patient_id = item['value']

        file_obj = FileList.objects.filter(id=file_info['id']).first()
        url = file_obj.url
        cell_id, cell_name = self.get_recognition(url)
        file_obj.cell_id = cell_id
        file_obj.cell_name = cell_name
        file_obj.patient_id = patient_id
        print(patient_id)
        file_obj.save()
        for obj_id, data in data_mapping.items():
            instance_obj = SystemConfig.objects.filter(id=obj_id).first()
            if instance_obj is None:
                # return SystemConfig.objects.create(**data)
                serializer = SystemConfigCreateSerializer(data=data)
            else:
                serializer = SystemConfigCreateSerializer(instance_obj, data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
        data = {"cell_id": cell_id, "cell_name": cell_name, "patient_id": patient_id}
        return DetailResponse(msg="保存成功", data=data)

    def save_multi(self, request):
        body = request.data
        file_info = dict()
        file_list = []
        cell_ids = []
        cell_names = []
        patient_id = 0
        for key, item in body.items():
            if key == "cell_picture":
                file_list = item
                if len(file_list) == 0:
                    return DetailResponse(msg="图片数量为零")
            elif key == 'patient_id':
                patient_id = item

        for file_info in file_list:
            file_obj = FileList.objects.filter(id=file_info['id']).first()
            url = str(file_obj.url)
            cell_id, cell_name = self.get_recognition(url)
            file_obj.cell_id = cell_id
            file_obj.cell_name = cell_name
            cell_ids.append(cell_id)
            cell_names.append(cell_name)
            file_obj.patient_id = patient_id
            file_obj.save()
        data = {"cell_ids": cell_ids, "cell_names": cell_names, "patient_id": patient_id}
        return DetailResponse(msg="保存成功", data=data)

    def save_detect(self, request):
        body = request.data
        file_info = dict()
        file_list = []
        cell_slices = []
        cell_detect = []
        patient_id = 0
        for key, item in body.items():
            if key == "cell_picture":
                file_list = item
                if len(file_list) == 0:
                    return DetailResponse(msg="图片数量为零")
            elif key == 'patient_id':
                patient_id = item

        for file_info in file_list:
            print(file_info['id'])
            file_obj = DetectFileList.objects.filter(id=file_info['id']).first()
            # if file_obj == None:
            #     continue
            url = 'media/' + str(file_obj.url)
            name = file_obj.name
            res_url, cell_slice = self.get_detect(name, url)
            cell_slices.extend(cell_slice)
            cell_detect.append(res_url)
        data = {"cell_detect": cell_detect, "patient_id": patient_id, "cell_slices":cell_slices}
        return DetailResponse(msg="保存成功", data=data)
        

    def get_recognition(self, file):
        cell_id = random.randint(1, 11)
        CELL_ITEM_LIST = ["待识别", "原始细胞", "淋巴细胞", "单核细胞", "浆细胞", "红细胞", "早幼粒细胞", "嗜中性中幼粒细胞", \
         "嗜中性晚幼粒细胞", "嗜中性杆状核细胞", "嗜中性分页核细胞", "嗜酸性粒细胞", "其他细胞"]
        cell_name = CELL_ITEM_LIST[cell_id]
        return cell_id, cell_name


    def get_detect(self, file_name, file_url):
        file_info = os.path.splitext(file_name)[0]
        json_file = file_info + '.json'
        json_file = os.path.join(BASE_DIR, 'media', 'point', json_file)
        img_file = os.path.join(BASE_DIR, *file_url.split('/'))
        data = dict()
        if os.path.exists(json_file):
            with open(json_file, 'r') as f:
                data = json.load(f)
        else:
            data['shapes'] = []
        print(img_file)
        img = Image.open(img_file)
        w, h = img.size
        img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
        cell_slices = []
        idx = 0
        for s in data['shapes']: 
            if s["shape_type"] != "rectangle":
                continue
            pts = np.array(s['points']).astype(np.int)
            x1  = max(min(pts[:, 0]), 0)
            y1  = max(min(pts[:, 1]), 0)
            x2  = min(max(pts[:, 0]), w - 1)
            y2  = min(max(pts[:, 1]), h - 1)
            if y1 >= y2 or x1 >= x2:
                continue
            cut_img = img[y1:y2, x1:x2]
            print(x1, y1, x2, y2)
            cut_img = Image.fromarray(cv2.cvtColor(cut_img, cv2.COLOR_BGR2RGB))
            cut_obj = self.file2obj(cut_img, file_info + str(idx))
            cell_slices.append('media/' + str(cut_obj.url))
            idx += 1

        for s in data['shapes']: 
            if s["shape_type"] != "rectangle":
                continue
            pts = np.array(s['points']).astype(np.int)
            x1  = max(min(pts[:, 0]), 0)
            y1  = max(min(pts[:, 1]), 0)
            x2  = min(max(pts[:, 0]), w - 1)
            y2  = min(max(pts[:, 1]), h - 1)
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 3)

        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        res_obj = self.file2obj(img, file_info)
        # with open(res_file, 'rb') as f:
        #     res_obj = DetectFileList.objects.create(url=File(f), name=file_info + '_res.jpg')
        #     res_obj.save()
        res_url = 'media/' + str(res_obj.url)
        return res_url, cell_slices

    def get_zip(self, request):
        body = request.data
        file_list = []
        for key, item in body.items():
            if key == "files":
                file_list = item
        # zip_file = os.path.join(BASE_DIR, 'media', 'zip', 'tmp.zip')
        zip_io = io.BytesIO()
        z = zipfile.ZipFile(zip_io, 'w', zipfile.ZIP_DEFLATED)
        for file in file_list:
            z.write(file, os.path.split(file)[1])
        z.close()
        zip_io.seek(0)
        # response = StreamingHttpResponse(self.file_iterator(zip_file))
        # response['Content-Type'] = 'application/octet-stream'
        # response['Content-Disposition'] = 'attachment;filename="{0}"'.format('res.zip')
        # response = FileResponse(zip_io, as_attachment=True, filename="res.zip") 
        response = HttpResponse(content_type='application/x-zip-compressed')
        response['Content-Disposition'] = 'attachment; filename=test.zip'
        response.write(zip_io.getvalue())
        return response


        

    def file2obj(self, img, file_info):
        f = io.BytesIO()
        f.name = 'tmp.jpg'
        img.save(f, format='jpeg')
        f.seek(0)
        res_obj = DetectFileList.objects.create(url=File(io.BufferedReader(f)), name=file_info + '_res.jpg')
        res_obj.save()
        return res_obj

    def file_iterator(self, filename, chunk_size=512):
        with open(filename,'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

        
        



    # def get_association_table(self, request):
    #     """
    #     获取所有的model及字段信息
    #     """
    #     res = [ele.get('table') for ele in get_all_models_objects().values()]
    #     return DetailResponse(msg="获取成功", data=res)

    # def get_table_data(self, request, pk):
    #     """
    #     动态获取关联表的数据
    #     """
    #     instance = SystemConfig.objects.filter(id=pk).first()
    #     if instance is None:
    #         return ErrorResponse(msg="查询出错了~")
    #     setting = instance.setting
    #     if setting is None:
    #         return ErrorResponse(msg="查询出错了~")
    #     table = setting.get('table')  # 获取model名
    #     model = get_all_models_objects(table).get("object", {})
    #     # 自己判断一下不存在
    #     queryset = model.objects.values()
    #     body = request.query_params
    #     search_value = body.get('search', None)
    #     if search_value:
    #         search_fields = setting.get('searchField')
    #         filters = Q()
    #         filters.connector = 'OR'
    #         for item in search_fields:
    #             filed = '{0}__icontains'.format(item.get('field'))
    #             filters.children.append((filed, search_value))
    #         queryset = model.objects.filter(filters).values()
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         return self.get_paginated_response(queryset)
    #     return SuccessResponse(msg="获取成功", data=queryset, total=len(queryset))

    # def get_relation_info(self, request):
    #     """
    #     查询关联的模板信息
    #     """
    #     body = request.query_params
    #     var_name = body.get('varName', None)
    #     table = body.get('table', None)
    #     instance = SystemConfig.objects.filter(key=var_name, setting__table=table).first()
    #     if instance is None:
    #         return ErrorResponse(msg="未获取到关联信息")
    #     relation_id = body.get('relationIds', None)
    #     relationIds = []
    #     if relation_id is None:
    #         return ErrorResponse(msg="未获取到关联信息")
    #     if instance.form_item_type in [13]:
    #         relationIds = [relation_id]
    #     elif instance.form_item_type in [14]:
    #         relationIds = relation_id.split(',')
    #     queryset = SystemConfig.objects.filter(value__in=relationIds).first()
    #     if queryset is None:
    #         return ErrorResponse(msg="未获取到关联信息")
    #     serializer = SystemConfigChinldernSerializer(queryset.parent)
    #     return DetailResponse(msg="查询成功", data=serializer.data)


class InitSettingsViewSet(APIView):
    """
    获取初始化配置
    """
    authentication_classes = []
    permission_classes = []

    def filter_system_config_values(self, data: dict):
        """
        过滤系统初始化配置
        :param data:
        :return:
        """
        if not self.request.query_params.get('key', ''):
            return data
        new_data = {}
        for key in self.request.query_params.get('key', '').split('|'):
            if key:
                new_data.update(**dict(filter(lambda x: x[0].startswith(key), data.items())))
        return new_data

    def get(self, request):
        data = dispatch.get_system_config()
        if not data:
            dispatch.refresh_system_config()
            data = dispatch.get_system_config()
        # 不返回后端专用配置
        backend_config = [f"{ele.get('parent__key')}.{ele.get('key')}" for ele in
                          SystemConfig.objects.filter(status=False, parent_id__isnull=False).values('parent__key',
                                                                                                    'key')]
        data = dict(filter(lambda x: x[0] not in backend_config, data.items()))
        data = self.filter_system_config_values(data=data)
        return DetailResponse(data=data)
