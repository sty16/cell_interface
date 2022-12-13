<template>
  <d2-container>
    <div>
      <el-header>
        <div class="yxt-flex-between">
          <div>
            <el-tag>多图识别: 您可以选择文件夹中多张图片进行识别</el-tag>
          </div>
          <div>
          </div>
        </div>
      </el-header>
    </div>
    <el-tabs type="border-card" v-model='tabPaneName'>
      <el-tab-pane
        :key=1
        label="多图识别"
        name="first"
      >
        <formContent></formContent>
        
      </el-tab-pane>
    </el-tabs>
  </d2-container>
</template>

<script>
import { AddObj, GetObj, GetList, UpdateObj, DelObj, GetSelfReceive } from './api'
import { crudOptions } from './crud'
import { d2CrudPlus } from 'd2-crud-plus'
import formContent from '@/views/system/recognition/components/formContent'
import viewTemplate from './viewTemplate.js'
export default {
  name: 'recognition',
  components: {
    formContent
  },
  mixins: [d2CrudPlus.crud],
  data () {
    return {
      tabActivted: 'send',
      tabPaneName: 'first'
    }
  },

  computed: {
  },
  methods: {
    getCrudOptions () {
      return crudOptions(this)
    },
    pageRequest (query) {
      if (this.tabActivted === 'receive') {
        return GetSelfReceive({ ...query })
      }
      return GetList(query)
    },
    infoRequest (query) {
      return GetObj(query)
    },
    addRequest (row) {
      return AddObj(row).then(res => {
        const message = {
          message_id: res.data.id,
          contentType: 'INFO',
          content: '您有新的消息,请到消息中心查看~'
        }
        this.$websocket.webSocketSend(message)
      })
    },
    updateRequest (row) {
      return UpdateObj(row)
    },
    delRequest (row) {
      return DelObj(row.id)
    },
    onView ({ row, index }) {
      this.getD2Crud().showDialog({
        mode: 'view',
        rowIndex: index,
        template: viewTemplate
      })
      this.infoRequest(row)
      this.doRefresh()
    },
    onTabClick (tab) {
      const { name } = tab
      this.tabActivted = name
      this.doRefresh()
    }
  }
}
</script>
