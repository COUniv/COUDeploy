<template>
  <div class="articles-container">
    
    <Panel shadow :padding="30">
      <!-- 게시글 제목 -->
      <div slot="title" style="font-size: 1.5em;">
        {{article.title}}
      </div>
      
      <!-- 게시글 정보 및 버튼 -->
      <div slot="extra">

        <!-- 게시글 수정 버튼(작성자만 보임) -->
        <Button v-if="is_writer" icon="ios-create" @click="goModify">Modify</Button>

        <!-- 게시글 삭제 버튼(작성자만 보임) -->
        <Button v-if="is_writer" icon="md-trash" @click="deletemodal=true">Delete</Button>
        <Modal
          v-model="deletemodal"
          title="경고"
          @on-ok="ok"
          @on-cancel="cancel">
          <p>게시물을 삭제합니다.</p>
        </Modal>

        <!-- 뒤로가기 버튼 -->
        <Button icon="ios-undo" @click="goBack">{{$t('m.Back')}}</Button>
      </div>

      <!-- 작성자명 및 작성 시간-->
      <div style="margin-bottom:50px">
        <a style="display:inline-block" @click="goUser"><b>{{username}}</b></a>
        <div style="display:inline-block; padding-left:30px">{{article.create_time}}</div>
      </div>
      
      <!-- 질문 게시판의 경우 문제 링크 -->
      <div v-if="problemid">
        <button @click="goProblemDetail(problemid)">{{ problemid }}</button>
      </div>

      <!-- 게시글 내용 -->
      <div style="display:flex; margin-top:30px">
        <div v-katex v-html="article.content" key="content" class="content-container markdown-body"></div>
      </div>

      <div style="margin-top:30px; padding-bottom:30px">
        <div style="float:right; clear:both;">
          <div slot="extra">
            <!-- 좋아요 버튼 -->
            <Button icon="ios-heart-outline" @click="like">좋아요</Button>
          </div>
        </div>
      </div>
      <!-- 구분선 -->
      <div style="padding-top:15px; clear:both;"></div>
      <hr>
      <!-- 댓글 목록 -->
      <div v-for="(comment,index) in comments" :key="index" style="padding-top:20px">

          <Card>
            <!-- 사용자 정보영역 -->
            <Card style="background:#eee;" dis-hover>
              <div style="overflow: hidden;">
                <div class="linkdiv" @click="goCommentUesr(comment.username)">
                  <b>{{ comment.username }}</b>
                </div>
                <div style="float:right;">
                  {{ comment.create_time }}
                </div>
              </div>
            </Card>


            <div style="padding-top:15px; margin: 0 15px 0 15px; clear:both;">{{ comment.content }}</div>
            <div style="float:right; padding-top:15px; ">
              <Button v-if="comment.is_comment_writer" icon="ios-undo" @click="modifyForm(comment)">modify</Button>
              <Button v-if="comment.is_comment_writer" icon="ios-undo" @click="deleteComment(comment)">delete</Button>
            </div>
            <div style="padding-top:15px; clear:both;">
              <!-- 댓글 수정 입력 폼 - 댓글 수정 버튼 클릭 시 보임 -->
              <Input v-show="comment.modify" type="text" v-model="comment.content" :placeholder="Comment"></Input>
              <Button v-show="comment.modify" type="primary" @click="modifyComment(comment)" class="btn">Modify</Button>
            </div>
          </Card>

      </div>

      <!-- 댓글 입력 -->
      <div style="margin-top:30px">
        <Input type="text" v-model="formComment.content" :placeholder="Comment"></Input>
        <Button style="margin-top:15px; float:right;" type="primary" @click="commentSubmit" class="btn">Submit</Button>
      </div>
      <!-- float 겹침 방지 (삭제하지마세요) -->
      <div style="clear:both;"></div>
    </Panel>
  </div>
</template>

