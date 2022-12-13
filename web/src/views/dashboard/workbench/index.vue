<template>
  <d2-container>
    <div class="page-header">

      <el-avatar src="/image/avatar-voxel.png" class="user-avatar">

      </el-avatar>
      <div class="title">
        <h1>邃蓝智能骨髓血细胞图像智能处理平台</h1>
        <span> Accurate. Efficient. Free Access Platform.！ </span>
      </div>
    </div>

    <el-row :gutter="20">


      <el-col :span="12">
        <div class="grid-content bg-purple">
          <el-card class="box-card" >
            <div slot="header" class="clearfix">
              <span>快捷导航</span>
            </div>
            <el-row>
              <el-col :span="12" v-for="({name,icon,route,color},index) of navigators" :key="index" style="padding: 0">
                <el-card shadow="hover">
                  <div  style="display: flex;align-items: center;flex-direction: column;cursor: pointer" @click="()=>{gotoRoute(route)}">
                    <d2-icon-svg :name="icon" style="width: 25px;height: 25px;" :style="{fill:color}"/>
                    <div style="text-align: center;font-size: 12px;margin-top: 20px" v-text="name"></div>
                  </div>
                </el-card>
              </el-col>
            </el-row>
          </el-card>
          <el-card class="box-card" style="margin-top: 20px">
            <div slot="header" class="clearfix">
              <span>病例分析</span>
              <el-button style="float: right; padding: 3px 0" type="text">
                <el-link href="https://www.deep-voxel.com/" target="_blank" type="primary">更多</el-link>
              </el-button>
            </div>
            <el-row>
              <div class="echart" id="mychart" style="float: left;width: 100%; height: 360px"></div>
            </el-row>
          </el-card>
        </div>
      </el-col>
      <el-col :span="12">
        <el-card class="box-card" >
              <div slot="header" class="clearfix">
                <span>病例分析</span>
                <el-button style="float: right; padding: 3px 0" type="text">
                  <el-link href="https://www.deep-voxel.com/" target="_blank" type="primary">更多</el-link>
                </el-button>
              </div>
              <el-row>
                <div class="echart" id="rosechart" style="float: left;width: 100%; height: 500px"></div>
              </el-row>
          </el-card>
      </el-col>
    </el-row>

  </d2-container>
</template>

<script>
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { PieChart } from 'echarts/charts'
import * as echarts from "echarts";
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent
} from 'echarts/components'

use([
  CanvasRenderer,
  PieChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent
])
export default {
  name: 'workbench',
  data () {
    return {
      myChartStyle: { float: "left", width: "100%", height: "400px" },
      navigators: [
        {
          name: '控制台',
          icon: 'home',
          route: {
            name: 'index'
          },
          color: 'rgb(31, 218, 202);'
        },
        {
          name: '血细胞识别',
          icon: 'department',
          route: {
            name: 'config'
          },
          color: 'rgb(225, 133, 37);'
        },
        {
          name: '患者图像管理',
          icon: 'role',
          route: {
            name: 'file'
          },
          color: 'rgb(191, 12, 44);'
        },
        {
          name: '日志管理',
          icon: 'log',
          route: {
            name: 'operationLog'
          },
          color: 'rgb(0, 216, 255);'
        }
      ],
    }
  },
  mounted() {
    this.initEcharts();
    this.initRowEcharts();
  },
  methods: {
    gotoRoute (route) {
      this.$router.push(route)
    },
    initEcharts() {
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
            data: [558, 188, 37, 40, 529, 76, 201, 143, 201, 216, 111], 
          }
        ],
        title: {
          text: "某患者骨髓血细胞数量统计分析",
          left: "center",
        },
        toolbox: {
            show: true,
            feature: {
              mark: { show: true },
              dataView: { show: true, readOnly: false },
              restore: { show: true },
              saveAsImage: { show: true }
            }
        }
      };
      const myChart = echarts.init(document.getElementById("mychart"));
      myChart.setOption(option);
      //随着屏幕大小调节图表
      window.addEventListener("resize", () => {
        myChart.resize();
      });
    },
    initRowEcharts() {
      var chartDom = document.getElementById('rosechart');
      var myChart = echarts.init(chartDom);
      var option = {
          legend: {
            top: 'bottom'
          },
          toolbox: {
            show: true,
            feature: {
              mark: { show: true },
              dataView: { show: true, readOnly: false },
              restore: { show: true },
              saveAsImage: { show: true }
            }
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
              data: [
                { value: 58, name: '原始细胞' },
                { value: 188, name: '淋巴细胞' },
                { value: 37, name: '单核细胞' },
                { value: 40, name: '浆细胞' },
                { value: 59, name: '红细胞' },
                { value: 76, name: '早幼粒' },
                { value: 101, name: '中幼粒' },
                { value: 143, name: '杆状核' },
                { value: 116, name: '分叶核' },
                { value: 111, name: '嗜酸性' }
              ]
            }
          ],
          title: {
            text: "某患者骨髓血细胞数量统计分析",
            left: "center",
          }
        }
        myChart.setOption(option);
        window.addEventListener("resize", () => {
          myChart.resize();
        });
    }
  }
}
</script>

<style scoped lang="scss">

  $userAvatarLength: 72px;

  .page-header{
    box-sizing: border-box;
    padding: 16px;
    .user-avatar{
        width: $userAvatarLength;
        height: $userAvatarLength;
        line-height: $userAvatarLength;
      display: inline-block;
    }

    .title{
      display: inline-block;
      padding: 0 0 0 15px;
      position: relative;
      top: -5px;

      h1{
        font-size: 1.125rem;
        font-weight: 500;
        line-height: 1.75rem;
      }
      span{
        font-size: 14px;
        color: rgba(0,0,0,.45);
      }
    }

  }

  .project-detail{
    color: rgba(0,0,0,.45);
    height: 65px;
     img {
       width: 25px;
       height: 25px;
     }
    .name{
      margin-left: 1rem;
      font-size: 1rem;
      line-height: 2rem;
      height: 2rem;
      display: inline-block;
      color: rgba(0,0,0,.85);
      position: relative;
      top: -5px;
    }
    .slogan{
      font-size: 12px;
      padding: 5px 0;
      overflow:hidden;
      text-overflow:ellipsis;
      white-space:nowrap;
    }
    .team{
      font-size: 14px;
    }
  }

  .activity{
    padding: 0;
    .activity-avatar{
      width: 40px;
      height: 40px;
      line-height: 40px;
    }
    .activity-detail{
      padding: 10px;
      line-height: 15px;
      font-size: 14px;
      color: rgba(0,0,0,.85);
    }
  }
  .chart {
    height: 408px;
  }

  .el-divider--horizontal{
    margin: 4px 0;
    background: 0 0;
    border-top: 1px solid #e8eaec;

  }
  .el-card, .el-message {
    border-radius: 0;
  }
</style>
