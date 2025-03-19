<template>
  <div class="settings-page">
    <div class="page-header">
      <h1>系统设置</h1>
      <div class="header-actions">
        <button @click="saveAllSettings" class="btn btn-primary" :disabled="!hasChanges">
          <i class="icon-save"></i> 保存设置
        </button>
      </div>
    </div>
    
    <div class="settings-container" v-if="!isLoading">
      <div class="settings-nav">
        <div 
          v-for="(section, index) in settingSections" 
          :key="index"
          class="nav-item"
          :class="{ 'active': activeSection === index }"
          @click="activeSection = index"
        >
          <i :class="`icon-${section.icon}`"></i>
          <span>{{ section.title }}</span>
        </div>
      </div>
      
      <div class="settings-content">
        <div class="card">
          <h2>{{ settingSections[activeSection].title }}</h2>
          <p class="section-description">{{ settingSections[activeSection].description }}</p>
          
          <div class="settings-form">
            <template v-if="activeSection === 0">
              <!-- 常规设置 -->
              <div class="form-group">
                <label for="botName">机器人名称</label>
                <input 
                  id="botName" 
                  type="text" 
                  v-model="settings.general.botName"
                  class="form-control"
                />
              </div>
              
              <div class="form-group">
                <label>自动重启</label>
                <div class="toggle-switch">
                  <label class="switch">
                    <input type="checkbox" v-model="settings.general.autoRestart">
                    <span class="slider round"></span>
                  </label>
                  <span class="toggle-label">{{ settings.general.autoRestart ? '开启' : '关闭' }}</span>
                </div>
              </div>
              
              <div class="form-group">
                <label for="logLevel">日志级别</label>
                <select id="logLevel" v-model="settings.general.logLevel" class="form-control">
                  <option value="DEBUG">调试</option>
                  <option value="INFO">信息</option>
                  <option value="WARNING">警告</option>
                  <option value="ERROR">错误</option>
                </select>
              </div>
            </template>
            
            <template v-else-if="activeSection === 1">
              <!-- Web服务设置 -->
              <div class="form-group">
                <label>Web服务</label>
                <div class="toggle-switch">
                  <label class="switch">
                    <input type="checkbox" v-model="settings.webServer.enabled">
                    <span class="slider round"></span>
                  </label>
                  <span class="toggle-label">{{ settings.webServer.enabled ? '开启' : '关闭' }}</span>
                </div>
              </div>
              
              <div class="form-group">
                <label for="webPort">Web端口</label>
                <input 
                  id="webPort" 
                  type="number" 
                  v-model="settings.webServer.port"
                  class="form-control"
                  :disabled="!settings.webServer.enabled"
                />
              </div>
              
              <div class="form-group">
                <label>访问控制</label>
                <div class="toggle-switch">
                  <label class="switch">
                    <input type="checkbox" v-model="settings.webServer.requireAuth">
                    <span class="slider round"></span>
                  </label>
                  <span class="toggle-label">{{ settings.webServer.requireAuth ? '开启' : '关闭' }}</span>
                </div>
              </div>
            </template>
            
            <template v-else-if="activeSection === 2">
              <!-- 通知设置 -->
              <div class="form-group">
                <label>状态变更通知</label>
                <div class="toggle-switch">
                  <label class="switch">
                    <input type="checkbox" v-model="settings.notifications.statusChange">
                    <span class="slider round"></span>
                  </label>
                  <span class="toggle-label">{{ settings.notifications.statusChange ? '开启' : '关闭' }}</span>
                </div>
              </div>
              
              <div class="form-group">
                <label>错误通知</label>
                <div class="toggle-switch">
                  <label class="switch">
                    <input type="checkbox" v-model="settings.notifications.errors">
                    <span class="slider round"></span>
                  </label>
                  <span class="toggle-label">{{ settings.notifications.errors ? '开启' : '关闭' }}</span>
                </div>
              </div>
              
              <div class="form-group">
                <label for="notifyMethod">通知方式</label>
                <select id="notifyMethod" v-model="settings.notifications.method" class="form-control">
                  <option value="pushplus">PushPlus</option>
                  <option value="email">邮件</option>
                  <option value="wxpusher">微信推送</option>
                </select>
              </div>
            </template>
            
            <!-- 更多设置部分 -->
          </div>
        </div>
      </div>
    </div>
    
    <div class="loading-state" v-else>
      <div class="spinner"></div>
      <p>加载设置中...</p>
    </div>
  </div>
