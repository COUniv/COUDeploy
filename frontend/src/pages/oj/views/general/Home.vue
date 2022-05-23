<template>
  <div v-if="listVisible" class="home_container">
  <!-- <Row type="flex" justify="space-around">
    <Col :span="22"> -->
    <!-- <panel shadow v-if="contests.length" class="contest">
      <div slot="title">
        <Button type="text"  class="contest-title" @click="goContest">{{contests[index].title}}</Button>
      </div>
      <Carousel v-model="index" trigger="hover" autoplay :autoplay-speed="6000" class="contest">
        <CarouselItem v-for="(contest, index) of contests" :key="index">
          <div class="contest-content">
            <div class="contest-content-tags">
              <Button type="info" shape="circle" size="small" icon="calendar">
                {{contest.start_time | localtime('YYYY-M-D HH:mm') }}
              </Button>
              <Button type="success" shape="circle" size="small" icon="android-time">
                {{getDuration(contest.start_time, contest.end_time)}}
              </Button>
              <Button type="warning" shape="circle" size="small" icon="trophy">
                {{contest.rule_type}}
              </Button>
            </div>
            <div class="contest-content-description">
              <blockquote v-html="contest.description"></blockquote>
            </div>
          </div>
        </CarouselItem>
      </Carousel>
    </panel> -->
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
                  <TabPane :index=0 label="공지사항" name="name1" style="padding: 0 30px 10px 30px">
                    <p class="announcement_title" style="padding: 17px 10px 3px 10px;">{{$t('m.No_Announcements')}}</p>
                  </TabPane>
                </div>
                <div v-else>
                  <TabPane :index=1 label="공지사항" name="name1" style="padding: 0 30px 10px 30px">
                    <p v-for="announcement in announcements" :key="announcement.title" class="announcement_title" @click="goAnnouncement(announcement)"  style="padding: 17px 10px 3px 10px;">
                      <a>
                        ▶︎ {{announcement.title}}
                      </a>
                    </p>
                  </TabPane>
                </div>
                <div>
                  <TabPane :index=1 label="대회일정" name="name2" style="padding: 0 30px 10px 30px">
                    <p class="contest_title" style="padding: 17px 10px 3px 10px;">대회일정</p>
                    <p class="contest_title" style="padding: 17px 10px 3px 10px;">대회일정</p>
                    <p class="contest_title" style="padding: 17px 10px 3px 10px;">대회일정</p>
                    <p class="contest_title" style="padding: 17px 10px 3px 10px;">대회일정</p>
                    <p class="contest_title" style="padding: 17px 10px 3px 10px;">대회일정</p>
                  </TabPane>
                </div>
              </Tabs>
            <!-- </Col> -->
          <!-- </Row> -->
        </div>
        <div class="right_rankings" style="float:right">
          <div class="rankings_title">사용자 순위</div>
          <div style="padding: 0 30px 0 30px">
            <div class="rankings_user" style="padding: 33px 10px 0 10px;" v-for="(data, index) in dataRank" :key="data.user.username" @click="goUser(data.user)">
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
  import { CONTEST_STATUS, RULE_TYPE } from '@/utils/constants'
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
        contests: [],
        index: 0,
        value1: 0,
        dataRank: []
      }
    },
    mounted () {
      let params = {status: CONTEST_STATUS.NOT_START}
      api.getContestList(0, 5, params).then(res => {
        this.contests = res.data.data.results
      })
      this.getAnnouncementList()
      this.getRankData(1)
    },
    methods: {

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
          params: {contestID: this.contests[this.index].id}
        })
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
    padding: 25px 10px 3px 10px;
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
