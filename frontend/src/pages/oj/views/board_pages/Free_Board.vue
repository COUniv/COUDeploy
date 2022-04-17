<template>
  <div class="free_board">
    <div class="community" style="float:left">
      <div class="community_menu_name">커뮤니티</div>
      <div class="community_menu">
        <router-link to="/Free_Board"
          ><div class="community_menu_list_main" name="/FreeBoard">
            자유 게시판
          </div></router-link
        >
        <router-link to="/Question_Board"
          ><div class="community_menu_list" name="/QuestionBoard">
            질문 게시판
          </div></router-link
        >
        <router-link to="/Request_Board"
          ><div class="community_menu_list" name="/RequestBoard">
            요청 게시판
          </div></router-link
        >
      </div>
    </div>
    <div class="community_free" style="float:right">
      <div class="community_free_title">자유 게시판</div>
      <div class="community_free_bar">
        <div class="community_free_search">
          <Input
            @on-enter="changeRoute"
            @on-click="changeRoute"
            v-model="query.keyword"
            placeholder="검색할 내용을 입력하세요"
            icon="ios-search-strong"
          />
          <!-- <router-link to="/Board_Post" class="community_free_btn"><Button type="primary" name="/BoardPost">게시물 작성</Button></router-link> -->
        </div>
        <div class="community_free_btn">
          <router-link to="/Board_Post"
            ><Button type="primary" name="/BoardPost"
              >게시물 작성</Button
            ></router-link
          >
          <!-- <Button type="primary" name="/BoardPost">게시물 작성</Button> -->
        </div>
      </div>
      <div class="community_free_list">
        <Table
          style="width: 100%; font-size: 16px"
          :columns="freeBoardColumns"
          :data="freeBoardList"
        ></Table>
        <Pagination
          :total="total"
          :page-size.sync="query.limit"
          @on-change="pushRouter"
          @on-page-size-change="pushRouter"
          :current.sync="query.page"
          :show-sizer="true"
        ></Pagination>
      </div>
      <!-- <div class="community_free_btn"> -->
      <!-- <router-link to="/Board_Post"><Button type="primary" name="/BoardPost">게시물 작성</Button></router-link> -->
      <!-- <Button type="primary" name="/BoardPost">게시물 작성</Button> -->
      <!-- </div> -->
    </div>
  </div>
</template>

<script>
export default {
  // name: 'FreeBoardList',

  data () {
    return {
      freeBoardColumns: [
        {
          title: '#',
          width: 70,
          align: 'center',
          key: 'number'
        },
        {
          title: '제목',
          // width: 60,
          align: 'center',
          key: 'title'
        },
        {
          title: '작성자',
          width: 130,
          align: 'center',
          key: 'name'
        },
        {
          title: '등록일',
          width: 150,
          align: 'center',
          key: 'date'
        },
        {
          title: '조회',
          width: 70,
          align: 'center',
          key: 'count'
        }
      ],
      // data1: [
      //     {
      //         name: 'John Brown',
      //         age: 18,
      //         address: 'New York No. 1 Lake Park',
      //         date: '2016-10-03'
      //     }
      // ],
      freeBoardList: [
        {
          number: 1,
          title: 'abc',
          name: '123',
          date: '2022-02-27',
          count: 10
        },
        {
          number: 1,
          title: 'abc',
          name: '123',
          date: '2022-02-27',
          count: 10
        },
        {
          number: 1,
          title: 'abc',
          name: '123',
          date: '2022-02-27',
          count: 10
        },
        {
          number: 1,
          title: 'abc',
          name: '123',
          date: '2022-02-27',
          count: 10
        }
      ],
      limit: 20,
      total: 0,
      loadings: {
        table: true,
        tag: true
      },
      routeName: '',
      query: {
        keyword: '',
        difficulty: '',
        tag: '',
        page: 1,
        limit: 10
      }
    }
  }
}
</script>
<style>
    .free_board {
        margin: 0 10% 0 10%;
        /* font-size: 0px; */
    }

    .community {
        display: inline-block;
        vertical-align: top;
        /* padding: 0 0 20px 0; */
        width: 20%;
        height: 20%;
        padding: 0 0 20px 0;
        font-size: 16px;
        text-align: center;
    }

    .community_menu_name {
        display: block;
        font-size: 32px;
        color: #1f4e79;
    }

    .community_menu {
        display: block;
        /* vertical-align: top; */
        /* width: 20%; */
        /* height: 20%; */
        margin-top: 10px;
        padding: 0 0 20px 0;
        font-size: 16px;
        /* text-align: center; */
        /* background-color: rgb(232, 238, 177);  */
        border-top: 2px solid rgb(61, 61, 61);
        color: black;
    }

    .community_menu_list_main{
        padding: 10px 0;
        color: white;
        border-bottom: 1px solid rgb(61, 61, 61);
        background: #1f4e79;
    }

    .community_menu_list {
        padding: 10px 0;
        color: black;
        border-bottom: 1px solid rgb(61, 61, 61);
    }

    .community_menu_list:hover {
        background-color: #1f4e79;
        color: white;
    }

    .community_free {
        display: inline-block;
        vertical-align: top;
        width: 80%;
        height: 60%;
        padding: 0 20px 0 20px;
        /* background-color: rgb(136, 167, 138); */
    }

    .community_free_title {
        /* display: block; */
        /* margin-top: -10px; */
        padding: 0 0 10px 0;
        border-bottom: 2px solid black;
        font-size: 32px;
        color: #1f4e79;
        /* background-color: rgb(255, 234, 239); */
    }

    .community_free_bar{
        display: flex;
        justify-content: right;
        margin: 20px 0 10px 0;
    }
    
    .community_free_search{
        display: inline-block;
        width: 25%;
        margin-right: 10px;
    }
    .community_free_btn{
            display: inline-block;
            /* width: 20%; */
    }

    .community_free_list {
        display: block;
        clear: both;
        /* margin-top: 40px; */
        /* padding: 0 0 20px 0; */
        /* background-color: rgb(231, 206, 255); */
    }

</style>
