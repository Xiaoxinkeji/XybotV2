<template>
  <div class="dashboard">
    <div class="page-header">
      <h1>仪表盘</h1>
      <div class="header-actions">
        <button @click="refreshData" class="btn btn-outline">
          <i class="icon-refresh"></i> 刷新数据
        </button>
      </div>
    </div>
    
    <div class="dashboard-content" v-if="!isLoading">
      <div class="stats-cards">
        <div class="stat-card">
          <div class="stat-icon" :class="botStatus.online ? 'online' : 'offline'">
            <i class="icon-activity"></i>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ botStatus.online ? '在线' : '离线' }}</div>
            <div class="stat-label">机器人状态</div>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon plugins">
            <i class="icon-package"></i>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.pluginsCount }} <span class="sub-stat">({{ stats.enabledPlugins }} 已启用)</span></div>
            <div class="stat-label">插件数量</div>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon messages">
            <i class="icon-message-square"></i>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.messagesCount }}</div>
            <div class="stat-label">今日消息</div>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon uptime">
            <i class="icon-clock"></i>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ uptimeFormatted }}</div>
            <div class="stat-label">运行时间</div>
          </div>
        </div>
      </div>
      
      <system-monitor :system-info="systemInfo" :uptime="botStatus.uptime" />
      
      <div class="dashboard-row">
        <div class="dashboard-card recent-messages">
          <div class="card-header">
            <h3>最近消息</h3>
            <router-link to="/messages" class="view-all">查看全部</router-link>
          </div>
          
          <div class="messages-list">
            <div 
              v-for="(message, index) in recentMessages" 
              :key="index"
              class="message-item"
              :class="message.type"
            >
              <div class="message-sender">
                <div class="avatar">{{ message.sender.substring(0, 1) }}</div>
                <div class="sender-name">{{ message.sender }}</div>
              </div>
              
              <div class="message-content">{{ message.content }}</div>
              
              <div class="message-time">{{ formatTime(message.timestamp) }}</div>
            </div>
            
            <div class="no-data" v-if="recentMessages.length === 0">
              暂无消息记录
            </div>
          </div>
        </div>
        
        <div class="dashboard-card active-plugins">
          <div class="card-header">
            <h3>活跃插件</h3>
            <router-link to="/plugins" class="view-all">管理插件</router-link>
          </div>
          
          <div class="plugins-list">
            <div 
              v-for="plugin in activePlugins" 
              :key="plugin.id"
              class="plugin-item"
            >
              <div class="plugin-icon">
                <i class="icon-package"></i>
              </div>
              
              <div class="plugin-info">
                <div class="plugin-name">{{ plugin.name }}</div>
                <div class="plugin-version">v{{ plugin.version }}</div>
              </div>
              
              <div class="plugin-status" :class="{ 'enabled': plugin.enabled }">
                {{ plugin.enabled ? '已启用' : '已禁用' }}
              </div>
            </div>
            
            <div class="no-data" v-if="activePlugins.length === 0">
              暂无活跃插件
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="loading-state" v-else>
      <div class="spinner"></div>
      <p>加载中...</p>
    </div>
  </div>
</template>

<script>
import SystemMonitor from '@/components/dashboard/SystemMonitor.vue';
import { getStatus } from '@/api/status';
import { getPlugins } from '@/api/plugins';
import { getRecentMessages } from '@/api/messages';
import { getSystemInfo } from '@/api/system';
import { formatDuration, formatTime } from '@/utils/time';

