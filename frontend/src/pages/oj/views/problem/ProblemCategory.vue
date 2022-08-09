<template>
  <div class="category">
    <div class="title">문제 카테고리</div>
    <hr style="color: gray;">
    <div class="item_box">
      <div class="item" v-for="category in problemCategoryList" :key="category.title" @click="goProblemList(category.id)">
        <h3>{{ category.title }}</h3>
        <div class="description" v-katex v-html="category.description"></div>
        <div class="progress"><Progress :percent="category.percent" /></div>
      </div>
    </div>
  </div>
</template>

<script>
  import api from '@oj/api'
  import utils from '@/utils/utils'
  export default {
    data () {
      return {
        problemCategoryList: {}
      }
    },
    mounted () {
      this.init()
    },
    methods: {
      init () {
        api.getProblemCategoryList().then(res => {
          this.problemCategoryList = res.data.data
          // this.problemCategoryList.forEach(element => {
          //   api.getProblemPercent(element.id).then(res => {
          //     element.percent = res.data.data
          //   })
          // })
        })
      },
      goProblemList (id) {
        let query = {
          keyword: '',
          difficulty: '',
          tag: '',
          category: id,
          page: 1,
          limit: 10
        }
        this.$router.push({
          name: 'problem-list',
          query: utils.filterEmptyValue(query)
        })
      }
    }
  }
</script>

<style lang="less" scoped>
@import '../../../../styles/common.less';

  .progress{
    display: absolute;
    bottom: 0;
  }
  .category{
    width:100%;
    margin: 80px 0 120px !important;
    background-color: @white;
    border-radius: @size-border-radius;
    box-shadow: 2px 5px 20px 2px rgba(90, 82, 128, 0.31);
    .title {
      background-color: @purple;
      border-radius: 5px 5px 0 0;
      padding: 10px;
      color: @white;
      font-size: 24px;
      text-align: center;
      font-weight: @weight-bold;
    }
  }

  .item_box{
    display: flex;
    flex-wrap: wrap;
    align-content: flex-start;
    margin-top: 20px;
    padding: 10px 20px;
  }

  .item{
    position: relative;
    /* width: 37vh;
    height: 20vh; */
    width: 345px;
    height: 200px;
    font-size: 16px;
    /* background: salmon; */
    border: 2px solid #DDD7FA;
    background-color: @white;
    border-radius: 0px 20px;
    box-shadow: 0px 4px 20px #DDD7FA;
    margin: 0 1.5% 20px 1.5%;
    padding: 24px;
    cursor: pointer;
    h3, div {
      padding-bottom: 10px;
    }
    h3 {
      font-size: 24px;
      color: @black;
    }
    .description {
      font-weight: @weight-bold;
      color: @gray;
      font-size: 18px;
    }
    p {
      font-size: 16px;
      width: 100%;
      padding-top: 10px;
    }
  }

  .progress{
    position: absolute;
    bottom: 0;
    width: 100%;
    left: 0;
    padding: 10px 0 0 10px;
  }

</style>