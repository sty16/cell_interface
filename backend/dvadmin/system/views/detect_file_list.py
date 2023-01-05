from rest_framework import serializers

from dvadmin.system.models import DetectFileList
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet


class DetectFileSerializer(CustomModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    def get_url(self, instance):
        return 'media/' + str(instance.url)

    class Meta:
        model = DetectFileList
        fields = "__all__"

    def create(self, validated_data):
        validated_data['name'] = str(self.initial_data.get('file'))
        validated_data['url'] = self.initial_data.get('file')
        return super().create(validated_data)


class DetectFileViewSet(CustomModelViewSet):
    """
    文件管理接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = DetectFileList.objects.all()
    serializer_class = DetectFileSerializer
    filter_fields = ['name', 'id', 'patient_id']
    permission_classes = []
