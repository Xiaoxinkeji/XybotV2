<template>
  <div id="app">
    <div class="app-container" :class="{'sidebar-collapsed': sidebarCollapsed}">
      <!-- 侧边栏组件 -->
      <sidebar :collapsed="sidebarCollapsed" @toggle-sidebar="toggleSidebar" />
      
      <!-- 主内容区 -->
      <div class="main-content">
        <!-- 顶部导航 -->
        <header-nav :collapsed="sidebarCollapsed" :user="currentUser" />
        
        <!-- 路由视图 -->
        <div class="content-wrapper">
          <router-view />
        </div>
        
        <!-- 页脚 -->
        <app-footer />
      </div>
    </div>
  </div>
</template>

<script>
import Sidebar from '@/components/layout/Sidebar.vue';
import HeaderNav from '@/components/layout/HeaderNav.vue';
import AppFooter from '@/components/layout/AppFooter.vue';

export default {
  name: 'App',
  components: {
    Sidebar,
    HeaderNav,
    AppFooter
  },
  data() {
    return {
      sidebarCollapsed: false,
      currentUser: {
        name: 'Admin',
        avatar: require('@/assets/default-avatar.png')
      }
    };
  },
  methods: {
    toggleSidebar() {
      this.sidebarCollapsed = !this.sidebarCollapsed;
    }
  }
}
</script>

<style>
:root {
  /* 浅色模式变量 */
  --primary-color: #4361ee;
  --primary-color-light: #edf2ff;
  --primary-color-dark: #3a56d4;
  
  --text-color: #1a202c;
  --text-color-secondary: #4a5568;
  --text-color-tertiary: #718096;
  
  --bg-color: #f7f9fc;
  --card-bg: #ffffff;
  --border-color: #e1e5eb;
  --hover-bg: #f5f7fa;
  
  --success-color: #10b981;
  --warning-color: #f59e0b;
  --error-color: #ef4444;
  --info-color: #3b82f6;
  
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

/* 深色模式变量 */
.dark-mode {
  --primary-color: #6366f1;
  --primary-color-light: #1e1f45;
  --primary-color-dark: #818cf8;
  
  --text-color: #f1f5f9;
  --text-color-secondary: #cbd5e1;
  --text-color-tertiary: #94a3b8;
  
  --bg-color: #0f172a;
  --card-bg: #1e293b;
  --border-color: #334155;
  --hover-bg: #283548;
  
  --success-color: #34d399;
  --warning-color: #fbbf24;
  --error-color: #f87171;
  --info-color: #60a5fa;
  
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.3);
  --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -1px rgba(0, 0, 0, 0.2);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.3), 0 4px 6px -2px rgba(0, 0, 0, 0.2);
}

/* 全局样式使用CSS变量 */
body {
  font-family: 'Inter', sans-serif;
  margin: 0;
  padding: 0;
  background-color: var(--bg-color);
  color: var(--text-color);
  transition: background-color 0.3s, color 0.3s;
}

/* 更新其他样式使用变量 */
.card {
  background-color: var(--card-bg);
  box-shadow: var(--shadow);
}

/* 更多全局样式... */
.app-container {
  display: flex;
  min-height: 100vh;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  transition: all 0.3s;
}

.content-wrapper {
  flex: 1;
  padding: 20px;
  background-color: #f5f7fa;
  overflow-y: auto;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .app-container {
    flex-direction: column;
  }
}
</style> 