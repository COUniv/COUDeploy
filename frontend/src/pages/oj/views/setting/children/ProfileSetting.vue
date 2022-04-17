<template>
  <div class="mypage">
    <div class="section-title">{{$t('m.Profile_Setting')}}</div>  
      <Form ref="formProfile" :model="formProfile">        

        <div class="mypage_main">
          <div class="mypage_img" >
            
            <template class="container_img" v-if="!avatarOption.imgSrc">
              <Upload type="drag"
                      class="container_img"
                      accept=".jpg,.jpeg,.png,.bmp,.gif"
                      action=""
                      :before-upload="handleSelectFile">
                <div style="padding: 30px 0">
                  <Icon type="ios-cloud-upload" size="52" style="color: #3399ff"></Icon>
                  <p>마우스로 파일을 끌어오거나 클릭하세요</p>
                </div>
              </Upload>
            </template>
        
            <template v-else>
              <div class="flex-container">
                <div class="cropper-main inline">
                  <vueCropper
                    ref="cropper"
                    autoCrop
                    fixed
                    :autoCropWidth="200"
                    :autoCropHeight="200"
                    :img="avatarOption.imgSrc"
                    :outputSize="avatarOption.size"
                    :outputType="avatarOption.outputType"
                    :info="true"
                    @realTime="realTime">
                  </vueCropper>
                </div>
                <ButtonGroup vertical class="cropper-btn">
                  <Button @click="rotate('left')">
                    <Icon type="md-return-right" size="20"></Icon>
                  </Button>
                  <Button @click="rotate('right')">
                    <Icon type="md-return-left" size="20"></Icon>
                  </Button>
                  <Button @click="reselect">
                    <Icon type="md-refresh" size="20"></Icon>
                  </Button>
                  <Button @click="finishCrop">
                    <Icon type="md-checkmark-circle-outline" size="20">
                  </Button>
                </ButtonGroup>
                <div class="cropper-preview" :style="previewStyle">
                  <div :style=" preview.div">
                    <img :src="avatarOption.imgSrc" :style="preview.img">
                  </div>
                </div>
              </div>
            </template>
            <Modal v-model="uploadModalVisible"
                  title="프로필 업러드">
              <div class="upload-modal">
                <p class="notice">프로필 사진이 다음과 같이 보여지게 됩니다</p>
                <img :src="uploadImgSrc"/>
              </div>
              <div slot="footer">
                <Button @click="uploadAvatar" :loading="loadingUploadBtn">업로드</Button>
              </div>
            </Modal>

          </div>

          <div class="mypage_info">
            <FormItem class="mypage_info_input" label="이름"> 
              <!-- <Input v-model="formProfile.real_name"/> -->
            </FormItem>
            <Form-item class="mypage_info_input" label="학과">
              <!-- <Input v-model="formProfile.major"/> -->
            </Form-item>
            <Form-item class="mypage_info_input" label="회원분류">
              <!-- <Input v-model="formProfile.classification"/> -->
            </Form-item>
            <Form-item class="mypage_info_input" label="이메일">
              <!-- <Input v-model="formProfile.email"/> -->
            </Form-item>
            <!-- <Form-item class="mypage_info_submit">
              <Button type="primary" @click="updateProfile" :loading="loadingSaveBtn">수정하기</Button>
            </Form-item> -->
          </div>
        </div>
      </Form>
  </div>
</template>

