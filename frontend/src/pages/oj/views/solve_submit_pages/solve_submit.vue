<template>
  <div class="demo-split">
    <div class="ss_header">
      <div class="logo" style="color:white" >Online Judge Platform</div>
      <div style="float: right">
        <div class="btn">
          <Button type="text" size="large" style="z-index: '1' " @click="help_btn"><p style="color:white">도움말</p></Button>
        </div>
        <!-- <div class="btn">
          <Button type="text" size="large" style="z-index: '2'" @click="compile_opt"><p style="color:white">컴파일 옵션</p></Button>
        </div> -->
      </div>  
    </div>

    <!-- <div style="height: 80vh"> -->
      <Split v-model="split3" v-bind:min="min1" v-bind:max="max1">
        <div slot="left" class="left-split-pane" >
          
          <Tabs value="name1" type="card" :animated="false">
            <TabPane label="문제1" name="name1" >   <!-- style="padding: 0 30px 10px 30px" -->
              <div class="problem_contents">
                신입사원 무지는 게시판 불량 이용자를 신고하고 처리 결과를 메일로 발송하는 시스템을 개발하려 합니다. 무지가 개발하려는 시스템은 다음과 같습니다. <br>
                각 유저는 한 번에 한 명의 유저를 신고할 수 있습니다. <br>
                신고 횟수에 제한은 없습니다. 서로 다른 유저를 계속해서 신고할 수 있습니다. <br>
                한 유저를 여러 번 신고할 수도 있지만, 동일한 유저에 대한 신고 횟수는 1회로 처리됩니다. <br>
                k번 이상 신고된 유저는 게시판 이용이 정지되며, 해당 유저를 신고한 모든 유저에게 정지 사실을 메일로 발송합니다. <br>
                유저가 신고한 모든 내용을 취합하여 마지막에 한꺼번에 게시판 이용 정지를 시키면서 정지 메일을 발송합니다. <br>
                다음은 전체 유저 목록이 ["muzi", "frodo", "apeach", "neo"]이고, k = 2(즉, 2번 이상 신고당하면 이용 정지)인 경우의 예시입니다.  <br>
                
              </div>
            </TabPane>
          </Tabs>
        </div>
        <div slot="right" class="right-split-pane no-padding">
          <!-- Right Padding -->
          <div class="problem_input">
            <!-- <Problem></Problem> -->
            <Card :padding="20" id="submit-codes" dis-hover>
              <CodeMirror :value.sync="code"
                          :languages="problem.languages"
                          :language="language"
                          :theme="theme"
                          :height="700"
                          @resetCode="onResetToTemplate"
                          @changeTheme="onChangeTheme"
                          @changeLang="onChangeLang"></CodeMirror>
              <Row type="flex" justify="space-between">
                <Col :span="10">
                  <div class="status" v-if="statusVisible">
                    <template v-if="!this.contestID || (this.contestID && OIContestRealTimePermission)">
                      <span>{{$t('m.Status')}}</span>
                      <Tag type="dot" :color="submissionStatus.color" @click.native="handleRoute('/status/'+submissionId)">
                        {{$t('m.' + submissionStatus.text.replace(/ /g, "_"))}}
                      </Tag>
                    </template>
                    <template v-else-if="this.contestID && !OIContestRealTimePermission">
                      <Alert type="success" show-icon>{{$t('m.Submitted_successfully')}}</Alert>
                    </template>
                  </div>
                  <div v-else-if="problem.my_status === 0">
                    <Alert type="success" show-icon>{{$t('m.You_have_solved_the_problem')}}</Alert>
                  </div>
                  <div v-else-if="this.contestID && !OIContestRealTimePermission && submissionExists">
                    <Alert type="success" show-icon>{{$t('m.You_have_submitted_a_solution')}}</Alert>
                  </div>
                  <div v-if="contestEnded">
                    <Alert type="warning" show-icon>{{$t('m.Contest_has_ended')}}</Alert>
                  </div>
                </Col>

                <Col :span="12">
                  <template v-if="captchaRequired">
                    <div class="captcha-containers">
                      <Tooltip v-if="captchaRequired" content="Click to refresh" placement="top">
                        <img :src="captchaSrc" @click="getCaptchaSrc"/>
                      </Tooltip>
                      <Input v-model="captchaCode" class="captcha-codes"/>
                    </div>
                  </template>
