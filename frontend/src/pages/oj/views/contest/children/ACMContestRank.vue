<template>
  <div class="main">
    <div class="ranking-container">
      <div>
        <span>
          <h3 class="title" style="display:inline; float: left">{{ contest.title }} Ranking</h3>
          <Tooltip trigger="hover" placement="bottom" max-width="300"  style="display:inline; float: left; margin-left:4px;">
            <i class="mdi mdi-help-circle" id="help-icn"></i>
            <div slot="content" style="font-size: 7px;">
              <p>순위는 맞은 문제 > 틀린 횟수 > 총 시간 순서로 정해집니다</p>
            </div>
          </Tooltip>
        </span>
        <span @click="downloadRankCSV" class="my-position-btn"><i class="mdi mdi-download download-icon"></i>{{$t('m.download_csv')}}</span>
        <span class="update-rating-btn">
          <span class="title">자동 업데이트(10s)</span>
          <i-switch :disabled="refreshDisabled" @on-change="handleAutoRefresh" size="small" class="switch"></i-switch>
        </span>
      </div>

      <table class="ranking-list">
        <!-- 제목 -->
        <thead>
          <tr class="ranking_title">
            <td style="width: 15%">순위</td>
            <td style="width: 25%">아이디</td>
            <td style="width: 10%">맞은 문제</td>
            <td style="width: 20%">제출</td>
            <td style="width: 15%">정답 비율</td>
            <td style="width: 15%">Option</td>
          </tr>
        </thead>
        <!-- 내용 -->
        <tbody :ref="index + 'tbody'" v-for="(data, index) in dataRank" :v-model="data.visible" v-on:change="data.visible" :key="index">
          <tr>
            <td class="no"> {{toRank(index)}} </td>
            <td class="name" @click="goUser(data.user)">{{data.user.username}}</td>
            <td>{{data.accepted_number}}</td>
            <td>{{data.submission_number}}</td>
            <td>{{toPercent(data)}}</td>
            <td class="detail" @click="opemModal('vis', index)">detail</td>
          </tr>
          <Modal :ref="index + 'modal'" v-bind:value="isOpen(data)" :width="430" @on-cancel="closeModal(index)">
            <div slot="header" class="modal-title">{{data.user.username}}</div>
            <div class="modal-center">
              <div class="accepted-problems">맞은 문제 : {{data.accepted_number}}</div>
              <div class="total-submit">총 제출 수 : {{data.submission_number}}</div>
              <div class="total-time">총 시간 : {{data.total_time}}s</div>
              <div class="split-detail-box">Details</div>
              <div class="problem-details" v-for="(da, i, idx) in data.submission_info" v-bind="getProblemID(i, data.contest, idx, index)">
                <div class="problem-details-title">
                  <span :ref="index + 'p_title'"></span>
                  (<span :ref="index + 'p_id'"></span>)
                </div>
                <div class="problem-details-detail">
                  <div class="is-accepted">
                    <span>통과 여부 : </span>
                    <span v-if="da.is_ac" class="passed">Passed</span>
                    <span v-else class="failed">Failed</span>
                  </div>
                  <div class="ac-time">
                    <span>소요 시간 : </span>
                    <span>{{getTime(da.ac_time)}}</span>
                    <span> ({{da.ac_time}}s)</span>
                  </div>
                  <div class="first-blood">
                    <span>First Blood : </span>
                    <span v-if="da.is_first_ac" class="is-first">첫 통과자</span>
                    <span v-else>해당 없음</span>
                  </div>
                  <div class="fail-count">
                    <span>실패 횟수 : </span>
                    <span>{{da.error_number}}</span>
                  </div>
                  <div class="passed-per">
                    <span>성공률 : </span>
                    <span>{{getPercentage(da.error_number)}} % </span>
                  </div>
                </div>
              </div>
            </div>
            <div slot="footer" style="display: none"></div>
          </Modal>
        </tbody>
      </table>
      <Pagination :total="total" :page-size.sync="limit" :current.sync="page"
                  @on-change="getContestRankData(1)" show-sizer
                  @on-page-size-change="getContestRankData(1)"
                  style="margin: 20px 0 10px; display: flex; justify-content:center; float: none;"></Pagination>
      </div>
  </div>
