<template>
  <div class="flex-container">
    <div class="header">
      <div class="cdreview_title" slot="title">{{ mainTitle }}</div>
      <button type="button" id="add-new" @click="Create">추가하기</button>
    </div>
    <Card :padding="20" class="reviewContainer">
      <div class="reviewBox markdown-body">
    <ul v-if="mainItem && mainItem.length" @click="gotoDetail">
      <li class="category-list">
        <div><strong>번호</strong></div> 
        <div><strong>언어</strong></div>
        <div><strong>문제 번호</strong></div>
        <div><strong>제목</strong></div>
        <div><strong>작성자 아이디</strong></div>
      </li>
      <li v-for="(item, index) in mainItem" :key="index">
        <div class="list-item">
          <div>{{ index + 1 }}</div> 
          <div>{{ item.languagetype }}</div>
          <div>{{ item.problemid }}</div>
          <div>{{ item.title }}</div>
          <div>{{ item.username }}</div>
        </div>
      </li>
    </ul>
        <p v-else>Loading...</p>
      </div>
    </Card>
    <div style="display:flex; justify-content: center">
      <div style="float:right">
        <Pagination :total="total" :page-size="limit" @on-change="changeRoute" :current.sync="page"></Pagination>
      </div>
    </div>
  </div>
</template>

<script>
import Pagination from '@/pages/oj/components/Pagination'
import api from '@oj/api';

export default {
  components: {
    Pagination
  },
  data () {
    return {
      mainTitle: '코드리뷰',
      mainItem: [] // 초기 데이터는 빈 배열로 설정
    };
  },
  created () {
    this.fetchCodeReviews();
  },
  methods: {
    async fetchCodeReviews () {
      try {
        const response = await api.codeReviewMain();
        this.mainItem = response.data; // API 응답으로 받은 데이터를 mainItem에 할당
      } catch (error) {
        console.error('API 호출 중 에러 발생:', error);
      }
    },
    Create () {
      this.$router.push({ name: 'createcodereview' }).catch(() => {});
    },
    gotoDetail () {
      this.$router.push({ name: 'codereviewdetail' }).catch(() => {});
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
  #add-new {
    margin-top: 20px;
    width: 80px;
    height: 30px;
    font-size: 16px;
    color: white;
    background-color: #0064FF;
    border-radius: 30px;
    border: none;
    cursor: pointer;
  }

  #add-new:hover {
    background-color: #3592FF;
  }
  .reviewContainer {
    width: 95%;
    margin-top: 50px;
    cursor: pointer;
    border-radius: 10px;
    background-color: rgba(255, 255, 255, 0.4); 
  }
  .reviewBox {
    width: 100%;
    padding: 20px;
    margin: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    color: black; 
  }
  .reviewBox ul {
    width: 100%;
    height: 150px;
  }
  .list-item, .category-list {
    display: flex;
    justify-content: space-between;
    width: 95%;
    padding: 0 0px;
    border-bottom: 1px solid grey; 
    height: 30px;
  }

  .category-list {
    font-weight: bold;
    padding-bottom: 10px;
    border-bottom: 1px solid black;
    margin-bottom: 20px;
    background-color: #8C8C8C; 
    border-top: 1px solid grey;
  }
</style>
