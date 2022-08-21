<template>
  <div class="setting-main">
    <div class="section-title">
      <div v-if="profile.user">
        <p style="font-size: 18px">
          <span @v-if="profile.user" class="emphasis" style="margin: 2em; margin-top:10px; margin-botton:15px; font-weight:600">{{profile.user.username}}</span>
          <span v-if="profile.school">{{profile.school}}</span>
        </p>
        <p v-if="profile.mood">
          {{profile.mood}}
        </p>
        <hr id="split"/>

        <div class="flex-container">
          <div class="left">
            <p>{{$t('m.UserHomeSolved')}}</p>
            <p class="emphasis">{{profile.accepted_number}}</p>
          </div>
          <div class="middle">
            <p>{{$t('m.UserHomeserSubmissions')}}</p>
            <p class="emphasis">{{profile.submission_number}}</p>
          </div>
          <div class="right">
            <p>{{$t('m.UserHomeScore')}}</p>
            <p class="emphasis">{{profile.total_score}}</p>
          </div>
        </div>
        <div class="flex-container">
          <div id="problems">
            <div v-if="problems.length">{{$t('m.List_Solved_Problems')}}
              <Poptip v-if="refreshVisible" trigger="hover" placement="right-start">
                <Icon type="ios-help-outline"></Icon>
                <div slot="content">
                  <p>If you find the following problem id does not exist,<br> try to click the button.</p>
                  <Button type="info" @click="freshProblemDisplayID">regenerate</Button>
                </div>
              </Poptip>
            </div>
            <p v-else>{{$t('m.UserHomeIntro')}}</p>
            <div class="btns">
              <div class="problem-btn" v-for="problemID of problems" :key="problemID">
                <Button @click="goProblem(problemID)">{{problemID}}</Button>
              </div>
            </div>
          </div>
        </div>
        <div class="flex-container">
          <div id="icons">
            <a :href="profile.github">
              <Icon type="social-github-outline" size="30"></Icon>
            </a>
            <a :href="'mailto:'+ profile.user.email">
              <Icon class="icon" type="ios-email-outline" size="30"></Icon>
            </a>
            <a :href="profile.blog">
              <Icon class="icon" type="ios-world-outline" size="30"></Icon>
            </a>
          </div>
        </div>
      </div>

      <Grass></Grass>

      <!-- account setting, profile setting button -->
      <div class="flex-container">
        <div class="btn-menu">
          <div style="margin-top: 10px;">
            <Button
              shape="circle"
              @click="goCommentList"
              style="margin-left: 5px;">
              댓글 단 글
            </Button>
            <Button
              shape="circle"
              @click="goLikeList"
              style="margin-left: 5px;">
              좋아요 한 글
            </Button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
  import { mapActions } from 'vuex'
  import time from '@/utils/time'
  import api from '@oj/api'
  import Grass from '../../user/Grass.vue'
  export default {
    components: {
      Grass
    },
    data () {
      return {
        username: '',
        profile: {},
        problems: []
      }
    },
    mounted () {
      this.init()
    },
    methods: {
      ...mapActions(['changeDomTitle']),
      init () {
        this.username = this.$route.query.username
        api.getUserInfo(this.username).then(res => {
          this.changeDomTitle({title: res.data.data.user.username})
          this.profile = res.data.data
          this.getSolvedProblems()
        })
      },
      goProfileSetting () {
        this.$router.push({name: 'profile-setting'}).catch(() => {})
      },
      goAccountSetting () {
        this.$router.push({name: 'account-setting'}).catch(() => {})
      },
      goCommentList () {
        this.$router.push({name: 'comment-list'}).catch(() => {})
      },
      goLikeList () {
        this.$router.push({name: 'like-list'}).catch(() => {})
      },
      getSolvedProblems () {
        let ACMProblems = this.profile.acm_problems_status.problems || {}
        let OIProblems = this.profile.oi_problems_status.problems || {}
        // todo oi problems
        let ACProblems = []
        for (let problems of [ACMProblems, OIProblems]) {
          Object.keys(problems).forEach(problemID => {
            if (problems[problemID]['status'] === 0) {
              ACProblems.push(problems[problemID]['_id'])
            }
          })
        }
        ACProblems.sort()
        this.problems = ACProblems
      },
      goProblem (problemID) {
        this.$router.push({name: 'problem-details', params: {problemID: problemID}}).catch(() => {})
      },
      freshProblemDisplayID () {
        api.freshDisplayID().then(res => {
          this.$success('Update successfully')
          this.init()
        })
      }
    },
    computed: {
      refreshVisible () {
        if (!this.username) return true
        if (this.username && this.username === this.$store.getters.user.username) return true
        return false
      }
    },
    watch: {
      '$route' (newVal, oldVal) {
        if (newVal !== oldVal) {
          this.init()
        }
      }
    }
  }
</script>

<style lang="less" scoped>
  .container {
    position: relative;
    text-align: center;
    margin: 170px auto;
    p {
      margin-top: 8px;
      margin-bottom: 8px;
    }
    .avatar-container {
      position: absolute;
      left: 50%;
      transform: translate(-50%);
      z-index: 1;
      top: -90px;
      .avatar {
        width: 140px;
        height: 140px;
        border-radius: 50%;
        box-shadow: 0 1px 1px 0;
      }
    }
    .emphasis {
      font-size: 20px;
      font-weight: 400;
      text-align: center;
    }
    #split {
      margin: 20px auto;
      width: 90%;
    }
    .flex-container {
      margin-top: 30px;
      padding: auto 20px;
      text-align: center;
      font-weight: 400;
      font-size: 16px;
      .left {
        flex: 1 1;
      }
      .middle {
        flex: 1 1;
        border-left: 1px solid #999;
        border-right: 1px solid #999;
      }
      .right {
        flex: 1 1;
      }
      .btn-menu {
        font-size: 16px;
        float: right;
        margin-right: 10px;
        margin-top: 15px;
      }
    }
    #problems {
      margin-top: 40px;
      padding-left: 30px;
      padding-right: 30px;
      font-size: 18px;
      font-weight: 400;
      text-align: center;
      .btns {
        margin-top: 15px;
        .problem-btn {
          display: inline-block;
          margin: 5px;
        }
      }
    }
    #icons {
      position: absolute;
      padding-bottom: auto 20px;
      left: 50%;
      transform: translate(-50%);
      .icon {
        padding-left: 20px;
      }
    }
  }
</style>
