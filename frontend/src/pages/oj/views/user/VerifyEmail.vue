<template>
  <Panel :padding="30" class="container">
    <div slot="title" class="center">계정 인증하기</div>
    <template v-if="!resetSuccess">
    <Button type="primary"
            @click="verifyEmail"
            class="btn" long
            :loading="btnLoading">인증 완료하기
    </Button>
    </template>

    <template v-else>
      <Alert type="success">정상적으로 인증되었습니다.</Alert>
    </template>
  </Panel>
</template>

<script>
  import {FormMixin} from '@oj/components/mixins'
  import api from '@oj/api'

  export default {
    name: 'verify-email',
    mixins: [FormMixin],
    data () {
      return {
        btnLoading: false,
        resetSuccess: false,
        formVerifyEmail: {
          token: ''
        }
      }
    },
    mounted () {
      this.formVerifyEmail.token = this.$route.params.token
    },
    methods: {
      verifyEmail () {
        this.btnLoading = true
        this.formVerifyEmail.token = this.$route.params.token
        let data = Object.assign({}, this.formVerifyEmail)
        api.verifyEmail(data).then(res => {
          this.btnLoading = false
          this.resetSuccess = true
          setTimeout(this.goRoute(), 1000)
        }, _ => {
          this.btnLoading = false
        })
      },
      goRoute () {
        this.$success('이메일 인증이 완료되었습니다. 다시 로그인 해주시길 바랍니다.')
        this.$router.replace({
          path: '/logout'
        })
      }
    }
  }
</script>
<style lang="less" scoped>
  .container {
    width: 450px;
    height: 250px;
    margin: auto;
    .center {
      text-align: center;
    }
    #captcha {
      display: flex;
      flex-wrap: nowrap;
      justify-content: space-between;
      width: 100%;
      height: 36px;
      #captchaCode {
        flex: auto;
      }
      #captchaImg {
        margin-left: 10px;
        padding: 3px;
        flex: initial;
      }
    }
    .btn {
      margin-top: 18px;
      text-align: center;
    }
  }
</style>