<!--                   
                  <Button type="warning" icon="edit" :loading="submitting" @click="submitCode"
                          :disabled="problemSubmitDisabled || submitted"
                          class="fl-right">
                    <span v-if="submitting">{{$t('m.Submitting')}}</span>
                    <span v-else>{{$t('m.Submit')}}</span>
                  </Button> -->
                
                </Col>
              </Row>
            </Card>
          </div>
        </div>
      </Split>
    <!-- </div> -->

    
    <div class="ss_footer">
    <!-- <Menu mode="horizontal" :theme="theme1" active-name="1" class="solve_submit_navbar"> -->
      <div class="footer_title" style="color:white" >2022년 3월 코딩 테스트</div>
      <div style="float: right">
        <div class="footer_btn" style="color:white">
          <!-- <Select v-model="model1" size="large" style="width:80px">
            <Option style="z-index: '1'" v-for="item in open_data" :value="item.value" :key="item.value">{{ item.label }}</Option>
          </Select> -->
          <Button type="primary" size="large" style="z-index: '1' " :class="[isActive ? 'green' : 'red']" @click="toggle">{{isActive ? '공개' : '비공개'}}</Button>
        </div>
        <!-- <div class="footer_btn" style="color:white">
          <Button type="primary" size="large" style="z-index: '2'" >초기화</Button>
        </div>
        <div class="footer_btn" style="color:white">
          <Button type="primary" size="large" style="z-index: '3'" >코드 실행</Button>
        </div> -->
        <div class="footer_btn" style="color:white">
          <Button type="primary" size="large" style="z-index: '4'" >
            <span v-if="submitting">{{$t('m.Submitting')}}</span>
            <span v-else>{{$t('m.Submit')}}</span>
          </Button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// import Problem from '../../views/solve_submit_pages/solve_submit.vue'
import {mapGetters, mapActions} from 'vuex'
import {types} from '../../../../store'
import CodeMirror from '@oj/components/SubmitCodeMirror.vue'
import storage from '@/utils/storage'
import {FormMixin} from '@oj/components/mixins'
import {JUDGE_STATUS, CONTEST_STATUS, buildProblemCodeKey} from '@/utils/constants'
import api from '@oj/api'