</template>

<script>
  import api from '@oj/api'
  import Pagination from '@oj/components/Pagination'
  import utils from '@/utils/utils'
  import { RULE_TYPE } from '@/utils/constants'
  import ContestRankMixin from './contestRankMixin'
  import { mapGetters, mapActions } from 'vuex'
  export default {
    name: 'acm-rank',
    components: {
      Pagination
    },
    mixins: [ContestRankMixin],
    data () {
      return {
        modal: {
          username: '',
          submission_number: '',
          accepted_number: '',
          total_time: '',
          submissions: []
        },
        modalVisible: [],
        page: 1,
        total: 0,
        loadingTable: false,
        dataRank: [],
        forceupdatekey: 0
      }
    },
    mounted () {
      this.modalVisible = Array(300).fill({value: false})
      this.contestID = this.$route.params.contestID
      this.forceupdatekey = 0
      this.forceUpdate = true
      this.getContestRankData(1)
      // this.getRankData(1)
    },
    methods: {
      ...mapActions(['getContestProblems']),
      opemModal (data, index) {
        this.dataRank[index].visible = data
        this.forceupdatekey += 1
        this.$forceUpdate()
      },
      closeModal (index) {
        this.dataRank[index].visible = ''
        this.$forceUpdate()
      },
      isOpen (data) {
        return data.visible === 'vis'
      },
      getContestRankData (page = 1, refresh = false) {
        let offset = (page - 1) * this.limit
        let params = {
          offset,
          limit: this.limit,
          contest_id: this.$route.params.contestID,
          force_refresh: this.forceUpdate ? '1' : '0'
        }
        api.getContestRank(params).then(res => {
          this.total = res.data.data.total
          this.dataRank = res.data.data.results
          for (let v of this.dataRank) {
            v.visible = 'none'
          }
        })
      },
      downloadRankCSV () {
        utils.downloadFile(`contest_rank?download_csv=1&contest_id=${this.$route.params.contestID}&force_refrash=${this.forceUpdate ? '1' : '0'}`)
      },
      updateForceRating () {
        this.loadingTable = true
        api.updateForceRating().then(res => {
          this.getRankData(1)
          this.$success('업데이트가 완료되었습니다')
        }, _ => {
          this.loadingTable = false
          this.$error('업데이트에 실패하였습니다')
        })
      },
      goUser (user) {
        this.$router.push({
          name: 'user-home',
          query: {username: user.username}
        }).catch(() => {})
      },
      goMyPosition () {
        this.$router.push({
          name: 'user-position'
        }).catch(() => {})
      },
      toPercent (rank) {
        return utils.getACRate(rank.accepted_number, rank.submission_number)
      },
      toRating (rank) {
        return Math.floor(rank.rating_score * 100)
      },
      toRank (index) {
        return (this.page - 1) * this.limit + index + 1
      },
      getProblemID (problemID, contestID, idx, index) {
        api.getContestProblemID(problemID, contestID).then(res => {
          this.$refs[index + 'p_title'][idx].textContent = res.data.data.title
          this.$refs[index + 'p_id'][idx].textContent = res.data.data._id
          return res.data.data._id
        }, () => {
          this.$Loading.error()
        })
      },
      getTime (sec) {
        // Hours, minutes and seconds
        var days = ~~(sec / 86400)
        var hrs = ~~((sec % 86400) / 3600)
        var mins = ~~((sec % 3600) / 60)
        var secs = ~~sec % 60
        // Output like "1:01" or "4:03:59" or "123:03:59"
        var ret = ''
        if (hrs > 0) {
          if (days > 0) {
            ret += '' + days + '일 '
          }
          ret += '' + hrs + '시간 ' + (mins < 10 ? '0' : '')
        }
        ret += '' + mins + '분 ' + (secs < 10 ? '0' : '')
        ret += '' + secs + '초'
        return ret
      },
      getPercentage (count) {
        return Number(((1 / (count + 1)) * 100).toFixed(3))
      }
    },
    computed: {
      ...mapGetters(['isSuperAdmin', 'modalStatus'])
    },
    watch: {
      dataRank: {
        deep: true,
        handler (val) {
        }
      },
      $route (newVal, oldVal) {
      }
    }
  }
