<template>
  <div class="view">
    <Panel id="tt">
      <div slot="title">
        <i class="mdi mdi-chevron-left back-btn" @click="backPage"></i>
        {{title}}
      </div>
      <div slot="header">
        <div class="header-time">
          관리자 : {{writer.username}}
        </div>
        <div class="header-time">
          마지막 수정 날짜 : {{lastUpdateTime | localtime}}
        </div>
        <div class="header-time">
          생성 날짜 : {{createTime | localtime}}
        </div>
      </div>
      <el-row :gutter="20" class="content-title">
        <el-col :span="16">{{content}}</el-col>
      </el-row>
      <el-row v-show="!editorVisible" class="editor-container">
        <i class="mdi mdi-square-edit-outline edit-btn" @click="viewEditor">
          <span>이메일 편집기 열기</span>
          <span v-show="!isFirstOpen">
            <i v-show="(!isEidit)" class="mdi mdi-checkbox-marked-circle-outline is-save-icn" style="font-size: 14px;"><span>저장 됨</span></i>
            <i v-show="isEidit" class="mdi mdi-alert-circle-check-outline is-edit-icn" style="font-size: 14px;"><span>수정 중</span></i>
          </span>
        </i>
      </el-row>
      <el-row v-show="editorVisible" class="editor-container">
        <i class="mdi mdi-square-edit-outline edit-btn" @click="closeEditor">
          <span>이메일 편집기 닫기</span>
        </i>
      </el-row>
      <el-row v-show="editorVisible" class="editor-container">
        <el-divider class="editor-hor" content-position="left">이메일 편집</el-divider>
        <el-col style="width: 60%;">
          <div style="margin-left:10px; color:gray;">* 제목</div>
          <el-input v-model="sendMailForm.title" placeholder="메일 제목" required></el-input>
        </el-col>
      </el-row>
      <el-row v-show="editorVisible" :gutter="20">
        <div style="margin-left:20px; margin-bottom:4px; color:gray;">
          * 내용 (편집 후 반드시 저장 버튼을 누르세요)
          <i v-show="!isEidit" class="mdi mdi-checkbox-marked-circle-outline is-save-icn"><span>저장 됨</span></i>
          <i v-show="isEidit" class="mdi mdi-alert-circle-check-outline is-edit-icn"><span>수정 중</span></i>
        </div>
        <el-col style="width: 48%;"><mavon-editor v-model="textContent" defaultOpen="edit" :language="`en`" :ishljs="ishljs" @change="changes" @save="save" :toolbars="toolbars"/></el-col>
        <el-col style="width: 48%;" class="ex-box"><div v-html.lazy="convertTextContent" ref="divHTML" id="divHTML" class="text-example"></div></el-col>
      </el-row>
      <el-row :gutter="20" class="content-title">
        <el-button v-show="selectedUsers.length"
                   class="email-btn"
                   type="primary" icon="el-icon-s-promotion"
                   @click="sendMail"
                   >이메일 보내기
        </el-button>
        <el-button v-show="selectedUsers.length === 0"
                   class="email-btn"
                   type="primary" icon="el-icon-s-promotion"
                   disabled>이메일 보내기
        </el-button>
      </el-row>
      
      <el-divider class="user-list-title" content-position="left">관리 목록</el-divider>
      <el-table
        ref="table"
        v-loading="loadingTable"
        element-loading-text="loading"
        @selection-change="handleSelectionChange"
        :data="userlist"
        style="width: 100%">
        <el-table-column type="selection" width="55"></el-table-column>

        <el-table-column prop="username" label="사용자 이름"></el-table-column>

        <el-table-column prop="email" label="이메일"></el-table-column>

        <el-table-column prop="last_activity" label="마지막 활동">
          <template slot-scope="scope">
            {{scope.row.last_activity | localtime }}
          </template>
        </el-table-column>

        <el-table-column prop="create_time" label="생성일자">
          <template slot-scope="scope">
            {{scope.row.create_time | localtime }}
          </template>
        </el-table-column>
      </el-table>
    </Panel>
  </div>
