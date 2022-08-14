<template>
  <div class="flex-container">
    <div class="flex-item">
    <svg class="grass-container" style="height:112px">
      <template  v-for="(__, idx_x) in 52">
        <g>
          <rect v-for="(_, idx_y) in 7" class="grass-pointer" v-bind:style="{'x':getPositionX(idx_x) ,'y': getPositionY(idx_y)}" style="height:10px; width:10px; x:0px; background-color:blueviolet"></rect>
        </g>
      </template>
    </svg>
    </div>
  </div>
</template>
<script>
  import api from '@oj/api'
  export default {
    data () {
      return {
        grassList: []
      }
    },
    mounted () {
      this.getGrassList()
    },
    methods: {

      getGrassList () {
        api.getGrassList().then(res => {
          this.grassList = res.data.data.grass
          console.log(this.grassList)
        })
      },
      getPositionX (x) {
        return 13 * x
      },
      getPositionY (y) {
        return 13 * y
      }
    }
  }
</script>
<style lang="less" scoped>

.flex-container {
  width:100%;
  margin-top: 30px;
  padding: auto 20px;
  text-align: center;
  font-weight: 400;
  font-size: 16px;

  .flex-item {
    width:75%;
    overflow-x: auto;
  }
  .grass-container {
    width: 677px;
    margin: 0 auto;
  }
}
</style>