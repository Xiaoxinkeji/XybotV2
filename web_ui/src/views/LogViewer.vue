<template>
  <div class="log-viewer">
    <div class="page-header">
      <h1>运行日志</h1>
      <div class="header-actions">
        <div class="filters">
          <select v-model="logLevel" class="filter-select">
            <option value="ALL">所有级别</option>
            <option value="DEBUG">调试</option>
            <option value="INFO">信息</option>
            <option value="WARNING">警告</option>
            <option value="ERROR">错误</option>
            <option value="CRITICAL">严重</option>
          </select>
          
          <input 
            type="text" 
            v-model="searchQuery" 
            placeholder="搜索日志内容..." 
            class="search-input"
          />
        </div>
        
        <div class="btn-group">
          <button @click="refreshLogs" class="btn btn-outline">
            <i class="icon-refresh"></i> 刷新
          </button>
          
          <button @click="downloadLogs" class="btn btn-outline">
            <i class="icon-download"></i> 导出
          </button>
          
          <button @click="clearSearch" class="btn btn-outline" :disabled="!hasFilters">
            <i class="icon-x"></i> 清除筛选
          </button>
        </div>
      </div>
    </div>
    
    <div class="logs-container" v-if="!isLoading">
      <div class="log-entries">
        <virtual-list
          class="list"
          :data-key="'id'"
          :data-sources="filteredLogs"
          :data-component="logEntryComponent"
          :estimate-size="60"
          :item-class="'log-entry-wrapper'"
          :keeps="30"
        />
      </div>
    </div>
    
    <div class="loading-state" v-else>
      <div class="spinner"></div>
      <p>加载日志中...</p>
    </div>
    
    <!-- 日志详情模态框 -->
    <modal v-if="selectedLog" @close="selectedLog = null">
      <template #header>
        <h3>日志详情</h3>
      </template>
      
      <template #body>
        <div class="log-detail">
          <div class="detail-header">
            <div class="badge" :class="selectedLog.level.toLowerCase()">
              {{ selectedLog.level }}
            </div>
            <div class="timestamp">{{ formatTimestamp(selectedLog.timestamp) }}</div>
          </div>
          
          <div class="detail-message">{{ selectedLog.message }}</div>
          
          <div class="detail-metadata" v-if="selectedLog.metadata">
            <h4>元数据</h4>
            <pre>{{ JSON.stringify(selectedLog.metadata, null, 2) }}</pre>
          </div>
          
          <div class="detail-traceback" v-if="selectedLog.traceback">
            <h4>错误堆栈</h4>
            <pre class="traceback">{{ selectedLog.traceback }}</pre>
          </div>
        </div>
      </template>
    </modal>
  </div>
</template>

<script>
import Modal from '@/components/ui/Modal.vue';
import { getLogs } from '@/api/logs';
import LogEntry from '@/components/logs/LogEntry.vue';
import VirtualList from 'vue-virtual-scroll-list';

export default {
  name: 'LogViewer',
  components: {
    Modal,
    VirtualList
  },
  data() {
    return {
      isLoading: true,
      logs: [],
      selectedLog: null,
      logLevel: 'ALL',
      searchQuery: '',
      autoRefresh: false,
      refreshInterval: null,
      logEntryComponent: LogEntry
    };
  },
  computed: {
    filteredLogs() {
      let filtered = [...this.logs];
      
      // 筛选日志级别
      if (this.logLevel !== 'ALL') {
        filtered = filtered.filter(log => log.level === this.logLevel);
      }
      
      // 搜索内容
      if (this.searchQuery.trim()) {
        const query = this.searchQuery.trim().toLowerCase();
        filtered = filtered.filter(log => 
          log.message.toLowerCase().includes(query) || 
          (log.module && log.module.toLowerCase().includes(query))
        );
      }
      
      return filtered;
    },
    hasFilters() {
      return this.logLevel !== 'ALL' || this.searchQuery.trim() !== '';
    }
  },
  methods: {
    async fetchLogs() {
      this.isLoading = true;
      try {
        const response = await getLogs();
        this.logs = response.map((log, index) => ({
          ...log,
          id: index
        }));
      } catch (error) {
        console.error('获取日志失败:', error);
        this.$toast.error('获取日志失败');
      } finally {
        this.isLoading = false;
      }
    },
    refreshLogs() {
      this.fetchLogs();
    },
    clearSearch() {
      this.logLevel = 'ALL';
      this.searchQuery = '';
    },
    toggleAutoRefresh() {
      this.autoRefresh = !this.autoRefresh;
      
      if (this.autoRefresh) {
        this.refreshInterval = setInterval(this.fetchLogs, 5000);
      } else if (this.refreshInterval) {
        clearInterval(this.refreshInterval);
      }
    },
    formatTimestamp(timestamp) {
      const date = new Date(timestamp);
      return date.toLocaleString();
    },
    viewLogDetail(log) {
      this.selectedLog = log;
    },
    downloadLogs() {
      const logsJson = JSON.stringify(this.filteredLogs, null, 2);
      const blob = new Blob([logsJson], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      
      const a = document.createElement('a');
      a.href = url;
      a.download = `xybot-logs-${new Date().toISOString().slice(0, 10)}.json`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }
  },
  created() {
    this.fetchLogs();
  },
  beforeDestroy() {
    if (this.refreshInterval) {
      clearInterval(this.refreshInterval);
    }
  }
}
</script>

<style scoped>
.log-viewer {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.header-actions {
  display: flex;
  gap: 16px;
}

.filters {
  display: flex;
  gap: 8px;
}

.filter-select, .search-input {
  padding: 8px;
  border: 1px solid #e1e5eb;
  border-radius: 4px;
}

.search-input {
  width: 250px;
}

.btn-group {
  display: flex;
  gap: 8px;
}

.logs-container {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  height: calc(100vh - 220px);
  overflow: hidden;
}

.log-entries {
  height: 100%;
  overflow: hidden;
}

.list {
  height: 100%;
  overflow-y: auto;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  border-top-color: #4361ee;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.btn {
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.btn-outline {
  background: transparent;
  border: 1px solid #e1e5eb;
  color: #4a5568;
}

.btn-outline:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* 日志详情样式 */
.log-detail {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.badge.debug {
  background: #e2e8f0;
  color: #4a5568;
}

.badge.info {
  background: #ebf8ff;
  color: #3182ce;
}

.badge.warning {
  background: #fffbeb;
  color: #d97706;
}

.badge.error {
  background: #fef2f2;
  color: #dc2626;
}

.badge.critical {
  background: #f8ebfe;
  color: #9333ea;
}

.timestamp {
  color: #8b9cb3;
  font-size: 14px;
}

.detail-message {
  font-size: 16px;
  line-height: 1.5;
  background: #f7fafc;
  padding: 12px;
  border-radius: 4px;
  white-space: pre-line;
}

.detail-metadata h4, .detail-traceback h4 {
  margin-bottom: 8px;
}

.detail-metadata pre, .detail-traceback pre {
  background: #f7fafc;
  padding: 12px;
  border-radius: 4px;
  overflow-x: auto;
  font-family: monospace;
}

.traceback {
  color: #e53e3e;
}
</style> 