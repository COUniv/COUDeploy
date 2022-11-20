<template>
  <div style="padding: 45px;">
    <Panel shadow :padding="10">
      <div style="float:right; padding-right:150px; display: block;">
      <Tooltip placement="bottom-end" :delay="500" max-width="300">
        <i class="mdi mdi-help-circle" id="help-icn">도움말</i>
        <div slot="content" style="font-size: 7px;">
          <p>데이터는 최대 500명의 데이터로 제한됩니다.<br>500명이 넘을 경우 전체 유저 중 500명을 무작위 추출합니다.</p>
          <p>레이팅은 통과한 문제 수 및 문제의 난이도 별 추가점수가 부여되며<br>해당 식은 악용을 방지하기 위해 비공개합니다.</p>
          <p>데이터 반영 시간까지 최대 10분정도 소요될 수 있습니다.</p>
        </div>
      </Tooltip>
      </div>
      <div style="clear: both;"></div>
      <div v-if="isAuthenticated && (!isSuperAdmin)" class="echartss">
        <ECharts @on.native="option" :option="option" ref="echart" autoresize></ECharts>
      </div>
      <div v-else class="echartss">
        <ECharts @on.native="option2" :option="option2" ref="echart2" autoresize></ECharts>
      </div>
      <div class="slider-div">
        <div class="slider-container">
          <Slider v-model="degree" :min="1" :max="100" show-input></Slider>
          <div class="slider-footer">
            <span class="slider-degree">Degree</span>
            <Button class="change-btn" shape="circle" icon="md-checkmark-circle-outline" @click.native="changeDegree">변경</Button>
          </div>
        </div>
      </div>
      <div v-if="(isAuthenticated && (!isSuperAdmin))" class="footer-h">
        <div class="main-container">
          <div class="main-box">
            나의 레이팅 : {{option.series[2].data[0][1]}} 점
          </div>
          <div class="main-box">
            해당 구간에서의 회귀 레이팅 : {{this.avgRating}}
          </div>
          <div class="main-box">
            현재 표기 된 데이터 수 : {{this.usersCount}}
          </div>
          <!-- <div class="main-box">
            현재 회귀식 : {{this.expr}}
          </div> -->
        </div>
      </div>
      <div v-else class="footer-h">
        <div class="main-container">
          <div class="main-box">
            현재 표기 된 데이터 수 : {{this.usersCount}}
          </div>
          <!-- <div class="main-box">
            현재 회귀식 : {{this.expr}}
          </div>   -->
        </div>
      </div>
    </Panel>
  </div>
</template>
<script>
  import { mapGetters } from 'vuex'
  import api from '@oj/api'
  import * as ecStat from 'echarts-stat'
  export default {
    data () {
      return {
        degree: 3,
        usersCount: 0,
        avgRating: 0,
        expr: '',
        option: {
          title: {
            text: '나의 포지션 (beta)',
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
            text: '유저 포지션 (beta)',
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
          let addMinSource = [[0, 0]]
          let maxX = 0
          let maxY = 0
          res.data.data.forEach(el => {
            if (maxX < el[0]) {
              maxX = el[0]
            }
            if (maxY < el[1]) {
              maxY = el[1]
            }
            el[1] = Math.floor(el[1] * 100)
            sources.push(el)
            addMinSource.push(el)
          })
          this.usersCount = sources.length
          this.option.series[1].data = sources
          this.option.xAxis.max = maxX + 2
          this.option.yAxis.max = (Math.floor(maxY) * 100) + 100
          this.option.dataZoom[0].endValue = maxX + 2
          this.option.dataZoom[1].endValue = (Math.floor(maxY) * 100) + 100

          const myReg = ecStat.regression('polynomial', addMinSource, this.degree)
          this.expr = myReg.expression
          this.option.title.subtext = this.$store.state.user.username
          this.option.series[0].data = myReg.points
          api.getMyRatingChart().then(res => {
            let source = res.data.data
            source[0][1] = Math.floor(source[0][1] * 100)
            this.option.series[2].data = source
            let sourceX = source[0][0]
            this.avgRating = 0
            if (sourceX !== 0) {
              var i = 0
              myReg.parameter.forEach(e => {
                this.avgRating += e * Math.pow(sourceX, i)
                i += 1
              })
              this.avgRating = Math.floor(this.avgRating)
            }
          })
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
            el[1] = Math.floor(el[1] * 100)
            sources.push(el)
          })
          this.usersCount = sources.length
          this.option2.series[1].data = sources
          this.option2.xAxis.max = maxX + 2
          this.option2.yAxis.max = (Math.floor(maxY) * 100) + 100
          this.option2.dataZoom[0].endValue = maxX + 2
          this.option2.dataZoom[1].endValue = (Math.floor(maxY) * 100) + 100
          const myReg = ecStat.regression('polynomial', sources, this.degree)
          this.expr = myReg.expression

          this.option2.series[0].data = myReg.points
        })
      },
      changeDegree () {
        let addMinSource = [[0, 0]]
        if (this.isAuthenticated && (!this.isSuperAdmin)) {
          addMinSource.push(...this.option.series[1].data)
          let myReg1 = ecStat.regression('polynomial', addMinSource, this.degree)
          this.expr = myReg1.expression
          this.option.series[0].data = myReg1.points
          let dataX = this.option.series[2].data[0][0]
          if (dataX !== 0) {
            this.avgRating = 0
            var i = 0
            myReg1.parameter.forEach(e => {
              this.avgRating += e * Math.pow(dataX, i)
              i += 1
            })
            this.avgRating = Math.floor(this.avgRating)
          }
        } else {
          addMinSource.push(...this.option2.series[1].data)
          let myReg2 = ecStat.regression('polynomial', addMinSource, this.degree)
          this.expr = myReg2.expression
          this.option2.series[0].data = myReg2.points
        }
      }
    },
    computed: {
      ...mapGetters(['user', 'isAuthenticated', 'isSuperAdmin'])
    }
  }
</script>
<style lang="less">
@import '../../../../styles/common.less';

#help-icn {
  font-style: normal;
  font-size: 12px;
  transition: all ease-in 0.2s;
  &:hover {
    color: @orange;
  }
}
.footer-h {
  min-height: 100px;
  padding-bottom: 20px;
  margin-top: 15px;
  .main-container {
    margin: 0 auto;
    width: 75%;

    .main-box {
      margin-bottom: 10px;
    }
  }
}
.echartss {
  display: flex;
  justify-content:center;
}
.echarts {
  width: 85%;
  height: 400px;
}
.slider-div {
  width: 75%;
  display: flex;
  justify-content:flex-end;
  margin: 0 auto;
  .slider-container {
    width: 30%;
    min-width: 220px;
  }
  .slider-degree {
    float: left;
    display: block;
  }
  .change-btn {
    float: right;
    display: block;
  }
}

</style>