<script>
  import api from '@oj/api'
  import time from '@/utils/time'

  export default {
    name: 'ArticleDetails',
    data () {
      return {
        deletemodal: false,
        is_writer: false, // 현재 보는 게시글의 작성자 여부
        article: { // 게시글 내용 출력용 data
          title: '',
          content: '',
          create_time: ''
        },
        formComment: {
          articleid: '',
          content: ''
        },
        comments: [], // 댓글 목록
        articleID: '', // 게시글 ID
        username: '', // 게시글 작성자 명
        problemid: '',
        is_liked: false
      }
    },
    mounted () {
      this.init()
    },
    methods: {
      ok () {
        this.deleteArticle()
      },
      cancel () {
      },
      convertUTC () {
        this.comments.forEach(element => {
          element.create_time = time.utcToLocal(element.create_time, 'YYYY-MM-DD HH:mm:ss')
        })
      },
      init () {
        this.articleID = this.$route.params.articleID
        api.getArticle(this.articleID).then(res => { // 게시글 ID를 통해 해당 게시글 정보를 가져옴
          let article = res.data.data
          this.article.title = article.title
          this.article.content = article.content
          this.article.create_time = time.utcToLocal(article.create_time, 'YYYY-MM-DD HH:mm:ss')
          this.is_writer = article.is_writer
          this.username = article.username
          this.comments = article.comments
          this.is_liked = article.is_liked
          this.convertUTC()
          if (article.boardtype === 'QUESTION') {
            this.problemid = article.problemid
          }
        }, () => {
        })
      },
      goBack () { // 뒤로 가기 - 게시글 목록으로 이동
        this.$router.push({name: 'article-list'})
      },
      goModify () { // 게시글 수정 - 현재 게시글 ID를 전송
        this.$router.push({name: 'modify-article', params: {articleID: this.articleID}})
      },
      deleteArticle () { // 게시글 삭제
        api.deleteArticle(this.articleID).then(res => { // 게시글 ID를 전송해 해당 게시글을 삭제함
          this.$Message.error('삭제되었습니다.')
          this.$router.push({name: 'article-list'})
        })
      },
      commentSubmit () { // 댓글 작성
        this.formComment.articleid = this.articleID
        console.log(this.formComment.content)
        api.createComment(this.formComment).then(res => {
          this.$success('create success')
          this.$router.go()
        })
      },
      deleteComment (comment) { // 댓글 삭제
        api.deleteComment(comment.id).then(res => { // 댓글 ID를 전송해 해당 댓글을 삭제함
          this.$success('delete success')
          this.$router.go()
        })
      },
      modifyForm (comment) { // 댓글 수정 버튼 클릭 이벤트 리스너 - 댓글 수정 폼 출력
        if (comment.modify) { // 댓글의 modify값 = 댓글 수정 폼 출력을 위한 변수, true - 보임 / false - 안보임
          this.$set(comment, 'modify', false) // 수정 폼이 보이는 상태에서 버튼 클릭 시 폼을 숨김
        } else {
          this.$set(comment, 'modify', true) // 수정 폼이 안 보이는 상태에서 버튼 클릭 시 폼을 출력
        }
      },
      like () { // 좋아요
        api.likeArticle(this.articleID).then(res => { // 게시글 ID를 전송
          this.$success(res.data.data)
        })
      },
      modifyComment (comment) { // 댓글 수정 제출 버튼 클릭 이벤트 리스너
        // let data = {id: comment.id, content: this.modifyContent}
        let data = {id: comment.id, content: comment.content} // 댓글 ID, 새로 작성한 content 데이터 전송
        api.modifyComment(data).then(res => {
          this.$success('modify success')
          this.$router.go()
        })
      },
      goUser () {
        this.$router.push(
          {
            name: 'user-home',
            query: {username: this.username}
          }
        )
      },
      goCommentUesr (usr) {
        this.$router.push(
          {
            name: 'user-home',
            query: {username: usr}
          }
        )
      },
      goProblemDetail (problemid) {
        this.$router.push(
          {
            name: 'problem-details',
            params: {problemID: problemid}
          }
        )
      }
    }
  }
</script>

<style scoped lang="less">
  .flex-container {
      margin: 0 5% 0 5%;
      padding-top: 15px;
  }
  .articles-container {
    margin: 0 5% 0 5%;
    padding-top: 15px;
    li {
      padding-top: 15px;
      list-style: none;
      padding-bottom: 15px;
      margin-left: 20px;
      font-size: 16px;
      border-bottom: 1px solid rgba(187, 187, 187, 0.5);
      &:last-child {
        border-bottom: none;
      }
      .flex-container {
        .title {
          flex: 1 1;
          text-align: left;
          padding-left: 10px;
          a.entry {
            color: #495060;
            &:hover {
              color: #2d8cf0;
              border-bottom: 1px solid #2d8cf0;
            }
          }
        }
        .creator {
          flex: none;
          width: 200px;
          text-align: center;
        }
        .date {
          flex: none;
          width: 200px;
          text-align: center;
        }
      }
    }
    a {
      font-size: 1.3em;
      color: #3c4250;
    }
    a:hover {
      color:cornflowerblue
    }
  }

  .linkdiv {
    float: left;
    font-size:1.3em;
    color: #3c4250;
  }
  .linkdiv:hover {
    color:cornflowerblue
  }
  .content-container {
    padding: 0 20px 20px 20px;
  }

  .no-article {
    text-align: center;
    font-size: 16px;
  }changeLocale

  .article-animate-enter-active {
    animation: fadeIn 1s;
  }

</style>
