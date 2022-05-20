<template>
  <div>
    <div class="main_contents">
      <el-form ref="form" :model="formArticle" :rules="rules" label-position="top" label-width="70px">
        <div class="selectform">
          <Select v-if="mode !== 'modify'" v-model="formArticle.boardtype" placeholder="카테고리" clearable style="width=200px">
            <Option v-for="type in typeList" :value="type.value" :key="type.value">
              {{ type.label }}
            </Option>
          </Select>
        </div>

        <!-- 게시판 타입 선택 dropdown 버튼 -->
        <!-- <div>
          <Dropdown @on-click="handleTypeChange">
            게시판
            <Icon type="arrow-down-b"></Icon>
            <Dropdown-menu slot="list">
              <Dropdown-item name="1">자유</Dropdown-item>
              <Dropdown-item name="2">질문</Dropdown-item>
              <Dropdown-item name="2">요청</Dropdown-item>
            </Dropdown-menu>
          </Dropdown>
        </div> -->
        
        <!-- 질문 게시판의 경우 질문 관련 언어 설정 -->
        <div v-if="formArticle.boardtype === '2'" class="selectform">
          <Select v-model="formArticle.problemtype" placeholder="언어" clearable>
            <Option v-for="type in problemtypeList" :value="type.value" :key="type.value">
              {{ type.value }}
            </Option>
          </Select>
        </div>

        <!-- 질문 게시판의 경우 질문 관련 문제 번호 설정 -->
        <div v-if="formArticle.boardtype === '2'" style="padding-top: 15px; width: 10%;">
            <el-form-item prop="problemid" label="ProblemId" required>
              <!-- 문제 번호 입력 - formArticle.problemid -->
              <Input type="text" v-model="formArticle.problemid" placeholder="문제 번호" size="large"></Input>
            </el-form-item>
        </div>

        <div class="title_form">
            <el-form-item prop="title" required>
              <!-- 게시글 제목 입력 - formArticle.title -->
              <Input type="text" v-model="formArticle.title" placeholder="제목" size="large"></Input>
            </el-form-item>
        </div>
        
        <!-- 게시글 내용 입력 - formArticle.content -->
        <div class="contents_form">
            <el-form-item prop="content" required>
              <Simditor v-model="formArticle.content"></Simditor>
            </el-form-item>
        </div>

        <!-- 게시글 제출 버튼 - submit -->
        <div class="submit_btn">
          <Button type="primary" @click="submit">Submit</Button>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script>
  import Simditor from '@/pages/admin/components/Simditor'
  import api from '@oj/api'

  export default {
    name: 'CreateArticle',
    components: {
      Simditor // 게시글 내용 입력 폼
    },
    data () {
      return {
        typeList: [
          {
            value: '1',
            label: '자유 게시판'
          },
          {
            value: '2',
            label: '질문 게시판'
          }
        ],
        problemtypeList: [ // 질문 가능한 언어 리스트
          {
            value: 'Java'
          },
          {
            value: 'C'
          },
          {
            value: 'C++'
          },
          {
            value: 'Python'
          }
        ],
        rules: {
          title: {required: true, message: 'Title is required', trigger: 'blur'},
          content: {required: true, message: 'Content is required', trigger: 'blur'}
        },
        formArticle: { // 전송 데이터
          title: '', // 게시글 제목
          content: '', // 게시글 내용
          boardtype: '', // 게시글 타입
          problemtype: '', // 질문 게시글의 경우 질문 관련 언어
          problemid: '' // 질문 게시글의 경우 질문 관련 문제 ID
        },
        mode: '', // 게시글 수정(modify) or 신규 작성
        articleID: '' // 게시글 id
      }
    },
    mounted () {
      this.routeName = this.$route.name
      if (this.routeName === 'modify-article') { // route명이 게시글 수정인 경우
        this.mode = 'modify' // 게시글 수정
      }
      this.init()
    },
    methods: {
      init () {
        if (this.mode === 'modify') { // 게시글 수정인 경우
          this.articleID = this.$route.params.articleID
          api.getArticle(this.articleID).then(res => { // db에서 해당 ID의 게시글 원래 내용 가져옴
            let article = res.data.data
            this.formArticle.title = article.title
            this.formArticle.content = article.content
            this.formArticle.boardtype = article.boardtype
          })
        }
      },
      submit () { // 게시글 제출 함수
        let data = Object.assign({}, this.formArticle)
        if (this.mode === 'modify') { // 게시글 수정인 경우
          api.modifyArticle(data.title, data.content, this.articleID).then(res => {
            this.$success('success!!')
            this.$router.push({name: 'article-list'}) // 작성 완료 후 게시글 목록으로 돌아감
          })
        } else { // 게시글 신규 작성인 경우
          api.createArticle(data).then(res => {
            this.$success('success!!')
            this.$router.push({name: 'article-list'}) // 작성 완료 후 게시글 목록으로 돌아감
          })
        }
      }
    }
  }
</script>
<style scoped lang="less">
.main_contents {
  margin: 0 10% 0 10%;
  padding-top: 15px;
}
.selectform {
  padding-top: 15px;
  width: 150px;
}
.title_form {
  padding-top: 15px;
  width: 50%;
  min-width: 350px;
}
.contents_form {
  padding-top: 15px;
  min-width: 350px;
}
.submit_btn {
  padding-top: 15px;
}
</style>