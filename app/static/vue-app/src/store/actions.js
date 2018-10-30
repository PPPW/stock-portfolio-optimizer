export default {
  addStock ({ commit }, { ticker, allocation }) {
    commit('addStock', {
      ticker: ticker,
      allocation: allocation
    })
  },

  removeStock ({ commit }, ticker) {    
    commit('removeStock', { ticker })
  },

  updateOptimization ({ commit }, { optimized_allocations }) {    
    commit('updateOptimization', { optimized_allocations: optimized_allocations })
  },

  changeDate({ commit }, { startDate, endDate }) {
    commit('removeStock', {  startDate, endDate })
  }
}