<template>
  <div id="app">
    <el-container>
      <el-container>
        <el-aside width="300px">
          <dashboard />
        </el-aside>
        <el-container>
          <!-- <el-header>Header</el-header> -->
          <el-main>
            <charts />
          </el-main>        
        </el-container>
      </el-container>
      <el-footer></el-footer>
    </el-container>    
  </div>
</template>

<script>
import Dashboard from './components/Dashboard.vue'
import Charts from './components/Charts.vue'

export default {
  name: 'app',
  components: {
    Dashboard, Charts
  }
}
</script>

<style>
  #app {
    font-family: Helvetica Neue, Arial, sans-serif;
    font-size: 14px;
    color: #444;
  }

  .el-header, .el-footer {
    background-color: #B3C0D1;
    color: #333;
    text-align: center;
    line-height: 60px;
  }
  
  .el-aside {
    background-color: #D3DCE6;
    color: #333;
    text-align: center;
    line-height: 50px;
  }
  
  .el-main {
    background-color: #E9EEF3;
    color: #333;
    text-align: center;
    line-height: 0;
  }
  
  body > .el-container {
    margin-bottom: 40px;
  }
  
  .el-container:nth-child(5) .el-aside,
  .el-container:nth-child(6) .el-aside {
    line-height: 260px;
  }
  
  .el-container:nth-child(7) .el-aside {
    line-height: 320px;
  }
</style>
