
<template>
  <div class="demo-split">
    <div class="ss_header">
      <div class="header-left">
        <div class="logo" @click="goHome">COU</div>
        <!-- <div class="problem-name" style="color: #bdbdbd" >[2022년 3월 코딩 테스트]</div> -->
        <div class="problem-name"> {{ problem.title }}</div>
      </div>
      <div class="header-right">
        <div class="auto-save-block" v-show="autosaveLoading">
          <div class="loading-box"
            v-loading="`true`"
            element-loading-background="rgba(0, 0, 0, 0)"
            element-loading-spinner="el-icon-loading"></div>
          <div class="text-block">저장중...</div>
        </div>
        <div class="auto-save-block" v-show="!autosaveLoading">
          <div class="loading-box"><i class="check-icon mdi mdi-check-bold"></i></div>
          <div class="text-block">저장됨</div>
        </div>
        <div class="help">
          <p @click="help_btn" class="help-btn">도움말</p>
        </div>
        <div v-if="!isAfterSubmit">
          <Button v-if="isActive" type="primary" size="large" style="z-index: '1'" :loading="submitted" class="hide-btn" @click="toggle(false)">공개
            <Icon type="md-eye" />
          </Button>
          <Button v-else type="primary" size="large" style="z-index: '1'" :loading="submitted" class="hide-btn" @click="toggle(true)"  :disabled="sharedButtonDisabled">비공개
            <Icon type="md-eye-off" />
          </Button>
        </div>
        <div v-else="isAfterSubmit">
          <Button v-if="isActive" type="primary" size="large" style="z-index: '1'" disabled>공개로 제출 됨</Button>
          <Button v-else type="error" size="large" style="z-index: '1'" disabled>비공개로 제출 됨</Button>
        </div>
        <div>
          <!-- 제출 오남용을 방지하기 위해 제출 한 번으로 제한 -->
          <Button v-if="!isAfterSubmit" type="primary" size="large" style="z-index: '4'" :loading="submitted" @click="submitCode"
                  :disabled="problemSubmitDisabled" class="submit-btn">
            <span v-if="submitted">채점중</span>
            <span v-else>{{$t('m.Submit')}}</span>
          </Button>
          <Button v-else type="primary" size="large" @click="goSubmissionList" class="submit-btn">
            채점 현황 보러가기
            <Icon type="ios-arrow-forward"></Icon>
          </Button>
        </div>
      </div>  
    </div>
    <Split v-model="split3" v-bind:min="min1" v-bind:max="max1">
      <div slot="left" class="left-split-pane" >
        <Tabs value="name1" :animated="false">
          <TabPane :label="problem.title" name="name1" >   <!-- style="padding: 0 30px 10px 30px" -->
            <div class="problem_contents">
              <div id="problem-content" class="markdown-body" v-katex>
                <p class="title">{{$t('m.Description')}}</p>
                <p class="content" v-html="problem.description"></p>
                <p class="title">입력 <span v-if="problem.io_mode.io_mode=='File IO'">({{$t('m.FromFile')}}: {{ problem.io_mode.input }})</span></p>
                <p class="content" v-html="problem.input_description"></p>
                <p class="title">출력 <span v-if="problem.io_mode.io_mode=='File IO'">({{$t('m.ToFile')}}: {{ problem.io_mode.output }})</span></p>
                <p class="content" v-html="problem.output_description"></p>
                <div v-for="(sample, index) of problem.samples" :key="index">
                  <div class="flex-container-submit-mode sample split-sapple">
                    <div class="sample-input">
                      <p class="title">{{$t('m.Sample_Input')}} {{index + 1}}
                        <a class="copy"
                            v-clipboard:copy="sample.input"
                            v-clipboard:success="onCopy"
                            v-clipboard:error="onCopyError">
                          <Icon type="md-clipboard"></Icon>
                        </a>
                      </p>
                      <div style="white-space: pre;" class="input-for-pre">{{sample.input}}</div>
                    </div>
                    <div class="sample-output">
                      <p class="title">{{$t('m.Sample_Output')}} {{index + 1}}</p>
                      <div style="white-space: pre;" class="input-for-pre">{{sample.output}}</div>
                    </div>
                  </div>
                </div>
                <div v-if="problem.hint">
                  <div class="hide" @click="hintHide()">
                    <p class="title">{{$t('m.Hint')}}</p>
                    <Button v-if="!hintHidden" size="large" class="hint-hide-btn"><Icon type="md-eye" /></Button>
                    <Button v-else size="large" class="hint-hide-btn"><Icon type="md-eye-off" /></Button>
                  </div>
                  <p v-html="problem.hint" v-bind:style="[hintHidden ?{'visibility' : 'hidden'}:{'display' : 'block'}]"></p>
                </div>
              </div>
            </div>
          </TabPane>
          <TabPane v-if="contestID" label="문제 리스트" name="problem_list">
            <div class="contest-list" :class="item._id === problemID ? 'purple' : ''" 
                v-for="(item, index) in problems"
                @click="goContestProblem(item)">
              <div class="left-contest-list">
                <div v-if="item.accepted_number">
                  <i class="badge mdi mdi-checkbox-marked-circle-outline"></i> 
                </div>
                <div v-else style="margin-left: 15px;"></div>
                <div style="margin-right: 5px;">{{index + 1}}) </div> 
                <div>{{item.title}}</div>
              </div>
              <!-- {{item.difficulty}} 
              {{item.submission_number}}  -->
              <div style="margin-right: 15px;">{{item.difficulty}}</div>
            </div>
          </TabPane>
        </Tabs>
      </div>
      <div slot="right" class="right-split-pane">
        <div style="clear:both;"></div>
        <!-- Right Padding -->
        <div class="problem_input">
          <!-- <Problem></Problem> -->
            <!-- height는 SubmitCodeMirror랑 같게 할 것 -->
          <SubmitCodeMirror :value.sync="code"
                      :languages="problem.languages"
                      :language="language"
                      :theme="theme"
                      :my_status="problem.my_status"
                      :statusVisible="statusVisible"
                      :contestID="this.contestID"
                      :OIContestRealTimePermission="OIContestRealTimePermission"
                      :submissionStatus="submissionStatus"
                      :submissionId = "submissionId"
                      :submissionExists="submissionExists"
                      :contestEnded="contestEnded"
                      @keyup.native="codeKeyUp"
                      @resetCode="onResetToTemplate"
                      @changeTheme="onChangeTheme"
                      @changeLang="onChangeLang"
                      :key="codeMirrorForceRender"></SubmitCodeMirror>
 
        </div>
      </div>
    </Split>
  </div>