</template>

<script>
import { getSystemSettings, saveSystemSettings } from '@/api/settings';

export default {
  name: 'Settings',
  data() {
    return {
      isLoading: true,
      activeSection: 0,
      originalSettings: null,
      settings: {
        general: {
          botName: 'XyBotV2',
          autoRestart: true,
          logLevel: 'INFO'
        },
        webServer: {
          enabled: true,
          port: 8080,
          requireAuth: false
        },
        notifications: {
          statusChange: true,
          errors: true,
          method: 'pushplus'
        }
      },
      settingSections: [
        { 
          title: '常规设置', 
          icon: 'settings', 
          description: '基本系统设置，包括机器人名称、自动重启等选项。' 
        },
        { 
          title: 'Web服务', 
          icon: 'globe', 
          description: '管理Web服务器配置，包括端口和访问控制。' 
        },
        { 
          title: '通知设置', 
          icon: 'bell', 
          description: '控制系统事件的通知方式和时机。' 
        },
        { 
          title: '高级选项', 
          icon: 'sliders', 
          description: '高级系统配置，仅推荐有经验的用户修改。' 
        }
      ]
    };
  },
  computed: {
    hasChanges() {
      return JSON.stringify(this.settings) !== JSON.stringify(this.originalSettings);
    }
  },
  methods: {
    async fetchSettings() {
      this.isLoading = true;
      try {
        const response = await getSystemSettings();
        this.settings = response;
        this.originalSettings = JSON.parse(JSON.stringify(response));
      } catch (error) {
        console.error('获取系统设置失败:', error);
        this.$toast.error('获取系统设置失败');
      } finally {
        this.isLoading = false;
      }
    },
    async saveAllSettings() {
      try {
        await saveSystemSettings(this.settings);
        this.originalSettings = JSON.parse(JSON.stringify(this.settings));
        this.$toast.success('设置保存成功');
      } catch (error) {
        console.error('保存设置失败:', error);
        this.$toast.error(`保存设置失败: ${error.message}`);
      }
    }
  },
  created() {
    this.fetchSettings();
  }
}
</script>

<style scoped>
.settings-page {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.settings-container {
  display: flex;
  gap: 20px;
}

.settings-nav {
  width: 220px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 16px;
  cursor: pointer;
  border-left: 3px solid transparent;
  transition: all 0.3s;
}

.nav-item i {
  margin-right: 12px;
  font-size: 18px;
}

.nav-item:hover {
  background: #f5f7fa;
}

.nav-item.active {
  background: #edf2ff;
  color: #4361ee;
  border-left-color: #4361ee;
}

.settings-content {
  flex: 1;
}

.card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  padding: 20px;
}

.section-description {
  color: #8b9cb3;
  margin-bottom: 24px;
}

.settings-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-weight: 500;
  color: #4a5568;
}

.form-control {
  padding: 10px;
  border: 1px solid #e1e5eb;
  border-radius: 4px;
  font-size: 14px;
}

.toggle-switch {
  display: flex;
  align-items: center;
  gap: 12px;
}

.toggle-label {
  font-size: 14px;
  color: #4a5568;
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

.btn-primary {
  background: #4361ee;
  border: 1px solid #4361ee;
  color: white;
}

.btn-primary:disabled {
  background: #b8c2cc;
  border-color: #b8c2cc;
  cursor: not-allowed;
}

/* 开关样式 */
.switch {
  position: relative;
  display: inline-block;
  width: 40px;
  height: 22px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: .4s;
}

.slider:before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 2px;
  bottom: 2px;
  background-color: white;
  transition: .4s;
}

input:checked + .slider {
  background-color: #4361ee;
}

input:focus + .slider {
  box-shadow: 0 0 1px #4361ee;
}

input:checked + .slider:before {
  transform: translateX(18px);
}

.slider.round {
  border-radius: 34px;
}

.slider.round:before {
  border-radius: 50%;
}
</style> 