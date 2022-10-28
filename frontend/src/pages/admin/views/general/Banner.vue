<template>
  <div class="announcement view">
    <Panel title="배너 관리">
      <div class="switch">
        <span>사용중인 배너만 보기</span>
        <el-switch v-model="showOnlyUsingBanner"
                   active-color="#2d7ec9"
                   inactive-color="#ff4949">
        </el-switch>
      </div>
      <div class="list">
        <transition-group name="fade" mode="out-in">
          <el-table
            v-if="!showOnlyUsingBanner"
            key="all"
            v-loading="loading"
            element-loading-text="loading"
            ref="table"
            :data="BannerList"
            style="width: 100%">
            <el-table-column
              width="100"
              prop="id"
              label="ID">
            </el-table-column>
            <el-table-column
              prop="title"
              label="Title">
              <template slot-scope="scope">
                <el-button type="text" @click.native="openShowUpImageDialog(scope.row.banner)">
                  {{scope.row.title}}
                </el-button>
              </template>
            </el-table-column>
            <el-table-column
              width="300"
              prop="create_time"
              label="create_time">
              <template slot-scope="scope">
                {{scope.row.create_time | localtime }}
              </template>
            </el-table-column>
            <el-table-column
              width="100"
              prop="isUse"
              label="isUse">
              <template slot-scope="scope">
                <el-checkbox v-model="scope.row.isUse" :checked="scope.row.isUse" @change="bannerActive(scope.row.id, scope.row.isUse)">
                </el-checkbox>
              </template>
            </el-table-column>
            <el-table-column
              width="100"
              label="Delete">
              <template slot-scope="scope">
                <icon-btn name="삭제" size="large" icon="trash" @click.native="showRemoveDialogWindow(scope.row.id)"></icon-btn>
              </template>
            </el-table-column>
          </el-table>

          <el-table
            v-else
            key="notall"
            v-loading="loading"
            element-loading-text="loading"
            ref="table"
            :data="usingBannerList"
            style="width: 100%">
            <el-table-column
              width="100"
              prop="id"
              label="ID">
            </el-table-column>
            <el-table-column
              prop="title"
              label="Title">
            </el-table-column>
            <el-table-column
              width="300"
              prop="create_time"
              label="create_time">
              <template slot-scope="scope">
                {{scope.row.create_time | localtime }}
              </template>
            </el-table-column>
            <el-table-column
              width="100"
              prop="isUse"
              label="isUse">
              <template slot-scope="scope">
                <el-checkbox v-model="scope.row.isUse" :checked="scope.row.isUse" @change="bannerActive(scope.row.id, scope.row.isUse)">
                </el-checkbox>
              </template>
            </el-table-column>
            <el-table-column
              width="100"
              label="Delete">
              <template slot-scope="scope">
                <icon-btn name="삭제" size="large" icon="trash" @click.native="showRemoveDialogWindow(scope.row.id)"></icon-btn>
              </template>
            </el-table-column>
          </el-table>
        </transition-group>
        <div class="panel-options">
          <el-button type="primary" size="small" @click="openAnnouncementDialog(null)" icon="el-icon-plus">Create</el-button>
        </div>
      </div>
    </Panel>

    <el-dialog :title="DialogTitle" :visible.sync="showDialog"
               @open="onOpenEditDialog" :close-on-click-modal="false">
      <el-form label-position="top">
        <el-form-item label="배너 이미지 추가 (5MB이하 18:9~2.39:1 사이 권장 *표준:21:9)" required>
          <el-input
            v-model="banner.title"
            placeholder="배너 이미지 제목" class="title-input" required>
          </el-input>
        </el-form-item>
        <div class="img-container">
          <el-form-item v-if="banner.image" label="preview" required>
            <img :src="banner.image" alt=""/>
          </el-form-item>
        </div>
        <input @change="handleSelectFile" ref="bannerImg" :label="$t('m.Announcement_Content')" type="file" accept="image/*" required>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <cancel @click.native="closedShowDialog"></cancel>
        <el-button type="primary" @click.native="submitBanner">업로드</el-button>
      </span>
    </el-dialog>
    <el-dialog title="주의" :visible.sync="showRemoveDialog" width="300px" class="dialog"
               @open="onOpenEditDialog" :close-on-click-modal="false" center>
      <span class="dial-mo">이미지를 삭제하시겠습니까?</span>
      <span slot="footer" class="dialog-footer">
        <cancel @click.native="closedRemoveDialog"></cancel>
        <el-button type="danger" @click.native="removeBanner">삭제</el-button>
      </span>
    </el-dialog>
    <el-dialog class="img-container" :visible.sync="showUpImageDialog"
               @open="onOpenEditDialog" :close-on-click-modal="false" :before-close="closeShowUpImageDialog">
      <div class="img-container">
        <img :src="cacheShowBannerSrc" alt=""/>
      </div>
    </el-dialog>
  </div>
