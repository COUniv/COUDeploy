<template>
  <div class="view">
    <Panel :title="`특별 사용자 관리`">
      <div slot="header">
        <el-row :gutter="20">
          <el-col :span="4">
            <i class="mdi mdi-plus plus-hov"
                       @click="createList">
            </i>
          </el-col>
          <el-col :span="16">
            <el-input v-model="keyword" prefix-icon="el-icon-search" placeholder="Keywords"></el-input>
          </el-col>
        </el-row>
      </div>
      <el-table
        v-loading="loadingTable"
        element-loading-text="loading"
        
        ref="table"
        :data="manageUserList"
        style="width: 100%">
        <!-- <el-table-column type="selection" width="55"></el-table-column> -->

        <el-table-column prop="title" label="제목"></el-table-column>

        <el-table-column prop="content" label="내용"></el-table-column>

        <el-table-column prop="writer.username" label="관리자"></el-table-column>

        <el-table-column prop="create_time" label="생성일자">
          <template slot-scope="scope">
            {{scope.row.create_time | localtime }}
          </template>
        </el-table-column>

        <el-table-column prop="last_update_time" label="마지막 수정일">
          <template slot-scope="scope">
            {{scope.row.last_update_time | localtime }}
          </template>
        </el-table-column>
        <el-table-column fixed="right" label="옵션" width="200">
          <template slot-scope="{row}">
            <el-button icon="el-icon-edit" size="mini" @click.native="openUserDialog(row.id)"></el-button>
            <el-button icon="el-icon-delete" size="mini" @click.native="deleteList([row.id])"></el-button>
          </template>
        </el-table-column>
      </el-table>
      <div class="panel-options">
        <el-pagination
          class="page"
          layout="prev, pager, next"
          @current-change="currentChange"
          :page-size="pageSize"
          :total="total">
        </el-pagination>
      </div>
    </Panel>
  </div>
</template>

<script>
  import api from '../../api.js'

  export default {
    name: 'ManagedUserList',
    data () {
      return {
        // 한 페이지에 표시되는 사용자 수
        pageSize: 10,
        // 총 사용자 수
        total: 0,
        // 사용자목록
        manageUserList: [],
        // 키워드 검색
        keyword: '',
        // 사용자 대화 상자를 표시할지 여부
        showUserDialog: false,
        // 현재 사용자 model
        user: {},
        loadingTable: false,
        // 현재 페이지 번호
        currentPage: 0,
        selectedManageList: []
      }
    },
    mounted () {
      this.getManageUserList(1)
    },
    methods: {
      createList () {
        this.$router.push({name: 'create-manage-user-list'}).catch(() => {})
      },
      // 토글 페이지 번호 콜백
      currentChange (page) {
        this.currentPage = page
        this.getManageUserList(page)
      },
      // 사용자 정보를 수정하기 위한 메서드
      saveUser () {
        api.editUser(this.user).then(res => {
          // 업데이트 목록
          this.getManageUserList(this.currentPage)
        }).then(() => {
          this.showUserDialog = false
        }).catch(() => {
        })
      },
      // 사용자 대화 상자 열기
      openUserDialog (id) {
        this.showUserDialog = true
        api.getUser(id).then(res => {
          this.user = res.data.data
          this.user.password = ''
          this.user.real_tfa = this.user.two_factor_auth
        })
      },
      // 사용자 목록 가져오기
      getManageUserList (page) {
        this.loadingTable = true
        api.getAllManagedUserList((page - 1) * this.pageSize, this.pageSize, this.keyword).then(res => {
          this.loadingTable = false
          this.total = res.data.data.total
          this.manageUserList = res.data.data.results
          for (let idx = 0; idx < this.manageUserList.length; idx++) {
            var content = this.manageUserList[idx].content
            if (content.length > 9) {
              this.manageUserList[idx].content = (content.substr(0, 10) + '...')
            }
          }
        }, res => {
          this.loadingTable = false
        })
      },
      deleteList (ids) {
        this.$confirm('정말로 삭제하시겠습니까? 삭제하면 되돌릴 수 없습니다.', 'confirm', {
          type: 'warning'
        }).then(() => {
          api.deleteManagedUserList(ids[0]).then(res => {
            console.log(res)
            this.getManageUserList(this.currentPage)
          })
        }, () => {
        })
      },
      handleSelectionChange (val) {
        this.selectedManageList = val
      }
    },
    computed: {
      selectedManageIDs () {
        let ids = []
        for (let id of this.selectedManageList) {
          ids.push(id)
        }
        return ids
      }
    },
    watch: {
      'keyword' () {
        this.currentChange(1)
      },
      'user.admin_type' () {
        if (this.user.admin_type === 'Super Admin') {
          this.user.problem_permission = 'All'
        } else if (this.user.admin_type === 'Regular User') {
          this.user.problem_permission = 'None'
        }
      }
    }
  }
</script>

<style scoped lang="less">
  .import-user-icon {
    color: #555555;
    margin-left: 4px;
  }

  .userPreview {
    padding-left: 10px;
  }

  .notification {
    p {
      margin: 0;
      text-align: left;
    }
  }
  .plus-hov {
    border: solid 1px;
    font-size: 20px;
    padding: 5px;
    height: 40px;
    width: 40px;
    line-height: 40px;
    cursor: pointer;
    &:hover {
      color: #F5A547;
    }
  }
</style>
<style lang="less">
  .dialogView {
    .el-dialog {
      min-width: 600px;
    }
  }
</style>
