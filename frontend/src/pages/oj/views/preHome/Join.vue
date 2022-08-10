<template>
  <div class="join">
    <div class="form">
      <Form ref="formLogin" :model="formLogin" :rules="ruleLogin">
        <!-- 회원가입 박스 title-->
        <div class="join_title"><p @click="goRoute('/')">COU</p></div>
                
        <div class = "join_edge">
          <FormItem prop="username">
            <p class="form_title">아이디</p>
            <Input class ="login_input" type="text" v-model="formLogin.username" placeholder="아이디를 입력해주세요" size="large" @on-enter="handleLogin">
            </Input>
          </FormItem>
          <FormItem prop="password">
            <p class="form_title">비밀번호</p>
            <Input class ="login_input" type="password" v-model="formLogin.password" placeholder="비밀번호를 입력해주세요" size="large" @on-enter="handleLogin">
            </Input>
          </FormItem>
          <FormItem prop="password">
            <p class="form_title">비밀번호 확인</p>
            <Input class ="login_input" type="password" v-model="formLogin.password" placeholder="비밀번호를 다시 한 번 입력해주세요" size="large" @on-enter="handleLogin">
            </Input>
          </FormItem>
          <FormItem prop="email">
            <p class="form_title">이메일</p>
            <Input class ="login_input" type="password" v-model="formLogin.password" placeholder="이메일을 입력해주세요" size="large" @on-enter="handleLogin">
            </Input>
          </FormItem>
          <FormItem>
            <div class="login_btn">
              <Button 
                type="primary"
                @click="handleLogin"
                class="primary btn" v-if="website.allow_register" long
                :loading="btnLoginLoading">
                회원가입
              </Button>
            </div>
          </FormItem>
        </div>
      </Form>
      <div class="join_foot" @click="$router.push('/login')"> &#60; 로그인 페이지</div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import api from '@oj/api'
import { FormMixin } from '@oj/components/mixins'
import register from '@oj/views/user/Register'
export default {
  mixins: [FormMixin],
  components: {
    register
  },
  data () {
    // LoginStaus :false;  //로그인 상태 초기값 : false
    const CheckRequiredTFA = (rule, value, callback) => {
      if (value !== '') {
        api.tfaRequiredCheck(value).then(res => {
          this.tfaRequired = res.data.data.result
        })
      }
      callback()
    }

    return {
      lastURL: '',
      tfaRequired: false,
      btnLoginLoading: false,
      formLogin: {
        username: '',
        password: '',
        // 로그인 상태  prop 값
        login_status: false,
        tfa_code: ''
      },
      ruleLogin: {
        username: [
          {required: true, trigger: 'blur'},
          {validator: CheckRequiredTFA, trigger: 'blur'}
        ],
        password: [
          {required: true, trigger: 'change', min: 6, max: 20}
        ]
      }
    }
  },
  methods: {
    ...mapActions(['changeModalStatus', 'getProfile']),
    handleBtnClick (mode) {
      this.changeModalStatus({
        visible: true,
        mode: mode
      })
    },
    changeInputText (event) {
      this.formLogin.username = event
    },
    changeInputTextP (event) {
      this.formLogin.password = event
    },

    handleLogin () {
      this.validateForm('formLogin').then(valid => {
        this.btnLoginLoading = true
        let formData = Object.assign({}, this.formLogin)
        if (!this.tfaRequired) {
          delete formData['tfa_code']
        }
        api.login(formData).then(res => {       // login : api.js파일의 login 함수를 사용하게 함
          this.btnLoginLoading = false
          this.changeModalStatus({visible: false})
          this.getProfile()
          this.$success(this.$i18n.t('m.Welcome_back'))
          setTimeout(() => {
            this.afterlogin(this.lastURL)
          }, 500)
        }, _ => {
          this.btnLoginLoading = false
        })
      })
    },
    afterlogin (route) {
      if (route) {
        this.$router.push({path: route.path})
      } else {
        this.$router.push({path: '/'})
      }
    },
    goRoute (route) {
      if (route) {
        this.$router.push({path: route})
      } else {
        this.$router.push({path: '/'})
      }
    },
    goResetPassword () {
      this.changeModalStatus({visible: false})
      this.$router.push({name: 'apply-reset-password'})
    },
    isAlreadyLoggedin () {
      if (this.$store.getters.isAuthenticated === true) {
        this.$router.push({
          name: 'home'
        })
      }
    }
  },
  beforeRouteEnter (to, from, next) {
    next(vm => {
      vm.lastURL = from
    })
  },
  computed: {
    ...mapGetters(['website', 'modalStatus']),
    visible: {
      get () {
        return this.modalStatus.visible
      },
      set (value) {
        this.changeModalStatus({visible: value})
      }
    }
  },
  mounted () {
    this.isAlreadyLoggedin()
  }
}
</script>

<style scoped lang="less">
@import '../../../../styles/common.less';

.join {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 120vh;
  height: calc(~"100vh - 80px");
}


@media screen and (max-width: 1200px) {
  .join {
    margin: -80px -50px -190px -50px;
    position: relative;
  }
}

@media screen and (max-height: 725px) {
  .join {
    margin: -80px -50px -190px -50px;
    position: relative;
  }
}

@media screen and (min-width: 1200px) {
  .join {
    margin: -80px -50px -190px -50px;
  }
}

.nav {
  top: -80px;
  position: absolute;
}
.image{
  display: block;
  left: -20px;
  top: 0px;
  width: 100%;
  height: 60vh;
  background-color: rgb(39, 39, 39);
  color: white;
  font-size: 36px;
  font-weight: bold;
}
.form {
  display: inline-block;
  background-color: @white;
  box-shadow: 2px 5px 20px 2px rgba(90, 82, 128, 0.31);
  border-radius: @size-border-radius;
  padding: 20px;
  width: 30%;
  max-width: 500px;
  overflow: auto;
  .btn {
    margin: 0 0 0 0;
    &:last-child {
      margin: 0 0 60px 0;
    }
  }
}


/* 회원가입 박스의 Coding Platform Dev title css */
.join_title{
  width: 100%;
  height: 13%;
  margin: 30px 0;
  background: @white;
  padding: 0px;
  text-align: center;
  font-size: @font-large;
  font-weight: @weight-bold;
  line-height: 50px;
  color: @purple;
  p {
    display:inline-block;
    cursor: pointer;
    margin: 0 auto;
  }
}

/* 회원가입 입력 박스 css */
.join_edge{
  // margin-top: 10px;
  padding: 0px 50px 30px;
  background-color: @white;
  .form_title {
    font-size: @font-micro;
    font-weight: bold;
    color: @purple;
  }
}


/* 로그인 입력 textbox css */
.login_input {
  text-justify: center;
  font-size: 18px;
}

/* 로그인 상태 유지 checkbox css */
.login_check{
  text-align: left;
}

.register_btn{
  margin-top: 20px;
}

.btn {
  border: none;
  border-radius: @size-border-radius;
  text-justify: center;
  padding: 12px 0;
  color: white;
  font-size: @font-small;
  font-weight: bold;
  &.primary {
    background: @purple;
  }
  &.second {
    background: @light-gray;
    color: @gray;
  }
}

/* 로그인 회원가입하기 & 아이디/비밀번호 찾기 */
.join_foot {
  color: @gray;
  font-weight: @weight-bold;
  &:hover {
    cursor: pointer;
  }
}

.footer {
    background-color: @black;
    position: relative;
    left: 0;
    bottom: 0;
    width: 100%;
    height: 10vh;
    text-align: center;
    font-size: small;
  }

</style>
