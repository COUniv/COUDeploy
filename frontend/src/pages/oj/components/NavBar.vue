<template>
  <div id="header">

    <Menu theme="light" mode="horizontal" @on-select="handleRoute" :active-name="activeMenu" class="oj-menu">
      <!-- <div class="logo"> -->
        
      <Menu-item class="home_bar" name="/" >COU</Menu-item>
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
        <div class="login_menu">
          <Button type="text"
                  ref="loginBtn"
                  shape="circle"
                  @click="goLogin"
                  style="line-height:50%;">
                  <p>{{$t('m.Login')}}</p>
          </Button>
          <!-- <Button v-if="website.allow_register"
                  type="text"
                  shape="circle"
                  @click="handleBtnClick('register')"
                  style="margin-left: 5px;">
                  <p>{{$t('m.Register')}}</p>
          </Button> -->
        </div>
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
        <div class="right_menu">
          <!-- 알림 출력 버튼 -->
          <div class="alarm">
            <Badge dot v-if="init_notification_count > 0" class="alram-box">
              <Button type="text" class="bell bells" size="large" @click="changeNoti" @mouseover.native="alarmHoverForActive" @mouseleave.native="alarmHoverForNoActive">
                <i v-bind:class="AlarmHoverActive" style="padding-bottom:5px"></i>
              </Button>
              <!-- <Icon type="ios-notifications" /> -->
            </Badge>
            
            <Badge v-else>
              <Button type="text" class="bell bells" size="large" @click="changeNoti" @mouseover.native="alarmHoverForActive" @mouseleave.native="alarmHoverForNoActive">
                <i v-bind:class="AlarmHoverActive" style="padding-bottom:5px"></i>
              </Button>
            </Badge>
          </div>
            <!--사용자 아이디 출력-->
          <div @click="viewModal" @blur="visibleAccount = false" class="account_tab"> <!--/setting/mypage-->
            <Icon type="md-contact" size="30" color="#5030E5"/>
            <span class="username">{{ user.username }}</span>
          </div>
          <div style="clear:both"></div>
          <div v-if="visibleAccount" class="account_modal" v-click-outside="closeModal">
            <div class="profile">
              <div class="photo">
                <Icon type="md-contact" size="100" color="#5030E5"/>
              </div>
              <div class="name">{{ user.username }}</div>
              <div class="email">root@gmail.com</div>
            </div>
            <div class="mypage_btn" @click="goMySettingPage">계정관리</div>
            <div class="line"></div>
            <div class="logout_btn" @click="goLogOut">로그아웃</div>
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
    <Modal v-model="modalVisible" :width="430">
      <div slot="header" class="modal-title">인증이 필요해요!</div>
      <component :is="modalStatus.mode" v-if="modalVisible"></component>
      <div slot="footer" style="display: none"></div>
    </Modal>
  </div>
</template>

<script>
  import { mapGetters, mapActions } from 'vuex'
  import GuardMessage from '@oj/views/user/GuardMessage.vue'
  import api from '@oj/api'
  import vClickOutside from 'v-click-outside'
  export default {
    directives: {
      clickOutside: vClickOutside.directive
    },
    components: {
      GuardMessage
    },
    data () {
      return {
        alarmHoverActive: false,
        init_notification_count: 0,
        emptyChar: '알람이 존재하지 않습니다.',
        showHeaderandborder: false,
        dishovering: true,
        visivleDraw: false,
        visibleAccount: false,
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
      handleBtnClick () {
        this.changeModalStatus({
          visible: true,
          mode: 'GuardMessage'
        })
        this.handleRoute('GuardMessage')
      },
      goLogOut () {
        this.$router.push({path: '/logout'}).catch(() => {})
      },
      goMySettingPage () {
        this.$router.push({name: 'my-page'}).catch(() => {})
      },
      goLogin () {
        this.$router.push({path: '/login'}).catch(() => {})
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
      viewModal () {
        this.visibleAccount = !this.visibleAccount
      },
      closeModal () {
        if (this.visibleAccount === true) {
          this.visibleAccount = false
        }
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
        }).catch(() => {})
      },
      alarmHoverForActive () {
        this.alarmHoverActive = true
      },
      alarmHoverForNoActive () {
        this.alarmHoverActive = false
      }
    },

    computed: {
      ...mapGetters(['website', 'modalStatus', 'user', 'isAuthenticated', 'isAdminRole', 'isVerifiedEmail']),
      AlarmHoverActive () {
        if (this.alarmHoverActive) {
          return 'ivu-icon ivu-icon-ios-notifications'
        } else {
          return 'ivu-icon ivu-icon-ios-notifications-outline'
        }
      },
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
      },
      '$route' (to, from) {
        if (this.visibleAccount !== false) {
          this.visibleAccount = false
        }
      }
    }
  }
