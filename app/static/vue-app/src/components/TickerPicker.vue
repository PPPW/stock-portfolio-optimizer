<template>
  <div>
    <!-- TODO: change to autocomplete -->
    <el-input
      placeholder="Search"
      prefix-icon="el-icon-search"
      v-model="tickerSearch"
      @keyup.enter.native="addStockClick(tickerSearch)">
    </el-input>
    <table v-if="stocks.tickers.length" class="el-table el-table--border">
      <thead>
        <tr>
          <th v-for="(key, index) in header" :key="index">
            {{ key }}
          </th>
          <th />
        </tr>
      </thead>
      <tbody>
        <tr v-for="(ticker, index) in stocks.tickers" :key="index">
          <td>
            {{ ticker }}
          </td>
          <td>
            <el-input            
              v-model="stocks.allocations[index]">
            </el-input>
          </td>
          <td>
            {{ optimized_allocations[index] }}
          </td>          
          <td>
            <el-button type="default" icon="el-icon-delete" 
              @click="removeStock(ticker)">
            </el-button>
          </td>
        </tr>
      </tbody>
    </table>
    <p v-else>
      No data.
    </p>    
  </div>
</template>

<script>
import axios from 'axios'
import { mapState, mapActions } from 'vuex'

export default {
    name: 'ticker-picker',
    data() {
      return {
        tickerSearch: '',        
        header: [ 'Ticker', 'Allocation', 'Optimized' ]        
      }
    },
    computed: mapState(['stocks', 'optimized_allocations']),
    methods: {
      ...mapActions(['addStock', 'removeStock']),
      addStockClick(tickerSearch) {    
        if (tickerSearch === '') return
        let contained = false
        for (let i in this.stocks.tickers) {            
          if (this.stocks.tickers[i] === tickerSearch) {
            contained = true
            break
          }
        }
        if (contained) {
          this.$alert('"' + tickerSearch + '" is already in the portfolio.')
          return
        }
        axios.get('api/ticker', {
          params: { ticker: tickerSearch }
        })
        .then(response => {          
          if(response.data.exist)
            this.addStock({ ticker: tickerSearch, allocation: 0})
          else {
            this.$alert('Ticker not found: ' + tickerSearch)
          }
        })        
      }
    }
}
</script>

<style>
  .el-table th {
    text-align: center
  }
</style>