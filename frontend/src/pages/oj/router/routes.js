// all routes here.
import {
  About,
  ACMRank,
  Announcements,
  ApplyResetPassword,
  ApplyVerifyEmail,
  Languages,
  Home,
  NotFound,
  OIRank,
  Problem,
  ProblemList,
  ResetPassword,
  SubmissionDetails,
  SubmissionList,
  UserHome,
  VerifyEmail,
  ArticleList,
  CreateArticle,
  Article,
  Notification,
  AnnouncementList
} from '../views'
import Logout from '../views/user/Logout.vue'
import StartLogin from '../views/create_pages/Start_Login.vue'
// import FreeBoard from '../views/board_pages/Free_Board.vue'
// import RequestBoard from '../views/board_pages/Request_Board.vue'
// import QuestionBoard from '../views/board_pages/Question_Board.vue'
import SolveSubmit from '../views/solve_submit_pages/solve_submit.vue'
import * as Contest from '@oj/views/contest'
import * as Setting from '@oj/views/setting'

export default [
  {
    name: 'notification-list',
    path: '/notification-list',
    meta: {requiresAuth: true, isEmailVerify: true, title: 'notification-list'},
    component: Notification
  },
  // {
  //   name: 'StartLogin',
  //   path: '/',
  //   meta: {title: 'StartLogin'},
  //   component: StartLogin
  // },
  {
    name: 'start-login',
    path: '/login',
    meta: {title: 'StartLogin'},
    component: StartLogin
  },
  {
    name: 'solve-submit',
    path: '/solve-submit/:problemID',
    meta: {requiresAuth: true, title: 'Solve Submit'},
    component: SolveSubmit
  },

  // {
  //   name: 'Free_Board',
  //   path: '/Free_Board',
  //   meta: {requiresAuth: true, title: 'Free_Board'},
  //   component: FreeBoard
  // },
  // {
  //   name: 'Request_Board',
  //   path: '/Request_Board',
  //   meta: {requiresAuth: true, title: 'Request_Board'},
  //   component: RequestBoard
  // },
  // {
  //   name: 'Question_Board',
  //   path: '/Question_Board',
  //   meta: {requiresAuth: true, title: 'Question_Board'},
  //   component: QuestionBoard
  // },
  {
    path: '/article/modify/:articleID',
    name: 'modify-article',
    meta: {requiresAuth: true, isEmailVerify: true, title: 'Article Modify'},
    component: CreateArticle
  },
  {
    name: 'article-details',
    path: '/article/:articleID',
    meta: {requiresAuth: true, isEmailVerify: true, title: 'Article Details'},
    component: Article
  },
  {
    name: 'article-list',
    path: '/article-list',
    meta: {requiresAuth: true, isEmailVerify: true, title: 'Article List'},
    component: ArticleList
  },
  {
    name: 'create-article',
    path: '/create-article',
    meta: {requiresAuth: true, isEmailVerify: true, title: 'Create Article'},
    component: CreateArticle
  },
  {
    name: 'apply-verify-email',
    path: '/apply-verify-email',
    meta: {requiresAuth: true, title: 'Apply Verify Email'},
    component: ApplyVerifyEmail
  },
  {
    name: 'verify-email',
    path: '/verify-email/:token',
    meta: {requiresAuth: true, title: 'Verify Email'},
    component: VerifyEmail
  },
  {
    name: 'home',
    path: '/',
    meta: {requiresAuth: true, isEmailVerify: true, title: 'Home'},
    alias: '/main-announcement',
    component: Home
  },
  {
    name: 'announcement-list',
    path: '/announcement-list',
    meta: {requiresAuth: true, isEmailVerify: true, title: 'Announcement List'},
    component: AnnouncementList
  },
  {
    name: 'logout',
    path: '/logout',
    meta: {requiresAuth: true, title: 'Logout'},
    component: Logout
  },
  {
    name: 'apply-reset-password',
    path: '/apply-reset-password',
    meta: {title: 'Apply Reset Password'},
    component: ApplyResetPassword
  },
  {
    name: 'reset-password',
    path: '/reset-password/:token',
    meta: {title: 'Reset Password'},
    component: ResetPassword
  },
  {
    name: 'problem-list',
    path: '/problem',
    meta: {requiresAuth: true, isEmailVerify: true, title: 'Problem List'},
    component: ProblemList
  },
  {
    name: 'problem-details',
    path: '/problem/:problemID',
    meta: {requiresAuth: true, isEmailVerify: true, title: 'Problem Details'},
    component: Problem
  },
  {
    name: 'submission-list',
    path: '/status',
    meta: {requiresAuth: true, isEmailVerify: true, title: 'Submission List'},
    component: SubmissionList
  },
  {
    name: 'submission-details',
    path: '/status/:id/',
    meta: {requiresAuth: true, isEmailVerify: true, tle: 'Submission Details'},
    component: SubmissionDetails
  },
  {
    name: 'contest-list',
    path: '/contest',
    meta: {requiresAuth: true, isEmailVerify: true, title: 'Contest List'},
    component: Contest.ContestList
  },
  {
    name: 'contest-details',
    path: '/contest/:contestID/',
    component: Contest.ContestDetails,
    meta: {requiresAuth: true, isEmailVerify: true, title: 'Contest Details'},
    children: [
      {
        name: 'contest-submission-list',
        path: 'submissions',
        component: SubmissionList
      },
      {
        name: 'contest-problem-list',
        path: 'problems',
        component: Contest.ContestProblemList
      },
      {
        name: 'contest-problem-details',
        path: 'problem/:problemID/',
        component: Problem
      },
      {
        name: 'solve-submit',
        path: '/solve-submit/:problemID/',
        meta: {requiresAuth: true, title: 'Solve Submit'},
        component: SolveSubmit
      },
      {
        name: 'contest-announcement-list',
        path: 'announcements',
        component: Announcements
      },
      {
        name: 'contest-rank',
        path: 'rank',
        component: Contest.ContestRank
      },
      {
        name: 'acm-helper',
        path: 'helper',
        component: Contest.ACMContestHelper
      }
    ]
  },
  {
    name: 'acm-rank',
    path: '/acm-rank',
    meta: {requiresAuth: true, isEmailVerify: true, title: 'ACM Rankings'},
    component: ACMRank
  },
  {
    name: 'oi-rank',
    path: '/oi-rank',
    meta: {requiresAuth: true, isEmailVerify: true, title: 'OI Rankings'},
    component: OIRank
  },
  {
    name: 'user-home',
    path: '/user-home',
    component: UserHome,
    meta: {requiresAuth: true, title: 'User Home'}
  },
  {
    path: '/setting',
    component: Setting.Settings,
    children: [
      {
        name: 'default-setting',
        path: '',
        meta: {requiresAuth: true, title: 'Default Settings'},
        component: Setting.ProfileSetting
      },
      {
        name: 'comment-list',
        path: 'comment',
        meta: {requiresAuth: true, title: 'Comment List'},
        component: Setting.AccountArticleList
      },
      {
        name: 'like-list',
        path: 'like',
        meta: {requiresAuth: true, title: 'Like List'},
        component: Setting.AccountArticleList
      },
      {
        name: 'profile-setting',
        path: 'profile',
        meta: {requiresAuth: true, title: 'Profile Settings'},
        component: Setting.ProfileSetting
      },
      {
        name: 'account-setting',
        path: 'account',
        meta: {requiresAuth: true, title: 'Account Settings'},
        component: Setting.AccountSetting
      },
      {
        name: 'security-setting',
        path: 'security',
        meta: {requiresAuth: true, isEmailVerify: true, title: 'Security Settings'},
        component: Setting.SecuritySetting
      },
      {
        name: 'my-page',
        path: 'mypage',
        meta: {requiresAuth: true, title: 'My Page'},
        component: Setting.MyPage
      }
    ]
  },
  {
    path: '/help',
    name: 'help',
    meta: {requiresAuth: true, isEmailVerify: true, title: 'About'},
    component: About
  },
  {
    path: '/languages',
    name: 'languages',
    meta: {requiresAuth: true, isEmailVerify: true, title: 'languages'},
    component: Languages
  },
  {
    path: '*',
    meta: {title: '404'},
    component: NotFound
  }
]
