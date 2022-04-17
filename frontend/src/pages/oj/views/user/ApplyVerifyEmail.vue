<template>
  <Panel :padding="30" class="container">
    <div slot="title" class="center">계정 인증</div>
    <template v-if="!successApply">
      <Form :rules="ruleVerifyEmail" :model=formVerifyEmail ref="formVerifyEmail">
        <Form-item prop="email">
          <Input v-model="formVerifyEmail.email" size="large" readonly>
          <Icon type="ios-mail-outline" slot="prepend"></Icon>
          </Input>
        </Form-item>
      </Form>
      <Button type="primary"
              @click="sendEmail"
              class="btn" long
              :loading="btnLoading">이메일 보내기
      </Button>
    </template>
    <template v-else>
      <Alert type="success" show-icon>
        {{$t('Success')}}
        <span slot="desc"> 이메일이 성공적으로 보내졌습니다.</span>
      </Alert>
    </template>
  </Panel>
</template>
<script>
  import api from '@oj/api'
  import {FormMixin} from '@oj/components/mixins'

  export default {
    mixins: [FormMixin],
    data () {
      const CheckEmailExist = (rule, value, callback) => {
        if (value !== '') {
          api.checkUsernameOrEmail(undefined, value).then(res => {
            if (res.data.data.email === false) {
              callback(new Error(this.$i18n.t('m.The_email_doesnt_exist')))
            } else {
              callback()
            }
          }, _ => callback())
        } else {
          callback()
        }
      }
      return {
        captchaSrc: '',
        successApply: false,
        btnLoading: false,
        formVerifyEmail: {
          email: ''
        },
        ruleVerifyEmail: {
          email: [
            {required: true, type: 'email', trigger: 'blur'},
            {validator: CheckEmailExist, trigger: 'blur'}
          ]
        }
      }
    },
    mounted () {
      this.getMail()
    },
    methods: {
      getMail () {
        this.formVerifyEmail.email = this.$store.getters.user.email
        setTimeout(() => {
        }, 1000)
      },
      sendEmail () {
        this.validateForm('formVerifyEmail').then(() => {
          this.btnLoading = true
          this.formVerifyEmail.email = this.$store.getters.user.email
          let data = Object.assign({}, this.formVerifyEmail)
          api.applyVerifyEmail(data).then(res => {
            // 伪加载
            setTimeout(() => {
              this.btnLoading = false
              this.successApply = true
            }, 2000)
          }, _ => {
            this.btnLoading = false
          })
        })
      }
    }
  }
</script>

<style scoped lang="less">
  .container {
    width: 450px;
    height: 250px;
    margin: auto;
    .center {
      text-align: center;
    }
    .btn {
      margin-top: 18px;
      text-align: center;
    }
  }
</style>
