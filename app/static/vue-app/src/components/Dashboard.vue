<template>
  <div>
    <div>
      <label>Start Date:</label>
      <el-date-picker
        v-model="stocks.startDate"
        type="date"
        placeholder="Pick a day"
        format="yyyy-MM-dd"
        value-format="MM/dd/yyyy">
      </el-date-picker>      
    </div>
    <div>
      <label>End Date:</label>
      <el-date-picker
        v-model="stocks.endDate"
        type="date"
        placeholder="Pick a day"
        format="yyyy-MM-dd"
        value-format="MM/dd/yyyy">
      </el-date-picker>
    </div>
    <ticker-picker></ticker-picker>
  </div>
</template>

<script>
import TickerPicker from './TickerPicker.vue'
import { mapState } from 'vuex'

export default {
  name: 'dashboard',  
  components: {
    TickerPicker
  },
  computed: mapState(['stocks'])
}
</script>
