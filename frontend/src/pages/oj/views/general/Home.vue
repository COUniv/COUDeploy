<template>
  <div v-if="listVisible" class="home_container">

    <div class="img_container" style="width: 100%;">
        <Carousel autoplay v-model="value1" loop arrow="hover" @on-change="handleChange">
            <CarouselItem>
                <div class="demo-carousel">
                  <img src="../../../../assets/main01.png" />
                </div>
            </CarouselItem>
            <CarouselItem>
                <div class="demo-carousel">
                  <img src="../../../../assets/main01.png" />
                </div>
            </CarouselItem>
            <CarouselItem>
                <div class="demo-carousel">
                  3
                </div>
            </CarouselItem>
            <CarouselItem>
                <div class="demo-carousel">4</div>
            </CarouselItem>
        </Carousel>
        <!-- <Button @click="value1 = 2">change</Button> -->
    </div>
    <div class="main_container">
      <div class="list_container" style="display: block">
        <div class="left_announcement" style="float:left">
          <ul class="tab-menu">
            <li v-for="(tab, index) in tabs" :key="index" class="tab-item" :class="{ active: currentTab===index }">
              <a @click="currentTab = index">{{tab}}</a>
            </li>
            <Dropdown v-show="currentTab == 1" @on-click="onStatusChange" :transfer="true" class="contest-status-list">
                <span>{{contest_stat === '' ? this.$i18n.t('m.Status') : this.$i18n.t('m.' + CONTEST_STATUS_REVERSE[contest_stat].name.replace(/ /g,"_"))}}
                </span>
                <Icon type="ios-arrow-down" />
                <Dropdown-menu slot="list" >
                  <Dropdown-item name="">모든 대회</Dropdown-item>
                  <Dropdown-item name="0">진행 중인 대회</Dropdown-item>
                  <Dropdown-item name="1">개최 예정인 대회</Dropdown-item>
                </Dropdown-menu>
              </Dropdown>
            <div class="plus" @click="addPage"><Icon type="md-add" size="30" color="#858585"/></div>
          </ul>
          
          <div class="tab-content">
            <!-- 공지사항 탭-->
            <div v-show="currentTab == 0">
              <div v-if="!announcements.length" class="no_announcement">
                공지사항이 없습니다
              </div>
              <div v-else v-for="announcement in announcements" :key="announcement.title" class="announcement_title" @click="goAnnouncement(announcement)">
                <div class="announcement-title-box">
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
                <div style="clear:both;"></div>
                    </div>
            </div>
          </div>
          <!-- <Row :gutter="32"> -->
            <!-- <Col span="12" class="demo-tabs-style1" style="background: #ebebeb;"> -->

              <!-- <Tabs value="name1" type="card" :animated="false">
                <div v-if="!announcements.length" key="no-announcement">
                  <TabPane :index=0 label="공지사항" name="name1" class="tabpan_padding">
                    <p class="announcement_title">{{$t('m.No_Announcements')}}</p>
                  </TabPane>
                </div>
                <div v-else>
                  <TabPane :index=1 label="공지사항" name="name1" class="tabpan_padding">
                    <div v-for="announcement in announcements" :key="announcement.title" class="announcement_title" @click="goAnnouncement(announcement)">
                      <div class="announcement-title-box">
                        <a>
                          ▶︎ {{announcement.title}}
                        </a>
                      </div>
                      <div class="announcement-time"> {{announcement.create_time | localtime('YY/M/D') }} </div>
                      <div style="clear:both;"></div>
                    </div>
                    <div style="clear:both;"></div>
                  </TabPane>
                </div>
                <div>
                  <TabPane v-model="contest_idx" :index=1 label="대회일정" name="name2" class="tabpan_padding-s">
                    <Dropdown @on-click="onStatusChange" :transfer="true" class="contest-status-list">
                      <span>{{contest_stat === '' ? this.$i18n.t('m.Status') : this.$i18n.t('m.' + CONTEST_STATUS_REVERSE[contest_stat].name.replace(/ /g,"_"))}} -->
                        <!-- <Icon type="arrow-down-b"></Icon> -->
                        <!-- <Icon type="md-arrow-dropdown" />
                      </span>
                      <Dropdown-menu slot="list">
                        <Dropdown-item name="">모든 대회</Dropdown-item>
                        <Dropdown-item name="0">진행 중인 대회</Dropdown-item>
                        <Dropdown-item name="1">개최 예정인 대회</Dropdown-item>
                      </Dropdown-menu>
                    </Dropdown>

                    <div class="contest_title" v-for="(contest, contest_idx) in contests" :key="contest_idx" @click="goContest">
                      <div v-if="contest.status == '1'">
                        <div style="float:left"><Tag style="margin-top:0px" type="dot" :color="CONTEST_STATUS_REVERSE[contest.status].color">{{$t('m.' + CONTEST_STATUS_REVERSE[contest.status].name.replace(/ /g, "_"))}}</Tag></div>
                        <div class="color-yellow"> {{contest.title}} </div>
                        <div class="contest-time"> {{contest.start_time | localtime('YY/M/D')}} -->
                          <!-- ~ {{contest.end_time | localtime('YY/M/D')}}  -->
                        <!-- </div>
                        <div style="clear:both"></div>
                      </div>
                      <div v-else-if="contest.status == '0'">
                        <div style="float:left"><Tag style="margin-top:0px" type="dot" :color="CONTEST_STATUS_REVERSE[contest.status].color">{{$t('m.' + CONTEST_STATUS_REVERSE[contest.status].name.replace(/ /g, "_"))}}</Tag></div>
                        <div class="color-green"> {{contest.title}} </div>
                        <div class="contest-time"> {{contest.start_time | localtime('YY/M/D')}} -->
                          <!-- ~ {{contest.end_time | localtime('YY/M/D')}}  -->
                        <!-- </div>
                        <div style="clear:both"></div>
                      </div>
                      <div style="clear:both;"></div>
                    </div>
                  </TabPane>
                </div>
              </Tabs> -->
            <!-- </Col> -->
          <!-- </Row> -->
        </div>
        <div class="right_rankings" style="float:right">
          <div class="rankings_title">사용자 순위</div>
          <div style="padding: 30px">
            <div class="rankings_user" v-for="(data, index) in dataRank" :key="data.user.username" @click="goUser(data.user)">
              <!-- <span v-if="index > 2">{{index + 1}} 등 : </span> -->
              <a v-if="index == 0" class="first">
                <img class="rankings-img" src="../../../../assets/rank1.png"/>
                {{data.user.username}}
              </a>
              <a v-else-if="index == 1" class="second">
                <img class="rankings-img" src="../../../../assets/rank2.png"/>
                {{data.user.username}}
              </a>
              <a v-else-if="index == 2" class="third">
                <img class="rankings-img" src="../../../../assets/rank3.png"/>
                {{data.user.username}}
              </a>
              <a v-else class="defa">
                <img v-if="index == 3" class="rankings-img" src="../../../../assets/rank4.png"/>
                <img v-if="index == 4" class="rankings-img" src="../../../../assets/rank5.png"/>
                {{data.user.username}}
              </a>
            </div>
          </div>
        </div>
      </div>
      <ProblemCategory style="margin: 20px 0 0 0"></ProblemCategory>
    </div>
    <!-- <Announcements class="announcement"></Announcements> -->
    <!-- </Col>
  </Row> -->
  </div>
  <div v-else>
    <Panel shadow :padding="10">
    <div slot="title">
      {{title}}
    </div>
    <div slot="extra">
      <Button v-if="listVisible" type="info" @click="init" :loading="btnLoading">{{$t('m.Refresh')}}</Button>
      <Button v-else icon="ios-undo" @click="goBack">{{$t('m.Back')}}</Button>
    </div>
    <transition-group name="announcement-animate" mode="in-out">
      <template>
        <div v-katex v-html="announcement.content" key="content" class="content-container markdown-body"></div>
      </template>
    </transition-group>
  </Panel>
  </div>
  
