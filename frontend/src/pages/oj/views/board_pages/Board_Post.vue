<template>
  <div class="board_post">

    <form method="get" action="write_action.php">
      <table align="center" width="700px" border="0">
        <tr>
          <td class="board_form">게시판 작성하기</td>
        </tr>
        <tr>
          <td bgcolor="white">
            <table class="table2">
              <tr>
                <td>작성자</td>
                <td>
                  <!-- <input type = text name = name size=20>  -->
                  <template v-if="isAuthenticated">
                    {{ user.username }}
                  </template>
                </td>
              </tr>

              <tr>
                <td>제목</td>
                <td><input type="text" name="title" size="60" /></td>
              </tr>

              <tr>
                <td>내용</td>
                <td>
                  <textarea name="content" cols="100" rows="15"></textarea>
                </td>
              </tr>

              <tr>
                <td>비밀번호</td>
                <td>
                  <input type="password" name="pw" size="10" minlength="8" />
                </td>
              </tr>
            </table>

            <div class="submit_btn">
              <Button type="primary">작성하기</Button>
            </div>
          </td>
        </tr>
      </table>
    </form>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
export default {
  data() {
    return {};
  },
  computed: {
    ...mapGetters(["user", "isAuthenticated"]),
  },
};
</script>

<style>
.board_post {
  /* background: rgb(240, 240, 240); */
  background-color: #ccc;
  margin: 0 10%;
  padding: 20px;
  font-size: 16px;
}

/* .board_form_title{
        
    }

    .board_form_content{
        height: 40%;
    }  */

.board_form {
  height: 20px;
  text-align: center;
  /* background: rgb(240, 240, 240); */
  background: #ccc;
  font-size: 32px;
  padding: 0 0 10px 0;
}

table.table2 {
  border-collapse: separate;
  border-spacing: 1px;
  text-align: left;
  line-height: 1.5;
  border-top: 1px solid #ccc;
  margin: 20px 10px;
}

table.table2 tr {
  width: 50px;
  padding: 10px;
  font-weight: bold;
  vertical-align: top;
  border-bottom: 1px solid #ccc;
}

table.table2 td {
  width: 200px;
  padding: 10px;
  vertical-align: top;
  border-bottom: 1px solid #ccc;
}

.submit_btn {
  display: flex;
  justify-content: right;
  padding: 0 10px 10px 0;
}
</style>