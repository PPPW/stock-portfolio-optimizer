<script>
  import { Line, mixins } from 'vue-chartjs'

  const { reactiveProp } = mixins

  export default {
    extends: Line,
    mixins: [reactiveProp],
    data () {
      return {        
        options: {
          //showScale: true,
          scales: { 
              xAxes: [{
                  type: 'time',
                  time: {
                      parser: 'YYYY-MM-DD',
                      unit: 'day',
                      displayFormats: {
                          day: 'YYYY-MM-DD'
                      },
                    },
              }],
              //yAxes: [ ]
            },
          //tooltips: { },
          //legend: { display: false },
          elements: { line: { tension: 0 } },
          responsive: true,
          maintainAspectRatio: false
        }
      }
    },
    mounted () {         
      this.renderChart(this.chartData, this.options)      
    },
  }
</script>
