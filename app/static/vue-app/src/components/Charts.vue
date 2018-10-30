<template>
  <div>
    <el-tabs type="border-card" v-model="activeName">
      <el-tab-pane label="Performance" name="line">        
        <line-chart :chart-data="lineData" v-if="activeName==='line'"></line-chart>
      </el-tab-pane>
      <el-tab-pane label="Portfolio" name="pie">
        <pie-chart :chart-data="pieData" v-if="activeName==='pie'"></pie-chart>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import LineChart from './LineChart.vue'
import PieChart from './PieChart.vue'
import axios from 'axios'
import { getColor } from '../utils/utils'
import { mapState, mapActions } from 'vuex'

export default {
    name: 'charts',
    components: { LineChart, PieChart },
    data () {
      return {
        lineData: {},        
        activeName: 'line'
      }        
    },
    mounted () {
      //this.debouncedRequestData = _.debounce(this.requestData, 500)     
      this.requestData() 
      this.$store.watch(state => state.stocks,
        () => {           
          this.requestData() 
        },
        { deep: true }
      )
    },
    computed: {
      ...mapState(['stocks', 'optimized_allocations']),      
      pieData() {        
        return {
          datasets: [{
            data: this.stocks.allocations, 
            backgroundColor: this.stocks.tickers.map((t,index) => getColor(index))
          }],
          labels: this.stocks.tickers
        } 
      }         
    },
    methods: {
      ...mapActions(['updateOptimization']),
      requestData () {       
        axios.get('api/opt', {
          params: this.stocks
        })
        .then(response => {          
          let lineDataset = [{
              label: 'My Portfolio',
              data: response.data.performance,            
            },
            {
              label: 'Optimized Portfolio',
              data: response.data.opt_performance,            
            },
            // TODO: add a benchmark, such as S&P 500
          ]

          lineDataset.forEach(function (value, index) {
            let color = getColor(index)
            lineDataset[index].backgroundColor = color
            lineDataset[index].borderColor = color
            lineDataset[index].fill = false
          })

          this.lineData = {           
            datasets: lineDataset,
            labels: response.data.date_range
          }    
          
          this.updateOptimization({optimized_allocations:response.data.opt_allocations})
        })
        .catch(error => { 
          this.$alert(error.response.data)          
          this.lineData = {           
            datasets: [],
            labels: []
          }
        })          
      }
    }
}
</script>
