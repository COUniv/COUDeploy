<template>
  <div class="echartss">
    <ECharts :option="option" autoresize></ECharts>
  </div>
</template>
<script>
  import { mapGetters } from 'vuex'
  import api from '@oj/api'
  export default {
    data () {
      return {
        option: {
          title: {
            text: '나의 포지션',
            subtext: 'username',
            left: 'center'
          },
          tooltip: {
            trigger: 'item',
            axisPointer: {
              type: 'cross'
            }
          },
          dataset: [
            {
              source: [[] ,[]]
            },
            {
              transform: {
                type: 'ecStat:regression',
                config: {
                  // method: 'linear'
                  // method: 'exponential' -> not useful
                  // method: 'logarithmic'
                  method: 'polynomial', order: 20
                }
              }
            }
          ],
          legend: {
            bottom: 5
          },
          xAxis: {
            scale: true
          },
          yAxis: {
            scale: true
          },
          series: [
            {
              name: '회귀선',
              type: 'line',
              smooth: true,
              datasetIndex: 1,
              symbolSize: 0.1,
              lineStyle: {width: 1},
              symbol: 'circle',
              color: '#5130e58f',
              label: { show: false, fontSize: 12 },
              labelLayout: { dx: -20 },
              encode: { label: 2, tooltip: 1 }
            },
            {
              name: '유저',
              type: 'scatter',
              color: '#f5a447ab',
              symbolSize: 4,
              datasetIndex: 0
            }
          ]
        }
      }
    },
    mounted () {
      this.init()
    },
    methods: {
      init () {
        api.getUserRatingChart().then(res => {
          this.option.dataset.source = res.data.data
        })
        if (isAuthenticated) {
          api.getMyRatingChart().then(res => {
            this.option.series.push({
              name: '나의 위치',
              type: 'effectScatter',
              symbolSize: 7,
              color: '#EE2E03',
              data: res.data.data
            })
          })
        }
      }
    },
    computed: {
      ...mapGetters(['user', 'isAuthenticated'])
    }
  }
</script>
<style lang="less">  
.echarts {
    width: 95%;
    height: 400px;
  }
</style>