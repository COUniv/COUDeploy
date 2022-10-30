<template>
  <Panel :padding="30" class="container">
    <div slot="title" class="center">아이디 찾기</div>
    <template v-if="!successApply">
      <div>
        <div class="text-center">
          <span>가입 때 입력했던 이메일을 입력해주세요</span>
        </div>
        <div>
          <Input v-model="formEmail.email" :placeholder="$t('m.ApplyEmail')" size="large">
          <Icon type="ios-mail-outline" slot="prepend"></Icon>
          </Input>
        </div>
      </div>
      <Button type="primary"
              @click="sendEmail"
              class="btn" long
              :loading="btnLoading">아이디 찾기
      </Button>
    </template>
    <template v-else>
      <Alert type="success" show-icon>
        {{$t('Success')}}
        <span slot="desc"> {{$t('Password_reset_mail_sent')}}</span>
      </Alert>
    </template>
  </Panel>
</template>
<script>
  import api from '@oj/api'
  export default {
    data () {
      return {
        successApply: false,
        btnLoading: false,
        findID: '',
        formEmail: {
          email: ''
        }
      }
    },
    methods: {
      sendEmail () {
        this.btnLoading = true
        let data = Object.assign({}, this.formEmail)
        api.getFindusername(this.formEmail.email).then(res => {
          this.findID = res.data.data.username
          console.log(this.findID)
          setTimeout(() => {
            this.btnLoading = false
            this.successApply = true
          }, 2000)
        }, _ => {
          this.findID = '아이디가 존재하지 않습니다.'
          this.btnLoading = false
        })
      }
    }
  }
</script>

<style scoped lang="less">
  .container {
    width: 450px;
    height: 360px;
    margin: auto;
    .center {
      text-align: center;
    }
    .btn {
      margin-top: 18px;
      text-align: center;
    }
  }
  .text-center {
    margin-bottom: 10px;
    text-align: center;
    font-size: 1.2em;
  }
</style>
