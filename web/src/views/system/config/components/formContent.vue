<template>
  <div>
    <el-row :gutter="20">
      <el-col :span="12">变量标题</el-col>
      <el-col :span="12">变量值</el-col>
    </el-row>
    <el-form ref="form" :model="form" label-width="360px" label-position="left" style="margin-top: 20px">
      <el-form-item :label="item.title" :prop="['array'].indexOf(item.form_item_type_label) >-1?'':item.key"
                    :key="index" :rules="item.rule || []"
                    v-for="(item,index) in formList"

      >
        <template slot="label">
          <el-input v-if="item.edit" v-model="item.title" style="display: inline-block;width: 200px;" placeholder="请输入标题"></el-input>
          <span v-else>{{item.title}}</span>
        </template>
        <el-col :span="16" >
          <el-input :key="index" v-if="['text','textarea'].indexOf(item.form_item_type_label) >-1"
                    :type="item.form_item_type_label"
                    v-model="form[item.key]" :placeholder="item.placeholder" :readonly="item.readonly" clearable></el-input>
          <el-input-number v-else-if="item.form_item_type_label === 'number'" v-model="form[item.key]"
                           :min="0" :key="index"></el-input-number>
          <div v-else-if="['img','imgs'].indexOf(item.form_item_type_label) >-1" :key="index">
            <el-upload
              :action="uploadUrl"
              :headers="uploadHeaders"
              name="file"
              :accept="'image/*'"
              :on-preview="handlePictureCardPreview"
              :on-success="(response, file, fileList)=>{handleUploadSuccess(response, file, fileList, item.key)}"
              :on-error="handleError"
              :on-exceed="handleExceed"
              :before-remove="(file, fileList)=>{beforeRemove(file, fileList, item.key)}"
              :multiple=false
              :limit=1
              :ref="'imgUpload_' + item.key"
              :data-keyname="item.key"
              :file-list="item.value?item.value:[]"
              list-type="picture-card"
            >
              <i class="el-icon-plus"></i>
              <div slot="tip" class="el-upload__tip">只能上传jpg/png文件</div>
            </el-upload>
            <el-dialog :visible.sync="dialogImgVisible">
              <img width="100%" :src="dialogImageUrl" alt="">
            </el-dialog>
          </div>
        </el-col>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit">提交</el-button>
      </el-form-item>
      <el-divider></el-divider>
      <el-form-item label="分类类别">
        <el-col :span="16" >
        <el-input type="text" v-model="cell_id" placeholder="待识别" :readonly=true>
        </el-input>
      </el-col>
      </el-form-item>
      <el-form-item label="分类名称">
        <el-col :span="16" >
        <el-input type="text" v-model="cell_name" placeholder="待识别" :readonly=true>
        </el-input>
      </el-col>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import * as api from '../../config/api'
import util from '@/libs/util'
import tableSelector from '@/components/table-selector/table-selector'

