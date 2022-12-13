<template>
  <div>
    <el-row :gutter="20">
      <el-col :span="8">变量标题</el-col>
      <el-col :span="8">变量值</el-col>
    </el-row>
    <el-form ref="form" :model="form" label-width="360px" label-position="left" style="margin-top: 20px">
      <el-form-item>
      <template slot="label">
          <span >操作人</span>
      </template>
      <el-col :span="8">
        <el-input :key=1 type="text" v-model=operator placeholder="" :readonly=true clearable></el-input>
      </el-col>
    </el-form-item>
    <el-form-item label="患者ID" :required=true>
      <el-col :span="8">
        <el-input-number v-model="patient_id" :min="0"></el-input-number>
      </el-col>
    </el-form-item>
    <el-form-item :required=true>
      <template slot="label">
          <span >上传文件夹图像</span>
      </template>
      <el-col :span="16">
        <el-upload
              :action="uploadUrl"
              :headers="uploadHeaders"
              multiple
              name="file"
              :accept="'image/*'"
              :on-preview="handlePictureCardPreview"
              :on-success="(response, file, fileList)=>{handleUploadSuccess(response, file, fileList, 'cell_picture')}"
              :on-error="handleError"
              :on-exceed="handleExceed"
              :before-remove="(file, fileList)=>{beforeRemove(file, fileList, 'cell_picture')}"
              :limit=150
              ref='imgUpload_cell_picture'
              data-keyname="cell_picture"
              :file-list=fileList
              list-type="picture-card"
            >
            <i class="el-icon-plus"></i>
              <div slot="tip" class="el-upload__tip">只能上传jpg/png文件, 单次最多150张</div>
            </el-upload>
      </el-col>
    </el-form-item>
    <el-form-item>
        <el-button type="primary" @click="onSubmit">提交</el-button>
      </el-form-item>
      <el-divider></el-divider>
      <el-col style="margin-bottom: 20px">
        <el-tag effect="dark" type="warning">详细识别信息到患者数据管理/血细胞文件管理查看</el-tag>
      </el-col>
      <el-form-item label="分类类别 (按上传顺序排序)">
        <el-col :span="16">
        <el-input type="text" v-model="cell_ids" placeholder="待识别" :readonly=true>
        </el-input>
      </el-col>
      </el-form-item>
      <el-form-item label="分类名称 (按上传顺序排序)">
        <el-col :span="16" >
        <el-input type="text" v-model="cell_names" placeholder="待识别" :readonly=true>
        </el-input>
      </el-col>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import * as api from '../api'
import util from '@/libs/util'
import tableSelector from '@/components/table-selector/table-selector'

export default {
  name: 'formContent',
  inject: ['refreshView'],
  components: {
    tableSelector
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
      fileList: [],
      operator: "",
      form: {},
      childTableData: [],
      childRemoveVisible: false,
      hideUpload: false,
      cell_ids: undefined,
      patient_id: undefined,
      cell_names: undefined,
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
      api.getCurrentUserInfo().then(res => {
          const key = 'site_operator'
          const userinfo = res.data
          this.operator = userinfo.name
          // console.log(JSON.stringify(this.form))
        })

    },
    onSubmit () {
      const that = this
      let imgkey = 'cell_picture'
      let patientkey = 'patient_id'
      // that.$message.error('图片不能为空')
      if (typeof this.patient_id === "undefined") {
        that.$message.error('患者ID不能为空')
        return 
      }
      this.form[patientkey] = this.patient_id
      if (that.form[imgkey].length === 0) {
        that.$message.error('图片不能为空')
        return
      }
      that.$refs.form.clearValidate()
      that.$refs.form.validate((valid) => {
        if (valid) {
          api.saveContent(
            this.form).then(res => {
            this.$message.success('保存成功')
            // this.refreshView()
            const data = res.data
            this.cell_names = JSON.stringify(data.cell_names)
            this.cell_ids = JSON.stringify(data.cell_ids)
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

<style scoped>
.hide .el-upload--picture-card {
  display: none
}
.el-input-number {
  width: 350px;
  line-height: 37px;
  height: 35px;
}
</style>
