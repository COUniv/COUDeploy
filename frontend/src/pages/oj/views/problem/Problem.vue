<template>
  <div>
    <div>
      <template v-if="!submitmode">
        <div class="flex-container">
          <div id="problem-main">
            <!--problem main-->
            <Panel :padding="40" shadow>
              <div slot="title">{{problem.title}}</div>
              <div id="problem-content" class="markdown-body" v-katex>
                <p class="title">{{$t('m.Description')}}</p>
                <p class="content" v-html=problem.description></p>
                <!-- {{$t('m.music')}} -->
                <p class="title">{{$t('m.Input')}} <span v-if="problem.io_mode.io_mode=='File IO'">({{$t('m.FromFile')}}: {{ problem.io_mode.input }})</span></p>
                <p class="content" v-html=problem.input_description></p>

                <p class="title">{{$t('m.Output')}} <span v-if="problem.io_mode.io_mode=='File IO'">({{$t('m.ToFile')}}: {{ problem.io_mode.output }})</span></p>
                <p class="content" v-html=problem.output_description></p>

                <div v-for="(sample, index) of problem.samples" :key="index">
                  <div class="flex-container sample">
                    <div class="sample-input">
                      <p class="title">{{$t('m.Sample_Input')}} {{index + 1}}
                        <a class="copy"
                            v-clipboard:copy="sample.input"
                            v-clipboard:success="onCopy"
                            v-clipboard:error="onCopyError">
                          <Icon type="clipboard"></Icon>
                        </a>
                      </p>
                      <pre>{{sample.input}}</pre>
                    </div>
                    <div class="sample-output">
                      <p class="title">{{$t('m.Sample_Output')}} {{index + 1}}</p>
                      <pre>{{sample.output}}</pre>
                    </div>
                  </div>
                </div>

                <div v-if="problem.hint">
                  <p class="title">{{$t('m.Hint')}}</p>
                  <Card dis-hover>
                    <div class="content" v-html=problem.hint></div>
                  </Card>
                </div>

                <div v-if="problem.source">
                  <p class="title">{{$t('m.Source')}}</p>
                  <p class="content">{{problem.source}}</p>
                </div>

              </div>
            </Panel>
            <!--problem main end-->
            <Card :padding="20" id="submit-code" dis-hover>
              <CodeMirror :value.sync="code"
                          :languages="problem.languages"
                          :language="language"
                          :theme="theme"
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
                    <div class="captcha-container">
                      <Tooltip v-if="captchaRequired" content="Click to refresh" placement="top">
                        <img :src="captchaSrc" @click="getCaptchaSrc"/>
                      </Tooltip>
                      <Input v-model="captchaCode" class="captcha-code"/>
                    </div>
                  </template>
                  <Button type="warning" icon="edit" :loading="submitting" @click="submitCode"
                          :disabled="problemSubmitDisabled || submitted"
                          class="fl-right">
                    <span v-if="submitting">{{$t('m.Submitting')}}</span>
                    <span v-else>{{$t('m.Submit')}}</span>
                  </Button>
                </Col>
              </Row>
            </Card>
          </div>

          <div id="right-column">

            <!-- 제출 버튼 -->
            <VerticalMenu style="margin-bottom: 20px;">
              <!-- <VerticalMenu-item :route="{name: 'contest-problem-list', params: {contestID: contestID}}"> -->
                <Button type="primary" long=ture size="large" @click="goSubmitView">제출하기</Button>
              <!-- </VerticalMenu-item> -->
            </VerticalMenu>


            <VerticalMenu @on-click="handleRoute">
              <template v-if="this.contestID">
                <VerticalMenu-item :route="{name: 'contest-problem-list', params: {contestID: contestID}}">
                  <Icon type="ios-photos"></Icon>
                  {{$t('m.Problems')}}
                </VerticalMenu-item>

                <VerticalMenu-item :route="{name: 'contest-announcement-list', params: {contestID: contestID}}">
                  <Icon type="chatbubble-working"></Icon>
                  {{$t('m.Announcements')}}
                </VerticalMenu-item>
              </template>

              <VerticalMenu-item v-if="!this.contestID || OIContestRealTimePermission" :route="submissionRoute">
                <Icon type="navicon-round"></Icon>
                {{$t('m.Submissions')}}
              </VerticalMenu-item>

              <template v-if="this.contestID">
                <VerticalMenu-item v-if="!this.contestID || OIContestRealTimePermission"
                  :route="{name: 'contest-rank', params: {contestID: contestID}}">
                  <Icon type="stats-bars"></Icon>
                  {{$t('m.Rankings')}}
                </VerticalMenu-item>
                <VerticalMenu-item :route="{name: 'contest-details', params: {contestID: contestID}}">
                  <Icon type="home"></Icon>
                  {{$t('m.View_Contest')}}
                </VerticalMenu-item>
              </template>
            </VerticalMenu>

            <Card id="info">
              <div slot="title" class="header">
                <Icon type="information-circled"></Icon>
                <span class="card-title">{{$t('m.Information')}}</span>
              </div>
              <ul>
                <li><p>ID</p>
                  <p>{{problem._id}}</p></li>
                <li>
                  <p>{{$t('m.Time_Limit')}}</p>
                  <p>{{problem.time_limit}}MS</p></li>
                <li>
                  <p>{{$t('m.Memory_Limit')}}</p>
                  <p>{{problem.memory_limit}}MB</p></li>
                <li>
                <li>
                  <p>{{$t('m.IOMode')}}</p>
                  <p>{{problem.io_mode.io_mode}}</p>
                </li>
                <li>
                  <p>{{$t('m.Created')}}</p>
                  <p>{{problem.created_by.username}}</p></li>
                <li v-if="problem.difficulty">
                  <p>{{$t('m.Level')}}</p>
                  <p>{{$t('m.' + problem.difficulty)}}</p></li>
                <li v-if="problem.total_score">
                  <p>{{$t('m.Score')}}</p>
                  <p>{{problem.total_score}}</p>
                </li>
                <li>
                  <p>{{$t('m.Tags')}}</p>
                  <p>
                    <Poptip trigger="hover" placement="left-end">
                      <a>{{$t('m.Show')}}</a>
                      <div slot="content">
                        <Tag v-for="tag in problem.tags" :key="tag">{{tag}}</Tag>
                      </div>
                    </Poptip>
                  </p>
                </li>
              </ul>
            </Card>

            <!-- <Card id="pieChart" :padding="0" v-if="!this.contestID || OIContestRealTimePermission">
              <div slot="title">
                <Icon type="ios-analytics"></Icon>
                <span class="card-title">{{$t('m.Statistic')}}</span>
                <Button size="small" id="detail" @click="graphVisible = !graphVisible">Details</Button>
              </div>
              <div class="echarts">
                <ECharts :options="pie"></ECharts>
              </div>
            </Card>
          </div>

          <Modal v-model="graphVisible">
            <div id="pieChart-detail">
              <ECharts :options="largePie" :initOptions="largePieInitOpts"></ECharts>
            </div>
            <div slot="footer">
              <Button @click="graphVisible=false">{{$t('m.Close')}}</Button>
            </div>
          </Modal> -->
        </div>
      </template>
      <template v-else>
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
          
            <Split v-model="split3" v-bind:min="min1" v-bind:max="max1" style="overflow: hidden!important;">
              <div slot="left" class="left-split-pane" >

                <Tabs value="name1" type="card" :animated="false">
                  <TabPane :label="problem.title" name="name1" >   <!-- style="padding: 0 30px 10px 30px" -->
                    <div class="problem_contents">
                      <div id="problem-content" class="markdown-body" v-katex>
                        <p class="title">{{$t('m.Description')}}</p>
                        <p class="content" v-html=problem.description></p>
                        <p class="title">{{$t('m.Input')}} <span v-if="problem.io_mode.io_mode=='File IO'">({{$t('m.FromFile')}}: {{ problem.io_mode.input }})</span></p>
                        <p class="content" v-html=problem.input_description></p>

                        <p class="title">{{$t('m.Output')}} <span v-if="problem.io_mode.io_mode=='File IO'">({{$t('m.ToFile')}}: {{ problem.io_mode.output }})</span></p>
                        <p class="content" v-html=problem.output_description></p>

                        <div v-for="(sample, index) of problem.samples" :key="index">
                          <div class="flex-container sample">
                            <div class="sample-input">
                              <p class="title">{{$t('m.Sample_Input')}} {{index + 1}}
                                <a class="copy"
                                    v-clipboard:copy="sample.input"
                                    v-clipboard:success="onCopy"
                                    v-clipboard:error="onCopyError">
                                  <Icon type="clipboard"></Icon>
                                </a>
                              </p>
                              <pre>{{sample.input}}</pre>
                            </div>
                            <div class="sample-output">
                              <p class="title">{{$t('m.Sample_Output')}} {{index + 1}}</p>
                              <pre>{{sample.output}}</pre>
                            </div>
                          </div>
                        </div>

                        <div v-if="problem.hint">
                          <p class="title">{{$t('m.Hint')}}</p>
                          <Card dis-hover>
                            <div class="content" v-html=problem.hint></div>
                          </Card>
                        </div>
                      </div>
                    </div>
                  </TabPane>
                </Tabs>
              </div>
              <div slot="right" class="right-split-pane">
                <div class="undo-btn">
                  <Button icon="ios-undo" @click="undoSubmitView">{{$t('m.Back')}}</Button>
                </div>
                <div style="clear:both;"></div>
                <!-- Right Padding -->
                <div class="problem_input">
                  <!-- <Problem></Problem> -->
                  <Card :padding="20" id="submit-codes" style="margin: 0;" dis-hover>
                    <!-- height는 SubmitCodeMirror랑 같게 할 것 -->
                    <SubmitCodeMirror :value.sync="code"
                                :languages="problem.languages"
                                :language="language"
                                :theme="theme"
                                @resetCode="onResetToTemplate"
                                @changeTheme="onChangeTheme"
                                @changeLang="onChangeLang"></SubmitCodeMirror>
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
                <Button type="primary" size="large" style="z-index: '4'" :loading="submitting" @click="submitCode"
                        :disabled="problemSubmitDisabled || submitted">
                  <span v-if="submitting">{{$t('m.Submitting')}}</span>
                  <span v-else>{{$t('m.Submit')}}</span>
                </Button>
              </div>
            </div>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>



