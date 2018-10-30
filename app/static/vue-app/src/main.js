import Vue from 'vue'
import lang from 'element-ui/lib/locale/lang/en';
import locale from 'element-ui/lib/locale';
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css'

import App from './App.vue'
import store from './store'


Vue.config.productionTip = false

locale.use(lang)
Vue.use(ElementUI)

new Vue({
  store,
  render: h => h(App)
}).$mount('#app')