export default {
  name: 'Dashboard',
  components: {
    SystemMonitor
  },
  data() {
    return {
      isLoading: true,
      botStatus: {
        online: false,
        uptime: 0,
        version: '1.0.0',
        lastActivity: null
      },
      stats: {
        pluginsCount: 0,
        enabledPlugins: 0,
        messagesCount: 0
      },
      systemInfo: {
        cpu: { percent: 0, cores: 0 },
        memory: { total: 0, available: 0, percent: 0 },
        disk: { total: 0, free: 0, percent: 0 },
        platform: { system: '', release: '', version: '' },
        python: ''
      },
      recentMessages: [],
      activePlugins: []
    };
  },
  computed: {
    uptimeFormatted() {
      return formatDuration(this.botStatus.uptime);
    }
  },
  methods: {
    async fetchStatus() {
      try {
        this.botStatus = await getStatus();
      } catch (error) {
        console.error('获取状态失败:', error);
      }
    },
    
    async fetchPlugins() {
      try {
        const plugins = await getPlugins();
        this.stats.pluginsCount = plugins.length;
        this.stats.enabledPlugins = plugins.filter(p => p.enabled).length;
        this.activePlugins = plugins.filter(p => p.enabled).slice(0, 5);
      } catch (error) {
        console.error('获取插件失败:', error);
      }
    },
    
    async fetchMessages() {
      try {
        const messages = await getRecentMessages();
        this.recentMessages = messages.slice(0, 5);
        this.stats.messagesCount = messages.length;
      } catch (error) {
        console.error('获取消息失败:', error);
      }
    },
    
    async fetchSystemInfo() {
      try {
        this.systemInfo = await getSystemInfo();
      } catch (error) {
        console.error('获取系统信息失败:', error);
      }
    },
    
    formatTime(timestamp) {
      return formatTime(timestamp);
    },
    
    async refreshData() {
      this.isLoading = true;
      await Promise.all([
        this.fetchStatus(),
        this.fetchPlugins(),
        this.fetchMessages(),
        this.fetchSystemInfo()
      ]);
      this.isLoading = false;
    }
  },
  async created() {
    await this.refreshData();
  }
}
</script>

<style scoped>
.dashboard {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
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

.stats-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  padding: 20px;
  display: flex;
  align-items: center;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
  font-size: 24px;
  color: white;
}

.stat-icon.online {
  background: #10b981;
}

.stat-icon.offline {
  background: #ef4444;
}

.stat-icon.plugins {
  background: #3b82f6;
}

.stat-icon.messages {
  background: #f59e0b;
}

.stat-icon.uptime {
  background: #8b5cf6;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 18px;
  font-weight: 600;
  color: #1a202c;
  margin-bottom: 4px;
}

.sub-stat {
  font-size: 14px;
  color: #718096;
  font-weight: normal;
}

.stat-label {
  font-size: 14px;
  color: #718096;
}

.dashboard-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.dashboard-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  padding: 16px;
  height: 420px;
  display: flex;
  flex-direction: column;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.card-header h3 {
  margin: 0;
}

.view-all {
  font-size: 14px;
  color: #4361ee;
  text-decoration: none;
}

.view-all:hover {
  text-decoration: underline;
}

.messages-list, .plugins-list {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.message-item {
  padding: 12px;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  border: 1px solid #e1e5eb;
}

.message-item.received {
  background: #f5f7fa;
}

.message-sender {
  display: flex;
  align-items: center;
  gap: 8px;
}

.avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #4361ee;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
}

.message-item.sent .avatar {
  background: #10b981;
}

.sender-name {
  font-weight: 500;
}

.message-content {
  font-size: 14px;
  line-height: 1.5;
  padding-left: 40px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.message-time {
  font-size: 12px;
  color: #8b9cb3;
  text-align: right;
}

.plugin-item {
  display: flex;
  align-items: center;
  padding: 12px;
  border-radius: 8px;
  border: 1px solid #e1e5eb;
}

.plugin-icon {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  background: #edf2ff;
  color: #4361ee;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  margin-right: 12px;
}

.plugin-info {
  flex: 1;
}

.plugin-name {
  font-weight: 500;
  margin-bottom: 4px;
}

.plugin-version {
  font-size: 12px;
  color: #8b9cb3;
}

.plugin-status {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  background: #e2e8f0;
  color: #4a5568;
}

.plugin-status.enabled {
  background: #e6fffa;
  color: #0d9488;
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

.no-data {
  padding: 32px;
  text-align: center;
  color: #8b9cb3;
  font-style: italic;
}
</style> 