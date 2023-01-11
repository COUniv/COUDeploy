<template>
  <div v-if="listVisible" class="home_container">
    <div class="img_container" style="width: 100%;">
      <Carousel v-model="value1" loop arrow="hover" :autoplay="bannerOpt.autoplay">
          <CarouselItem v-for="(item, idx) in bannerList" :key="idx">
            <div class="demo-carousel">
              <img :src="item.url"/>
            </div>
          </CarouselItem>
      </Carousel>
      <!-- <Button @click="value1 = 2">change</Button> -->
    </div>
    <div class="main_container">
      <div class="list_container">
        <div class="left_announcement">
          <ul class="tab-menu">
            <li v-for="(tab, index) in tabs" :key="index" class="tab-item" @click="currentTab = index" :class="{ active: currentTab===index }">
              <p>{{tab}}</p>
            </li>
            <Dropdown v-show="currentTab == 1" @on-click="onStatusChange" :transfer="true" class="contest-status-list" trigger="click">
                <span>{{contest_stat === '' ? this.$i18n.t('m.Status') : this.$i18n.t('m.' + CONTEST_STATUS_REVERSE[contest_stat].name.replace(/ /g,"_"))}}
                </span>
                <Icon type="ios-arrow-down" />
                <Dropdown-menu slot="list" >
                  <Dropdown-item name="">모든 대회</Dropdown-item>
                  <Dropdown-item name="0">진행 중인 대회</Dropdown-item>
                  <Dropdown-item name="1">개최 예정인 대회</Dropdown-item>
                </Dropdown-menu>
              </Dropdown>
            <div class="plus" @click="addPage"><Icon type="ios-arrow-forward" size="40"/></div>
          </ul>
          
          <div class="tab-content">
            <!-- 공지사항 탭-->
            <div v-show="currentTab == 0">
              <div v-if="!announcements.length" class="no_announcement">
                공지사항이 없습니다
              </div>
              <div v-else v-for="announcement in announcements" :key="announcement.title" class="announcement_title">
                <div v-if="isAuthenticated" class="announcement-title-box" @click="goAnnouncement(announcement)">
                  <a>
                    {{announcement.title}}
                  </a>
                </div>
                <div v-else class="announcement-title-box-no-click">
                  <a>
                    {{announcement.title}}
                  </a>
                </div> 
                <div class="announcement-time"> {{announcement.create_time | localtime('YYYY.MM.DD') }} </div> 
                <div style="clear:both;"></div>
              </div>
              <div style="clear:both;"></div>
            </div>
            <!-- 대회일정 탭-->
            <div v-show="currentTab == 1">
              <div v-if="!contests.length" class="no_contest">
                대회일정이 없습니다
              </div>
              <div class="contest_title" v-for="(contest, contest_idx) in contests" :key="contest_idx" @click="goContest">
                <div v-if="contest.status == '1'">
                  <div style="float:left"><Tag style="margin-top:0px" type="dot" :color="CONTEST_STATUS_REVERSE[contest.status].color">{{$t('m.' + CONTEST_STATUS_REVERSE[contest.status].name.replace(/ /g, "_"))}}</Tag></div>
                  <div class="color-yellow"> {{contest.title}} </div>
                  <div class="contest-time"> {{contest.start_time | localtime('YYYY.MM.DD')}}
                  </div>
                  <div style="clear:both"></div>
                </div>
                <div v-else-if="contest.status == '0'">
                  <div style="float:left"><Tag style="margin-top:0px" type="dot" :color="CONTEST_STATUS_REVERSE[contest.status].color">{{$t('m.' + CONTEST_STATUS_REVERSE[contest.status].name.replace(/ /g, "_"))}}</Tag></div>
                  <div class="color-green"> {{contest.title}} </div>
                  <div class="contest-time"> {{contest.start_time | localtime('YYYY.MM.DD')}}
                  </div>
                  <div style="clear:both"></div>
                </div>
                <!-- 해당 부분은 종료된 contest를 표시하지만 실제로는 사전 필터링으로 인해 사용되지 않습니다
                추후 종료된 컨텐츠를 사용하고자 할 때 쓰일 수 있도록 두었습니다. -->
                <div v-else-if="contest.status == '-1'">
                  <div style="float:left"><Tag style="margin-top:0px" type="dot" :color="CONTEST_STATUS_REVERSE[contest.status].color">{{$t('m.' + CONTEST_STATUS_REVERSE[contest.status].name.replace(/ /g, "_"))}}</Tag></div>
                  <div class="color-red"> {{contest.title}} </div>
                  <div class="contest-time"> {{contest.start_time | localtime('YYYY.MM.DD')}}
                  </div>
                  <div style="clear:both"></div>
                </div>
                <div style="clear:both;"></div>
              </div>
            </div>
          </div>

        </div>
        <div class="right_rankings">
          <table>
            <!-- 제목 -->
            <thead>
              <tr class="ranking_title">
                <td>순위</td>
                <td>아이디</td>
                <td>레이팅</td>
              </tr>
            </thead>
            <!-- 내용 -->
            <tbody class="rankings_user" v-for="(data, index) in dataRank" :key="data.user.username" @click="goUser(data.user)">
              <tr v-if="index == 0" class="ranker first">
                <td class="image">
                  <img class="rankings-img" src="../../../../assets/gold crown.png"/>
                  <span class="no">1</span>
                </td>
                <td class="name">{{data.user.username}}</td>
                <td class="score">{{convertRating(data)}}</td>
              </tr>
              <tr v-else-if="index == 1" class="ranker second">
                <td class="image">
                  <img class="rankings-img" src="../../../../assets/silver crown.png"/>
                  <span class="no">2</span>
                </td>
                <td class="name">{{data.user.username}}</td>
                <td class="score">{{convertRating(data)}}</td>
              </tr>
              
              <tr v-else-if="index == 2" class="ranker third">
                <td class="image">
                  <img class="rankings-img" src="../../../../assets/bronse crown.png"/>
                  <span class="no" style="color: white">3</span>
                </td>
                <td class="name">{{data.user.username}}</td>
                <td class="score">{{convertRating(data)}}</td>
              </tr>
              <tr v-else-if="index == 3" class="ranker defa">
                <td class="no">4</td>
                <td class="name">{{data.user.username}}</td>
                <td class="score">{{convertRating(data)}}</td>
              </tr>
              <tr v-else-if="index == 4" class="ranker defa">
                <td class="no">5</td>
                <td class="name">{{data.user.username}}</td>
                <td class="score">{{convertRating(data)}}</td>
              </tr>
              <tr v-else-if="index == 5" class="ranker defa">
                <td class="no">6</td>
                <td class="name">{{data.user.username}}</td>
                <td class="score">{{convertRating(data)}}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div class="problem-category-container">
        <ProblemCategory></ProblemCategory>
      </div>
    </div>

  </div>
  <div v-else style="padding-left:50px; padding-right:50px">
    <Panel shadow :padding="20">
    <div style="line-height: 50px; display: flex; flex-direction: column;" slot="title">
      <div>
        <i v-if="!listVisible" id="back-button" @click="goBack" class="mdi mdi-arrow-left-circle"></i>
        {{title}}
      </div>
      <div v-if="!listVisible" class="announcements-container-header">
        <div class="div-first-box">{{ createName }}</div>
        <div>|</div>
        <div>{{ createDate }}</div>
      </div>
    </div>
    <div slot="extra">
      <Button v-if="listVisible" type="info" @click="init" :loading="btnLoading">{{$t('m.Refresh')}}</Button>
    </div>
    <Row type="flex" justify="space-around">
      <Col :span="22">
        <transition-group name="announcement-animate" mode="in-out">
          <template>
            <div v-katex v-html="announcement.content" key="content" class="content-container markdown-body"></div>
          </template>
        </transition-group>
      </Col>
    </Row>
  </Panel>
  </div>
  