</template>




<script>
  import {mapGetters, mapActions, mapState} from 'vuex'
  import {types} from '../../../../store'
  import SubmitCodeMirror from '@oj/components/SubmitCodeMirror.vue'
  import CodeMirror from '@oj/components/CodeMirror.vue'
  import NavBar from '@oj/components/NavBar.vue'
  import storage from '@/utils/storage'
  import {FormMixin} from '@oj/components/mixins'
  import {JUDGE_STATUS, CONTEST_STATUS, buildProblemCodeKey} from '@/utils/constants'
  import api from '@oj/api'
  import {pie, largePie} from './chartData'
  import SHA3 from 'js-sha3'
  import _ from 'lodash'
  // 이 상태의 그래픽 점유만 표시
  const filtedStatus = ['-1', '-2', '0', '1', '2', '3', '4', '8']

  export default {
    name: 'ProblemSubmission',
    components: {
      NavBar,
      CodeMirror,
      SubmitCodeMirror
    },
    mixins: [FormMixin],
    data () {
      return {
        codeMirrorForceRender: false,
        autosaveLoading: false,
        isChangeLanguage: false,
        isFirst: true,
        autosave: false,
        reselectModalVisible: false,
        checksum: '',
        draftID: '',
        sharedButtonDisabled: false,
        openHelpModal: false,
        lastURL: '',
        version: process.env.VERSION,
        // submit 화면 여부
        isAfterSubmit: false,
        isActive: false,
        split3: 0.4,
        min1: '270px',
        max1: '97vw',
        statusVisible: false,
        captchaRequired: false,
        graphVisible: false,
        submissionExists: false,
        captchaCode: '',
        captchaSrc: '',
        contestID: '',
        problemID: '',
        submitting: false,
        code: '',
        language: 'C++',
        theme: 'base16-light',
        submissionId: '',
        submitted: false,
        hintHidden: true,
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
        },
        pie: pie,
        largePie: largePie,
        // echarts 无法获取隐藏dom的大小，需手动指定
        largePieInitOpts: {
          width: '500',
          height: '480'
        }
      }
    },
    beforeRouteEnter (to, from, next) {
      let problemCode = storage.get(buildProblemCodeKey(to.params.problemID, to.params.contestID))
      if (problemCode) {
        next(vm => {
          vm.lastURL = from
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
      this.getWebsiteConfig()
    },
    methods: {
      ...mapActions(['changeDomTitle', 'getWebsiteConfig', 'changeModalStatus']),
      help_btn () {
        // this.openHelpModal = true
        this.$Notice.open({
          title: '도움말',
          duration: 0,
          render: h => {
            return h('p', [
              '입력과 출력은 모두 Standard IO를 통해 읽고 출력하게 됩니다. 해당 문서는 ',
              h('a', {
                on: {
                  click: () => {
                    let routeData = this.$router.resolve({
                      name: 'languages'
                    })
                    window.open(routeData.href, '_blank')
                  }
                }
              }, '언어별 도움말'),
              '을 참고해주세요'
            ])
          }
        })
      },
      toggle (shared) {
        this.isActive = shared
      },
      codeKeyUp () {
        if (this.autosave && this.isFirst === false && this.isChangeLanguage === false) {
          this.debounceDraft()
        } else {
          this.isFirst = false
          this.autosave = true
          this.isChangeLanguage = false
        }
      },
      init (language) {
        this.isFirst = true
        this.autosave = false
        this.isChangeLanguage = true
        this.$Loading.start()
        // routes.js에 정의 된 params
        this.contestID = this.$route.params.contestID
        this.problemID = this.$route.params.problemID
        let func = this.$route.name === 'problem-submission' ? 'getProblem' : 'getContestProblem'
        this.sharedButtonDisabled = this.isContestRoute()
        api[func](this.problemID, this.contestID).then(res => {
          this.$Loading.finish()
          let problem = res.data.data
          this.changeDomTitle({title: problem.title})
          api.submissionExists(problem.id).then(res => {
            this.submissionExists = res.data.data
          })
          problem.languages = problem.languages.sort()
          this.problem = problem
          // console.log(problem)
          this.changePie(problem)
          // 로컬에 코드가 있고 템플릿을 로드할 필요가 없음을 나타내는 beforeRouteEnter에서 수정됨
          if (this.code !== '') {
            this.code = ''
          }
          // try to load problem template
          if (language === undefined) {
            this.language = this.problem.languages[0]
          } else {
            this.language = language
          }
          let template = this.problem.template
          if (template && template[this.language]) {
            this.code = template[this.language]
          }
          this.getDraftCode()
          this.updateCodeMirrorForceRender()
        }, () => {
          this.$Loading.error()
        })
      },
      updateCodeMirrorForceRender () {
        this.codeMirrorForceRender = !this.codeMirrorForceRender
      },
      updateDraftCode () {
        this.autosaveLoading = true
        if (this.autosave && !this.isFirst && this.isChangeLanguage === false) {
          let func = this.$route.name === 'problem-submission' ? 'updateDraftCode' : 'updateContestDraftCode'
          api[func](this.draftID, this.problemID, this.contestID, this.language, this.checksum, this.code).then(res => {
            this.autosaveLoading = false
          }, err => {
            console.log(err)
            this.autosaveLoading = false
          })
        }
      },
      debounceDraft: _.debounce(function (newVal, oldVal) {
        this.updateDraftCode()
        this.isChangeLanguage = false
      }, 1000),
      getDraftCode () {
        let func = this.$route.name === 'problem-submission' ? 'getDraftCode' : 'getContestDraftCode'
        api[func](this.problemID, this.contestID, this.language).then(res => {
          let msg = SHA3.sha3_256.update('nonedraftcode' + this.$store.getters.user.username).hex()
          if (res.data.data === msg) {
            this.makeDraftCode()
            this.autosave = true
          } else {
            if (res.data.data.code === undefined || res.data.data.code === null || res.data.data.code === 'null') {
              this.checksum = res.data.data.checksum
              this.draftID = res.data.data.id
              this.code = ''
            } else {
              this.checksum = res.data.data.checksum
              this.code = res.data.data.code
              this.draftID = res.data.data.id
            }
            this.autosave = true
            this.isFirst = false
          }
        })
      },
      makeDraftCode () {
        api.makeDraftCode(this.problemID, this.contestID, this.language).then(res => {
          let func = this.$route.name === 'problem-submission' ? 'getDraftCode' : 'getContestDraftCode'
          api[func](this.problemID, this.contestID, this.language).then(res => {
            if (res.data.data.code === undefined || res.data.data.code === null || res.data.data.code === 'null') {
              this.checksum = res.data.data.checksum
              this.draftID = res.data.data.id
            } else {
              this.checksum = res.data.data.checksum
              this.code = res.data.data.code
              this.draftID = res.data.data.id
            }
          })
        }, _ => {
        })
      },
      changePie (problemData) {
        // 특정 상태일때만 표시
        for (let k in problemData.statistic_info) {
          if (filtedStatus.indexOf(k) === -1) {
            delete problemData.statistic_info[k]
          }
        }
        let acNum = problemData.accepted_number
        let data = [
          {name: 'WA', value: problemData.submission_number - acNum},
          {name: 'AC', value: acNum}
        ]
        this.pie.series[0].data = data
        // 큰 그림의 AC만 선택합니다. 여기서 딥카피를 수행해야 합니다.
        let data2 = JSON.parse(JSON.stringify(data))
        data2[1].selected = true
        this.largePie.series[1].data = data2

        // 결과에 따라 범례를 설정합니다. 제출되지 않은 범례는 표시되지 않습니다.
        let legend = Object.keys(problemData.statistic_info).map(ele => JUDGE_STATUS[ele].short)
        if (legend.length === 0) {
          legend.push('AC', 'WA')
        }
        this.largePie.legend.data = legend

        // ac 데이터를 추출하고 마지막에 넣습니다.
        let acCount = problemData.statistic_info['0']
        delete problemData.statistic_info['0']

        let largePieData = []
        Object.keys(problemData.statistic_info).forEach(ele => {
          largePieData.push({name: JUDGE_STATUS[ele].short, value: problemData.statistic_info[ele]})
        })
        largePieData.push({name: 'AC', value: acCount})
        this.largePie.series[0].data = largePieData
      },
      onChangeLang (newLang) {
        if (this.problem.template[newLang]) {
          if (this.code.trim() === '') {
            this.code = this.problem.template[newLang]
          }
        }
        this.language = newLang
        this.isChangeLanguage = true
        this.init(this.language)
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
        // 일부 문제를 방지하려면 setTimeout을 사용하십시오.
        if (this.refreshStatus) {
          // 이전 제출 상태 확인이 중지되지 않은 경우 중지하십시오. 그렇지 않으면 시간 초과에 대한 참조가 손실되고 무한 요청이 발생합니다.
          clearTimeout(this.refreshStatus)
        }
        const checkStatus = () => {
          let id = this.submissionId
          api.getSubmission(id).then(res => {
            this.result = res.data.data
            if (Object.keys(res.data.data.statistic_info).length !== 0) {
              this.submitting = false
              this.submitted = false
              this.isAfterSubmit = true
              clearTimeout(this.refreshStatus)
              this.init(this.language)
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
            this.updateShareSubmission(this.submissionId, this.isActive)
            // 실시간 상태확인
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
                // 대화 상자와 다음 프롬프트 대화 상자 간의 충돌을 일시적으로 해결합니다(그렇지 않으면 깜박임).
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
      isContestRoute () {
        return this.$route.name === 'contest-problem-submission'
      },
      updateShareSubmission (submissionId, shared) {
        if (!this.isContestRoute) {
          let data = {id: submissionId, shared: shared}
          api.updateSubmission(data).then(res => {
          }, () => {
            this.$error('코드 공유 여부 변경에 실패하였습니다')
          })
        }
      },
      onCopy (event) {
        this.$success('Code copied')
      },
      onCopyError (e) {
        this.$error('Failed to copy code')
      },
      undoPage () {
        this.$router.push({path: this.lastURL.path}).catch(() => {})
      },
      goHome () {
        this.$router.push('/').catch(() => {})
      },
      goSubmissionList () {
        if (this.contestID) {
          this.$router.push({name: 'contest-submission-list', query: {problemID: this.problemID}}).catch(() => {})
        } else {
          this.$router.push({name: 'submission-list', query: {problemID: this.problemID}}).catch(() => {})
        }
      },
      goContestProblem (row) {
        this.isChangeLanguage = true
        this.autosave = false
        let template = this.problem.template
        this.isChangeLanguage = true
        if (template && template[this.language]) {
          this.code = template[this.language]
          this.isFirst = true
          this.autosave = false
          this.checksum = ''
          this.draftID = ''
          this.isAfterSubmit = false
        } else {
          this.isFirst = true
          this.autosave = false
          this.checksum = ''
          this.draftID = ''
          this.code = ''
          this.isAfterSubmit = false
        }
        this.$router.push({ name: 'contest-problem-submission',
          params: {
            contestID: this.contestID,
            problemID: row._id
          }
        }).catch(() => {}).then(res => {
        })
      },
      hintHide () {
        this.hintHidden = !this.hintHidden
      }
    },
    computed: {
      ...mapState({
        problems: state => state.contest.contestProblems
      }),
      ...mapGetters(['problemSubmitDisabled', 'contestRuleType', 'OIContestRealTimePermission', 'contestStatus', 'website', 'isVerifiedEmail', 'isAuthenticated']),
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
      // 구성 요소 전환 후 지속적인 요청 방지
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
      },
      'website' () {
        this.changeDomTitle()
      }
    }
  }
</script>

<style lang="less" scoped>
  @import '../../../../styles/common.less';
  .card-title {
    margin-left: 8px;
  }

  .flex-container {
    max-width: calc(~"100vw - 100px");
    margin-left: 50px;
    margin-right: 50px;
    justify-content: flex-start;
    #problem-main {
      flex: auto;
      margin-right: 18px;
    }
    #right-column {
      flex: none;
      width: 220px;
    }
  }
  .flex-container-submit-mode {
    max-width: calc(~"100vw - 100px");
    margin-left: 0px;
    margin-right: 0px;
    justify-content: flex-start;
  }
  #problem-content {
    margin-top: -50px;
    margin-left: 10px;
    .title {
      font-size: 17px;
      font-weight: 400;
      -webkit-text-stroke: .5px;
      margin: 50px 0 20px 0;
      color: @purple;
      .copy {
        padding-left: 8px;
        i {
          color: @purple;
        }
      }
    }
    p.content {
      margin: 0 20px 0 0;
      font-size: 15px;
    }
    .sample {
      align-items: stretch;
      &-input, &-output {
        min-width: 200px;
        width: 45%;
        flex: 1 1 auto;
        display: flex;
        flex-direction: column;
        margin-right: 5%;
      }
      pre {
        flex: 1 1 auto;
        align-self: stretch;
        border-style: solid;
        background: transparent;
      }
    }
  }
  .split-sapple {
    justify-content: flex-start;
    flex-flow: row wrap;
    -ms-flex-flow: row wrap;
  }
  #submit-code {
    margin-top: 20px;
    margin-bottom: 20px;
    .status {
      position: relative;
      float: left;
      span {
        margin-right: 10px;
        margin-left: 10px;
      }
    }
    .captcha-container {
      display: inline-block;
      .captcha-code {
        width: auto;
        margin-top: -20px;
        margin-left: 20px;
      }
    }
  }

  #info {
    ivu-card-body {
      margin-left: 20px;
      margin-right: 20px;
    }
    margin-bottom: 20px;
    margin-top: 20px;
    ul {
      list-style-type: none;
      li {
        border-bottom: 1px dotted #e9eaec;
        margin-bottom: 10px;
        p {
          display: inline-block;
        }
        p:first-child {
          width: 90px;
        }
        p:last-child {
          float: right;
        }
      }
    }
  }


  #pieChart-detail {
    margin-top: 20px;
    width: 500px;
    height: 480px;
  }
  .problem_contents{
    /* width: ; */
    height: 75vh;
    font-size: 16px;
    overflow-y: scroll;
    &::-webkit-scrollbar {
      width: 20px;
      height: 20px;
    }

    &::-webkit-scrollbar-track {
      background-color: transparent;
    }

    &::-webkit-scrollbar-thumb {
      background-color: @dark-white;
      border-radius: 20px;
      border: 6px solid transparent;
      background-clip: content-box;
    }
  }

  .problem_input{
    padding: 0 20px 0 20px;
    background-color: @white;
    height: 100%;
  }

  .input-for-pre {
    min-width: 90px;

  }

  .demo-split {
    height: 87vh;
    margin-left: 0px !important;
    margin-right: 0px !important;
    /* margin: -80px -45px -250px -45px; 
    /* border: 1px solid #dcdee2; */
  }
  .ss_header{
    background: @purple;
    color: @black;
    position: relative;
    display: flex;
    justify-content: space-between;
    left: 0px;
    top: 0px;
    width: 100%;
    height: 60px;
    line-height: 60px;
    box-shadow: 0 1px 5px 0 rgba(0, 0, 0, 0.1);

    .header-left {
      display: flex;
      .problem-name {
        font-size: 120%;
        -webkit-text-stroke: .5px;
        color: @white;
        padding: 0 4px;
      }
    }

    .header-right {
      display: flex;
      
      .hide-btn {
        background-color: @light-purple;
        border-radius: 5px;
        -webkit-text-stroke: .3px;
        &:focus {
          color: @white;
        }
        &:hover {
          background-color: #947dff;
        }
      }
    }

    #undo-icon {
      float: left;
      width: 40px;
      text-align: center;
      line-height: 60px;
      color: @purple;
      * {
        transition: all 0.1s ease-in-out;
      }
      &:hover {
        cursor: pointer;
        color: @purple;
        * {
          color: @purple;
        }
      }
    }
    .logo {
      float: left;
      color: @white;
      font-size: 28px;
      font-weight: 900;
      margin: 0 20px;
      -webkit-text-stroke: 1px;
      &:hover {
        cursor: pointer;
      }
    }
    div {
      line-height: 60px;
    }
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
    position: absolute;
    left: 0;
    bottom: 0;
    width: 100%;
    height: 60px;
    line-height: 60px;
    z-index: 99;
    /* text-align: center; */
  }  

  @media screen and (max-width: 1200px) {
    .demo-split{
      margin: -80px -50px -200px -50px;
    }
  }
  @media screen and (min-width: 1200px) {
    .demo-split{
      margin: -80px -50px -200px -50px;
    }
  }

  .left-split-pane{

    padding: 10px;
    height: 100%;
    background: @white;
  }

  .right-split-pane{
    /* padding: 10px; */
    height: 100%;
    min-width: 600px;
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
  .blockingdrag {
    -webkit-user-select:none;
    -moz-user-select:none;
    -ms-user-select:none;
    user-select:none
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
  .undo-btn {
    float: right;
    margin: 10px 25px 10px 0;
  }

  .problem-animate-enter-active {
    animation: fadeIn 1s;
  }
  .tag-card {
    & > .ivu-card-body {
      padding-left: 20px;
      padding-right: 20px;
    }
  }

  .auto-save-block {
    margin-right: 30px;
    .loading-box {
      float: left;
      width: 30px;
      height: 60px;
      display: block;
      line-height: 60px;
      margin-left: 5px;
      .check-icon {
        font-size: 1.5em;
        color: rgba(230, 228, 228, 0.864);
      }
    }
    .text-block {
      float: right;
      width: 60px;
      font-size : 14px;
      font-weight: 400;
      line-height: 60px;
      color: #e9eaece2;
    }
  }
  .help {
    cursor: pointer;
    margin-right: 10px;
    .help-btn {
      font-size: 14px;
      font-weight: 400;
      line-height: 60px;
      color: @white;
      background-color: transparent;
      border-color: transparent;
      transition: all 0.3s ease-in-out;
      &:hover {
        color: @light-purple;
      }
    }
  }
  .hide {
    display: flex;
    cursor: pointer;
  }
  .hint-hide-btn {
    padding: 0px;
    margin-left: 10px;
    margin-top: 25px;
    border-color: transparent;
    color: @purple;
    &:hover, &:focus {
      border-color: transparent;
      box-shadow: none;
    }
  }

  .submit-btn {
    background-color: #E05252;
    margin: 0 35px 0 10px;
    color: @white;
    -webkit-text-stroke: .3px;
    &:hover {
      background-color: @red;
      transition: background-color .3s ease-in-out;
    }
  }

  p {
    padding: 0;
    margin: 0;
  }

  .result {
    -webkit-text-stroke: .3px; 
    font-size: 15px;
    border-width: 2px;
  }

  .contest-list {
    display: flex;
    justify-content: space-between;
    padding: 15px 10px;
    font-size: 15px;
    -webkit-text-stroke: .5px;
    cursor: pointer;
    .left-contest-list {
      display: flex;
    }

    &:hover {
      color: @purple;
      background-color: #f7f6ff;
      transition: all .1s ease-in;
    }

    &.purple {
      -webkit-text-stroke: .5px;
      color: @purple;
    }
    div:first-child {
      padding-right: 10px;
    }
  }
</style>
<style lang="less">
  .el-loading-spinner {
    top: initial;
    margin-top: initial;
    i {
      font-size: 1.4em;
      color: rgba(255, 255, 255, 0.864);
    }
  }
</style>
