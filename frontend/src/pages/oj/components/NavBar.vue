<template>
  <div id="header">

    <Menu theme="light" mode="horizontal" @on-select="handleRoute" :active-name="activeMenu" class="oj-menu">
      <!-- <div class="logo"> -->
        
      <Menu-item class="home_bar" name="/" >Online Judge Platform</Menu-item>
        <!-- <span><a href="/">Online Judge Platform</a></span> -->
        
      <!-- </div> -->
      <!-- <Menu-item name="/">
        <Icon type="home"></Icon>
        {{$t('m.Home')}}
      </Menu-item> -->
      
      
      
      <Menu-item class="bar_list" name="/problem">
        <!-- <Icon type="ios-keypad"></Icon>
        {{$t('m.NavProblems')}} -->
        문제
      </Menu-item>
      <Menu-item class="bar_list" name="/contest">
        <!-- <Icon type="trophy"></Icon>
        {{$t('m.Contests')}} -->
        대회
      </Menu-item>

      <Submenu class="bar_list" name="/info">
        <template slot="title">
          정보
        </template>
          <MenuItem name="/announcement-list">공지사항</MenuItem>
          <MenuItem name="/help">자주 묻는 질문</MenuItem>
          <MenuItem name="/languages">언어별 도움말</MenuItem>
          <MenuItem name="/acm-rank">사용자 순위</MenuItem>
      </Submenu>

      <Submenu class="bar_list" name="/community">
        <template slot="title">
          커뮤니티
        </template>
          <MenuItem name="/article-list?boardtype=0">전체 게시판</MenuItem>
          <MenuItem name="/article-list?boardtype=1">자유 게시판</MenuItem>
          <MenuItem name="/article-list?boardtype=2">질문 게시판</MenuItem>
          <MenuItem name="/article-list?boardtype=3">요청 게시판</MenuItem>
      </Submenu>


      <Menu-item class="bar_list" name="/status">
        <!-- <Icon type="ios-pulse-strong"></Icon> -->
        {{$t('m.NavStatus')}}
      </Menu-item>
      <!-- <Menu-item class="bar_list" name="/about">
        커뮤니티
      </Menu-item> -->
      <!-- <Menu-item class="bar_list" name="/acm-rank">
        랭킹
      </Menu-item> -->


      <!-- <Menu-item class="bar_list" name="/about"> -->
      <!-- <Menu-item class="bar_list">
        <div class="dropdown">
          <button class="dropbtn">Dropdown 
            <i class="fa fa-caret-down"></i>
          </button>
          <div class="dropdown-content">
            <a href="#">Link 1</a>
            <a href="#">Link 2</a>
            <a href="#">Link 3</a>
          </div>
        </div>

      </Menu-item> -->



      <!-- <Menu-item class="bar_list" name="/about">
        도움말
      </Menu-item> -->

      <!-- <Submenu name="rank">
        <template slot="title">
          <Icon type="podium"></Icon>
          {{$t('m.Rank')}}
        </template>
        <Menu-item name="/acm-rank">
          {{$t('m.ACM_Rank')}}
        </Menu-item>
        <Menu-item name="/oi-rank">
          {{$t('m.OI_Rank')}}
        </Menu-item>
      </Submenu> -->
      <!-- <Submenu name="about">
        <template slot="title">
          <Icon type="information-circled"></Icon>
          {{$t('m.About')}}
        </template>
        <Menu-item name="/about">
          {{$t('m.Judger')}}
        </Menu-item>
        <Menu-item name="/FAQ">
          {{$t('m.FAQ')}}
        </Menu-item>
      </Submenu> -->
      <!-- <Submenu name="about">
        <template slot="title">
          <Icon type="information-circled"></Icon>
          {{$t('m.About')}}
        </template> -->
        <!-- <Menu-item name="/FAQ">
          {{$t('m.FAQ')}}
        </Menu-item> -->
      <!-- </Submenu> -->
      <template v-if="!isAuthenticated">
        <!-- <div class="btn-menu">
          <Button type="ghost"
                  ref="loginBtn"
                  shape="circle"
                  @click="handleBtnClick('login')">
                  <p style="color:white">{{$t('m.Login')}}</p>
          </Button>
          <Button v-if="website.allow_register"
                  type="ghost"
                  shape="circle"
                  @click="handleBtnClick('register')"
                  style="margin-left: 5px;">
                  <p style="color:white">{{$t('m.Register')}}</p>
          </Button>
        </div> -->
      </template>
      <template v-else>
        <!-- <Dropdown class="drop-menu" @on-click="handleRoute" placement="bottom" trigger="click">
          <Button type="text" class="drop-menu-title">{{ user.username }}
            <Icon type="arrow-down-b"></Icon>
          </Button>
          <Dropdown-menu slot="list">
            <Dropdown-item name="/user-home">{{$t('m.MyHome')}}</Dropdown-item>
            <Dropdown-item name="/status?myself=1">{{$t('m.MySubmissions')}}</Dropdown-item>
            <Dropdown-item name="/setting/profile">{{$t('m.Settings')}}</Dropdown-item>
            <Dropdown-item v-if="isAdminRole" name="/admin">{{$t('m.Management')}}</Dropdown-item>
            <Dropdown-item divided name="/logout">{{$t('m.Logout')}}</Dropdown-item>
          </Dropdown-menu>
        </Dropdown> -->
        <div style="right-div">
        <Menu-item class="drop-menu" name="/setting/mypage">
          {{ user.username }}
        </Menu-item>

        <!-- 알림 출력 버튼 -->
        <div class="alarm">
        <Badge v-if="init_notification_count > 0" dot style="height: 40px;margin-right: 10px;margin-top: 10px;">
          <Button type="text" style="
          margin-top: -20;
          margin-top: -40px;
          padding-left: 0px;
          padding-right: 6px" size="large" @click="changeNoti" icon="ios-notifications-outline">
          <!-- to change to white -> add "ghost" -->

          </Button>
          <!-- <Icon type="ios-notifications-outline" size="26"></Icon> -->
        </Badge>
        <Badge v-else style="height: 40px;margin-right: 10px;margin-top: 10px;">
          <Button type="text" style="
          margin-top: -20;
          margin-top: -40px;
          padding-left: 0px;
          padding-right: 6px" size="large" @click="changeNoti" icon="ios-notifications-outline">
          <!-- to change to white -> add "ghost" -->

          </Button>
          <!-- <Icon type="ios-notifications-outline" size="26"></Icon> -->
        </Badge>
        </div>
        </div>

        <!-- <Button @click="changeNoti" type="primary">Open</Button> -->
        <Drawer title="알림창" :width="300" :closable="true" v-model="visivleDraw">
          <div style="float:right; margin-bottom:15px" @click="goAllNotificationList"><a>알람 전체 보기</a></div>
          <div style="clear:both;"></div>
          <Table :border="dishovering" :no-data-text="emptyChar" :columns="colums" :data="vNotifications" :show-header="showHeaderandborder" :disabled-hover="dishovering"></Table>
        </Drawer>
      </template>
    </Menu>
    <Modal v-model="modalVisible" :width="400">
      <div slot="header" class="modal-title">{{$t('m.Welcome_to')}} {{website.website_name_shortcut}}</div>
      <component :is="modalStatus.mode" v-if="modalVisible"></component>
      <div slot="footer" style="display: none"></div>
    </Modal>
  </div>