</template>

<script>
  import Announcements from './Announcements.vue'
  import ProblemCategory from '../problem/ProblemCategory.vue'
  import api from '@oj/api'
  import time from '@/utils/time'
  import { CONTEST_STATUS_REVERSE } from '@/utils/constants'
  import { mapGetters } from 'vuex'
  import Panel from '../../components/Panel.vue'
  export default {
    name: 'home',
    components: {
      Announcements,
      ProblemCategory,
      Panel
    },
    data () {
      return {
        tabfirstidx: 0,
        tabsecidx: 1,
        limit: 5,
        total: 5,
        btnLoading: false,
        announcements: [],
        announcement: '',
        contest_idx: 0,
        value1: 0,
        bannerList: [],
        bannerOpt: {
          size: 0,
          autoplay: false
        },
        dataRank: [],
        contests: [],
        contest_stat: '',
        query: {
          status: '',
          keyword: '',
          rule_type: ''
        },
        currentTab: 0,
        tabs: ['공지사항', '대회일정'],
        CONTEST_STATUS_REVERSE: CONTEST_STATUS_REVERSE
      }
    },
    mounted () {
      this.query.status = ''
      this.query.rule_type = ''
      this.query.keyword = ''
      this.getAnnouncementList()
      this.getRankData(1)
      this.getContestList()
      this.getUsingBannerList()
      this.$store.commit('setlistVisible')
    },
    methods: {
      toggleVisible () {
        this.$store.commit('toggleVisible')
      },
      getUsingBannerList () {
        api.getUsingBannerList().then(res => {
          let temp = []
          temp = res.data.data
          if (temp.length < 2) {
            if (temp.length < 1) {
              temp.push({url: '/public/banner/default.png'})
            }
            this.bannerList = temp
            this.bannerOpt.size = this.bannerList.length
            this.bannerOpt.autoplay = false
          } else {
            this.bannerList = temp
            this.bannerOpt.size = this.bannerList.length
            this.bannerOpt.autoplay = true
          }
        }, () => {
          this.$error('배너를 불러오지 못했습니다.')
          this.bannerList.push({banner: '/public/banner/default.png'})
          this.bannerOpt.size = this.bannerList.length
          this.bannerOpt.autoplay = false
        })
      },
      getContestList (page = 1) {
        api.getContestList(0, this.limit, this.query).then((res) => {
          let notfiltercontests = res.data.data.results
          let contestlist = []
          // 종료된 contest는 필터링
          for (let v in notfiltercontests) {
            if (notfiltercontests[v].status === undefined || notfiltercontests[v].status === null || notfiltercontests[v].status === -1 || notfiltercontests[v].status === '-1') {
              continue
            }
            contestlist.push(notfiltercontests[v])
          }
          this.contests = contestlist
        }, () => {
          this.contests = []
        }).catch(() => {
          this.contests = []
        })
      },
      getRankData (page = 1) {
        let offset = (page - 1) * this.limit
        api.getUserRatingRank(offset, this.limit).then(res => {
          this.dataRank = res.data.data.results
          // bar.hideLoading()
        }).catch(() => {
        })
      },
      getAnnouncementList (page = 1) {
        this.btnLoading = true
        api.getAnnouncementList((page - 1) * this.limit, this.limit).then(res => {
          this.btnLoading = false
          this.announcements = res.data.data.results
          this.total = res.data.data.total
        }, () => {
          this.btnLoading = false
        })
      },
      convertDate (item) {
        return time.utcToLocal(item, 'YYYY-MM-DD HH:mm')
      },
      convertRating (item) {
        return Math.floor(item.rating_score * 100)
      },
      goUser (user) {
        this.$router.push({
          name: 'user-home',
          query: {username: user.username}
        }).catch(() => {})
      },
      goAnnouncement (announcement) {
        this.announcement = announcement
        this.toggleVisible()
      },
      getDuration (startTime, endTime) {
        return time.duration(startTime, endTime)
      },
      goBack () {
        this.toggleVisible()
        this.announcement = ''
      },
      goContest () {
        this.$router.push({
          name: 'contest-details',
          params: {contestID: this.contests[this.contest_idx].id}
        }).catch(() => {})
      },
      onStatusChange (status) {
        this.query.status = status
        this.contest_stat = status
        this.getContestList()
      },
      addPage () {
        if (this.currentTab === 0) {
          this.$router.push('/announcement-list').catch(() => {})
        } else if (this.currentTab === 1) {
          this.$router.push('/contest').catch(() => {})
        }
      }
    },
    computed: {
      ...mapGetters(['isAuthenticated']),
      title () {
        if (this.listVisible) {
          return this.$i18n.t('m.Announcements')
        } else {
          return this.announcement.title
        }
      },
      createName () {
        return this.announcement.created_by.username
      },
      createDate () {
        return this.convertDate(this.announcement.create_time)
      },
      listVisible () {
        return this.$store.getters.listVisible
      }
    }
  }