</script>
<style lang="less">
  .alram-box {
    .ivu-badge-dot {
      top: 5px !important;
      right: 5px !important;
    }
  }
  .bells {
    &.ivu-btn:hover {
      border-color: #fff;
    }
    &.ivu-btn:focus {
      border-color: transparent;
      box-shadow: none;
    }
  }
</style>
<style lang="less" scoped>
@import '../../../styles/common.less';

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
      position: relative;
      background: @white;
    }
    .logo {
      margin-left: 2%;
      margin-right: 2%;
      font-size: 20px;
      float: left;
      line-height: 60px;
    }
    .logo > span > a, .bar_list{
      color: @black;
      font-weight: @weight-regular;
    }
    .home_bar{
        color: @purple;
        font-size: @font-medium;
        font-weight: @weight-bold;
        -webkit-text-stroke: 1.5px;
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
      //margin-right: 50px;
      //position: fixed;
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
    // top: 0;
    // height: 40px;
    line-height: 50%;
    float: right;
    margin-right: 10px;
    .bell {
      color: @purple;
      font-size: 1.5em;
    }
  }
  .login_menu {
    overflow:hidden;
    float: right;
    padding: 0 30px;
    // position: fixed;
    height: 60px;
    padding: 0 60px;
    button {
      border: 2px solid @light-gray;
      border-radius: 5px;
      height: 40px;
      padding: 20px;
      font-weight: @weight-bold;
      &:hover {
        box-shadow: 0 1px 5px 0 rgba(90, 82, 128, 0.31);
        color: @purple;
      }
    }
  }
  .right_menu {
    display: flex;
    align-items: center;
    justify-content: center;
    line-height: 50%;
    overflow:hidden;
    float: right;
    padding: 0px 30px;
    // position: fixed;
    height: 60px;
    margin-right: 5px;
    .account_tab {
      &:hover {
        cursor: pointer;
        border: 1.5px solid @purple;
      }
      float: right;
      line-height: 50%;
      height: 45px;
      // vertical-align: middle;
      // top: 8px;
      // right: 20px;
      color: @purple;
      font-weight: 600;
      padding: 5px 7px 5px 5px;
      border: 1.5px solid #fff;
      border-radius: @size-border-radius;
      -webkit-transition: all .2s ease-in;
      -moz-transition: all .2s ease-in;
      -ms-transition: all .2s ease-in;
      -o-transition: all .2s ease-in;
      transition: all .2s ease-in;
      span {
        -webkit-text-stroke: 0.5px;
      }
    }
    .account_modal {
      position: absolute;
      display:flex;
      flex-direction: column;
      justify-content: space-between;
      align-items: center;
      border-radius: @size-border-radius;
      padding: 24px;
      top: 60px;
      right: 20px;
      width: 300px;
      min-width: 250px;
      height: 340px;
      min-height: 300px;
      background-color: @white;
      color: @black;
      box-shadow: 2px 5px 20px 2px rgba(90, 82, 128, 0.31);
      .profile {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: center;
        height: 150px;
        .name {
          color: @purple;
          font-size: @font-medium;
          font-weight: @weight-semi-bold;
        }
        .email {
          color: @gray;
          font-size: @font-small;
          margin-top: 10px;
        }
      }
      .mypage_btn {
        border: 2px solid @gray;
        border-radius: 20px;
        width: 40%;
        padding: 12px;
        margin: 10px 0;
        color: @gray;
        font-size: @font-micro;
        font-weight: @weight-bold;
        text-align: center;
        -webkit-transition: all .2s ease-in;
        -moz-transition: all .2s ease-in;
        -ms-transition: all .2s ease-in;
        -o-transition: all .2s ease-in;
        transition: all .2s ease-in;
        &:hover {
          cursor: pointer;
          border: 2px solid @purple;
          background-color: @purple;
          color: @white;
        }
      }

      .line {
        width: 100%;
        height: 2px;
        background-color: @light-gray;
      }
      .logout_btn {
        border: 2px solid @gray;
        border-radius: @size-border-radius;
        width: 80%;
        margin-top: 20px;
        padding: 15px;
        color: @gray;
        font-size: @font-small;
        font-weight: @weight-bold;
        text-align: center;
        // transition area
        -webkit-transition: all .2s ease-in;
        -moz-transition: all .2s ease-in;
        -ms-transition: all .2s ease-in;
        -o-transition: all .2s ease-in;
        transition: all .2s ease-in;
        &:hover {
          cursor: pointer;
          border: 2px solid @purple;
          background-color: @purple;
          color: @white;
        }
      }
    }
  }
  .username {
    height: 100%;
    line-height:30px;
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