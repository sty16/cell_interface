export const crudOptions = (vm) => {
  return {
    pageOptions: {
      compact: true
    },
    options: {
      height: '100%',
      maxHeight: '100%'
    },
    pagination: {
      pageSize: 5,
      small: true
    },
    rowHandle: {
      width: 100,
      view: {
        thin: true,
        text: '',
        disabled () {
          return !vm.hasPermissions('Retrieve')
        }
      },
      edit: {
        thin: true,
        text: '',
        disabled () {
          return !vm.hasPermissions('Update')
        }
      },
      remove: {
        thin: true,
        text: '',
        disabled () {
          return !vm.hasPermissions('Delete')
        }
      }
    },
    viewOptions: {
      componentType: 'form'
    },
    formOptions: {
      defaultSpan: 20, // 默认的表单 span
    },
    indexRow: { // 或者直接传true,不显示title，不居中
      title: '序号',
      align: 'center',
      width: 15
    },
    columns: [
      // {
      //   title: '关键词',
      //   key: 'search',
      //   show: false,
      //   disabled: true,
      //   search: {
      //     disabled: false
      //   },
      //   form: {
      //     disabled: true,
      //     component: {
      //       placeholder: '请输入关键词'
      //     }
      //   },
      //   view: {
      //     disabled: true
      //   }
      // },
      {
        title: '患者ID',
        width: 20,
        key: 'patient_id',
        align: 'center',
        form: {
          disabled: false,
          component: {
            placeholder: '患者ID'
          }
        },
        search: {
          disabled: false
        },
      },
      {
        title: '文件名称',
        key: 'name',
        search: {
          disabled: false
        },
        width: 40,
        type: 'input',
        form: {
          component: {
            placeholder: '请输入文件名称'
          }
        },
        align: 'center',
      },
      {
        title: '缩略图',
        key: 'url',
        type: 'image-uploader',
        search: {
          disabled: true
        },
        width: 26,
        component:{
            name: 'el-image',
            valueBinding: {
              prop: 'src',
              handle({value}) {
                return value[0]
              }
            },
            style: {width: "80px", height:"80px"}
        },
        align: 'center',
      },
      {
        title: '血细胞类别',
        width: 24,
        key: 'cell_id',
        align: 'center',
        value: 0,
        form: {
          disabled: false
        },
        component: {
          name: 'el-select',
          // 建议使用 d2-crud-plus 带的 dict-select组件,看下面
          children (h) {
            const items = []
            items.push(<el-option value="0">待识别</el-option>)
            items.push(<el-option value="1">原始细胞</el-option>)
            items.push(<el-option value="2">淋巴细胞</el-option>)
            items.push(<el-option value="3">单核细胞</el-option>)
            items.push(<el-option value="4">浆细胞</el-option>)
            items.push(<el-option value="5">红细胞</el-option>)
            items.push(<el-option value="6">早幼粒细胞</el-option>)
            items.push(<el-option value="7">嗜中性中幼粒细胞</el-option>)
            items.push(<el-option value="8">嗜中性晚幼粒细胞</el-option>)
            items.push(<el-option value="9">嗜中性杆状核细胞</el-option>)
            items.push(<el-option value="10">嗜中性分页核细胞</el-option>)
            items.push(<el-option value="11">嗜酸性粒细胞</el-option>)
            items.push(<el-option value="12">其他细胞</el-option>)
            return items
          },
          size: 'small'
        }
      },
      {
        title: '血细胞名称',
        width: 40,
        key: 'cell_name',
        align: 'center',
        form: {
          disabled: false
        }
      },
      {
        title: '上传/核验医师',
        width: 30,
        key: 'modifier_name',
        align: 'center',
        form: {
          disabled: false
        }
      },

      {
        title: '创建人',
        show: false,
        width: 100,
        key: 'modifier_name',
        form: {
          disabled: false
        }
      },
      // {
      //   title: '文件地址',
      //   key: 'url',
      //   type: 'file-uploader',
      //   search: {
      //     disabled: true
      //   },
      //   width: 120,
      // }, 
      {
        title: '是否人工确认',
        width: 25,
        key: 'is_confirmed',
        value: true,
        form: {
          disabled: false
        },
        component: {
          name: 'el-select',
          // 建议使用 d2-crud-plus 带的 dict-select组件,看下面
          children (h) {
            const items = []
            items.push(<el-option value="false">未确认</el-option>)
            items.push(<el-option value='true'>已确认</el-option>)
            return items
          },
          size: 'small'
        }
      },
      {
        title: '更新时间',
        key: 'update_datetime',
        width: 40,
        type: 'datetime',
        form: {
          disabled: false
        },
        align: 'center'
      }
    ]
  }
}