<script>
  import { mapGetters } from 'vuex'
  import api from '@oj/api'
  import utils from '@/utils/utils'
  import {VueCropper} from 'vue-cropper'
  import {types} from '@/store'
  import {languages} from '@/i18n'

  export default {
    components: {
      VueCropper
    },
    data () {
      return {
        loadingSaveBtn: false,
        loadingUploadBtn: false,
        uploadModalVisible: false,
        preview: {},
        uploadImgSrc: '',
        avatarOption: {
          imgSrc: '',
          size: 0.8,
          outputType: 'png'
        },
        languages: languages,
        formProfile: {
          real_name: '',
          mood: '',
          major: '',
          classification: '',
          email: '',
          blog: '',
          school: '',
          github: '',
          language: ''
        }
      }
    },
    mounted () {
      let profile = this.$store.state.user.profile
      Object.keys(this.formProfile).forEach(element => {
        if (profile[element] !== undefined) {
          this.formProfile[element] = profile[element]
        }
      })
    },
    methods: {
      checkFileType (file) {
        if (!/\.(gif|jpg|jpeg|png|bmp|GIF|JPG|PNG)$/.test(file.name)) {
          this.$Notice.warning({
            title: 'File type not support',
            desc: 'The format of ' + file.name + ' is incorrect ，please choose image only.'
          })
          return false
        }
        return true
      },
      checkFileSize (file) {
        // max size is 2MB
        if (file.size > 2 * 1024 * 1024) {
          this.$Notice.warning({
            title: 'Exceed max size limit',
            desc: 'File ' + file.name + ' is too big, you can upload a image up to 2MB in size'
          })
          return false
        }
        return true
      },
      handleSelectFile (file) {
        let isOk = this.checkFileType(file) && this.checkFileSize(file)
        if (!isOk) {
          return false
        }
        let reader = new window.FileReader()
        reader.onload = (e) => {
          this.avatarOption.imgSrc = e.target.result
        }
        reader.readAsDataURL(file)
        return false
      },
      realTime (data) {
        this.preview = data
      },
      rotate (direction) {
        if (direction === 'left') {
          this.$refs.cropper.rotateLeft()
        } else {
          this.$refs.cropper.rotateRight()
        }
      },
      reselect () {
        this.$Modal.confirm({
          content: '변경사항을 취소하시겠습니까?',
          onOk: () => {
            this.avatarOption.imgSrc = ''
          }
        })
      },
      finishCrop () {
        this.$refs.cropper.getCropData(data => {
          this.uploadImgSrc = data
          this.uploadModalVisible = true
        })
      },
      uploadAvatar () {
        this.$refs.cropper.getCropBlob(blob => {
          let form = new window.FormData()
          let file = new window.File([blob], 'avatar.' + this.avatarOption.outputType)
          form.append('image', file)
          this.loadingUploadBtn = true
          this.$http({
            method: 'post',
            url: 'upload_avatar',
            data: form,
            headers: {'content-type': 'multipart/form-data'}
          }).then(res => {
            this.loadingUploadBtn = false
            this.$success('새 프로필 업로드에 성공하였습니다')
            this.uploadModalVisible = false
            this.avatarOption.imgSrc = ''
            this.$store.dispatch('getProfile')
          }, () => {
            this.loadingUploadBtn = false
          })
        })
      },
      updateProfile () {
        this.loadingSaveBtn = true
        let updateData = utils.filterEmptyValue(Object.assign({}, this.formProfile))
        api.updateProfile(updateData).then(res => {
          this.$success('Success')
          this.$store.commit(types.CHANGE_PROFILE, {profile: res.data.data})
          this.loadingSaveBtn = false
        }, _ => {
          this.loadingSaveBtn = false
        })
      }
    },
    computed: {
      ...mapGetters(['website', 'modalStatus', 'user']),

      previewStyle () {
        return {
          'width': this.preview.w + 'px',
          'height': this.preview.h + 'px',
          'overflow': 'hidden'
        }
      }
    }
  }
</script>

<style lang="less" scoped>
  .inline {
    display: inline-block;
  }

  .copper-img {
    width: 400px;
    height: 300px;
  }

  .flex-container {
    flex-wrap: wrap;
    justify-content: flex-start;
    margin-bottom: 10px;
    .cropper-main {
      flex: none;
      .copper-img;
    }
    .cropper-btn {
      flex: none;
      vertical-align: top;
    }
    .cropper-preview {
      flex: none;
      /*margin: 10px;*/
      margin-left: 20px;
      box-shadow: 0 0 1px 0;
      .copper-img;
    }
  }

  .upload-modal {
    .notice {
      font-size: 16px;
      display: inline-block;
      vertical-align: top;
      padding: 10px;
      padding-right: 15px;
    }
    img {
      box-shadow: 0 0 1px 0;
      border-radius: 50%;
    }
  }



  .mypage{
    margin: 1% 2% 2% 3%;
  }

  .section-title{
    font-size: 28px;
    // background-color: magenta;
  }

  .mypage_main{
    margin-top: 2%;
    // background-color: aqua;

  }

  .mypage_img{
    // display: inline-block;
    // vertical-align: top;
    margin: 1% 0 0 5%;
    width: 300px;

  }

  .container_img{
    width: 300px;
    height: auto;
  }

  .mypage_info{
    margin: 5% 0 5% 5%;
    // padding-left: 200px;
    // display: inline-block;
    // vertical-align: top;
    width: 400px;
  }

  .mypage_info_submit{
    display: flex;
    justify-content: right;

  }


</style>
