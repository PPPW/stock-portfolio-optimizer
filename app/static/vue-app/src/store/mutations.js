export default {
  addStock (state, { ticker, allocation }) {    
    state.stocks.tickers.push(ticker)
    state.stocks.allocations.push(allocation)
    state.optimized_allocations.push(allocation)
  },

  removeStock (state, { ticker }) {   
    let indexToRemove = state.stocks.tickers.indexOf(ticker)
    state.stocks.tickers.splice(indexToRemove, 1)
    state.stocks.allocations.splice(indexToRemove, 1)
    state.optimized_allocations.splice(indexToRemove, 1)
  },

  updateOptimization (state, { optimized_allocations }) {    
    state.optimized_allocations = optimized_allocations
  },

  changeDate(state, { startDate, endDate }) {
    state.stocks.startDate = startDate
    state.stocks.endDate = endDate
  }
}