export default {
  name: 'Problem',
  components: {
    CodeMirror
  },
  mixins: [FormMixin],
  data () {
    return {
      isActive: false,
      split3: 0.4,
      split4: 0.7,
      min1: '500px',
      max1: '1000px',
      min2: '400px',
      statusVisible: false,
      captchaRequired: false,
      submissionExists: false,
      captchaCode: '',
      captchaSrc: '',
      contestID: '',
      problemID: '',
      submitting: false,
      code: '',
      language: 'C++',
      theme: 'solarized',
      submissionId: '',
      submitted: false,
      result: {
        result: 9
      },
      problem: {
        title: '',
        description: '',
        hint: '',
        my_status: '',
        template: {},
        languages: [],
        created_by: {
          username: ''
        },
        tags: [],
        io_mode: {'io_mode': 'Standard IO'}
      }
    }
  },
  beforeRouteEnter (to, from, next) {
    let problemCode = storage.get(buildProblemCodeKey(to.params.problemID, to.params.contestID))
    if (problemCode) {
      next(vm => {
        vm.language = problemCode.language
        vm.code = problemCode.code
        vm.theme = problemCode.theme
      })
    } else {
      next()
    }
  },
  mounted () {
    this.$store.commit(types.CHANGE_CONTEST_ITEM_VISIBLE, {menu: false})
    this.init()
  },
  methods: {
    help_btn () {
      this.$Notice.open({
        title: 'Notification title',
        desc: 'This notification does not automatically close, and you need to click the close button to close.',
        duration: 0
      })
    },
    compile_opt () {
      this.$Notice.open({
        title: 'Compile Option title',
        desc: 'This Compile Option does not automatically close, and you need to click the close button to close.',
        duration: 0
      })
    },
    toggle () {
      this.isActive = !this.isActive
    },
    ...mapActions(['changeDomTitle']),
    init () {
      this.$Loading.start()
      this.contestID = this.$route.params.contestID
      this.problemID = this.$route.params.problemID
      let func = this.$route.name === 'problem-details' ? 'getProblem' : 'getContestProblem'
      api[func](this.problemID, this.contestID).then(res => {
        this.$Loading.finish()
        let problem = res.data.data
        this.changeDomTitle({title: problem.title})
        api.submissionExists(problem.id).then(res => {
          this.submissionExists = res.data.data
        })
        problem.languages = problem.languages.sort()
        this.problem = problem
        // this.changePie(problem)
        // 在beforeRouteEnter中修改了, 说明本地有code，无需加载template
        if (this.code !== '') {
          return
        }
        // try to load problem template
        this.language = this.problem.languages[0]
        let template = this.problem.template
        if (template && template[this.language]) {
          this.code = template[this.language]
        }
      }, () => {
        this.$Loading.error()
      })
    },
    // changePie (problemData) {
    //   // 只显示特定的一些状态
    //   for (let k in problemData.statistic_info) {
    //     if (filtedStatus.indexOf(k) === -1) {
    //       delete problemData.statistic_info[k]
    //     }
    //   }
    //   let acNum = problemData.accepted_number
    //   let data = [
    //     {name: 'WA', value: problemData.submission_number - acNum},
    //     {name: 'AC', value: acNum}
    //   ]
    //   this.pie.series[0].data = data
    //   // 只把大图的AC selected下，这里需要做一下deepcopy
    //   let data2 = JSON.parse(JSON.stringify(data))
    //   data2[1].selected = true
    //   this.largePie.series[1].data = data2
    //   // 根据结果设置legend,没有提交过的legend不显示
    //   let legend = Object.keys(problemData.statistic_info).map(ele => JUDGE_STATUS[ele].short)
    //   if (legend.length === 0) {
    //     legend.push('AC', 'WA')
    //   }
    //   this.largePie.legend.data = legend
    //   // 把ac的数据提取出来放在最后
    //   let acCount = problemData.statistic_info['0']
    //   delete problemData.statistic_info['0']
    //   let largePieData = []
    //   Object.keys(problemData.statistic_info).forEach(ele => {
    //     largePieData.push({name: JUDGE_STATUS[ele].short, value: problemData.statistic_info[ele]})
    //   })
    //   largePieData.push({name: 'AC', value: acCount})
    //   this.largePie.series[0].data = largePieData
    // },
    handleRoute (route) {
      this.$router.push(route)
    },
    onChangeLang (newLang) {
      if (this.problem.template[newLang]) {
        if (this.code.trim() === '') {
          this.code = this.problem.template[newLang]
        }
      }
      this.language = newLang
    },
    onChangeTheme (newTheme) {
      this.theme = newTheme
    },
    onResetToTemplate () {
      this.$Modal.confirm({
        content: this.$i18n.t('m.Are_you_sure_you_want_to_reset_your_code'),
        onOk: () => {
          let template = this.problem.template
          if (template && template[this.language]) {
            this.code = template[this.language]
          } else {
            this.code = ''
          }
        }
      })
    },
    checkSubmissionStatus () {
      // 使用setTimeout避免一些问题
      if (this.refreshStatus) {
        // 如果之前的提交状态检查还没有停止,则停止,否则将会失去timeout的引用造成无限请求
        clearTimeout(this.refreshStatus)
      }
      const checkStatus = () => {
        let id = this.submissionId
        api.getSubmission(id).then(res => {
          this.result = res.data.data
          if (Object.keys(res.data.data.statistic_info).length !== 0) {
            this.submitting = false
            this.submitted = false
            clearTimeout(this.refreshStatus)
            this.init()
          } else {
            this.refreshStatus = setTimeout(checkStatus, 2000)
          }
        }, res => {
          this.submitting = false
          clearTimeout(this.refreshStatus)
        })
      }
      this.refreshStatus = setTimeout(checkStatus, 2000)
    },
    submitCode () {
      if (this.code.trim() === '') {
        this.$error(this.$i18n.t('m.Code_can_not_be_empty'))
        return
      }
      this.submissionId = ''
      this.result = {result: 9}
      this.submitting = true
      let data = {
        problem_id: this.problem.id,
        language: this.language,
        code: this.code,
        contest_id: this.contestID
      }
      if (this.captchaRequired) {
        data.captcha = this.captchaCode
      }
      const submitFunc = (data, detailsVisible) => {
        this.statusVisible = true
        api.submitCode(data).then(res => {
          this.submissionId = res.data.data && res.data.data.submission_id
          // 定时检查状态
          this.submitting = false
          this.submissionExists = true
          if (!detailsVisible) {
            this.$Modal.success({
              title: this.$i18n.t('m.Success'),
              content: this.$i18n.t('m.Submit_code_successfully')
            })
            return
          }
          this.submitted = true
          this.checkSubmissionStatus()
        }, res => {
          this.getCaptchaSrc()
          if (res.data.data.startsWith('Captcha is required')) {
            this.captchaRequired = true
          }
          this.submitting = false
          this.statusVisible = false
        })
      }
      if (this.contestRuleType === 'OI' && !this.OIContestRealTimePermission) {
        if (this.submissionExists) {
          this.$Modal.confirm({
            title: '',
            content: '<h3>' + this.$i18n.t('m.You_have_submission_in_this_problem_sure_to_cover_it') + '<h3>',
            onOk: () => {
              // 暂时解决对话框与后面提示对话框冲突的问题(否则一闪而过）
              setTimeout(() => {
                submitFunc(data, false)
              }, 1000)
            },
            onCancel: () => {
              this.submitting = false
            }
          })
        } else {
          submitFunc(data, false)
        }
      } else {
        submitFunc(data, true)
      }
    },
    onCopy (event) {
      this.$success('Code copied')
    },
    onCopyError (e) {
      this.$error('Failed to copy code')
    }
  },
  computed: {
    ...mapGetters(['problemSubmitDisabled', 'contestRuleType', 'OIContestRealTimePermission', 'contestStatus']),
    contest () {
      return this.$store.state.contest.contest
    },
    contestEnded () {
      return this.contestStatus === CONTEST_STATUS.ENDED
    },
    submissionStatus () {
      return {
        text: JUDGE_STATUS[this.result.result]['name'],
        color: JUDGE_STATUS[this.result.result]['color']
      }
    },
    submissionRoute () {
      if (this.contestID) {
        return {name: 'contest-submission-list', query: {problemID: this.problemID}}
      } else {
        return {name: 'submission-list', query: {problemID: this.problemID}}
      }
    }
  },
  beforeRouteLeave (to, from, next) {
    // 防止切换组件后仍然不断请求
    clearInterval(this.refreshStatus)
    this.$store.commit(types.CHANGE_CONTEST_ITEM_VISIBLE, {menu: true})
    storage.set(buildProblemCodeKey(this.problem._id, from.params.contestID), {
      code: this.code,
      language: this.language,
      theme: this.theme
    })
    next()
  },
  watch: {
    '$route' () {
      this.init()
    }
  }
}
</script>

