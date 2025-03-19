<template>
  <div class="system-monitor">
    <div class="monitor-header">
      <h3>系统资源监控</h3>
      <div class="refresh-control">
        <label class="auto-refresh">
          <input type="checkbox" v-model="autoRefresh">
          <span>自动刷新</span>
        </label>
        
        <select v-model="refreshRate" :disabled="!autoRefresh">
          <option value="5000">5秒</option>
          <option value="10000">10秒</option>
          <option value="30000">30秒</option>
          <option value="60000">1分钟</option>
        </select>
      </div>
    </div>
    
    <div class="charts-container">
      <div class="chart-wrapper">
        <h4>CPU使用率</h4>
        <div class="chart" ref="cpuChart"></div>
      </div>
      
      <div class="chart-wrapper">
        <h4>内存使用率</h4>
        <div class="chart" ref="memoryChart"></div>
      </div>
      
      <div class="chart-wrapper">
        <h4>磁盘使用率</h4>
        <div class="chart" ref="diskChart"></div>
      </div>
      
      <div class="chart-wrapper">
        <h4>网络流量</h4>
        <div class="chart" ref="networkChart"></div>
      </div>
    </div>
    
    <div class="system-details">
      <div class="detail-item">
        <div class="label">操作系统</div>
        <div class="value">{{ systemInfo.platform.system }} {{ systemInfo.platform.release }}</div>
      </div>
      
      <div class="detail-item">
        <div class="label">处理器</div>
        <div class="value">{{ processorInfo }}</div>
      </div>
      
      <div class="detail-item">
        <div class="label">Python</div>
        <div class="value">{{ systemInfo.python }}</div>
      </div>
      
      <div class="detail-item">
        <div class="label">上线时间</div>
        <div class="value">{{ uptimeFormatted }}</div>
      </div>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts/core';
import { LineChart } from 'echarts/charts';
import {
  TitleComponent,
  TooltipComponent,
  GridComponent,
  DataZoomComponent,
  LegendComponent
} from 'echarts/components';
import { CanvasRenderer } from 'echarts/renderers';
import { getSystemInfo } from '@/api/system';
import { formatDuration } from '@/utils/time';
import webSocketService from '@/api/websocket';

echarts.use([
  TitleComponent,
  TooltipComponent,
  GridComponent,
  DataZoomComponent,
  LegendComponent,
  LineChart,
  CanvasRenderer
]);