</script>

<style scoped lang="less">
@import '../../../../../styles/common.less';
  h3 {
    font-size: @font-medium;
    text-align: left;
    margin-bottom: 20px;
    color: @default-font-color;
  }
  .title {
    display:inline; 
    float: left;
  }
  #help-icn {
    font-style: normal;
    line-height: 22px;
    span {
      margin-left: 5px;
      color: #515a6e;
      font-size: 13px;
      font-weight: 400;
    }
    &:hover, &:hover > span {
      transition: all ease-in 0.1s;
      cursor: pointer;
      color: @dark-purple;
    }

  }  
  .update-rating-btn {
    display: inline;
    float: right;
    margin-right: 20px;
    height: 22px;
    line-height: 22px;
    font-weight: 700;
    .title {
      font-size: 12px;
      font-weight: 500;
      color:#515a6e;
      margin-right: 3px;
    }
    .switch {
      line-height: 22px;
      margin-bottom: 1px;
    }
  }
  .my-position-btn {
    display: inline;
    float: right;
    height: 22px;
    line-height: 22px;
    font-size: 13px;
    &:hover {
      color: @purple;
      cursor: pointer;
    }
  }
  .main {
    margin: auto;
    padding: 30px 20px;
    background-color: @white;
    border-radius: 5px;
    box-shadow: 0 1px 5px 0 rgba(0, 0, 0, 0.1);
    text-align: center;
  }
  .ranking-container {
    width: 100%;
    margin: auto;
  }
  .ranking-list {
    -webkit-text-stroke: .5px;
    border-collapse: collapse;
    width: 100% !important; 
    table-layout: fixed;
    text-align: center;
    padding: 8px;
    margin: auto;
    thead {
      border-bottom: 1px solid #c4c4c4;
      color: @gray;
      background-color: @light-gray;
    }
    td {
      padding: 8px;
      font-size: 12px;
    }
    th {
      padding: 8px;
    }
    tbody {
      color: @black;
      -webkit-text-stroke: .3px;
      height: 40px;
      font-size: @font-micro;
      tr {
        // cursor: pointer;
      }
      .image {
        position: relative;
        img {
          width: 30px;
          height: 30px;
        }
        .top {
          position:absolute;
          transform: translate( -50%, -50% );
          top: 55%;
          left: 50%;
          color: @black;
          -webkit-text-stroke: .5px;
        }
        .third {
          color: @white;
        }
      }
    }
  }
  .name {
    cursor: pointer;
    &:hover {
      color: @orange;
      transition: color .3s ease-in-out;
      }
    }
  .detail {
    color: @purple;
    cursor: pointer;
    &:hover {
      color: @orange;
      transition: color .3s ease-in-out;
      }
    }

  .modal-title {
    font-size: 16px;
    font-weight: 700;
  }
  .modal-center {
    .accepted-problems {
      height: 20px;
    }
    .total-submit {
      height: 20px;
    }
    .total-time {
      height: 20px;
    }
    .split-detail-box {
      font-size: 14px;
      font-weight: 500;
      height: 30px;
      line-height: 30px;
      border-bottom: solid 1px;
      margin-bottom: 10px;
    }
    .problem-details {
      padding-left: 5px;
      padding-right: 5px;
      border-bottom: solid 1px @light-white;
      padding-bottom: 10px;
      margin-bottom: 5px;
      .problem-details-title {
        font-weight: 700;
        margin-bottom: 5px;
        padding-left: 5px;
        padding-right: 5px;
      }
      .problem-details-detail {
        background-color: @light-white;
        padding: 7px;
        border-radius: 5px;

        .is-accepted {
          .passed {
            font-weight: 700;
            color: @dark-green;
          }
          .failed {
            font-weight: 700;
            color: @red;
          }
        }
        .ac-time {
        }
        .first-blood{
          .is-first {
            font-weight: 700;
            color: @purple;
          }
        }
        .fail-count {
        }

      }
    }
  }
  .download-icon {
    font-size: 14px;
    margin-right: 2px;
  }
</style>