</template>
<script>
  import api from '../../api.js'

  export default {
    name: 'ManagedUserDetail',
    data () {
      return {
        isFirstOpen: true,
        content: '',
        manageID: '',
        userlist: [],
        writer: '',
        title: '',
        textContent: '',
        convertTextContent: '',
        createTime: '',
        lastUpdateTime: '',
        loadingTable: false,
        selectedUsers: [],
        ishljs: false,
        editorVisible: false,
        isEidit: true,
        sendMailForm: {
          title: '',
          content: '',
          user_ids: []
        },
        toolbars: {
          bold: true,
          italic: true,
          header: true,
          underline: true,
          strikethrough: true,
          mark: true,
          superscript: true,
          subscript: true,
          quote: false,
          ol: true,
          ul: true,
          link: true,
          imagelink: false,
          code: false,
          table: false,
          fullscreen: false,
          readmodel: false,
          htmlcode: false,
          help: false,
          /* 1.3.5 */
          undo: true,
          redo: true,
          trash: true,
          save: true,
          /* 1.4.2 */
          navigation: false,
          /* 2.1.8 */
          alignleft: false,
          aligncenter: false,
          alignright: false,
          /* 2.2.1 */
          subfield: false,
          preview: false
        },
        defaultPresetPre: `<div>
                          <table cellpadding="0" align="center"
                                 style="overflow:hidden;background:#fff;margin:0 auto;text-align:left;position:relative;font-size:14px; font-family:'lucida Grande',Verdana;line-height:1.5;box-shadow:0 0 3px #ccc;border:1px solid #ccc;border-radius:5px;border-collapse:collapse;">
                              <tbody>
                              <tr>
                                  <th valign="middle"
                                      style="height:38px;color:#fff; font-size:14px;line-height:38px; font-weight:bold;text-align:left;padding:10px 24px 6px; border-bottom:1px solid #5030e5;background:#5030e5;border-radius:5px 5px 0 0;"> COU </th>
                              </tr>
                              <tr>
                                  <td style="padding: 20px; white-space:pre">`,
        defaultPresetLast: `
                                  </td>
                              </tr>
                              </tbody>
                          </table>
                      </div>`
      }
    },
    mounted () {
      this.init()
    },
    methods: {
      init () {
        this.manageID = this.$route.params.manageId
        this.loadingTable = true
        api.getManagedUserList(this.manageID).then(res => {
          let data = res.data.data
          this.title = data.title
          this.content = data.content
          this.writer = data.writer
          this.userlist = data.users
          this.createTime = data.create_time
          this.lastUpdateTime = data.last_update_time
          this.loadingTable = false
        })
        this.loadingTable = false
      },
      handleSelectionChange (val) {
        console.log(val)
        this.selectedUsers = val
      },
      backPage () {
        this.$router.push({name: 'manage-user-list'})
      },
      changes (status, value) {
        this.isEidit = true
        value = value.replaceAll('<br />', '<br style="display:none;"/>')
        this.convertTextContent = this.defaultPresetPre + value + this.defaultPresetLast
      },
      save (status, value) {
        if (!this.sendMailForm.title.length) {
          this.$error('이메일 제목이 입력되지 않았습니다')
          return
        }
        if (!value.length) {
          this.$error('이메일 내용이 입력되지 않았습니다')
          return
        }
        let li = value.split('\n')
        let inlineContent = ''
        for (let v of li) {
          inlineContent = inlineContent + v
        }
        this.sendMailForm.content = inlineContent
        this.isEidit = false
        this.$success('저장되었습니다')
      },
      sendMail () {
        if (this.isEidit) {
          this.$error('이메일이 아직 수정중입니다')
          return
        }
        if (!this.sendMailForm.title.length) {
          this.$error('이메일 제목이 입력되지 않았습니다')
          return
        }
        if (!this.sendMailForm.content.length) {
          this.$error('이메일 내용이 입력되지 않았습니다')
          return
        }
        for (let user of this.selectedUsers) {
          this.sendMailForm.user_ids.push(user.id)
        }
        console.log(this.sendMailForm)
        let data = Object.assign({}, this.sendMailForm)
      },
      viewEditor () {
        this.editorVisible = true
        this.isFirstOpen = false
      },
      closeEditor () {
        this.editorVisible = false
      }
    },
    watch: {
      'sendMailForm.title' () {
        this.isEidit = true
      }
    }
  }
</script>
<style scoped lang="less">
@import '../../../../styles/common.less';
.text-example {
  font-family: 'Manrope';
  ::v-deep p {
      display: block !important;
      margin-block-start: 1em !important;
      margin-block-end: 1em !important;
      margin-inline-start: 0px !important;
      margin-inline-end: 0px !important;
  }
  ::v-deep br {
    height: 0 !important;
    display: none !important;
  }
}
::v-deep .text-example p {
      display: block !important;
      margin-block-start: 1em !important;
      margin-block-end: 1em !important;
      margin-inline-start: 0px !important;
      margin-inline-end: 0px !important;
}
::v-deep .text-example br {
    height: 0 !important;
    display: none !important;
 }
.editor-container {
  margin-bottom: 20px;
}
.editor-hor {
  margin-bottom: 40px;
}
.content-title {
  font-size: 20px;
  color: #7b7b7b;
  margin-top: 10px;
  margin-bottom: 25px;
}
.user-list-title {
  margin-top: 40px;
}
.header-time {
  color: #9b9b9b;
  font-size : 12px;
}
.back-btn {
  font-size: 24px;
  cursor: pointer;
  transition: all 0.2s ease-in;
  &:hover {
    color: @dark-orange;
  }
}
.edit-btn {
  font-size: 24px;
  cursor: pointer;
  transition: all 0.2s ease-in;
  font-style: normal;
  &:hover {
    color: @dark-orange;
  }
  span {
    font-size: 14px;
    margin-left: 4px;
  }
}
.ex-box {
  overflow: auto;
  box-shadow: 0 0 5px 0px rgb(194, 194, 194);
  padding: 0 !important;
}
.email-btn {
  margin-top: 10px;
  margin-left: 10px;
}
.is-save-icn {
  margin-left: 20px;
  font-style: normal;
  color: green;
  span {
    color:#7b7b7b;
  }
}
.is-edit-icn {
  margin-left: 20px;
  font-style: normal;
  color: orange;
  span {
    color:#7b7b7b;
  }
}
</style>
<style lang="less">
#tt {
  header {
    .title {
      font-size: 24px;
      font-weight: 400;
      color: #707070;
    }
  }
}
.text-example {
  font-family: 'Manrope';
  ::v-deep p {
      display: block !important;
      margin-block-start: 1em !important;
      margin-block-end: 1em !important;
      margin-inline-start: 0px !important;
      margin-inline-end: 0px !important;
  }
  ::v-deep br {
    height: 0 !important;
    display: none !important;
  }
}
::v-deep .text-example p {
      display: block !important;
      margin-block-start: 1em !important;
      margin-block-end: 1em !important;
      margin-inline-start: 0px !important;
      margin-inline-end: 0px !important;
}
::v-deep .text-example br {
    height: 0 !important;
    display: none !important;
 }
</style>