import 'babel-polyfill'
import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from '@/store'
import i18n from '@/i18n'
import VueClipboard from 'vue-clipboard2'
import VueAnalytics from 'vue-analytics'
import { GOOGLE_ANALYTICS_ID } from '@/utils/constants'

// iview
import iView from 'iview'
import 'iview/dist/styles/iview.css'

import Panel from '@oj/components/Panel.vue'
import VerticalMenu from '@oj/components/verticalMenu/verticalMenu.vue'
import VerticalMenuItem from '@oj/components/verticalMenu/verticalMenu-item.vue'
import '@/styles/index.less'

import highlight from '@/plugins/highlight'
import katex from '@/plugins/katex'
import filters from '@/utils/filters.js'

import ECharts from 'vue-echarts'
import 'echarts-gl'
import * as ecStat from 'echarts-stat'
import * as echarts from 'echarts/core'
import { LineChart, BarChart, ScatterChart, EffectScatterChart } from 'echarts/charts'
import { GridComponent, TitleComponent, TooltipComponent, LegendComponent, DataZoomComponent } from 'echarts/components'
import { UniversalTransition } from 'echarts/features'
import { CanvasRenderer } from 'echarts/renderers'
// use([BarChart, GridComponent, CanvasRenderer])

import Element from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
// auto logout
// import IdleVue from 'idle-vue-3'
import '@mdi/font/css/materialdesignicons.css'
echarts.registerTransform(ecStat.transform.regression)
echarts.use([
  CanvasRenderer,
  TitleComponent,
  LineChart,
  BarChart,
  ScatterChart,
  GridComponent,
  TooltipComponent,
  EffectScatterChart,
  UniversalTransition,
  LegendComponent,
  DataZoomComponent
])
// register global utility filters.
Object.keys(filters).forEach(key => {
  Vue.filter(key, filters[key])
})

Vue.config.productionTip = false
const fixIdScrolling = {
  watch: {
    $route (to, from) {
      const currentRoute = this.$router.currentRoute
      const idToScrollTo = currentRoute.hash
      this.$nextTick(() => {
        if (idToScrollTo && document.querySelector(idToScrollTo)) {
          document.querySelector(idToScrollTo).scrollIntoView()
        }
      })
    }
  }
}

Vue.use(iView, {
  i18n: (key, value) => i18n.t(key, value)
})

Vue.use(VueClipboard)
Vue.use(highlight)
Vue.use(katex)
Vue.use(VueAnalytics, {
  id: GOOGLE_ANALYTICS_ID,
  router
})

// disable session expire
// const eventsHub = new Vue()
// Vue.use(IdleVue, {
//   eventEmitter: eventsHub,
//   store,
//   idleTime: 10000, // 10 seconds
//   startAtIdle: false
// })

Vue.component('ECharts', ECharts)
Vue.component(VerticalMenu.name, VerticalMenu)
Vue.component(VerticalMenuItem.name, VerticalMenuItem)
Vue.component(Panel.name, Panel)
Vue.use(Element, {
  i18n: (key, value) => i18n.t(key, value)
})
// 글로벌 메시지 알림 등록
Vue.prototype.$Message.config({
  duration: 2
})
Vue.prototype.$error = (s) => Vue.prototype.$Message.error(s)
Vue.prototype.$info = (s) => Vue.prototype.$Message.info(s)
Vue.prototype.$success = (s) => Vue.prototype.$Message.success(s)

new Vue(
  Vue.util.extend({mixins: [fixIdScrolling], router, store, i18n}, App)
).$mount('#app')
