<template>
  <div>
    <div class="flex-container">
      <div class="flex-item">
      <svg class="grass-container">
        <template>
          <g>
            <rect v-for="(_, day) in this.numOfDaysInYear" class="grass-pointer"
              v-bind:class="numberOfProblemsSolved(day)"
              v-bind:style="{'x':getPositionX(day) ,'y': getPositionY(day)}"></rect>
          </g>
        </template>
      </svg>
      </div>
    </div>
    <div class="flex-level-container">
      <div class="flex-level-item">
        <div class="level-left"></div>
        <div class="level-right">
          <div class="text">Less</div>
          <div class="svg-level-box">
          <svg class="level-svg">
            <rect class="grass-pointer level1"></rect>
          </svg>
          <svg class="level-svg">
            <rect class="grass-pointer level2"></rect>
          </svg>
          <svg class="level-svg">
            <rect class="grass-pointer level3"></rect>
          </svg>
          <svg class="level-svg">
            <rect class="grass-pointer level4"></rect>
          </svg>
          <svg class="level-svg last">
            <rect class="grass-pointer level5"></rect>
          </svg>
          </div>
          <div class="text">
          More
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
  import api from '@oj/api'
  import time from '@/utils/time'
  export default {
    data () {
      return {
        grassList: [],
        grassCount: {},
        numOfDaysInYear: 0,
        startingDayOfWeek: 0
      }
    },
    mounted () {
      this.getGrassList()
    },
    methods: {
      getGrassList () {
        api.getGrassList().then(res => {
          this.grassList = res.data.data.grass
          // console.log(this.grassList)
          this.getGrassListCount(this.grassList, '2022')
        })
      },
      getPositionX (day) {
        var currentDay = day + (this.startingDayOfWeek - 1)
        return Math.floor(currentDay / 7) * 13
      },
      getPositionY (day) {
        var currentDay = day + (this.startingDayOfWeek - 1)
        return currentDay % 7 * 13
      },
      getGrassListCount (list, chosenYear) {
        this.numOfDaysInYear = this.daysInYear(parseInt(chosenYear))
        this.startingDayOfWeek = new Date(parseInt(chosenYear), 0, 1).getDay()
        this.grassCount = new Array(this.numOfDaysInYear).fill(0)
        list.forEach(element => {
          if (time.utcToLocal(element, 'YYYY') === chosenYear) {
            var month = parseInt(time.utcToString(element, 'MM'))
            var day = parseInt(time.utcToString(element, 'DD'))
            var currentDay = this.whichDayInYear(month, day, this.numOfDaysInYear)
            this.grassCount[currentDay - 1] = this.grassCount[currentDay - 1] + 1
          }
        })
      },
      daysInYear (year) {
        return ((year % 4 === 0 && year % 100 > 0) || year % 400 === 0) ? 366 : 365
      },
      whichDayInYear (month, day, leapYear) {
        var dayInYear = 0
        for (let mo = 1; mo < month; mo++) {
          switch (mo) {
            case 1:
              dayInYear += 31
              break
            case 2:
              if (leapYear === 366) dayInYear += 29
              else dayInYear += 28
              break
            case 3:
              dayInYear += 31
              break
            case 4:
              dayInYear += 30
              break
            case 5:
              dayInYear += 31
              break
            case 6:
              dayInYear += 30
              break
            case 7:
              dayInYear += 31
              break
            case 8:
              dayInYear += 31
              break
            case 9:
              dayInYear += 30
              break
            case 10:
              dayInYear += 31
              break
            case 11:
              dayInYear += 30
              break
            case 12:
              dayInYear += 31
              break
            default:
              break
          }
        }
        dayInYear += day
        return dayInYear
      },
      numberOfProblemsSolved (day) {
        var number = this.grassCount[day]
        // console.log('current day ' + currentDay + ', number ' + number)
        if (number <= 0) return 'level1'
        else if (number < 2) return 'level2'
        else if (number < 4) return 'level3'
        else if (number < 6) return 'level4'
        else if (number > 7) return 'level5'
      }
    }
  }
</script>
<style lang="less" scoped>
@import '../../../../styles/common.less';

.flex-container {
  width:100%;
  text-align: center;
  font-weight: 400;
  font-size: 16px;
  margin-top: 50px;
  .flex-item {
    width:100%;
    overflow-x: auto;
  }
  .grass-container {
    width: 703px;
    height: 100px;
    margin: 0 auto;
  }
}
.grass-pointer {
  fill:@light-gray;
  rx: 2px;
  ry: 2px;
  height:10px; 
  width:10px;
  &.level1 {
    fill: @light-gray;
  }
  &.level2 {
    fill: @light-orange;
  }
  &.level3 {
    fill: @orange;
  }
  &.level4 {
    fill: @dark-orange;
  }
  &.level5 {
    fill: @deep-dark-orange;
  }
}
.flex-level-container {
  width:100%;
  text-align: center;
  font-weight: 400;
  font-size: 12px;
  margin-top: 10px;
  display: flex;
  flex-direction: row;
  justify-content: end;
  align-items: center;
  padding-right: 107px;
  .flex-level-item {
    height: 18px;
    .level-left {
      float: left;
      height: 18px;
    }
    .level-right {
      float: right;
      line-height: 18px;
      height: 18px;
      display: block;
      font-size: 12px;
      margin: auto;
      text-align: center;
      .text {
        display: block;
        float: left;
      }
      .svg-level-box {
        display: block;
        float: left;
        margin: auto 5px;
      }
      svg {
        rect {
          transform: translateY(50%);
          y: -5px;
        }
        height: 18px;
        line-height: 18px;
        margin: auto;
        text-align: center;
      }
    }
  }
  .grass-container {
    width: 703px;
    height: 100px;
    margin: 0 auto;
  }

  .level-svg {
    margin: 0 3px;
    display: block;
    float: left;
    width: 13px;
    &.last {
      width: 10px;
      margin-right: 0px;
    }
  }
}

@media screen and (max-width: 1500px) {
  .flex-container, .flex-level-container {
    display: none;
  }
}

@media screen and (min-width: 1500px) {
  .flex-container, .flex-level-container {
    display: flex;
  }
}
</style>