export default {
  name: 'formContent',
  inject: ['refreshView'],
  components: {
    tableSelector
  },
  props: {
    options: {
      type: Object
    },
    editableTabsItem: {
      type: Object
    }
  },
  watch: {
    options: {
      handler (nv) {
        if (nv && nv.id) {
          console.log(nv.id)
          this.getInit()
        }
      },
      immediate: true
    }
  },
  data () {
    return {
      formList: [],
      form: {},
      childTableData: [],
      childRemoveVisible: false,
      hideUpload: false,
      cell_id: undefined,
      cell_name: undefined,
      validRules: {
        title: [
          {
            required: true,
            message: '必须填写'
          }
        ],
        key: [
          {
            required: true,
            message: '必须填写'
          }
        ],
        value: [
          {
            required: true,
            message: '必须填写'
          }
        ]
      },
      uploadUrl: util.baseURL() + 'api/system/file/',
      uploadHeaders: {
        Authorization: 'JWT ' + util.cookies.get('token')
      },
      dialogImageUrl: '',
      dialogImgVisible: false,
      uploadImgKey: null
    }
  },
  methods: {
    // 获取数据
    getInit () {
      const that = this
      api.GetList({ parent: this.options.id, limit: 999 }).then(res => {
        const { data } = res.data
        this.formList = data
        const form = {}
        for (var item of data) {
          const key = item.key
          if (item.value) {
            form[key] = item.value
          }
          if (key === 'site_operator') {
            form[key] = 'site_operator'
          }
          if (item.form_item_type_label === 'array') {
            that.$nextTick(() => {
              const tableName = 'xTable_' + key
              const $table = this.$refs[tableName][0]
              $table.loadData(item.children)
            })
          }
        }
        this.form = JSON.parse(JSON.stringify(form))
      }).then(      
          api.getCurrentUserInfo().then(res => {
          const key = 'site_operator'
          const userinfo = res.data
          this.form[key] = userinfo.name
          // console.log(JSON.stringify(this.form))
        })
      )

      api.getCurrentUserInfo().then(res => {
          const key = 'site_operator'
          const userinfo = res.data
          this.form[key] = userinfo.name
          console.log(JSON.stringify(userinfo))
          // item.value = userinfo.username
        })
    },
    // 提交数据
    onSubmit () {
      const that = this
      const form = JSON.parse(JSON.stringify(this.form))
      const keys = Object.keys(form)
      const values = Object.values(form)
      for (const index in this.formList) {
        const item = this.formList[index]
        // eslint-disable-next-line camelcase
        keys.map((mapKey, mapIndex) => {
          if (mapKey === item.key) {
            if (item.form_item_type_label !== 'array') {
              item.value = values[mapIndex]
            }
            // 必填项的验证
            if (['img', 'imgs'].indexOf(item.form_item_type_label) > -1) {
              for (const arr of item.rule) {
                if (arr.required && item.value === null) {
                  that.$message.error(item.title + '不能为空')
                  return
                }
              }
            }
          }
        })
      }
      that.$refs.form.clearValidate()
      that.$refs.form.validate((valid) => {
        if (valid) {
          api.saveContent(this.options.id,
            this.formList).then(res => {
            this.$message.success('保存成功')
            // this.refreshView()
            const data = res.data
            console.log(JSON.stringify(res.data))
            this.cell_name = data.cell_name
            this.cell_id = data.cell_id
            // console.log(data['cell_id'])
          })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    // 追加
    async onAppend (tableName) {
      const $table = this.$refs[tableName][0]
      const { tableData } = $table.getTableData()
      const tableLength = tableData.length
      if (tableLength === 0) {
        const { row: newRow } = $table.insert()
        console.log(newRow)
      } else {
        const errMap = await $table.validate().catch(errMap => errMap)
        if (errMap) {
          this.$message.error('校验不通过！')
        } else {
          const { row: newRow } = $table.insert()
          console.log(newRow)
        }
      }
    },
    // 子表删除
    onRemoveChild (row, index, refName) {
      console.log(row, index)
      if (row.id) {
        api.DelObj(row.id).then(res => {
          this.refreshView()
        })
      } else {
        this.childTableData.splice(index, 1)
        const tableName = 'xTable_' + refName
        const tableData = this.$refs[tableName][0].remove(row)
        console.log(tableData)
      }
    },
    // 图片预览
    handlePictureCardPreview (file) {
      this.dialogImageUrl = file.url
      this.dialogImgVisible = true
    },
    // 判断是否为图片
    // 封装一个判断图片文件后缀名的方法
    isImage (fileName) {
      if (typeof fileName !== 'string') return
      const name = fileName.toLowerCase()
      return name.endsWith('.png') || name.endsWith('.jpeg') || name.endsWith('.jpg') || name.endsWith('.png') || name.endsWith('.bmp')
    },
    // 上传成功
    handleUploadSuccess (response, file, fileList, imgKey) {
      const that = this
      const {
        code,
        msg
      } = response
      if (code === 2000) {
        const { url } = response.data
        const { name } = file
        const { id } = response.data
        const type = that.isImage(name)
        if (!type) {
          this.$message.error('只允许上传图片')
        } else {
          const uploadImgKey = that.form[imgKey]
          if (!uploadImgKey || uploadImgKey === '') {
            that.form[imgKey] = []
          }
          // console.log(len)
          const dict = {
            name: name,
            url: util.baseURL() + url,
            id :  id
          }
          that.form[imgKey].push(dict)
        }
      } else {
        this.$message.error('上传失败,' + JSON.stringify(msg))
      }
    },
    // 上传失败
    handleError () {
      this.$message.error('上传失败')
    },
    // 上传超出限制
    handleExceed () {
      this.$message.error('超过文件上传数量')
    },
    // 删除时的钩子
    beforeRemove (file, fileList, key) {
      var index = 0
      this.form[key].map((value, inx) => {
        if (value.uid === file.uid) index = inx
      })
      this.form[key].splice(index, 1)
    },
    // 配置的行删除
    onDelRow (obj) {
      api.DelObj(obj.id).then(res => {
        this.refreshView()
      })
    },
    // 行编辑
    onEdit (index) {
      const that = this
      that.$set(that.formList[index], 'new_key', that.formList[index].key)
      that.$set(that.formList[index], 'edit', true)
    },
    // 行编辑保存
    onEditSave (obj) {
      obj.key = JSON.parse(JSON.stringify(obj.new_key))
      api.UpdateObj(obj).then(res => {
        this.refreshView()
      })
    },
	},
  mounted () {
    this.getInit()
  },

}
</script>

<style>
.hide .el-upload--picture-card {
  display: none
}
</style>