export default {
  name: 'SystemMonitor',
  props: {
    systemInfo: {
      type: Object,
      required: true
    },
    uptime: {
      type: Number,
      default: 0
    }
  },
  data() {
    return {
      cpuChart: null,
      memoryChart: null,
      diskChart: null,
      networkChart: null,
      cpuData: [],
      memoryData: [],
      diskData: [],
      networkInData: [],
      networkOutData: [],
      timeData: [],
      autoRefresh: true,
      refreshRate: 10000,
      refreshTimer: null,
      maxDataPoints: 20,
      wsConnected: false
    };
  },
  computed: {
    processorInfo() {
      return `${this.systemInfo.cpu.cores} 核心 / ${this.systemInfo.cpu.percent.toFixed(1)}% 使用率`;
    },
    uptimeFormatted() {
      return formatDuration(this.uptime);
    }
  },
  methods: {
    initCharts() {
      this.cpuChart = echarts.init(this.$refs.cpuChart);
      this.memoryChart = echarts.init(this.$refs.memoryChart);
      this.diskChart = echarts.init(this.$refs.diskChart);
      this.networkChart = echarts.init(this.$refs.networkChart);
      
      this.updateChartData();
      this.renderCharts();
      
      window.addEventListener('resize', this.resizeCharts);
    },
    resizeCharts() {
      this.cpuChart && this.cpuChart.resize();
      this.memoryChart && this.memoryChart.resize();
      this.diskChart && this.diskChart.resize();
      this.networkChart && this.networkChart.resize();
    },
    updateChartData() {
      const now = new Date();
      const timeStr = now.toLocaleTimeString();
      
      // 添加新数据点
      this.timeData.push(timeStr);
      this.cpuData.push(this.systemInfo.cpu.percent);
      this.memoryData.push(this.systemInfo.memory.percent);
      this.diskData.push(this.systemInfo.disk.percent);
      
      // 模拟网络数据（实际应当从API获取）
      const sent = Math.random() * 100;
      const received = Math.random() * 150;
      this.networkInData.push(received / 1024); // KB
      this.networkOutData.push(sent / 1024); // KB
      
      // 限制数据点数量
      if (this.timeData.length > this.maxDataPoints) {
        this.timeData.shift();
        this.cpuData.shift();
        this.memoryData.shift();
        this.diskData.shift();
        this.networkInData.shift();
        this.networkOutData.shift();
      }
    },
    renderCharts() {
      // CPU图表
      const cpuOption = {
        tooltip: {
          trigger: 'axis'
        },
        xAxis: {
          type: 'category',
          data: this.timeData
        },
        yAxis: {
          type: 'value',
          min: 0,
          max: 100,
          axisLabel: {
            formatter: '{value}%'
          }
        },
        series: [{
          data: this.cpuData,
          type: 'line',
          smooth: true,
          areaStyle: {
            opacity: 0.2
          },
          lineStyle: {
            width: 2
          },
          itemStyle: {
            color: '#4361ee'
          },
          name: 'CPU使用率'
        }]
      };
      
      // 内存图表
      const memoryOption = {
        tooltip: {
          trigger: 'axis'
        },
        xAxis: {
          type: 'category',
          data: this.timeData
        },
        yAxis: {
          type: 'value',
          min: 0,
          max: 100,
          axisLabel: {
            formatter: '{value}%'
          }
        },
        series: [{
          data: this.memoryData,
          type: 'line',
          smooth: true,
          areaStyle: {
            opacity: 0.2
          },
          lineStyle: {
            width: 2
          },
          itemStyle: {
            color: '#3f83f8'
          },
          name: '内存使用率'
        }]
      };
      
      // 磁盘图表
      const diskOption = {
        tooltip: {
          trigger: 'axis'
        },
        xAxis: {
          type: 'category',
          data: this.timeData
        },
        yAxis: {
          type: 'value',
          min: 0,
          max: 100,
          axisLabel: {
            formatter: '{value}%'
          }
        },
        series: [{
          data: this.diskData,
          type: 'line',
          smooth: true,
          areaStyle: {
            opacity: 0.2
          },
          lineStyle: {
            width: 2
          },
          itemStyle: {
            color: '#14b8a6'
          },
          name: '磁盘使用率'
        }]
      };
      
      // 网络图表
      const networkOption = {
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: ['上传', '下载']
        },
        xAxis: {
          type: 'category',
          data: this.timeData
        },
        yAxis: {
          type: 'value',
          axisLabel: {
            formatter: '{value}KB/s'
          }
        },
        series: [
          {
            name: '上传',
            type: 'line',
            smooth: true,
            data: this.networkOutData,
            itemStyle: {
              color: '#f43f5e'
            }
          },
          {
            name: '下载',
            type: 'line',
            smooth: true,
            data: this.networkInData,
            itemStyle: {
              color: '#8b5cf6'
            }
          }
        ]
      };
      
      this.cpuChart.setOption(cpuOption);
      this.memoryChart.setOption(memoryOption);
      this.diskChart.setOption(diskOption);
      this.networkChart.setOption(networkOption);
    },
    async fetchSystemInfo() {
      try {
        const response = await getSystemInfo();
        this.systemInfo = response;
        this.updateChartData();
        this.renderCharts();
      } catch (error) {
        console.error('获取系统信息失败:', error);
      }
    },
    startRealTimeMonitoring() {
      // 停止之前的定时器
      this.stopRealTimeMonitoring();
      
      // 注册WebSocket事件处理程序
      webSocketService.on('system_stats', this.handleSystemStats);
      
      // 如果未连接WebSocket，则连接
      if (!webSocketService.connected) {
        webSocketService.connect();
      }
      
      // 请求开始实时监控
      webSocketService.send('subscribe', {
        channel: 'system_stats',
        interval: parseInt(this.refreshRate)
      });
      
      // 保留一个后备定时器，以防WebSocket失败
      this.refreshTimer = setInterval(() => {
        if (!webSocketService.connected) {
          this.$emit('refresh');
        }
      }, parseInt(this.refreshRate));
    },
    stopRealTimeMonitoring() {
      if (this.refreshTimer) {
        clearInterval(this.refreshTimer);
        this.refreshTimer = null;
      }
      
      // 取消WebSocket订阅
      if (webSocketService.connected) {
        webSocketService.send('unsubscribe', {
          channel: 'system_stats'
        });
      }
    },
    restartRealTimeMonitoring() {
      this.stopRealTimeMonitoring();
      this.startRealTimeMonitoring();
    },
    handleSystemStats(data) {
      if (!data || !data.cpu) return;
      
      const now = new Date();
      const timeStr = now.toLocaleTimeString();
      
      // 更新图表数据
      this.timeData.push(timeStr);
      this.cpuData.push(data.cpu.percent);
      this.memoryData.push(data.memory.percent);
      this.diskData.push(data.disk.percent);
      
      if (data.network) {
        this.networkInData.push(data.network.bytes_recv / 1024); // KB
        this.networkOutData.push(data.network.bytes_sent / 1024); // KB
      }
      
      // 保持数据点数量合理
      const maxPoints = 20;
      if (this.timeData.length > maxPoints) {
        this.timeData.shift();
        this.cpuData.shift();
        this.memoryData.shift();
        this.diskData.shift();
        this.networkInData.shift();
        this.networkOutData.shift();
      }
      
      // 更新图表
      this.renderCharts();
    }
  },
  watch: {
    autoRefresh(newValue) {
      if (newValue) {
        this.startRealTimeMonitoring();
      } else {
        this.stopRealTimeMonitoring();
      }
    },
    refreshRate() {
      if (this.autoRefresh) {
        this.restartRealTimeMonitoring();
      }
    },
    systemInfo: {
      deep: true,
      handler() {
        this.updateChartData();
        this.renderCharts();
      }
    }
  },
  mounted() {
    this.initCharts();
    if (this.autoRefresh) {
      this.startRealTimeMonitoring();
    }
  },
  beforeDestroy() {
    this.stopRealTimeMonitoring();
    window.removeEventListener('resize', this.resizeCharts);
    
    // 清理WebSocket监听器
    webSocketService.off('system_stats');
  }
}
</script>

<style scoped>
.system-monitor {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  padding: 16px;
  margin-bottom: 24px;
}

.monitor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

h3 {
  margin: 0;
}

.refresh-control {
  display: flex;
  align-items: center;
  gap: 12px;
}

.auto-refresh {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
}

select {
  padding: 6px;
  border: 1px solid #e1e5eb;
  border-radius: 4px;
}

.charts-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin-bottom: 16px;
}

.chart-wrapper {
  border: 1px solid #e1e5eb;
  border-radius: 6px;
  padding: 12px;
}

h4 {
  margin-top: 0;
  margin-bottom: 12px;
  font-size: 14px;
  color: #4a5568;
}

.chart {
  height: 200px;
  width: 100%;
}

.system-details {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.detail-item {
  background: #f7fafc;
  border-radius: 6px;
  padding: 12px;
}

.label {
  font-size: 12px;
  color: #718096;
  margin-bottom: 6px;
}

.value {
  font-weight: 500;
  color: #2d3748;
}
</style> 