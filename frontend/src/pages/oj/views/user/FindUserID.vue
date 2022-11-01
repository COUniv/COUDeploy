<template>
  <Panel :padding="30" class="container">
    <template v-if="!successApply">
      <div slot="title" class="center">아이디 찾기</div>
      <Form ref="formEmail" :model="formEmail" :rules="ruleValidate" @submit.native.prevent="sendEmail">
        <div class="text-center">
          <span>가입 때 입력했던 이메일을 입력해주세요</span>
        </div>
        <FormItem prop="email">
          <Input v-model="formEmail.email" :placeholder="$t('m.ApplyEmail')" size="large">
            <Icon type="ios-mail-outline" slot="prepend"></Icon>
          </Input>
        </FormItem>
      </Form>
      <div class="btn-bottom">
        <Button type="primary"
              @click="sendEmail"
              class="btn" long
              :loading="btnLoading">아이디 찾기
        </Button>
      </div>
    </template>
    <template v-else>
      <div slot="title" class="center">아이디 찾기 결과</div>
      <div class="find-id">
        <span v-if="notExistID"> {{findID}} </span>
        <span v-if="!notExistID"> 아이디: {{findID}} </span>
      </div>
      <div class="btn-bottom">
        <div v-if="notExistID" class="head-btn">
          <ButtonGroup class="sub-btn">
            <Button v-if="notExistID" type="warning"
                  @click="research"
                  class="btn">다시 찾기
            </Button>
            <Button type="primary"
                  @click="goLogin"
                  class="btn"
                  :loading="btnLoading">로그인
            </Button>
          </ButtonGroup>
        </div>
        <div v-else>
          <Button type="primary"
                  @click="goLogin"
                  class="btn" long
                  :loading="btnLoading">로그인
          </Button>
        </div>
      </div>
      <!-- <Alert type="success" show-icon>
        {{$t('Success')}}
        <span slot="desc"> {{$t('Password_reset_mail_sent')}}</span>
      </Alert> -->
    </template>
  </Panel>
</template>
<script>
  import api from '@oj/api'
  import { FormMixin } from '@oj/components/mixins'
  export default {
    mixins: [FormMixin],
    data () {
      return {
        enableEnter: false,
        successApply: false,
        notExistID: false,
        btnLoading: false,
        findID: '',
        formEmail: {
          email: ''
        },
        ruleValidate: {
          email: [
            { required: true, message: '이메일을 입력해주세요', trigger: 'blur' },
            { type: 'email', message: '이메일 형식이 아닙니다', trigger: 'blur' }
          ]
        }
      }
    },
    methods: {
      sendEmail () {
        this.validateForm('formEmail').then(valid => {
          this.btnLoading = true
          api.getFindusername(this.formEmail).then(res => {
            this.findID = res.data.data.username
            if (this.findID === 'None' || this.findID === '') {
              this.findID = '아이디가 존재하지 않습니다.'
              this.notExistID = true
            }
            setTimeout(() => {
              this.btnLoading = false
              this.successApply = true
            }, 500)
          }, _ => {
            console.log(_)
            this.findID = '아이디가 존재하지 않습니다.'
            this.btnLoading = false
          })
        })
      },
      goLogin () {
        this.$router.push({path: '/login'}).catch(() => {})
      },
      research () {
        this.findID = ''
        this.formEmail.email = ''
        this.successApply = false
        this.notExistID = false
      }
    }
  }
</script>

<style scoped lang="less">
  .container {
    width: 450px;
    // height: 360px;
    margin: auto;
    .center {
      text-align: center;
      font-size: 1.6rem;
      font-weight: 700;
    }
    .btn {
      margin-top: 18px;
      text-align: center;
    }
  }
  .text-center {
    margin-bottom: 10px;
    text-align: center;
    font-size: 1.1em;
  }
  .find-id {
    text-align: center;
    font-weight: 700;
    margin-bottom: 20px;
  }
  .btn-bottom {
    margin-bottom: 20px;
  }
  // .sub-btn {
  //   & .btn .ivu-btn {
  //     width: 100%;
  //   }
  // }
</style>
<style lang="less">
  .head-btn {
    padding: 0 20px;
  }
  .sub-btn {
    width: 100% !important;
    display: block;
    clear: both;
    height: 50px;
    button {
      width: 45%;
      &:first-child {
        float: left;
      }
      &:last-child:not(:first-child){
        float: right;
      }
      border-radius: 5px !important;
    }
  }
</style>
