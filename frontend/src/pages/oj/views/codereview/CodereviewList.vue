<template>
  <div class="header">
    <div class="cdreview_title" slot="title">{{ mainTitle }}</div>
    <button type="button" id="add-new" @click="Create">+</button>
  </div>

  <Card :padding="20">
    <div class="reviewContainer markdown-body">
      <ul v-if="mainItem && mainItem.length">
  <li
    v-for="(item, index) in mainItem"
    :key="index"
    @click="gotoDetail(item)"
  >
          <b>{{ item.reviewTitle }}</b>
          <p>{{ item.userId }}</p>
          <p>{{ item.reviewContents }}</p>
          <button type="button" id="more" @click="More">더보기</button>
        </li>
      </ul>
    </div>
    <div v-for="(item, index) in reviewCode" :key="index">
      <BlockedCursorCodeMirror
        :value="{ item }"
        :theme="theme"
      ></BlockedCursorCodeMirror>
      <div class="ellipses">...</div>
    </div>
  </Card>
</template>

<script>
import api from "@oj/api";
import Pagination from "@/pages/oj/components/Pagination";
import BlockedCursorCodeMirror from "@oj/components/BlockedCursorCodeMirror";
export default {
  name: "codereview-list",
  components: {
    BlockedCursorCodeMirror,
    Pagination,
  },
  data() {
    return {
      theme: "solarized",
      count: 0,
      reviewItem: [],
      reviewCode: [],
      mainTitle: "코드리뷰",
    };
  },
  mounted() {
    this.getCodeReviewInfo();
    this.getReviewCodeSource();
  },
  methods: {
    Create() {

      this.$router.push({ name: "create-reviewcode" }).catch(() => {});
    },
    More() {
 
      this.$router.push({ name: "detail-reviewcode" }).catch(() => {});
    },

    getCodeReviewInfo() {
      api
        .getCodeReviewInfo()
        .then((res) => {
          this.reviewItem = res.data.reviewItem;
        })
        .catch(() => {
          this.loadingTable = false;
        });
    },
    getReviewCodeSource() {
      api
        .getReviewCodeSource()
        .then((res) => {
          this.reviewCode = res.data.reviewCode.slice(0, 3);
        })
        .catch(() => {
          this.loadingTable = false;
        });
    },
    gotoDetail (item) {
    this.$router.push({name: 'codereviewdetail', params: { data: item }}).catch(() => {})
  },
  },
  watch: {
    $route(newVal, oldVal) {
      if (newVal === "-1" || parseInt(newVal.query.boardtype) < 0) {
        this.$router.push({ path: "/404" }).catch(() => {});
      }
      if (newVal !== oldVal) {
        this.init();
      }
    },
  },
};
</script>

<style scoped lang="less">
.header {
  width: calc(100%-100px);
  margin: 0 auto;
}
.title {
  padding-top: 50px;
  margin: 0 50px 50px 50px;
  font-size: 30px;
  font-weight: 700;
}
.reviewContainer {
  margin-bottom: 20px;

  .content {
    font-size: 16px;
    margin: 0 50px 20px 50px;
    > ul {
      list-style: disc;
      li {
        line-height: 2;
        .title {
          font-weight: 500;
        }
      }
    }
  }
}
.reviewContainer:hover {
  box-shadow: 1px 1px 4px #bbb;
}
#add-new {
  cursor: pointer;
  padding: 0 10px;
  height: 35px;
  background-color: @white;
  border: solid 1px @gray;
  color: @gray;
  font-size: @font-regular;
  transition: all 0.3s ease-in-out;
}
#add-new:hover {
  background-color: @light-orange;
  color: @dark-orange;
  border: solid 1px @dark-orange;
}
#more {
  cursor: pointer;
  width: 70px;
  height: 35px;
  border: 1px solid @gray;
  color: @gray;
  font-size: @font-regular;
  transition: all 0.3s ease-in-out;
  background-color: @white;
}
#more:hover {
  background-color: @light-orange;
  color: @dark-orange;
  border: 1px solid @dark-orange;
  font-weight: 700;
}
.ellipses {
  text-align: center;
  font-size: 30px;
  padding: 10px 0;
}
</style>
