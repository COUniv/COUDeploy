<template>
  <div>
    <p><strong>언어:</strong> {{ item.languagetype }}</p>
    <p><strong>문제 번호:</strong> {{ item.problemid }}</p>
    <p><strong>제목:</strong> {{ item.title }}</p>
    <p><strong>작성자 아이디:</strong> {{ item.username }}</p>
    <p><strong>생성 시간:</strong> {{ item.create_time }}</p>
    <p><strong>댓글 수:</strong> {{ item.comment_count }}</p>
    
    <button @click="deleteCodeReview">삭제하기</button>
    
    <div class="comments-section">
    <h3>댓글</h3>
    <div v-for="comment in comments" :key="comment.id">
      {{ comment.content }} - {{ comment.username }}
      <button @click="modifyComment(comment)">수정</button>
      <button @click="deleteComment(comment.id)">삭제</button>
    </div>
      
    <input v-model="newComment" placeholder="댓글 작성" />
    <button @click="createComment">댓글 추가</button>
  </div>
</template>

<script>
export default {
  data () {
    return {
      item: {},
      comments: [],
      newComment: "",
      codeContent: ""  // 코드 내용을 저장할 변수 추가
    };
  },
  created () {
    if (this.$route.params.data) {
      this.item = this.$route.params.data;
      this.fetchComments();
    }
  },
  created () {
    if (this.$route.params.data) {
      this.item = this.$route.params.data;
      this.fetchComments();
      this.fetchCode();  // 코드를 가져오는 함수 호출
    }
  },
  methods: {
    async fetchCode() {
      try {
        const response = await this.$axios.get('/api/get_code_text', {
          params: {
            id: this.item.id
          }
        });

        if (response.data && response.data.success) {
          this.codeContent = response.data.content;  // 가져온 코드 내용 저장
        } else {
          console.error('코드 가져오기 에러:', response.data.error);
        }
      } catch (error) {
        console.error('API 호출 중 에러 발생:', error);
      }
    },
    async createComment() {
      try {
        const response = await this.$axios.post('/api/create_codereview_comment', {
          articleid: this.item.id,
          content: this.newComment,
          line: 0  //해당
        });

        if (response.data && response.data.success) {
          this.comments.push({
            id: response.data.commentId,
            content: this.newComment,
            username: "current_user"
          });
          this.newComment = "";
        } else {
          console.error('댓글 생성 중 에러:', response.data.error);
        }
      } catch (error) {
        console.error('API 호출 중 에러 발생:', error);
      }
    },

    async deleteComment(commentId) {
      try {
        const response = await this.$axios.get(`/api/delete_codereview_comment?id=${commentId}`);

        if (response.data && response.data.success) {
          this.comments = this.comments.filter(comment => comment.id !== commentId);
        } else {
          console.error('댓글 삭제 중 에러:', response.data.error);
        }
      } catch (error) {
        console.error('API 호출 중 에러 발생:', error);
      }
    },

    async modifyComment(comment) {
      const newContent = window.prompt("댓글 내용을 수정하세요:", comment.content);

      if (newContent) {
        try {
          const response = await this.$axios.post('/api/modify_codereview_comment', {
            id: comment.id,
            content: newContent
          });

          if (response.data && response.data.success) {
            comment.content = newContent;
          } else {
            console.error('댓글 수정 중 에러:', response.data.error);
          }
        } catch (error) {
          console.error('API 호출 중 에러 발생:', error);
        }
      }
    }
  }
};
</script>

<style scoped lang="less">
.flex-container {
  width: 100%;
  height: 100%;
  padding: 0 50px;
  margin: 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.header {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.cdreview_title {
  padding-top: 50px;
  margin-left: 50px;
  font-size: 1.75rem;
  font-weight: 700;
}

.comments-section {
  width: 95%;
  margin-top: 20px;
  padding: 20px;
  border-radius: 10px;
  background-color: rgba(255, 255, 255, 0.4);
  display: flex;
  flex-direction: column;
  align-items: center;
}

.comments-section h3 {
  width: 100%;
  font-weight: bold;
  margin-bottom: 20px;
  border-bottom: 1px solid grey;
  padding-bottom: 10px;
}

.comment-item {
  width: 95%;
  padding: 10px 0;
  border-bottom: 1px solid grey;
  display: flex;
  justify-content: space-between;
}

.comment-item:last-child {
  border-bottom: none;
}

input[type="text"] {
  width: 80%;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid grey;
  margin-right: 10px;
}

button {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  background-color: #0064FF;
  color: white;
  cursor: pointer;
  margin-top: 20px;  /* 버튼과 다른 요소 간 간격을 추가했습니다. */
}

button:hover {
  background-color: #3592FF;
}
</style>
