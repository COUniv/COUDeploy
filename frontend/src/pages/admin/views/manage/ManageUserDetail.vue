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
      <el-row :gutter="20" class="content-title">
        <el-button v-show="selectedUsers.length"
                   class="email-btn"
                   type="primary" icon="el-icon-s-promotion"
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
        manageID: '',
        userlist: [],
        writer: '',
        title: '',
        content: '',
        createTime: '',
        lastUpdateTime: '',
        loadingTable: false,
        selectedUsers: []
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
      }
    }
  }
</script>
<style scoped lang="less">
@import '../../../../styles/common.less';
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
.email-btn {
  margin-top: 10px;
  margin-left: 10px;
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
</style>