<style>

  .problem_contents{
    overflow: auto;
    /* width: ; */
    height: 79vh;
    font-size: 16px;
  }

  .problem_input{
    height: 79vh;
  }


  .demo-split {
    height: 87vh;
    /* margin: -80px -45px -250px -45px; */
    /* border: 1px solid #dcdee2; */
  }
  .ss_header{
    background: #404040;
    color: white;
    position: relative;
    left: 0px;
    top: 0;
    width: 100%;
    height: 62px;
    line-height: 62px;
  }
  .logo{
    float: left;
    color: white;
    font-size: 20px;
    padding: 0 5px;
    /* padding: 0; */
  }

  .btn{
    float: left;
    color: white;
    font-size: 16px;
    padding: 0 10px;
  }

  .solve_submit_footer{
    background: rgb(29, 29, 29);
    color: white;
  }

  .footer_title {
    float: left;
    color: white;
    font-size: 18px;
    padding: 0 10px;
  }
  
  .footer_btn{
    float: left;
    color: white;
    /* font-size: 16px; */
    padding: 0 5px;
  }

  .ss_footer {
    background-color: rgb(51, 51, 51);
    position: relative;
    left: 0px;
    bottom: 0;
    width: 100%;
    height: 59px;
    line-height: 59px;
    /* text-align: center; */
  }  

  @media screen and (max-width: 1200px) {
    .demo-split{
      margin: -160px -50px -200px -50px;
      padding-bottom: -80px;
    }
  }
  @media screen and (min-width: 1200px) {
    .demo-split{
      margin: -80px -50px -200px -50px;
      padding-bottom: -80px;
    }
  }

  .left-split-pane{

    padding: 10px;
    /* height: 100vh; */
    /* background: sandybrown; */
  }

  .right-split-pane{
    /* padding: 10px; */
    height: 100%;
    /* background: forestgreen; */
  }

  .right-split-pane.no-padding{
    height: 100%;
    padding: 0;
  }

  .rtop-split-pane{
    height : 100%;
    padding: 10px;
    background-color: #262626;
  }

  .rbottom-split-pane{
    min-height: 5%;
    height: 100%;
    padding: 10px;
    background-color: #262626;
  }

  .demo-split{
    height: 87vh;
    /* border: 1px solid #dcdee2; */
  }
  .demo-split-pane{
    padding: 10px;
  }
  .demo-split-pane.no-padding{
    height: 90%;
    padding: 0;
  }


  #submit-codes {
    margin-top: 40px;
    margin-bottom: 20px;
  }

  .status {
    float: left;
  }
  
  .status > span {
    margin-right: 10px;
    margin-left: 10px;
  }

  .captcha-containers {
    display: inline-block;
  }

  .captcha-codes {
    width: auto;
    height: 70vh;
    margin-top: -20px;
    margin-left: 20px;
  }

  .fl-rights {
    position: absolute;
    float: right;
  }
  
</style>