</template>

<script>
  import { mapGetters, mapActions } from 'vuex'
  import login from '@oj/views/user/Login'
  import register from '@oj/views/user/Register'
  import api from '@oj/api'
  export default {
    components: {
      login,
      register
    },
    data () {
      return {
        init_notification_count: 0,
        emptyChar: '알람이 존재하지 않습니다.',
        showHeaderandborder: false,
        dishovering: true,
        visivleDraw: false,
        vNotifications: [],
        colums: [
          {
            title: 'noti',
            render: (h, params) => {
              return h('div', {
                style: {
                }
              }, [
                h('div', {
                  style: {
                    'float': 'left',
                    'padding-top': '5px'
                  }
                }, [
                  h('a', {
                    style: {
                      'font-size': '1.2em',
                      'font-weight': 'bold',
                      'line-height': '1.3em'
                    },
                    on: { // 확인 클릭 시 알림이 발생한 곳으로 이동
                      click: () => {
                        api.checkNotification(params.row.id).then(res => {
                          window.open(params.row.url)
                        })
                      }
                    }
                  }, params.row.notificationtype),
                  h('p', {
                    style: {
                      'padding-bottom': '5px'
                    }
                  }, params.row.content)
                ]),
                h('div', {
                  style: {
                    'margin-top': '10px',
                    'float': 'right',
                    'max-width': '55px'
                  }
                }, [
                  h('Button', {
                    props: {
                      'type': 'error',
                      'size': 'small',
                      'icon': 'ios-trash-outline'
                    },
                    on: {
                      click: () => {
                        this.delete = true
                        this.close(params.row.id)
                        this.vGetNotifications()
                      }
                    }
                  })
                ])
              ]
              )
            }
          }
        ],
        notification_checked: false, // true - 현재 알림창 열림 / false - 현재 알림창 닫힘
        notifications: [], // 알림 목록
        delete: false // true - 알림창 close 시 알림 삭제 / false - 알림창 close 시 알림 삭제 X
      }
    },
    mounted () {
      this.init()
    },
    methods: {
      ...mapActions(['getProfile', 'changeModalStatus']),
      init () {
        this.getProfile()
        this.getOnlyNotificationsListLength()
      },
      handleRoute (route) {
        if (this.notification_checked) { // 변경될 때 마다 알림창을 닫음
          this.delete = false
          this.$Notice.destroy()
          this.notification_checked = false
        }
        if (route && route.indexOf('admin') < 0) {
          this.$router.push(route).catch(() => {}) // exception catch
        } else {
          window.open('/admin/')
        }
      },
      handleBtnClick (mode) {
        this.changeModalStatus({
          visible: true,
          mode: mode
        })
        this.handleRoute('login')
      },
      getOnlyNotificationsListLength () {
        // let li = []
        // api.getNotificationList().then(res => {
        //   li = res.data.data
        //   if (li === undefined || li === null || li.length <= 0) {
        //     this.init_notification_count = 0
        //   } else {
        //     this.init_notification_count = li.length
        //   }
        // })
        let li = []
        api.getReadNotification().then(res => { // 현재 접속한 유저의 알림을 전송 받음
          li = res.data.data
          if (li === undefined || li === null || li.length <= 0) {
            this.init_notification_count = 0
          } else {
            this.init_notification_count = li.length
          }
        })
      },
      changeNoti () {
        this.vGetNotifications()
        this.visivleDraw = true
      },
      vGetNotifications () {
        api.getNotificationList().then(res => {
          this.vNotifications = res.data.data
          this.getOnlyNotificationsListLength()
        })
      },
      close (notificationid) {
        if (this.delete) {
          api.deleteNotification(notificationid).then(res => { // 알림 고유 ID를 전송해 알림 삭제
            this.getOnlyNotificationsListLength()
          })
        }
      },
      goAllNotificationList () {
        this.visivleDraw = false
        this.$router.push({
          path: '/notification-list'
        })
      }
    },

    computed: {
      ...mapGetters(['website', 'modalStatus', 'user', 'isAuthenticated', 'isAdminRole', 'isVerifiedEmail']),
      activeMenu () {
        return '/' + this.$route.path.split('/')[1]
      },
      modalVisible: {
        get () {
          return this.modalStatus.visible
        },
        set (value) {
          this.changeModalStatus({visible: value})
        }
      }
    },
    watch: {
      init_notification_count: function (newVal, oldVal) {
        this.init_notification_count = newVal
      }
    }
  }
