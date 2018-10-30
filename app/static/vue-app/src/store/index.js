import Vue from 'vue'
import Vuex from 'vuex'
import mutations from './mutations'
import actions from './actions'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    // TODO: initialize in a proper place
    stocks: {
      tickers: ['GOOG', 'AAPL', 'AMZN'],
      allocations: [0.5, 0.3, 0.2],   
      startDate: (new Date(new Date().setFullYear(new Date().getFullYear() - 1))).toLocaleDateString(),
      endDate: (new Date()).toLocaleDateString()
    },
    optimized_allocations: [0, 0, 0],
  },
  actions,
  mutations
})