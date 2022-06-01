<template>
  <div class="setting-main">
    <div class="flex-container">
      <div class="left">
        <p class="section-title">{{$t('m.ChangePassword')}}</p>
        <Form class="setting-content" ref="formPassword" :model="formPassword" :rules="rulePassword">
          <FormItem label="Old Password" prop="old_password">
            <Input v-model="formPassword.old_password" type="password"></Input>
          </FormItem>
          <FormItem label="New Password" prop="new_password">
            <Input v-model="formPassword.new_password" type="password"></Input>
          </FormItem>
          <FormItem label="Confirm New Password" prop="again_password">
            <Input v-model="formPassword.again_password" type="password"></Input>
          </FormItem>
          <FormItem v-if="visible.tfaRequired" label="Two Factor Auth" prop="tfa_code">
            <Input v-model="formPassword.tfa_code"/>
          </FormItem>
          <FormItem v-if="visible.passwordAlert">
            <Alert type="success">You will need to login again after 5 seconds..</Alert>
          </FormItem>
          <Button type="primary" @click="changePassword">{{$t('m.Update_Password')}}</Button>
        </Form>
      </div>

      <div class="middle separator"></div>

      <div class="right">
        <p class="section-title">{{$t('m.ChangeEmail')}}</p>
        <Form class="setting-content" ref="formEmail" :model="formEmail" :rules="ruleEmail">
          <FormItem label="Current Password" prop="password">
            <Input v-model="formEmail.password" type="password"></Input>
          </FormItem>
          <FormItem label="Old Email">
            <Input type="text" v-model="formEmail.old_email" disabled></Input>
          </FormItem>
          <FormItem label="New Email" prop="new_email">
            <Input type="text" v-model="formEmail.new_email"></Input>
          </FormItem>
          <FormItem v-if="visible.tfaRequired" label="Two Factor Auth" prop="tfa_code">
            <Input type="text" v-model="formEmail.tfa_code"></Input>
          </FormItem>
          <Button type="primary" @click="changeEmail">{{$t('m.ChangeEmail')}}</Button>
        </Form>
      </div>
    </div>
    
    <div class="setting-delete">
      <div class="left">
        <p class="section-title">{{$t('m.Delete_Account')}}</p>
        <Form class="setting-content" ref="formDelete" :model="formDelete" :rules="ruleDelete">
          <FormItem label="Current Username" prop="username">
            <Input v-model="formDelete.username" type="text"></Input>
          </FormItem>
          <FormItem label="Current Password" prop="password">
            <Input v-model="formDelete.password" type="password"></Input>
          </FormItem>

          <FormItem label="Captcha" prop="captcha" style="margin-bottom:30px">
            <div class="oj-captcha">
              <div class="oj-captcha-code">
                <Input type="text" v-model="formDelete.captcha" size="large" @on-enter="deleteAccount"></Input>
              </div>
              <div class="oj-captcha-img">
                <Tooltip content="Click to refresh" placement="top">
                  <img :src="captchaSrc" @click="getCaptchaSrc"/>
                </Tooltip>
              </div>
            </div>
          </FormItem>
          <FormItem v-if="visible.tfaRequired" label="Two Factor Auth" prop="tfa_code">
            <Input type="text" v-model="formDelete.tfa_code"/>
          </FormItem>
          <FormItem v-if="visible.accountDelete">
            <Alert type="success">You will logout after 5 seconds..</Alert>
          </FormItem>
          <Button type="primary" @click="deleteAccount">{{$t('m.Delete_Account')}}</Button>
        </Form>
      </div>
    </div>
  </div>
</template>

