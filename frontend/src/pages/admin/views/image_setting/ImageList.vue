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
          label="제목">
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
            <icon-btn name="Edit" icon="edit" @click.native="openTagDialog(scope.row.id)"></icon-btn>
            <icon-btn icon="trash" name="Delete Category"
                      @click.native="deleteProblemTag(scope.row.id)"></icon-btn>
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

    <el-dialog title="이미지 추가" :visible.sync="showImageDialog" :close-on-click-modal="false">
      <el-form :model="tag" label-width="120px" label-position="left">
        <el-row :gutter="20">
          <el-col :span="12">
          </el-col>
        </el-row>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <cancel @click.native="showImageDialog = false">취소</cancel>
        <save @click.native="saveImage()"></save>
      </span>
    </el-dialog>
  </div>
</template>

<script>
  import api from '../../api.js'
  import utils from '@/utils/utils'
  import {mapGetters} from 'vuex'
  export default {
    name: 'ImageList',
    data () {
      return {
        showImageDialog: false
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
      openTagDialog (tagId) {
        this.showImageDialog = true
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
</style>