</script>

<style lang="less" scoped>
@import '../../../../styles/common.less';

  // .home_container{
  //   margin-top: -18px;
  //   padding-bottom: -120px;
  //   // margin-bottom: -0px
  // }

  @media screen and (max-width: 1200px) {
    .home_container{
      margin: -40px -50px -100px -50px;
      padding-bottom: -80px;
    }
  }
  @media screen and (min-width: 1200px) {
    .home_container{
      margin: -40px -50px -100px -50px;
      padding-bottom: -80px;
    }
  }
  .img_container{
    // margin-right: 21%;
    // padding-left : 20%;
    // margin: -40px -50px 0 -50px;
    // margin-top : -20px;
    // margin-bottom : -20px;
    // display: flex;
    // width: 80%; 
    // justify-content : center;
  }

  .home_header{
    height: 50%;
    width: 100%;
  }

  .demo-carousel{
    display: inline-block;
    // height: 456px;
    width: 100%;
    height: auto;
    //line-height: 60vh;
    //line-height: 456px;
    text-align: center;
    justify-content: center;
    color: #fff;
    font-size: 20px;
    background: #fafafa;
    img {
      display: inline-block;
      width: 100%;
      height: calc(100vw * 303.0 / 1280.0);
      max-height: 303px;
      max-width: 1180px;
    }
  }

  .contest {
    &-title {
      font-style: italic;
      font-size: 21px;
    }
    &-content {
      padding: 0 70px 40px 70px;
      &-description {
        margin-top: 25px;
      }
    }
  }
  .announcement-title-box {
    position: relative;
    float: left;
    height: 34px;
    line-height: 34px;
    font-size: 1rem;
    width: calc(80% - 40px);
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .announcement-title-box-no-click {
    position: relative;
    float: left;
    height: 34px;
    line-height: 34px;
    font-size: 1rem;
    width: calc(80% - 40px);
    overflow: hidden;
    text-overflow: ellipsis;
    cursor: none;
    pointer-events: none;
  }
  .announcement-time {
    // display: none;
    float: right;
    height: 34px;
    line-height: 34px;
    font-size: 14px;
    color: @gray;
  }
  .color-red {
    color: #ed4014;
    font-size: 1rem;
    transition: all 0.1s ease-in-out;
    height: 34px;
    line-height: 34px;
    float: left;
    padding-left: 10px;
    width: calc(95% - 170px); // default size - left button size(90px) - times(80px)
    overflow: hidden;
    text-overflow: ellipsis;
    &:hover {
      cursor: pointer;
      font-weight: 700;
      color: #ed4014;
    }
  }

  .color-green {
    color: rgba(2, 148, 2, 0.722);
    font-size: 1rem;
    transition: all 0.1s ease-in-out;
    height: 34px;
    line-height: 34px;
    float: left;
    padding-left: 10px;
    width: calc(95% - 170px); // default size - left button size(90px) - times(80px)
    overflow: hidden;
    text-overflow: ellipsis;
    &:hover {
      cursor: pointer;
      font-weight: 700;
      color: rgba(2, 137, 2, 0.722);
    }
  }

  .color-yellow {
    color: rgba(208, 170, 2, 0.922);
    font-size: 1rem;
    transition:all 0.1s ease-in-out;
    height: 34px;
    line-height: 34px;
    float: left;
    padding-left: 10px;
    width: calc(95% - 170px); // default size - left button size(90px) - times(80px)
    overflow: hidden;
    text-overflow: ellipsis;
    &:hover {
      cursor: pointer;
      font-weight: 700;
      color: rgba(231, 189, 4, 0.922);
    }
  }

  .color-red {
    color: rgba(208, 49, 0, 0.922);
    font-size: 1rem;
    transition:all 0.1s ease-in-out;
    height: 34px;
    line-height: 34px;
    float: left;
    padding-left: 10px;
    width: calc(95% - 170px); // default size - left button size(90px) - times(80px)
    overflow: hidden;
    text-overflow: ellipsis;
    &:hover {
      cursor: pointer;
      font-weight: 700;
      color: rgba(230, 54, 0, 0.922);
    }
  }
  .announcement {
    margin-top: 20px;
  }

  .main_container{
    display: block;
    margin: 50px 0 0 0;
    padding: 0 20%;
    width: 100%;
    // height: 100vh;
  }

  .list_container{
    display: flex;
    // margin: 10px 0 0 0;
    // padding: 0 20%;
    width: 100%;
    height: auto;
    flex-wrap: wrap;
    margin-bottom: 20px;
    // background: #506b9e;
  }

  .left_announcement{
    display: inline-block;
    vertical-align: top;
    width: calc(~"60% - 30px");
    min-width: 440px;
    flex-grow: 1;
    height: 450px;
    padding: 20px;
    margin: 15px 15px;
    background: #ffffff;
    border-radius: 5px;
    box-shadow: 2px 5px 20px 2px rgba(90, 82, 128, 0.31);
    // border-bottom: 1px solid rgb(213, 213, 213);
    // border-right: 1px solid rgb(208, 208, 208);
    ul.tab-menu {
      list-style: none;
      display: flex;
      position: relative;
      margin-bottom: 15px;
      li.tab-item {
        margin-right: 10px;
        padding: 10px 24px;
        border-radius: 25px;
        font-size: 18px;
        font-weight: @weight-bold;
        background-color: @light-gray;
        // transition: all 0.2s ease-in-out;
        &:hover {
          cursor: pointer;
        }
        p {
          color: @gray;
          &:hover {
            text-decoration:underline;
          }
        }
        &.active {
          transition: all 0.3s ease-in;
          background-color: @dark-orange;
          p {
            color: @white;
          }
        }
      }
      .plus {
        position: absolute;
        padding: 5px;
        right: 0;
        cursor: pointer;
        & i {
          transition: all 0.2s ease-in-out;
          border: 2px solid @light-gray;
          color: #858585 !important;
        }
        &:hover i {
          transform: rotate( 360deg );
          border: 2px solid @light-purple;
          color: @purple !important;
        }
      }
    }
  }

  .tab-content {
    .no_announcement, .no_contest {
      text-align: center;
      padding: 120px 0;
      font-size: 20px;
      color: @gray;
    }
  }

  .announcement_title, .contest_title{
    padding: 8px 14px;
    margin-bottom: 10px;
    border: 1px solid @light-gray;
    border-radius: 5px;
    font-size: 18px;
    overflow: hidden;
    text-overflow: ellipsis;
    // height: 2.8em;
    line-height: 1.7em;
    width: 100%;
    white-space: nowrap;
    a {
      color: @black;
      &:hover {
        color: @dark-orange;
      }
    }
  }
  .tabpan_padding {
    padding: 0px 10px 10px 10px;
  }
  .tabpan_padding-s {
    padding: 0px 10px 10px 10px;
  }
  table {
    width: 100%;
    td {
      text-align: center;
    }
    thead:after {
      content: "-";
      display: block; 
      line-height: 1.5em;
      color: transparent;
    }
  }

  .right_rankings{
    display: inline-block;
    vertical-align: top;
    margin: 15px 15px;
    border: 1px solid rgb(226, 226, 226);
    border-radius: 5px;
    padding: 30px 20px 10px 20px;
    width: calc(~"37% - 30px");
    min-width: 270px;
    flex-grow: 1;
    height: 450px;
    background: white;
    box-shadow: 2px 5px 20px 2px rgba(90, 82, 128, 0.31);
    // background: #dfdfdf;
    .ranking_title {
      color: @gray;
      font-size: 16px;
      margin-bottom: 20px;
    }
    .rankings_user {
      margin-bottom: 10px;
      font-size: 14px;
      height: 57px;
      width: 100%;
      .ranker {
        position: relative;
        height: 42px;
        line-height: 42px;
        margin-left: 15px;
        color: @black;
        font-weight: 600;
        &:hover {
          cursor: pointer;
          .name, .score{
            color: @dark-orange;
            transition-duration: 3ms;
          }
        }
        .image {
          position: relative;
          .no {
            position: absolute;
            font-weight: bold;
            top: 50%;
            left: 50%;
            transform: translate( -50%, -50% );
          }
        }
      }
    }
  }
  .content-container {
    padding: 0 20px 20px 20px;
  }
  .problem-category-container {
    margin: 10px 15px;
  }
  .announcement-animate-enter-active {
    animation: fadeIn 1s;
  }

  .ivu-tabs.ivu-tabs-card>.ivu-tabs-bar .ivu-tabs-tab{
    font-size: 20px;
    height: 35px;
    padding-top: 0px;
  }

</style>

<style lang="less" scoped>
@import '../../../../styles/common.less';

  .rankings-img {
    width: 35px;
    height: 35px;
    margin-top: 3px;
  }

  .contest-status-list {
    cursor: pointer;
    position: absolute;
    right: 64px;
    top: 16px;
    font-size: 14px;
    &:hover {
      color: @dark-orange;
    }
    * {
      z-index: 1000;
    }
  }

  .contest-time {
    float: right;
    height: 34px;
    line-height: 34px;
    font-size: 14px;
    color: @gray;
    pointer-events: none;
    z-index: 997;
  }
  @media screen and (max-width : 900px) {

    .home_container {
      margin: -20px -50px -100px -50px;
      display: flex;
      flex-direction: column;
      align-items: center;
    }
    .demo-carousel{
    display: inline-block;
    // height: 456px;
    width: 100%;
    height: auto;
    //line-height: 60vh;
    //line-height: 456px;
    text-align: center;
    justify-content: center;
    color: #fff;
    font-size: 20px;
    background: #fafafa;
      img {
        display: inline-block;
        width: 100%;
        height: calc(100vw * 303.0 / 1280.0);
        max-height: 303px;
        max-width: 1180px;
      }
    }
    .img_container {
      //display: none;
    }
    .main_container{
      display: flex;
      align-items: center;
      flex-direction: column;
      margin-top: 50px;
      margin-right: 0px !important;
      padding: 0 0;
      width: 90vw;
      // height: 100vh;
      .list_container {
        display: flex;
        flex-direction: column;
        align-items: center;
        min-width: 100%;
        margin: 0;
        .left_announcement {
          min-width: 100%;
          min-height: 100%;
          margin: 0;
          .tab-item {
            padding: 10px 16px;
            font-size: 1.4em;
          }
          .contest-status-list {
            position: absolute;
            right: 40px;
            span {
              //font-size: 12px;
            }
            i {
              visibility: hidden;
            }
          }
          .plus {
            padding: 0;
          }
        }
        .right_rankings {
          min-width: 100%;
          margin: 20px 0 0;
        }
      }
      .problem-category-container {
        width: 90vw;
      }
    }
    
  }
  #back-button {
    font-size: 120%;
    padding: 0px 8px;
    color: @gray;
    transition: all ease-in 0.1s;
    &:hover, &:focus {
      color: @dark-purple;
      opacity: 0.8;
      border-color: transparent;
      box-shadow: 0 0 0 transparent;
    }
  }
  .announcements-container-header-title {
    display:flex; 
    flex-direction: row;
  }
  .announcements-container-header {
    display:flex; 
    flex-direction: row;
    font-size: small;
    color: @gray;
    margin-bottom: 15px;
    .div-first-box {
      margin-left: 50px;
    }
    div {
      margin-right: 4px;
    }
  }
</style>
