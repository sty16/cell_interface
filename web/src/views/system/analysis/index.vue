<template>
  <d2-container>
    <div>
    </div>
    <el-tabs type="border-card" v-model='tabPaneName'>
      <el-tab-pane
        :key=1
        label="患者数据分析"
        name="first"
      >
      <el-form label-width="100px" label-position="left">
        <el-row>
          <el-col :span="3">
            <el-form-item :required=true label="患者ID">
              <el-input-number v-model="patient_id" :min="0" placeholder="请输入" clearable></el-input-number>
            </el-form-item>
          </el-col>
          <el-col :span="4" :offset="1">
            <el-form-item>
              <el-button type="primary" @click="onSubmit">查询</el-button>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col>
            <el-form-item label="患者详情">
              <el-input type="text" v-model=patient_info placeholder="患者血细胞数量详情" :readonly=true></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-divider></el-divider>
        <el-row>
            <el-col class="echart" id="mychart" style="float: left; width: 50%; height: 500px"></el-col>
            <el-col class="echart" id="rosechart" style="float: left; width: 50%; height: 500px"></el-col>
        </el-row>
      </el-form>
      </el-tab-pane>
    </el-tabs>
  </d2-container>
</template>

<script>
import { AddObj, GetObj, GetList, UpdateObj, DelObj, GetSelfReceive } from './api'
import * as echarts from "echarts";
export default {
  name: 'analysis',
  data () {
    return {
      tabPaneName: 'first',
      cell_data: [58, 188, 37, 40, 201, 76, 101, 121, 143, 116, 111],
      cell_rose_data: [
                { value: 58, name: '原始细胞' },
                { value: 188, name: '淋巴细胞' },
                { value: 37, name: '单核细胞' },
                { value: 40, name: '浆细胞' },
                { value: 201, name: '红细胞' },
                { value: 76, name: '早幼粒' },
                { value: 101, name: '中幼粒' },
                { value: 121, name: '晚幼粒' },
                { value: 143, name: '杆状核' },
                { value: 116, name: '分叶核' },
                { value: 111, name: '嗜酸性' }
              ],
      patient_id: "0",
      patient_info: "原始细胞:58, 淋巴细胞:188, 单核细胞:37, 浆细胞:40, 红细胞:201, 早幼粒:76, 中幼粒:101, 晚幼粒:121, 杆状核:143, 分叶核:116, 嗜酸性:111",
    }
  },
  mounted() {
    this.initEcharts(this.patient_id, this.cell_data);
    this.initRowEcharts(this.patient_id, this.cell_rose_data);
  },

  computed: {

  },
  methods: {
    initEcharts(patient_id, cell_data) {
      // 基本柱状图
      const option = {
        xAxis: {
          data: ["原始细胞", "淋巴细胞", "单核细胞", "浆细胞", "红细胞", "早幼粒", "中幼粒", "晚幼粒", "杆状核", "分叶核", "嗜酸性"],
          axisLabel: {
            rotate: 45
          }
        },
        yAxis: {
          type: "value",
          name: "数量(个)"
        },
        series: [
          {
            type: "bar", //形状为柱状图
            data: cell_data, 
          }
        ],
        title: {
          text: "患者" + patient_id.toString() + "骨髓血细胞数量统计分析",
          left: "center",
        },
      };
      const myChart = echarts.init(document.getElementById("mychart"));
      myChart.setOption(option);
      //随着屏幕大小调节图表
      window.addEventListener("resize", () => {
        myChart.resize();
      });
    },

    initRowEcharts(patient_id, cell_data) {
      var chartDom = document.getElementById('rosechart');
      var myChart = echarts.init(chartDom);
      var option = {
          legend: {
            top: 'bottom'
          },
          series: [
            {
              name: 'Nightingale Chart',
              type: 'pie',
              radius: [50, 150],
              center: ['50%', '50%'],
              roseType: 'area',
              itemStyle: {
                borderRadius: 8
              },
              data: cell_data
            }
          ],
          title: {
            text: "患者" + patient_id.toString() + "骨髓血细胞数量统计分析",
            left: "center",
          }
        }
        myChart.setOption(option);
        window.addEventListener("resize", () => {
          myChart.resize();
        });
    },

    onSubmit () {
      return
    }
  }
}
</script>
