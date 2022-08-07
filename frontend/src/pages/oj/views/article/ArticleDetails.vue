<template>
  <div class="articles-container">
    
    <Panel shadow>
      <!-- 게시글 제목 -->
      <div slot="title" style="font-size: 1.5em;">
        <!-- 뒤로가기 버튼 -->
        <Button icon="md-arrow-back" size="large" @click="goBack" type="text"></Button>
        {{article.title}}
      </div>
      
      <!-- 게시글 정보 및 버튼 -->
      <div slot="extra">

        <!-- 게시글 수정 버튼(작성자만 보임) -->
        <Button v-if="is_writer" type="primary" icon="md-create" @click="goModify"></Button>

        <!-- 게시글 삭제 버튼(작성자만 보임) -->
        <Button v-if="is_writer" type="primary" icon="md-trash" @click="deletemodal=true"></Button>
        <Modal v-model="deletemodal">
          <p slot="header" style="color:red">경고</p>
          <p>게시물을 삭제합니다.</p>
          <div slot="footer" class="slotWrapper">
            <Button @click="articleDeleteModalClosed">취소</Button>
            <Button type="primary" @click="ok">확인</Button>
          </div>
        </Modal>
      </div>

      <!-- 작성자명 및 작성 시간-->
      <div class="user-date">
        <div id="user-avatar"></div>
        <div>
          <a @click="goUser"><b>{{username}}</b></a>
          <div id="user-time">{{article.create_time}}</div>
        </div>
      </div>
      
      <!-- 질문 게시판의 경우 문제 링크 -->
      <div v-if="problemid">
        <button @click="goProblemDetail(problemid)">{{ problemid }}</button>
      </div>

      <!-- 게시글 내용 -->
      <div>
        <div v-katex v-html="article.content" key="content" class="content-container"></div>
      </div>

      <div style>
        <div>
          <div id="like-button" slot="extra" :v-model="is_liked">
            <!-- 좋아요 버튼 -->
            <Button v-if="!is_liked" icon="ios-heart-outline" :border="false" @click="like" size="large" class="like_button" type="text">{{article.like_count}}</Button>
            <Button v-else icon="ios-heart" :border="false" @click="like" size="large" class="like_button" type="text">{{article.like_count}}</Button>
          </div>
        </div>
      </div>
      <!-- 구분선 -->
      <div></div>
      <hr class="hr-style">
      <!-- 댓글 목록 -->
      <div v-for="comment in comments" :key="comment.id">

          <Card>
            <!-- 사용자 정보영역 -->
              <div class="comment-user-time">
                <div class="linkdiv" @click="goCommentUesr(comment.username)">
                  <b>{{ comment.username }}</b>
                </div>
                <div id="comment-time">
                  {{ comment.create_time }}
                </div>
              </div>


            <pre v-katex v-html="comment.content" style="white-space: pre-wrap; overflow: auto; word-break:break-all"></pre>
            <div>
              <!-- 수정 버튼 -->
              <Button v-if="comment.is_comment_writer" icon="ios-create" @click="onModalComment(comment)">수정</Button>
              <!-- 삭제 버튼 -->
              <Button v-if="comment.is_comment_writer" icon="md-trash"  @click="onDeleteModalComment(comment)">삭제</Button>
            </div>
            <Modal v-model="deletemodalcomment">
              <p slot="header" style="color:red">경고</p>
              <p style="font-size:14px">댓글을 삭제하시겠습니까?</p>
              <div slot="footer" class="slotWrapper">
                <Button @click="commentDeleteModalClosed">취소</Button>
                <Button type="primary" @click="commentDeleteOk(deleteComment_id)">확인</Button>
              </div>
            </Modal>

            <!-- 댓글 수정 modal창 -->
            <Modal v-model="commandmodal"
              :mask-closable="false" :fullscreen="fullscreen" :z-index="999">
              <p slot="header" style="color:#f60; text-align:center">
                <span>댓글 수정</span>
              </p>
              <div>
                <div class="fullscreen-btn">
                  <Button @click="isFullScreen">{{ fullscreen_btn_text }}</Button>
                </div>
                <Input type="textarea" :rows="8" v-model="tempComment.content"></Input>
              </div>
              <div slot="footer" class="slotWrapper">
                <Button @click="modalClosed">취소</Button>
                <Button type="primary" @click="modifyCommentOk(tempComment)">확인</Button>
              </div>
            </Modal>
          </Card>

      </div>

      <!-- 댓글 입력 -->
      <div class="comment-section">
        <Input type="textarea" v-model="formComment.content" :autosize="{minRows: 2, maxRows: 6}" placeholder="댓글 입력" class="comment_submit_input"></Input>
        <Button class="comment_submit_btn" type="text" icon="ios-paper-plane" @click="commentSubmit"></Button>
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
        fullscreen_btn_text: '전체 화면',
        fullscreen: false,  // 전체화면 여부
        commandmodal: false,  // 댓글 수정창 modal
        deletemodalcomment: false,  // 댓글 삭제 경고창 modal
        deletemodal: false, // 게시글 삭제 경고창 modal
        is_writer: false, // 현재 보는 게시글의 작성자 여부
        article: { // 게시글 내용 출력용 data
          title: '',
          content: '',
          create_time: '',
          like_count: ''
        },
        formComment: {
          articleid: '',
          content: ''
        },
        comments: [], // 댓글 목록
        articleID: '', // 게시글 ID
        username: '', // 게시글 작성자 명
        problemid: '',
        deleteComment_id: null, // 댓글 삭제를 위한 임시 value
        tempComment: {  // 댓글 수정을 위한 임시 value
          id: null,
          content: ''
        },
        is_liked: false
      }
    },
    mounted () {
      this.init()
    },
    methods: {
      articleDeleteModalClosed () {
        this.deletemodal = false
      },
      commentDeleteModalClosed () {
        this.deletemodalcomment = false
      },
      modalClosed () {
        this.commandmodal = false
        this.cancel()
      },
      onModalComment (comment) {
        this.tempComment.id = comment.id
        this.tempComment.content = comment.content
        this.commandmodal = true
      },
      onDeleteModalComment (comment) {
        this.deleteComment_id = comment.id
        this.deletemodalcomment = true
      },
      isFullScreen () {
        if (this.fullscreen) {
          this.cancel()
        } else {
          this.fullscreen = true
          this.fullscreen_btn_text = '전체 화면 종료'
        }
      },
      modifyCommentOk (comment) {
        this.modifyComment(comment)
        this.tempComment.id = null
        this.tempComment.content = '' // 수정 완료후 tempComment를 clear
        this.refreshComment()
        this.modalClosed()
      },
      ok () { // 게시글 삭제 button ok call
        this.deleteArticle()
      },
      cancel () {
        this.fullscreen_btn_text = '전체 화면'
        this.fullscreen = false
      },
      commentDeleteOk (comment) { // 댓글 삭제 button ok call
        this.deleteComment(comment)
        this.deletemodalcomment = false
      },
      convertUTC () {
        this.comments.forEach(element => {
          element.create_time = time.utcToLocal(element.create_time, 'YYYY-MM-DD HH:mm')
        })
      },
      init () {
        this.articleID = this.$route.params.articleID
        api.getArticle(this.articleID).then(res => { // 게시글 ID를 통해 해당 게시글 정보를 가져옴
          let article = res.data.data
          this.article.title = article.title
          this.article.content = article.content
          this.article.create_time = time.utcToLocal(article.create_time, 'YYYY-MM-DD HH:mm')
          this.is_writer = article.is_writer
          this.username = article.username
          this.comments = article.comments
          this.is_liked = article.is_liked
          this.article.like_count = article.like_count
          this.convertUTC()
          if (article.boardtype === 'QUESTION') {
            this.problemid = article.problemid
          }
        }, () => {
        })
      },
      refreshComment () {
        api.getArticle(this.articleID).then(res => {
          let article = res.data.data
          this.article.title = article.title
          this.article.content = article.content
          this.article.create_time = time.utcToLocal(article.create_time, 'YYYY-MM-DD HH:mm:ss')
          this.is_writer = article.is_writer
          this.username = article.username
          this.comments = article.comments
          this.formComment.articleid = ''
          this.formComment.content = ''
          this.convertUTC()
          if (article.boardtype === 'QUESTION') {
            this.problemid = article.problemid
          }
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
        api.createComment(this.formComment).then(res => {
          this.$success('생성 완료')
          this.refreshComment()
        })
      },
      deleteComment (commentId) { // 댓글 삭제
        api.deleteComment(commentId).then(res => { // 댓글 ID를 전송해 해당 댓글을 삭제함
          this.$success('삭제되었습니다.')
          this.refreshComment()
          this.deleteComment_id = null
        }, () => {
          this.deleteComment_id = null
        })
      },
      modifyForm (comment) { // 댓글 수정 버튼 클릭 이벤트 리스너 - 댓글 수정 폼 출력
        this.tempComment = comment.content
        if (comment.modify) { // 댓글의 modify값 = 댓글 수정 폼 출력을 위한 변수, true - 보임 / false - 안보임
          this.$set(comment, 'modify', false) // 수정 폼이 보이는 상태에서 버튼 클릭 시 폼을 숨김
        } else {
          this.$set(comment, 'modify', true) // 수정 폼이 안 보이는 상태에서 버튼 클릭 시 폼을 출력
        }
      },
      like () { // 좋아요
        api.likeArticle(this.articleID).then(res => { // 게시글 ID를 전송
          this.$success(res.data.data)
          this.init()
        })
      },
      modifyComment (comment) { // 댓글 수정 제출 버튼 클릭 이벤트 리스너
        // let data = {id: comment.id, content: this.modifyContent}
        let data = {id: comment.id, content: comment.content} // 댓글 ID, 새로 작성한 content 데이터 전송
        api.modifyComment(data).then(res => {
          this.$info('수정이 완료되었습니다.')
        }, () => {
          this.$error('Error')
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
@import '../../../../styles/common.less';
  .articles-container {
    margin: 0 5% 0 5%;
    //padding-top: 15px;
    li {
      //padding-top: 15px;
      list-style: none;
      //padding-bottom: 15px;
      //margin-left: 20px;
      font-size: 16px;
      //border-bottom: 1px solid rgba(187, 187, 187, 0.5);
      &:last-child {
        border-bottom: none;
      }
    }
    a {
      color: @black;
      //margin-right: 20px;
      &:hover {
        color: @purple;
      }
    }
  }

  .user-date {
    display: flex;
    margin: 5px 0px 5px 70px;
    line-height: 30px;
    div:nth-of-type(2) {
      display:flex;
      flex-direction: column;
      line-height: 15px;
    }
  }

  #user-avatar {
    height: 30px;
    width: 30px;
    border-radius: 15px;
    background-color: @purple;
    margin-right: 10px;
  }

  #user-time {
    font-size: 10px;
  }

  #like-button {
    margin: 5px 0px 5px 55px;
  }

  .fullscreen-btn {
    float: right;
    //margin-bottom: 20px;
  }

  .comment-user-time {
    line-height: 20px;
  }

  .linkdiv {
    float: left;
    //font-size:1.3em;
    margin-right: 15px;
    color: @black;
  }

  #comment-time {
    color: @gray;
    font-size: 10px;
  }

  .linkdiv:hover {
    color:@purple;
  }
  .content-container {
    margin: 15px 70px 5px 70px;
  }

  .no-article {
    text-align: center;
    font-size: 16px;
  }

  .article-animate-enter-active {
    animation: fadeIn 1s;
  }
  .hr-style {
    border: 1px solid #e8eaec;
  }

  .slotWrapper {
    //padding-top: 15px;
    border-top: 1px solid #e8eaec;
  }

  .comment_submit_input textarea {
    //padding-right: 45px;
    resize: none;
    
  }
  .comment-section {
    margin-top: 20px;
    padding: 0 65px;
  }
  .comment_submit_btn {
    margin: 10px;
    margin-bottom: 15px;
    float: right;
    font-size: 1.3em;
    position: relative;
    left: 10px;
    color: @purple;
    border: none;
    &:focus {
      outline: none !important;
      -webkit-box-shadow: none;
      box-shadow: none;
    }
    * > &:focus {
      outline: none !important;
      -webkit-box-shadow: none;
      box-shadow: none;
    }
    * > &:hover {
      color: @light-purple;
      background-color: @black;
      border-color: @black;
    }
    * {
      border: none;
    }
  }
  .like_button {
    &:focus {
      outline: none !important;
      -webkit-box-shadow: none;
      box-shadow: none;
    }
    * > &:focus {
      outline: none !important;
      -webkit-box-shadow: none;
      box-shadow: none;
    }
  }

</style>
