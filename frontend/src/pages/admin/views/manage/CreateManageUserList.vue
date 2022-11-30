<template>
  <div>
    <Panel :title="title" v-loading.fullscreen.lock="fullscreenLoading"
      element-loading-text="로딩중..."
      element-loading-spinner="el-icon-loading"
      element-loading-background="rgba(0, 0, 0, 0.7)">
      <el-form ref="form" :model="manageForm" :rules="rules" label-position="top" label-width="70px">
        <el-row :gutter="20">
          <el-col :span="18">
            <el-form-item prop="title" :label="$t('m.Title')" required>
              <el-input :placeholder="$t('m.Title')" v-model="manageForm.title"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item prop="content" :label="`설명`" required>
              <el-input :placeholder="`설명`" v-model="manageForm.content"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <div style="margin-top:20px; margin-bottom:20px;">
          <span>
            유저 추가
          </span>
          <el-autocomplete
            class="input-new-tag"
            popper-class="problem-tag-poper"
            v-model="keyword"
            @keyup.enter.native="addUser"
            @select="addUser"
            :fetch-suggestions="querySearch"
            placeholder="유저 검색">
            <template #default="{item}">
              <div style="float:left" name="아이디">{{ item.username }}</div>
              <div style="float:right; color: #9e9e9e;" name="고유번호">#{{ item.id }}</div>
            </template>
          </el-autocomplete>
          <span style="float:right">
            <el-button icon="Check"
                       type="success"
                       @click="save">
                       저장
            </el-button>
          </span>
        </div>  
      </el-form>

    </Panel>
    <Panel :title="`유저 리스트`">
      <div slot="header">
        <el-row :gutter="20">
          <el-col :span="8">
            <el-button v-show="selectedUsers.length"
                       type="warning" icon="el-icon-fa-trash"
                       @click="deleteUsers(selectedUserIDs)">삭제
            </el-button>
          </el-col>
        </el-row>
      </div>
      <el-table
        v-loading="loadingTable"
        element-loading-text="loading"
        ref="table"
        @selection-change="handleSelectionChange"
        :data="userList"
        style="width: 100%">
        <el-table-column type="selection" width="55"></el-table-column>

        <el-table-column prop="id" label="고유 ID" width="110"></el-table-column>

        <el-table-column prop="username" label="닉네임"></el-table-column>

        <el-table-column prop="create_time" label="생성일자">
          <template slot-scope="scope">
            {{scope.row.create_time | localtime }}
          </template>
        </el-table-column>
        <el-table-column prop="last_login" label="마지막 로그인">
          <template slot-scope="scope">
            {{scope.row.last_login | localtime }}
          </template>
        </el-table-column>
        <el-table-column prop="real_name" label="이름" width="140"></el-table-column>ß
        <el-table-column prop="email" label="이메일"></el-table-column>
        <el-table-column fixed="right" label="옵션" width="100">
          <template slot-scope="{row}">
            <icon-btn name="삭제" icon="trash" @click.native="deleteUsers([row.id])"></icon-btn>
          </template>
        </el-table-column>
      </el-table>
    </Panel>
  </div>
</template>
<script>
  import api from '../../api'
  export default {
    name: 'Problem',
    data () {
      return {
        title: '',
        fullscreenLoading: false,
        rules: {
          title: {required: true, message: '제목을 입력해주세요 (6자 이상 60자 이하)', trigger: 'blur', min: 6, max: 60},
          content: {required: true, message: '설명을 입력해주세요', trigger: 'blur'}
        },
        manageForm: {
          title: '',
          content: '',
          user_ids: []
        },
        selectedUsers: [],
        userList: [],
        keyword: '',
        inputVisible: false,
        loadingTable: false,
        mode: '',
        manageID: ''
      }
    },
    mounted () {
      this.routeName = this.$route.name
      this.fullscreenLoading = true
      if (this.routeName === 'manage-user-edit') { // route명이 리스트 수정인 경우
        this.mode = 'modify' // 리스트 수정
        this.title = '관리 리스트 수정'
        this.init()
      } else {
        this.title = '관리 리스트 생성'
        this.fullscreenLoading = false
      }
    },
    methods: {
      init () {
        this.manageID = this.$route.params.manageId
        this.fullscreenLoading = true
        this.loadingTable = true
        api.getManagedUserList(this.manageID).then(res => {
          let data = res.data.data
          this.manageForm.title = data.title
          this.manageForm.content = data.content
          this.userList = data.users
          this.loadingTable = false
          this.fullscreenLoading = false
        }, _ => {
          this.loadingTable = false
          this.fullscreenLoading = false
        })
      },
      querySearch (queryString, cb) {
        api.getUserList(0, 10, queryString).then(res => {
          let userList = []
          for (let user of res.data.data.results) {
            userList.push(user)
          }
          cb(userList)
        }).catch(() => {
        })
      },
      addUser (item) {
        this.loadingTable = true
        if (this.userList.some(e => e.id === item.id)) {
        } else {
          api.getUser(item.id).then(res => {
            this.userList.push(res.data.data)
            this.inputVisible = false
            this.loadingTable = false
          }, _ => {
            this.inputVisible = false
            this.loadingTable = false
          })
        }
        this.keyword = ''
      },
      handleSelectionChange (val) {
        this.selectedUsers = val
      },
      deleteUsers (ids) {
        this.$confirm('Sure to delete the user? The associated resources created by this user will be deleted as well, like problem, contest, announcement, etc.', 'confirm', {
          type: 'warning'
        }).then(() => {
          for (let v of ids) {
            let idx = this.userList.findIndex(e => e.id === v)
            if (idx > -1) {
              this.userList.splice(idx, 1)
            }
          }
        }, () => {
        })
      },
      save () {
        if (!this.manageForm.title.length) {
          this.$error('제목이 입력되지 않았습니다')
          return
        }
        if (!this.manageForm.content.length) {
          this.$error('설명이 입력되지 않았습니다')
          return
        }
        for (let user of this.userList) {
          this.manageForm.user_ids.push(user.id)
        }
        let data = Object.assign({}, this.manageForm)
        if (this.mode === 'modify') {
          data['id'] = this.manageID // append ID
          api.editManagedUserList(data).then(res => {
            this.$router.push({name: 'manage-user-details', params: {manageId: this.manageID}}).catch(() => {})
          })
        } else {
          api.addManagedUserList(data).then(res => {
            this.$router.push({name: 'manage-user-list'})
          })
        }
      }
    },
    computed: {
      selectedUserIDs () {
        let ids = []
        for (let user of this.selectedUsers) {
          ids.push(user.id)
        }
        return ids
      }
    }
  }
</script>
<style scoped lang="less">
.add-samples {
  width: 100%;
  background-color: #fff;
  border: 1px dashed #aaa;
  outline: none;
  cursor: pointer;
  color: #666;
  height: 35px;
  font-size: 14px;
  &:hover {
    background-color: #f9fafc;
  }
  i {
    margin-right: 10px;
  }
}
</style>