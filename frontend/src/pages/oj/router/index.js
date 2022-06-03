import Vue from 'vue'
import VueRouter from 'vue-router'
import routes from './routes'
import storage from '@/utils/storage'
import {STORAGE_KEY} from '@/utils/constants'
import {sync} from 'vuex-router-sync'
import {types, default as store} from '../../../store'

Vue.use(VueRouter, store)

const router = new VueRouter({
  mode: 'history',
  scrollBehavior (to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return {x: 0, y: 0}
    }
  },
  routes
})

// 글로벌 신원 확인
router.beforeEach(async(to, from, next) => {
  Vue.prototype.$Loading.start()
  // if(storage === undefined) {
  //   storage = await import('../../../store/index')
  // }
  if (to.matched.some(record => record.meta.requiresAuth) && from.path.substring(0, 13) !== '/verify-email') {
    if (!storage.get(STORAGE_KEY.AUTHED)) {
      Vue.prototype.$error('Please login first')
      // store.commit(types.CHANGE_MODAL_STATUS, {mode: 'login', visible: true})
      next({
        path: '/login'
      })
    } else if (to.matched.some(record => record.meta.isEmailVerify)) {
      if (!store.getters['isVerifiedEmail'] && !store.getters['isAdminRole'] && !(from.path === '/logout')) {
        Vue.prototype.$error('Please verifying email')
        // store.commit(types.CHANGE_MODAL_STATUS, {mode: 'login', visible: true})
        next({
          path: '/apply-verify-email'
        })
      } else {
        next()
      }
    } else {
      next()
    }
  } else {
    next()
  }
  // else {
  //   next()
  // }
})

router.afterEach((to, from, next) => {
  Vue.prototype.$Loading.finish()
})
sync(store, router)
export default router
