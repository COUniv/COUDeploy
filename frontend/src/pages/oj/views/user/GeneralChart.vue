<template>
  <div class="echartss">
    <div v-if="isAuthenticated && (!isSuperAdmin)">
      <ECharts @on.native="option" :option="option" ref="echart" autoresize></ECharts>
    </div>
    <div v-else>
      <ECharts @on.native="option2" :option="option2" ref="echart2" autoresize></ECharts>
    </div>
  </div>
</template>
<script>
  import { mapGetters } from 'vuex'
  import api from '@oj/api'
  import * as ecStat from 'echarts-stat'
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
          legend: {
            bottom: 5
          },
          xAxis: {
            name: 'Accepted Problems',
            nameLocation: 'center',
            nameGap: 25,
            scale: true,
            min: 0,
            // max: 0,
            axisLine: {
              onZero: false
            }
          },
          yAxis: {
            name: 'Rating',
            scale: true,
            min: 0,
            // max: 0,
            axisLine: {
              onZero: false
            }
          },
          dataZoom: [
            {
              show: true,
              type: 'inside',
              filterMode: 'none',
              startValue: 0,
              endValue: 100
            },
            {
              show: true,
              type: 'inside',
              filterMode: 'none',
              startValue: 0,
              endValue: 40
            }
          ],
          series: [
            {
              name: '회귀선',
              type: 'line',
              smooth: true,
              symbolSize: 0.1,
              lineStyle: {width: 1},
              symbol: 'circle',
              color: '#5130e58f',
              label: { show: false, fontSize: 12 },
              labelLayout: { dx: -20 },
              encode: { label: 2, tooltip: 1 },
              data: [[]]
            },
            {
              name: '유저',
              type: 'scatter',
              color: '#f5a447ab',
              symbolSize: 4,
              data: [[]]
            },
            {
              name: '나의 위치',
              type: 'effectScatter',
              symbolSize: 7,
              color: '#EE2E03',
              data: [
                [2, 72.2]
              ]
            }
          ]
        },
        option2: {
          title: {
            text: '유저 포지션',
            left: 'center'
          },
          tooltip: {
            trigger: 'item',
            axisPointer: {
              type: 'cross'
            }
          },
          legend: {
            bottom: 5
          },
          xAxis: {
            name: 'Accepted Problems',
            nameLocation: 'center',
            nameGap: 25,
            scale: true,
            min: 0,
            // max: 0,
            axisLine: {
              onZero: false
            }
          },
          yAxis: {
            name: 'Rating',
            scale: true,
            min: 0,
            // max: 0,
            axisLine: {
              onZero: false
            }
          },
          dataZoom: [
            {
              show: true,
              type: 'inside',
              filterMode: 'none',
              startValue: 0,
              endValue: 100
            },
            {
              show: true,
              type: 'inside',
              filterMode: 'none',
              startValue: 0,
              endValue: 40
            }
          ],
          series: [
            {
              name: '회귀선',
              type: 'line',
              smooth: true,
              symbolSize: 0.1,
              lineStyle: {width: 1},
              symbol: 'circle',
              color: '#5130e58f',
              label: { show: false, fontSize: 12 },
              labelLayout: { dx: -20 },
              encode: { label: 2, tooltip: 1 },
              data: [[]]
            },
            {
              name: '유저',
              type: 'scatter',
              color: '#f5a447ab',
              symbolSize: 4,
              data: [[]]
            }
          ]
        }
      }
    },
    mounted () {
      if (this.isAuthenticated && (!this.isSuperAdmin)) {
        this.init()
      } else {
        this.init2()
      }
    },
    methods: {
      init () {
        let bar = this.$refs.echart
        bar.clear()
        api.getUserRatingChart().then(res => {
          let sources = []
          let maxX = 0
          let maxY = 0
          res.data.data.forEach(el => {
            if (maxX < el[0]) {
              maxX = el[0]
            }
            if (maxY < el[1]) {
              maxY = el[1]
            }
            el[1] = Math.ceil(el[1] * 100)
            sources.push(el)
          })
          this.option.series[1].data = sources
          this.option.xAxis.max = maxX + 2
          this.option.yAxis.max = (Math.ceil(maxY) * 100) + 100
          this.option.dataZoom[0].endValue = maxX + 2
          this.option.dataZoom[1].endValue = (Math.ceil(maxY) * 100) + 100
          const myReg = ecStat.regression('exponential', sources, 20)
          const expr = myReg.expression
          console.log(this.$store.state.user.username)
          this.option.title.subtext = this.$store.state.user.username
          this.option.series[0].data = myReg.points
        })
        api.getMyRatingChart().then(res => {
          let source = res.data.data
          source[1] = Math.ceil(source[1] * 100)
          this.option.series[2].data = source
        })
      },
      init2 () {
        let bar = this.$refs.echart2
        bar.clear()
        api.getUserRatingChart().then(res => {
          let sources = []
          let maxX = 0
          let maxY = 0
          res.data.data.forEach(el => {
            if (maxX < el[0]) {
              maxX = el[0]
            }
            if (maxY < el[1]) {
              maxY = el[1]
            }
            el[1] = Math.ceil(el[1] * 100)
            sources.push(el)
          })
          this.option2.series[1].data = sources
          this.option2.xAxis.max = maxX + 2
          this.option2.yAxis.max = (Math.ceil(maxY) * 100) + 100
          this.option2.dataZoom[0].endValue = maxX + 2
          this.option2.dataZoom[1].endValue = (Math.ceil(maxY) * 100) + 100
          const myReg = ecStat.regression('exponential', sources, 20)
          const expr = myReg.expression

          this.option2.series[0].data = myReg.points
        })
      }
    },
    computed: {
      ...mapGetters(['user', 'isAuthenticated', 'isSuperAdmin'])
    }
  }
</script>
<style lang="less">  
.echarts {
    width: 95%;
    height: 400px;
  }
</style>