</template>

<script>
  import api from '../../api.js'

  export default {
    name: 'Banner',
    data () {
      return {
        showOnlyUsingBanner: false,
        usingBannerList: [],
        BannerList: [],
        // 공지사항 편집 대화상자 표시
        showDialog: false,
        showRemoveDialog: false,
        showUpImageDialog: false,
        mode: 'create',
        // 다이얼로그 제목
        DialogTitle: '공지사항 수정',
        // (new | edit) model
        banner: {
          title: '',
          image: ''
        },
        announcement: {
          title: '',
          visible: true,
          content: ''
        },
        loading: true,
        cacheRemoveBannerId: '',
        cacheShowBannerSrc: ''
      }
    },
    mounted () {
      this.init()
    },
    methods: {
      init () {
        this.loading = true
        api.getBannerList().then(res => {
          this.BannerList = res.data.data
          let usingList = []
          for (let item of res.data.data) {
            if (item.isUse) {
              usingList.push(item)
            }
          }
          this.usingBannerList = usingList
          this.loading = false
        }, () => {
          this.loading = false
        })
      },
      showRemoveDialogWindow (id) {
        this.cacheRemoveBannerId = id
        this.showRemoveDialog = true
      },
      closedRemoveDialog () {
        this.cacheRemoveBannerId = ''
        this.showRemoveDialog = false
      },
      openShowUpImageDialog (src) {
        this.cacheShowBannerSrc = src
        this.showUpImageDialog = true
      },
      closeShowUpImageDialog () {
        this.cacheShowBannerSrc = ''
        this.showUpImageDialog = false
      },
      preView () {
        return this.cacheShowBannerSrc
      },
      removeBanner () {
        let id = this.cacheRemoveBannerId
        api.deleteBanner(id).then(res => {
          this.closedRemoveDialog()
          this.$success('삭제가 완료되었습니다')
          this.init()
        }, re => {
          this.closedRemoveDialog()
          this.$success('삭제에 실패하였습니다')
        })
      },
      bannerActive (ids, active) {
        let temp = {
          id: ids,
          enable: active
        }
        let formData = Object.assign({}, temp)
        api.activeBanner(formData).then(res => {
          this.$success('업데이트가 완료되었습니다')
          this.init()
        }, _ => {
          this.$success('업데이트에 실패하였습니다')
        })
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
      handleSelectFile (load) {
        let file = load.target.files[0]
        let isOk = this.checkFileType(file) && this.checkFileSize(file)
        if (!isOk) {
          return false
        }
        let reader = new window.FileReader()
        reader.onload = (e) => {
          this.banner.image = e.target.result
        }
        reader.readAsDataURL(file)
        return false
      },
      checkFileSize (file) {
        // max size is QHD+ (5.5MB)
        if (file.size > 2 * 3200 * 2000 + 100) {
          this.$Notice.warning({
            title: 'Exceed max size limit',
            desc: 'File ' + file.name + ' is too big, you can upload a image up to 5MB in size'
          })
          return false
        }
        return true
      },
      submitBanner () {
        let form = new window.FormData()
        form.append('image', this.$refs.bannerImg.files[0])
        form.append('title', this.banner.title)
        form.append('url', 'http://localhost/banner')
        this.$http({
          method: 'post',
          url: 'admin/input_banner',
          data: form,
          headers: {'content-type': 'multipart/form-data'}
        }).then(res => {
          this.closedShowDialog()
          this.$success('배너 업로드에 성공하였습니다')
          this.init()
        }, () => {
          this.closedShowDialog()
          this.$error('배너 업로드에 실패하였습니다.')
        })
      },
      closedShowDialog () {
        this.showDialog = false
        this.banner.title = ''
        this.banner.imgae = ''
      },
      // 페이지 번호 콜백 전환
      currentChange (page) {
        this.currentPage = page
        this.getAnnouncementList(page)
      },
      getAnnouncementList (page) {
        this.loading = true
        api.getAnnouncementList((page - 1) * this.pageSize, this.pageSize).then(res => {
          this.loading = false
          this.total = res.data.data.total
          this.announcementList = res.data.data.results
        }, res => {
          this.loading = false
        })
      },
      getContestAnnouncementList () {
        this.loading = true
        api.getContestAnnouncementList(this.contestID).then(res => {
          this.loading = false
          this.announcementList = res.data.data
        }).catch(() => {
          this.loading = false
        })
      },
      // 편집 대화 상자 열기에 대한 콜백
      onOpenEditDialog () {
        // 일시적인 텍스트 편집기 표시 비정상 버그 해결
        setTimeout(() => {
          if (document.createEvent) {
            let event = document.createEvent('HTMLEvents')
            event.initEvent('resize', true, true)
            window.dispatchEvent(event)
          } else if (document.createEventObject) {
            window.fireEvent('onresize')
          }
        }, 0)
      },
      // 수정사항 제출
      // 기본 Mouse Event
      submitAnnouncement (data = undefined) {
        let funcName = ''
        if (!data.title) {
          data = {
            id: this.currentAnnouncementId,
            title: this.announcement.title,
            content: this.announcement.content,
            visible: this.announcement.visible
          }
        }
        if (this.contestID) {
          data.contest_id = this.contestID
          funcName = this.mode === 'edit' ? 'updateContestAnnouncement' : 'createContestAnnouncement'
        } else {
          funcName = this.mode === 'edit' ? 'updateAnnouncement' : 'createAnnouncement'
        }
        api[funcName](data).then(res => {
          this.showDialog = false
          this.init()
        }).catch()
      },
      // 공지사항 삭제
      deleteAnnouncement (announcementId) {
        this.$confirm('Are you sure you want to delete this announcement?', 'Warning', {
          confirmButtonText: 'Delete',
          cancelButtonText: 'Cancel',
          type: 'warning'
        }).then(() => {
          this.loading = true
          let funcName = this.contestID ? 'deleteContestAnnouncement' : 'deleteAnnouncement'
          api[funcName](announcementId).then(res => {
            this.loading = true
            this.init()
          })
        }).catch(() => {
          this.loading = false
        })
      },
      openAnnouncementDialog (id) {
        this.showDialog = true
        this.DialogTitle = '배너 생성'
        this.banner.title = ''
        this.banner.imgae = ''
        this.mode = 'create'
      },
      handleVisibleSwitch (row) {
        this.mode = 'edit'
        this.submitAnnouncement({
          id: row.id,
          title: row.title,
          content: row.content,
          visible: row.visible
        })
      }
    },
    watch: {
      $route () {
        this.init()
      }
    }
  }
</script>

<style lang="less" scoped>
  .title-input {
    margin-bottom: 20px;
  }
  .img-container {
    img {
      width: 100%;
      object-fit: cover;
      border: 1px solid rgb(163, 163, 163);
      border-radius: 5px;
    }
    margin-bottom: 10px;
  }
  .visible-box {
    margin-top: 10px;
    width: 205px;
    float: left;
  }
  .switch {
    float: right;
    margin-top: 7px;
    margin-bottom: 7px;
    margin-right: 5px;
    span {
      margin-right: 5px;
      color: #858585
    }
  }
  .fade-enter-to {
    transition: opacity 0s;
  }
  .fade-leave-active {
    animation: 0;
  }
</style>
<style lang="less">
  .dialog {
    & .el-dialog__title {
      color : rgb(255, 56, 7);
      font-weight: bold;
    }
    & .el-dialog__body {
      text-align: center;
      color: rgb(40, 40, 40);
      & .dial-mo {
        text-align: center;
      }
    }
  }
</style>