<script>
  import api from '@oj/api'
  import { FormMixin } from '@oj/components/mixins'

  export default {
    mixins: [FormMixin],
    data () {
      const oldPasswordCheck = [{required: true, trigger: 'blur', min: 6, max: 20}]
      const tfaCheck = [{required: true, trigger: 'change'}]
      const CheckAgainPassword = (rule, value, callback) => {
        if (value !== this.formPassword.new_password) {
          callback(new Error('password does not match'))
        }
        callback()
      }
      const CheckNewPassword = (rule, value, callback) => {
        if (this.formPassword.old_password !== '') {
          if (this.formPassword.old_password === this.formPassword.new_password) {
            callback(new Error('The new password doesn\'t change'))
          } else {
            // 对第二个密码框再次验证
            this.$refs.formPassword.validateField('again_password')
          }
        }
        callback()
      }
      return {
        loading: {
          btnPassword: false,
          btnEmail: false
        },
        visible: {
          passwordAlert: false,
          emailAlert: false,
          tfaRequired: false,
          accountDelete: false
        },
        formPassword: {
          tfa_code: '',
          old_password: '',
          new_password: '',
          again_password: ''
        },
        formEmail: {
          tfa_code: '',
          password: '',
          old_email: '',
          new_email: ''
        },
        formDelete: {
          username: '',
          tfa_code: '',
          password: '',
          captcha: ''
        },
        rulePassword: {
          old_password: oldPasswordCheck,
          new_password: [
            {required: true, trigger: 'blur', min: 6, max: 20},
            {validator: CheckNewPassword, trigger: 'blur'}
          ],
          again_password: [
            {required: true, validator: CheckAgainPassword, trigger: 'change'}
          ],
          tfa_code: tfaCheck
        },
        ruleEmail: {
          password: oldPasswordCheck,
          new_email: [{required: true, type: 'email', trigger: 'change'}],
          tfa_code: tfaCheck
        },
        ruleDelete: {
          username: [
            {required: true, trigger: 'blur'}
          ],
          password: oldPasswordCheck,
          captcha: [
            {required: true, trigger: 'blur', min: 1, max: 10}
          ],
          tfa_code: tfaCheck
        }
      }
    },
    mounted () {
      this.formEmail.old_email = this.$store.getters.user.email || ''
      this.getCaptchaSrc()
    },
    methods: {
      changePassword () {
        this.validateForm('formPassword').then(valid => {
          this.loading.btnPassword = true
          let data = Object.assign({}, this.formPassword)
          delete data.again_password
          if (!this.visible.tfaRequired) {
            delete data.tfa_code
          }
          api.changePassword(data).then(res => {
            this.loading.btnPassword = false
            this.visible.passwordAlert = true
            this.$success('Update password successfully')
            setTimeout(() => {
              this.visible.passwordAlert = false
              this.$router.push({name: 'logout'})
            }, 5000)
          }, res => {
            if (res.data.data === 'tfa_required') {
              this.visible.tfaRequired = true
            }
            this.loading.btnPassword = false
          })
        })
      },
      changeEmail () {
        this.validateForm('formEmail').then(valid => {
          this.loading.btnEmail = true
          let data = Object.assign({}, this.formEmail)
          if (!this.visible.tfaRequired) {
            delete data.tfa_code
          }
          api.changeEmail(data).then(res => {
            this.loading.btnEmail = false
            this.visible.emailAlert = true
            this.$success('Change email successfully')
            this.$refs.formEmail.resetFields()
          }, res => {
            if (res.data.data === 'tfa_required') {
              this.visible.tfaRequired = true
            }
          })
        })
      },
      deleteAccount () {
        this.validateForm('formDelete').then(valid => {
          this.loading.btnPassword = true
          let data = Object.assign({}, this.formDelete)
          if (!this.visible.tfaRequired) {
            delete data.tfa_code
          }
          api.deleteAccount(data).then(res => {
            this.loading.btnPassword = false
            this.visible.accountDelete = true
            this.$success('Delete Account successfully')
            this.$refs.formDelete.resetFields()
            setTimeout(() => {
              this.visible.accountDelete = false
              this.$router.push({name: 'delete-account'})
              this.$router.push({name: 'logout'})
            }, 5000)
          }, res => {
            if (res.data.data === 'tfa_required') {
              this.visible.tfaRequired = true
            }
          })
        })
      }
    }
  }
</script>

<style lang="less" scoped>

  .flex-container {
    justify-content: flex-start;
    .left {
      flex: 1 0;
      width: 250px;
      padding-right: 5%;
    }
    > .middle {
      flex: none;
    }
    .right {
      flex: 1 0;
      width: 250px;
    }
    .setting-delete {
      width: 470px;
      margin-top: 50px;
    }
  }
</style>