</script>

<style lang="less" scoped>
  #header {
    min-width: 300px;
    position: fixed;
    top: 0;
    left: 0;
    height: 60px;
    width: 100%;
    z-index: 1000;
    background-color: #fff;
    box-shadow: 0 1px 5px 0 rgba(0, 0, 0, 0.1);
    .oj-menu {
      //background: #404040;
      background: #fff;
    }
    .logo {
      margin-left: 2%;
      margin-right: 2%;
      font-size: 20px;
      float: left;
      line-height: 60px;
    }
    .logo > span > a, .bar_list{
      //color: white;
      color: #404040;
    }
    .home_bar{
        //color: white;
        color: #404040;
        font-size: 20px;
    }

    @media screen and (max-width : 900px) {
      .bar_list {
        visibility: hidden;
      }
    }
    @media screen and (min-width : 901px) {
      visibility: visible;
    }
    .bar_list {
      padding-right: 30px;
      padding-left: 30px;
      text-align: center;
    }
    .drop-menu {
      float: right;
      padding: 0 30px 0 30px;
      margin-right: 50px;
      position: fixed;
      right: 10px;
      //color: white;
      color: #404040;
      font-size: 18px;
      &-title {
        font-size: 20px;
      }
    }
    .btn-menu {
      display: block;
      position: fixed;
      font-size: 16px;
      float: right;
      margin-right: 10px;
    }
  }
  .modal {
    &-title {
      font-size: 18px;
      font-weight: 600;
    }
  }
  .alarm {
    float: right;
    position: fixed;
    right: 0;
    height: 40px;
    padding-top: 10px;
    margin-right: 20px;
  }
  .right-div {
    float: right;
    right: 0;
    padding: 0 0 0 0;
    position: fixed;
    width: 160px;
    height: 60px;
  }




// .dropdown {
//   float: left;
//   overflow: hidden;
// }

// .dropdown .dropbtn {
//   // font-size: 16px;  
//   border: none;
//   outline: none;
//   color: white;
//   // padding: 14px 16px;
//   background-color: #404040;
//   // font-family: inherit;
//   margin: 0;
// }

// // .navbar a:hover, .dropdown:hover .dropbtn {
// //   background-color: red;
// // }

// .dropdown-content {
//   display: none;
//   position: absolute;
  
//   background-color: #f9f9f9;
//   min-width: 160px;
//   // box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
//   z-index: 1;
// }

// .dropdown-content a {
//   float: none;
//   color: black;
//   padding-left: 10px;
//   // padding: 5px 7px;
//   text-decoration: none;
//   display: block;
//   text-align: left;
// }

// .dropdown-content a:hover {
//   background-color: #ddd;
// }

// .dropdown:hover .dropdown-content {
//   display: block;
// }


</style>