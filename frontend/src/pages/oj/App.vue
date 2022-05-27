<template>
  <div>
    <div class="content_container">
      <div class="blockingdrag">
        <NavBar v-show="$route.name !== 'start-login' && $route.name !== 'problem-details'"></NavBar>
      </div>
      <div class="content-app">
        <SessionExpire v-if="isIdle && $route.name !== 'start-login'"/>
        <transition name="fadeInUp" mode="out-in">
          <router-view></router-view>
        </transition>
        <!-- <div class="footer">
          <p v-html="website.website_footer"></p>
          <p>Powered by <a href="https://github.com/QingdaoU/OnlineJudge">OnlineJudge</a>
            <span v-if="version">&nbsp; Version: {{ version }}</span>
          </p>
        </div> -->
      </div>
      <BackTop></BackTop>
    </div>
    <div class="footer" v-show="$route.name !== 'start-login' && $route.name !== 'problem-details'">
      <p v-html="website.website_footer"></p>
      <p>Poweredaaa by <a href="https://github.com/OnlineJudgePlatformDev">COU</a>
        <span v-if="version">&nbsp; Version: {{ version }}</span>
      </p>
    </div>
  </div>
</template>

<script>
  import { mapActions, mapState } from 'vuex'
  import NavBar from '@oj/components/NavBar.vue'
  import SessionExpire from '@oj/components/SessionExpire.vue'
  export default {
    name: 'app',
    components: {
      NavBar,
      SessionExpire
    },
    data () {
      return {
        version: process.env.VERSION
      }
    },
    created () {
      try {
        document.body.removeChild(document.getElementById('app-loader'))
      } catch (e) {
      }
    },
    mounted () {
      this.getWebsiteConfig()
    },
    methods: {
      ...mapActions(['getWebsiteConfig', 'changeDomTitle'])
    },
    computed: {
      ...mapState(['website']),
      isIdle () {
        return this.$store.state.idleVue.isIdle
      }
    },
    watch: {
      'website' () {
        this.changeDomTitle()
      },
      '$route' () {
        this.changeDomTitle()
      }
    }
  }
</script>

<style lang="less">

  * {
    -webkit-box-sizing: border-box;
    -moz-box-sizing: border-box;
    box-sizing: border-box;
  }

  a {
    text-decoration: none;
    background-color: transparent;
    &:active, &:hover {
      outline-width: 0;
    }
  }

  .content_container {
    // screen height - navigation bar height - footer height - contanier bottom margin
    min-height: calc(~"100vh - 80px - 80px - 20px");
    margin: 0 50px 50px 50px;
    padding-bottom: 80px;
  }
  @media screen and (max-width: 1200px) {
    .content-app {
      margin-top: 80px;
      min-height: 100%;
      position: relative;
      padding-bottom: 90px;
    }
  }

  @media screen and (min-width: 1200px) {
    .content-app {
      margin-top: 80px;
      min-height: 100%;
      position: relative;
      padding-bottom: 90px;
    }
  }
  .blockingdrag {
    -webkit-user-select:none;
    -moz-user-select:none;
    -ms-user-select:none;
    user-select:none
  }



  .footer {
    background-color: rgb(41, 41, 41);
    position: relative;
    left: 0px;
    bottom: 0;
    width: 100%;
    height: 80px;
    text-align: center;
    font-size: small;
  }

  .fadeInUp-enter-active {
    animation: fadeInUp .8s;
  }



</style>
