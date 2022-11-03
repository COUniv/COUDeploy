<template>
  <div class="container">
    <div class="top-line">
        <div class="red"></div>
        <div class="yellow"></div>
        <div class="green"></div>
      <div class="tag" @click="$router.push('/setting/mypage')">마이페이지</div>
    </div>
    <div class="main-container">
      <div class="flex-container">
        <div class="menu" :class="{'no-show': noShow}">
          <Menu accordion @on-select="goRoute" :activeName="activeName" style="text-align: center;" width="auto">
            <div class="avatar-editor">
              <div class="avatar-container">
                <img class="avatar" :src="profile.avatar"/>
              </div>
              <button @click.stop="chanAvt({name: 'profile-setting'})"><Icon color="#5030e5" size=15 type="md-create" /></button>
              <div class="user-name">
                {{ profile.user.username }} 님
                <div class="logout_btn" @click="$router.push('/logout')">로그아웃</div>
              </div>
            </div>
            <Menu-item name="/setting/mypage">개요</Menu-item>
            <Menu-item name="/setting/profile">
              <Icon type="md-information-circle" class="mobile-icon"/>
              {{$t('m.Profile')}}
            </Menu-item>
            <Menu-item name="/setting/account">
              <Icon type="md-clipboard" class="mobile-icon"/>
              {{$t('m.Account')}}
            </Menu-item>
            <Menu-item v-if="isAdminRole" name="/admin">
              <Icon type="md-settings" class="mobile-icon" />
                {{$t('m.Management')}}
            </Menu-item>
            <!-- <Menu-item name="/setting/security">{{$t('m.Security')}}</Menu-item> -->
            <!-- <Menu-item name="/logout">로그아웃</Menu-item> -->
          </Menu>
        </div>
        <div class="panel">
          <transition name="fadeInUp">
            <router-view></router-view>
          </transition>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
  import { mapGetters } from 'vuex'

  export default {
    name: 'profile',
    methods: {
      chanAvt (routePath) {
        this.$router.push(routePath).catch(() => {})
      },
      goRoute (routePath) {
        if (routePath && routePath.indexOf('admin') < 0) {
          this.$router.push(routePath).catch(() => {})
        } else {
          window.open('/admin/')
        }
      }
    },
    computed: {
      ...mapGetters(['profile', 'isAdminRole']),
      activeName () {
        if (this.$route.path === '/logout') {
          this.goRoute('/logout')
        }
        return this.$route.path
      },
      noShow () {
        if (this.$route.path === '/setting' || this.$route.path === '/setting/mypage') {
          return false
        } else {
          return true
        }
      }
    },
    watch: {
      $route () {
        return this.noShow
      }
    }
  }
</script>

<style lang="less" scoped>
  @import '../../../../styles/common.less';
  @avatar-radius: 50%;
  .top-line {
    display: flex;
    height: 40px;
    background-color: @purple;
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
    padding: 10px 10px;
    .red, .yellow, .green {
      width: 15px;
      height: 15px;
      border-radius: 50%;
      margin: 3px 5px;
    }

    .red {
      background-color: #ED6A5F;
    }

    .yellow {
      background-color: #F6BE4F;
    }

    .green {
      background-color: #62C655;
    }

    .tag {
      background-color: @white;
      height: 30px;
      width: 120px;
      margin-left: 46px;
      border-top-left-radius: 5px;
      border-top-right-radius: 5px;
      padding-top: 8px;
      padding-left: 15px;
      -webkit-text-stroke: .5px;
      font-size: 110%;
      color: @gray;
      &:hover {
        cursor: pointer;
      }
    }

  }
  .container {
    width: 80%;
    min-width: 800px;
    margin: auto;
  }

  .main-container {
    background-color: @white;
    border-bottom-left-radius: 5px;
    border-bottom-right-radius: 5px;
    min-height: 160vh;
    border-right: 1px solid @dark-white;
    border-left: 1px solid @dark-white;
    border-bottom: 1px solid @dark-white;
      .flex-container {
        .menu {
          flex: 1 0 150px;
          max-width: 250px;
          .avatar-editor {
            padding: 10% 22%;
            margin-bottom: 10px;
            position: relative;
              .avatar {
                width: 100%;
                height: auto;
                max-width: 100% !important;
                display: block;
                border-radius: @avatar-radius;
                box-shadow: 0px 0px 1px 0px;
              }
          }
          .user-name {
            margin-top: 20px;
            font-size: 130%;
            -webkit-text-stroke: .5px;
            color: @black;
            .logout_btn {
              display: none;
              color: #654AE1;
            }
          }

          button {
            cursor: pointer;
            border-radius: 50%;
            height: 30px;
            width: 30px;
            position: absolute;
            border: none;
            background-color: @white;
            bottom: 70px;
            left: 150px;
            box-shadow: 1px 1px 2px #D4CBFE;
            &:hover {
              background-color: #e8e4fd;
              transition: background-color .3s ease-in-out;
            }
          }
          .mobile-icon {
            display: none;
          }
        }
      }
    }
    .panel {
          flex: auto;
          min-height: 160vh;
          border-left: 1px solid @dark-white;
        }

  .ivu-menu-vertical.ivu-menu-light:after {
    width: 0;
  }
  @media screen and (max-width : 900px) {
    .container {
      width: 100vw;
      .top-line {
        border-radius: 0;
      }
      .flex-container {
        flex-direction: column;
        .menu {
          min-width: 100vw;
          margin-bottom: 10px;
          &.no-show{
            display: none
          }
          .avatar-editor {
            display: flex;
            min-width: 500px;
            padding: 5%;
            height: 10%;
            .avatar-container {
              width: 20%;
              min-width: 130px;
              margin-right: 20px;
              .avatar {
                //width: 0%;
                margin-right: 0px !important;
              }
            }
            .user-name {
              margin-top: 40px;
              text-align: left;
              font-size: 1.8em;
              .logout_btn {
                display: block;
                font-size: 0.7em;
                cursor: pointer;
              }
            }
            button {
              bottom: 40px;
              left: 140px;
            }
          }
          .ivu-menu-item {
            font-size: 150%;
            text-align: left;
            padding-left: 40px;
            &:nth-child(2) {
              display: none;
            }
            border-top: 1px solid #C0C0C0;
            &:last-child {
              border-bottom: 1px solid #C0C0C0;
            }
            &::after {
              content: ">";
              float: right;
              font-size: 150%;
              color: #C0C0C0;
              line-height: 100%;
              margin-right: 12px;
            }
          }
          .mobile-icon {
            display: inline-block;
          }
        }
        
        .panel {
          min-width: 100vw;
        }
      }
      
    }
  }
</style>

<style lang="less">
  .setting-main {
    position: relative;
    margin: 10px 40px;
    padding-bottom: 20px;
    .setting-content {
      margin-left: 20px;
    }
    .mini-container {
      width: 500px;
    }
  }
  @media screen and (max-width : 900px) {
    .left {
          margin-bottom: 0 !important;
        }
    .setting-main {
      margin: 0 20px;
      .btn-menu {
        .button:first-child {
          margin-right: 100px !important;
        }
      }
    }
  }
</style>
