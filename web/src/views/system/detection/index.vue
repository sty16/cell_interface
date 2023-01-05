<template>
  <d2-container>
    <div>
    </div>
    <el-tabs type="border-card" v-model='tabPaneName'>
      <el-tab-pane
        :key=1
        label="血细胞检测"
        name="first"
      >
      <el-form ref="form" :model="form" label-width="300px" label-position="left">
        <el-row>
          <el-col :span="12">
            <el-form-item :required=true label="患者ID">
              <el-input-number v-model="patient_id" :min="0" placeholder="请输入" clearable></el-input-number>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item :required=true>
          <template slot="label">
              <span >上传文件夹图像</span>
          </template>
          <el-col :span="24">
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
        <el-button type="primary" @click="onSubmit">提交检测</el-button>
      </el-form-item>
      <el-divider></el-divider>
      <el-col style="margin-bottom: 20px">
        <el-tag effect="light" type="warning">请点击下载切片按钮，下载您上传图片的切片</el-tag>
      </el-col>
      <el-form-item>
          <el-button type="success" @click="onDownload" >下载切片</el-button>
      </el-form-item>
      <div class="position">检测结果展示</div>
      <div class="images">
        <div v-for="(item, index) in info" :key="index" class="image-middle">  
          <el-card shadow="hover" :body-style="{ padding: '10px' }">     
          <el-popover> 
            <img :src="info[index].src" slot="reference" class="image"/>    
            <img :src="info[index].src" class="imagePreview"/>
          </el-popover>  
          <div style="text-align:center;padding-top:12px">
          <span>{{info[index].name}}</span>   
          </div>     
          </el-card>
        
        </div>     
      </div>
      </el-form>
      </el-tab-pane>
    </el-tabs>
  </d2-container>
</template>

<script>
import util from '@/libs/util'
import * as api from './api'

export default {
  name: 'detection',
  data () {
    return {
      tabPaneName: 'first',
      uploadUrl: util.baseURL() + 'api/system/detect_file/',
      uploadHeaders: {
        Authorization: 'JWT ' + util.cookies.get('token')
      },
      fileList: [],
      form: {},
      patient_id: undefined,
      info: [],
      cell_slices: []
    }
  },

  computed: {

  },

  methods: {

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
            const data = res.data
            let urls = data.cell_detect
            this.info = []
            for (let i = 0; i < urls.length; i++) {
              const dict = {
                src: util.baseURL() + urls[i],
              }
              this.info.push(dict)
            }
            this.cell_slices = data.cell_slices
          })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },

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
    handlePictureCardPreview (file) {
      this.dialogImageUrl = file.url
      this.dialogImgVisible = true
    },
    isImage (fileName) {
      if (typeof fileName !== 'string') return
      const name = fileName.toLowerCase()
      return name.endsWith('.png') || name.endsWith('.jpeg') || name.endsWith('.jpg') || name.endsWith('.png') || name.endsWith('.bmp')
    },

    onDownload() {
      const files = {
        files: this.cell_slices
      }
      api.getZip(files).then((res) => {
        const fileName = 'res.zip'
        console.log(res)
        console.log(res.length)
        // console.log(res.data)
        let blob = new Blob([res], { type: "application/zip" })
        let url = window.URL.createObjectURL(blob)
        let link = document.createElement('a') // 创建a标签
        link.href = url
        link.download = fileName // 文件重命名，若无需重命名，将该行删去
        link.click()
        URL.revokeObjectURL(url)
      })
    }
  }
}
</script>

<style scoped>
 /* “Tissue Search”字体样式 */
.position {
  margin-left: 15px;
  font-size: 15px;
  font-weight: 300;
}
/* 图片总布局，样式 */
.images{
  display: flex;
  margin-top: 20px;
  margin-left: 21px;
  margin-right: 20px;
  flex-wrap: wrap;
}
/* 图片之间 */
.image-middle{
  margin-right: 15px;
  margin-bottom: 15px;
}
/* 单张图片样式 */
.image{
  width:110px;
  height: 110px;
}
 </style>
