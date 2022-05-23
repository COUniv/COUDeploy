<template>
  <div class="view">
    <Panel title="이미지 목록">
      <div slot="header">
        <el-input
          v-model="keyword"
          prefix-icon="el-icon-search"
          placeholder="Keywords">
        </el-input>
      </div>
      <el-table
        v-loading="loading"
        element-loading-text="loading"
        ref="table"
        :data="problemTagList"
        style="width: 100%">
        
        <el-table-column
          width="150"
          prop="id"
          label="ID">
        </el-table-column>
        
        <el-table-column
          prop="title"
          label="파일 명">
          <template slot-scope="{row}">
            <span v-show="!row.isEditing">{{row.name}}</span>
            <el-input v-show="row.isEditing" v-model="row.name">
            </el-input>
          </template>
        </el-table-column>


        <el-table-column
          fixed="right"
          label="수정"
          width="250">
          <div slot-scope="scope">
            <icon-btn name="Edit" icon="edit" @click.native="openImageDialog(scope.row.id)"></icon-btn>
            <icon-btn icon="trash" name="이미지 삭제"
                      @click.native="deleteImage(scope.row.id)"></icon-btn>
          </div>
        </el-table-column>
      </el-table>

      <div class="panel-options">
        <el-button type="primary" size="small"
                   @click="openImageDialog()" icon="el-icon-plus">이미지 추가
        </el-button>

        <el-pagination
          class="page"
          layout="prev, pager, next"
          @current-change="currentChange"
          :page-size="pageSize"
          :total="total">
        </el-pagination>
      </div>
    </Panel>

    <el-dialog width="80%" title="이미지 추가" :visible.sync="showImageDialog" :close-on-click-modal="false">
      <el-form :model="tag" label-width="120px" label-position="left">
        <el-row :gutter="20">
          <el-col :span="12">
            <div class="mypage_img">
              <div class="container_img" v-if="!avatarOption.imgSrc">
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
            </div>
        
            <div v-else>
              <div class="flex-container">
                <div class="cropper-main inline">
                  <vueCropper
                    ref="cropper"
                    autoCrop
                    fixed
                    :autoCropWidth="900"
                    :autoCropHeight="400"
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
            </div>
            <Modal v-model="uploadModalVisible"
                  title="프로필 업로드">
              <div class="upload-modal">
                <p class="notice">프로필 사진이 다음과 같이 보여지게 됩니다</p>
                <img :src="uploadImgSrc"/>
              </div>
              <div slot="footer">
                <Button @click="uploadAvatar" :loading="loadingUploadBtn">업로드</Button>
              </div>
            </Modal>
            </div>
          </el-col>
        </el-row>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <cancel @click.native="showImageDialog = false">취소</cancel>
        <save @click.native="uploadImage()"></save>
      </span>
    </el-dialog>
  </div>
</template>

<script>
  import api from '../../api.js'
  import utils from '@/utils/utils'
  import {mapGetters} from 'vuex'
  import {types} from '@/store'
  import {VueCropper} from 'vue-cropper'
  export default {
    name: 'ImageList',
    components: {
      VueCropper
    },
    data () {
      return {
        showImageDialog: false,
        loadingSaveBtn: false,
        loadingUploadBtn: false,
        uploadModalVisible: false,
        preview: {},
        uploadImgSrc: '',
        avatarOption: {
          imgSrc: '',
          size: 0.8,
          outputType: 'png'
        }
      }
    },
    mounted () {
      this.routeName = this.$route.name
    },
    computed: {
      ...mapGetters(['isSuperAdmin'])
    },
    methods: {
      handleDblclick (row) {
        row.isEditing = true
      },
      // 切换页码回调
      currentChange (page) {
        this.currentPage = page
      },
      openImageDialog () {
        this.showImageDialog = true
      },
      saveImage () {
        console.log('save')
      },
      deleteImage (id) {
        console.log('delete')
      },
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
    watch: {
      '$route' (newVal, oldVal) {
        this.routeName = newVal.name
        this.getProblemCategoryList(this.currentPage)
      },
      'keyword' () {
        this.getProblemCategoryList(this.currentPage)
      }
    }
  }
</script>

<style scoped lang="less">
  .copper-img {
    width: 100%;
    height: 500px;
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
 .mypage_img{
    // display: inline-block;
    // vertical-align: top;
    margin: 1% 0 0 5%;
    width: 100%;

  }

  .container_img{
    width: 100%;
    height: auto;
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

</style>
