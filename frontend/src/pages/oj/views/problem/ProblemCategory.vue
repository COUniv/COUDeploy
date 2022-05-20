<template>
  <div class="category">
    <div style="margin-top: 80px;">
      <div class="item_box">
        <div class="item" v-for="category in problemCategoryList" :key="category" @click="goProblemList(category.id)">
          <h3>{{ category.title }}</h3>
          <div v-katex v-html="category.description"></div>
          <div class="progress"><Progress :percent="category.percent" /></div>
        </div>
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
          console.log(this.problemCategoryList)
          this.problemCategoryList.forEach(element => {
            api.getProblemPercent(element.id).then(res => {
              element.percent = res.data.data
            })
          })
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
      },
      getPercent (id) {
        let percent
        api.getProblemPercent(id).then(res => {
          percent = res.data.data
        })
        return percent
      }
    }
  }
</script>

<style>

  .progress{
    display: absolute;
    bottom: 0;
  }
  .category{
    width:100%;
    margin: 50px;
  }

  /* .item_title{
    font-size: 24px;
    padding-bottom: 5px;
  } */

  .item_box{
    display: flex;
    flex-wrap: wrap;
    align-content: flex-start;
    margin-top: 120px;
  }

  .item{
    position: relative;
    /* width: 37vh;
    height: 20vh; */
    width: 345px;
    height: 200px;
    font-size: 16px;
    /* background: salmon; */
    border: 1px solid rgb(226, 226, 226);
    background-color: rgb(233, 233, 233);
    border-radius: 10px;
    margin: 0 1.5% 20px 1.5%;
    padding: 15px;
  }

  .item > h3, .item > div{
    padding-bottom: 10px;
  }

  .item > h3{
    font-size: 28px;
  }

  .item > p {
    font-size: 16px;
    width: 100%;
    padding-top: 10px;
  }

  .progress{
    position: absolute;
    bottom: 0;
    width: 100%;
    left: 0;
    padding: 10px 0 0 10px;
  }

</style>