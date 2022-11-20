<template>
  <div class="container">
    <div class="avatar-container">
      <img class="avatar" :src="profile.avatar"/>
    </div>
    <Card :padding="100">
      <div v-if="profile.user">
        <p style="margin-top: -10px">
          <span v-if="profile.user" class="emphasis">{{profile.user.username}}</span>
          <span v-if="profile.school">@{{profile.school}}</span>
        </p>
        <p v-if="profile.mood">
          {{profile.mood}}
        </p>
        <!-- <hr id="split"/> -->

        <div class="flex-container">
          <div class="left">
            <p class="emphasis">{{profile.accepted_number}}</p>
            <p>{{$t('m.UserHomeSolved')}}</p>
          </div>
          <div class="middle">
            <p class="emphasis">{{profile.submission_number}}</p>
            <p>{{$t('m.UserHomeserSubmissions')}}</p>
          </div>
          <div class="right">
            <p class="emphasis">{{rating}}</p>
            <p>{{$t('m.UserHomeScore')}}</p>
          </div>
        </div>
        <div id="problems">
          <div id="problem-title" v-if="problems.length">{{$t('m.List_Solved_Problems')}}
            <Poptip v-if="refreshVisible" trigger="hover" placement="right-start">
              <Icon type="ios-help-outline"></Icon>
              <div slot="content">
                <p>If you find the following problem id does not exist,<br> try to click the button.</p>
                <Button type="info" @click="freshProblemDisplayID">regenerate</Button>
              </div>
            </Poptip>
          </div>
          <p id="problem-title" v-else>{{$t('m.UserHomeIntro')}}</p>
          <div class="btns">
            <div v-for="problemID of problems" :key="problemID">
              <Button class="problem-btn" type="primary" @click="goProblem(problemID)">{{problemID}}</Button>
            </div>
          </div>
        </div>
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
    </Card>
  </div>
</template>
<script>
  import { mapActions } from 'vuex'
  import time from '@/utils/time'
  import api from '@oj/api'

  export default {
    data () {
      return {
        username: '',
        profile: {},
        problems: [],
        rating: 0
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
          api.getMyRatingChart(this.username).then(res => {
            let source = res.data.data
            this.rating = Math.floor(source[0][1] * 100)
          })
        })
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
@import '../../../../styles/common.less';
  .container {
    color: @black;
    position: relative;
    width: 75%;
    margin: 170px auto;
    text-align: center;
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
        width: 140px !important;
        height: 140px !important;
        border-radius: 50%;
        box-shadow: 0 1px 1px 0;
      }
    }
    .emphasis {
      font-size: 25px;
      font-weight: 400;
      -webkit-text-stroke: 1px;
      text-align: center;
    }
    #split {
      margin: 20px auto;
      width: 90%;
    }
    .flex-container {
      margin-top: 30px;
      padding: 20px;
      font-size: 20px;
      font-weight: 200;
      -webkit-text-stroke: .3px;
      box-shadow: 0px 3px 10px rgba(0, 0, 0, 0.25);
      border-radius: 5px;
      .left {
        flex: 1 1;
      }
      .middle {
        flex: 1 1;
        border-right: 2px solid @light-gray;
        border-left: 2px solid @light-gray;
      }
      .right {
        flex: 1 1;
      }
    }
    #problems {
      margin-top: 40px;
      padding: 20px;
      color: @purple;
      #problem-title {
        padding-bottom: 10px;
        font-size: 18px;
        font-weight: 200;
        -webkit-text-stroke: .3px;
        border-bottom: 2px solid @purple;
      }
      .btns {
        margin-top: 10px;
        display: flex;
        justify-content: start;
          .problem-btn {
            margin: 5px;
            padding: 2px 10px;
          }
      }
    }
    #icons {
      position: absolute;
      bottom: 20px;
      left: 50%;
      transform: translate(-50%);
      .icon {
        padding-left: 20px;
      }
    }
  }
</style>