</template>

<script>
  import Announcements from './Announcements.vue'
  import ProblemCategory from '../problem/ProblemCategory.vue'
  import api from '@oj/api'
  import time from '@/utils/time'
  import { CONTEST_STATUS_REVERSE, CONTEST_STATUS, RULE_TYPE } from '@/utils/constants'
  import { mapGetters } from 'vuex'
  export default {
    name: 'home',
    components: {
      Announcements,
      ProblemCategory
    },
    data () {
      return {
        tabfirstidx: 0,
        tabsecidx: 1,
        limit: 5,
        total: 5,
        btnLoading: false,
        listVisible: true,
        announcements: [],
        announcement: '',
        contest_idx: 0,
        value1: 0,
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
    },
    methods: {
      getContestList (page = 1) {
        api.getContestList(0, this.limit, this.query).then((res) => {
          this.contests = res.data.data.results
        })
      },
      getRankData (page = 1) {
        let offset = (page - 1) * this.limit
        api.getUserRank(offset, this.limit, RULE_TYPE.ACM).then(res => {
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
      goUser (user) {
        this.$router.push({
          name: 'user-home',
          query: {username: user.username}
        }).catch(() => {})
      },
      goAnnouncement (announcement) {
        this.announcement = announcement
        this.listVisible = false
      },
      getDuration (startTime, endTime) {
        return time.duration(startTime, endTime)
      },
      goBack () {
        this.listVisible = true
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
      handleChange (old, newval) {
        // console.log(old, newval)
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
      margin: -20px -50px -100px -50px;
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
    // height: 456px;
    height: 60vh;
    line-height: 60vh;
    // line-height: 456px;
    text-align: center;
    justify-content: center;
    color: #fff;
    font-size: 20px;
    background: #000000;
    img {
      width: 100%;
      height: 100%;
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
  .announcement-time {
    // display: none;
    float: right;
    height: 34px;
    line-height: 34px;
    font-size: 14px;
    color: @gray;
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
    display: block;
    // margin: 10px 0 0 0;
    // padding: 0 20%;
    width: 100%;
    height: 450px;
    margin-bottom: 50px;
    // background: #506b9e;
  }

  .left_announcement{
    display: inline-block;
    vertical-align: top;
    width: 60%;
    height: 450px;
    padding: 20px;
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
        padding: 10px 30px;
        border-radius: 25px;
        font-size: 20px;
        font-weight: @weight-bold;
        background-color: @light-gray;
        a {
          color: @gray;
        }
        &.active {
          background-color: @dark-orange;
          a {
            color: @white;
          }
        }
      }
      .plus {
        border: 2px solid @light-gray;
        position: absolute;
        padding: 5px;
        top: 5px;
        right: 0;
        cursor: pointer;
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
  .right_rankings{
    display: inline-block;
    vertical-align: top;
    border: 1px solid rgb(226, 226, 226);
    border-radius: 5px;
    width: 37%;
    height: 450px;
    background: white;
    // background: #dfdfdf;
  }

  .rankings_title{
    font-size: 20px;
    padding: 1px 15px;
    background: rgb(235, 235, 235);
  }


  .content-container {
    padding: 0 20px 20px 20px;
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

  .rankings_user{
    display: inline-block;
    margin-bottom: 10px;
    font-size: 16px;
    background: white;
    height: 42px;
    line-height: 42px;
    width: 100%;

    a {
      display: inline-block;
      height: 42px;
      line-height: 42px;
      img {
        display: block;
        float: left;
        margin-right: 15px;
      }
    }
    .first {
      height: 42px;
      line-height: 42px;
      color: #800080;
      margin-left: 15px;
      &:hover {
        color: #2d8cf0;
      }
    }
    .second {
      height: 42px;
      line-height: 42px;
      color: red;
      margin-left: 15px;
      &:hover {
        color: #2d8cf0;
      }
    }
    .third {
      height: 42px;
      line-height: 42px;
      color: orange;
      margin-left: 15px;
      &:hover {
        color: #2d8cf0;
      }
    }
    .defa {
      height: 42px;
      line-height: 42px;
      color: #495060;
      margin-left: 15px;
      &:hover {
        color: #2d8cf0;
      }
    }
  }
</style>