<script>
  import {mapGetters, mapActions} from 'vuex'
  import {types} from '../../../../store'
  import SubmitCodeMirror from '@oj/components/SubmitCodeMirror.vue'
  import CodeMirror from '@oj/components/CodeMirror.vue'
  import storage from '@/utils/storage'
  import {FormMixin} from '@oj/components/mixins'
  import utils from '@/utils/utils'
  import {JUDGE_STATUS, CONTEST_STATUS, buildProblemCodeKey} from '@/utils/constants'
  import api from '@oj/api'
  import {pie, largePie} from './chartData'

  // 只显示这些状态的图形占用
  const filtedStatus = ['-1', '-2', '0', '1', '2', '3', '4', '8']

  export default {
    name: 'Problem',
    components: {
      CodeMirror,
      SubmitCodeMirror
    },
    mixins: [FormMixin],
    data () {
      return {
        // submit 화면 여부
        submitmode: false,

        isActive: false,
        split3: 0.4,
        min1: '200px',
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
      ...mapActions(['changeDomTitle']),
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
          this.changePie(problem)
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
          this.submitmode = false
        }, () => {
          this.$Loading.error()
        })
      },
      changePie (problemData) {
        // 只显示特定的一些状态
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
        // 只把大图的AC selected下，这里需要做一下deepcopy
        let data2 = JSON.parse(JSON.stringify(data))
        data2[1].selected = true
        this.largePie.series[1].data = data2

        // 根据结果设置legend,没有提交过的legend不显示
        let legend = Object.keys(problemData.statistic_info).map(ele => JUDGE_STATUS[ele].short)
        if (legend.length === 0) {
          legend.push('AC', 'WA')
        }
        this.largePie.legend.data = legend

        // 把ac的数据提取出来放在最后
        let acCount = problemData.statistic_info['0']
        delete problemData.statistic_info['0']

        let largePieData = []
        Object.keys(problemData.statistic_info).forEach(ele => {
          largePieData.push({name: JUDGE_STATUS[ele].short, value: problemData.statistic_info[ele]})
        })
        largePieData.push({name: 'AC', value: acCount})
        this.largePie.series[0].data = largePieData
      },
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
      },
      goSubmitView () {
        // this.$router.push({
        //   name: 'solve-submit',
        //   query: utils.filterEmptyValue(this.$route.query)
        // })
        this.submitmode = true
      },
      undoSubmitView () {
        this.submitmode = false
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

<style lang="less" scoped>
  .card-title {
    margin-left: 8px;
  }

  .flex-container {
    #problem-main {
      flex: auto;
      margin-right: 18px;
    }
    #right-column {
      flex: none;
      width: 220px;
    }
  }

  #problem-content {
    margin-top: -50px;
    .title {
      font-size: 17px;
      font-weight: 400;
      margin: 50px 0 20px 0;
      color: #3091f2;
      .copy {
        padding-left: 8px;
      }
    }
    p.content {
      margin-left: 25px;
      margin-right: 20px;
      font-size: 15px
    }
    .sample {
      align-items: stretch;
      &-input, &-output {
        width: 50%;
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

  .fl-right {
    float: right;
  }

  #pieChart {
    .echarts {
      height: 250px;
      width: 210px;
    }
    #detail {
      position: absolute;
      right: 10px;
      top: 10px;
    }
  }

  #pieChart-detail {
    margin-top: 20px;
    width: 500px;
    height: 480px;
  }
  .problem_contents{
    overflow: auto;
    /* width: ; */
    height: 79vh;
    font-size: 16px;
  }

  .problem_input{
    padding: 0 20px 0 20px;
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
</style>
