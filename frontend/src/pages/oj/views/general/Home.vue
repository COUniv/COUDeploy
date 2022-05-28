<template>
  <div v-if="listVisible" class="home_container">

    <div class="img_container" style="width: 100%;">
        <Carousel autoplay height:400px v-model="value1" loop arrow="hover" @on-change="handleChange">
            <CarouselItem>
                <div class="demo-carousel">
                  <img src="../../../../assets/main03.jpg" />
                </div>
            </CarouselItem>
            <CarouselItem>
                <div class="demo-carousel">
                  <img src="../../../../assets/main01.jpg" />
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
      <div class="lsit_container" style="display: block">
        <div class="left_announcement" style="float:left">
          <!-- <Row :gutter="32"> -->
            <!-- <Col span="12" class="demo-tabs-style1" style="background: #ebebeb;"> -->
              <Tabs value="name1" type="card" :animated="false">
                <div v-if="!announcements.length" key="no-announcement">
                  <TabPane :index=0 label="공지사항" name="name1" class="tabpan_padding">
                    <p class="announcement_title">{{$t('m.No_Announcements')}}</p>
                  </TabPane>
                </div>
                <div v-else>
                  <TabPane :index=1 label="공지사항" name="name1" class="tabpan_padding">
                    <p v-for="announcement in announcements" :key="announcement.title" class="announcement_title" @click="goAnnouncement(announcement)">
                      <a>
                        ▶︎ {{announcement.title}}
                      </a>
                    </p>
                  </TabPane>
                </div>
                <div>
                  <TabPane v-model="contest_idx" :index=1 label="대회일정" name="name2" class="tabpan_padding-s">
                    <Dropdown @on-click="onStatusChange" :transfer="true" class="contest-status-list">
                      <span>{{contest_stat === '' ? this.$i18n.t('m.Status') : this.$i18n.t('m.' + CONTEST_STATUS_REVERSE[contest_stat].name.replace(/ /g,"_"))}}
                        <!-- <Icon type="arrow-down-b"></Icon> -->
                        <Icon type="md-arrow-dropdown" />
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
                      </div>
                      <div v-else-if="contest.status == '0'">
                        <div style="float:left"><Tag style="margin-top:0px" type="dot" :color="CONTEST_STATUS_REVERSE[contest.status].color">{{$t('m.' + CONTEST_STATUS_REVERSE[contest.status].name.replace(/ /g, "_"))}}</Tag></div>
                        <div class="color-green"> {{contest.title}} </div>
                      </div>
                      <div style="clear:both;"></div>
                    </div>
                  </TabPane>
                </div>
              </Tabs>
            <!-- </Col> -->
          <!-- </Row> -->
        </div>
        <div class="right_rankings" style="float:right">
          <div class="rankings_title">사용자 순위</div>
          <div style="padding: 0 30px 0 30px">
            <div class="rankings_user" v-for="(data, index) in dataRank" :key="data.user.username" @click="goUser(data.user)">
              <span>{{index + 1}} 등 : </span>
              <a v-if="index == 0" class="first">
                {{data.user.username}}
              </a>
              <a v-else-if="index == 1" class="second">
                {{data.user.username}}
              </a>
              <a v-else-if="index == 2" class="third"></a>
              <a v-else class="defa">
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
        })
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
        })
      },
      onStatusChange (status) {
        this.query.status = status
        this.contest_stat = status
        this.getContestList()
      },
      handleChange (old, newval) {
        // console.log(old, newval)
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
    background: #506b9e;
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
  .color-green {
    color: rgba(2, 148, 2, 0.722);
    transition: all 0.1s ease-in-out;
    height: 34px;
    line-height: 34px;
    float: left;
    padding-left: 10px;
    width: calc(95% - 90px);
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
    transition:all 0.1s ease-in-out;
    height: 34px;
    line-height: 34px;
    float: left;
    padding-left: 10px;
    width: calc(95% - 90px);
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

  .lsit_container{
    display: block;
    // margin: 10px 0 0 0;
    // padding: 0 20%;
    width: 100%;
    height: 350px;
    margin-bottom: 50px;
    // background: #506b9e;
  }

  .left_announcement{
    display: inline-block;
    vertical-align: top;
    width: 65%;
    height: 350px;
    padding: 0;
    background: #ffffff;
    border: 1px solid rgb(226, 226, 226);
    border-radius: 5px;
    // border-bottom: 1px solid rgb(213, 213, 213);
    // border-right: 1px solid rgb(208, 208, 208);
  }

  .announcement_title, .contest_title{
    padding: 17px 10px 3px 10px;
    font-size: 18px;
    // border-bottom: 1px solid rgb(95, 95, 95);
    overflow: hidden;
    text-overflow: ellipsis;
    // word-wrap: break-word;
    // display: -webkit-box;
    // -webkit-line-clamp: 1;
    // -webkit-box-orient: vertical;
    height: 2.8em;
    line-height: 1.7em;
    width: 100%;
    white-space: nowrap;
    a {
      color: #495060;
      &:hover {
        color: #2d8cf0;
      }
    }
  }
  .tabpan_padding {
    padding: 0 30px 10px 30px;
  }
  .tabpan_padding-s {
    padding: 0 30px 10px 10px;
  }
  .right_rankings{
    display: inline-block;
    vertical-align: top;
    // padding: 0px 20px 20px 20px;
    border: 1px solid rgb(226, 226, 226);
    border-radius: 5px;
    width: 34.5%;
    height: 350px;
    background: white;
    // background: #dfdfdf;
  }

  .rankings_title{
    font-size: 20px;
    padding: 1px 15px;
    background: rgb(235, 235, 235);
  }

  .rankings_user{
    padding: 33px 10px 0 10px;
    font-size: 16px;
    background: white;

    .first {
      color: purple;
      margin-left: 15px;
      &:hover {
        color: #2d8cf0;
      }
    }
    .second {
      color: red;
      margin-left: 15px;
      &:hover {
        color: #2d8cf0;
      }
    }
    .third {
      color: orange;
      margin-left: 15px;
      &:hover {
        color: #2d8cf0;
      }
    }
    .defa {
      color: #495060;
      margin-left: 15px;
      &:hover {
        color: #2d8cf0;
      }
    }
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

<style lang="less">
  .contest-status-list {
    position:relative;
    float:right;
    * {
      z-index: 1000;
    }
  }
</style>
