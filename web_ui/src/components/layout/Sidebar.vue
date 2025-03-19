<template>
  <div class="sidebar" :class="{ 'collapsed': collapsed }">
    <div class="logo-container">
      <img src="@/assets/logo.png" alt="XyBotV2" class="logo" />
      <span v-if="!collapsed" class="brand-name">XyBotV2</span>
    </div>
    
    <div class="divider"></div>
    
    <nav class="menu">
      <router-link 
        v-for="item in menuItems" 
        :key="item.path" 
        :to="item.path"
        class="menu-item"
        :class="{ 'active': isActive(item.path) }"
      >
        <i :class="`icon-${item.icon}`"></i>
        <span v-if="!collapsed" class="menu-label">{{ item.label }}</span>
      </router-link>
    </nav>
    
    <div class="sidebar-footer">
      <button class="collapse-btn" @click="$emit('toggle-sidebar')">
        <i :class="`icon-${collapsed ? 'chevron-right' : 'chevron-left'}`"></i>
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Sidebar',
  props: {
    collapsed: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      menuItems: [
        { path: '/', label: '仪表盘', icon: 'home' },
        { path: '/plugins', label: '插件管理', icon: 'package' },
        { path: '/messages', label: '消息记录', icon: 'message-circle' },
        { path: '/settings', label: '系统设置', icon: 'settings' },
        { path: '/logs', label: '运行日志', icon: 'activity' },
        { path: '/help', label: '帮助文档', icon: 'help-circle' }
      ]
    };
  },
  methods: {
    isActive(path) {
      return this.$route.path === path || 
        (path !== '/' && this.$route.path.startsWith(path));
    }
  }
}
</script>

<style scoped>
.sidebar {
  width: 240px;
  height: 100vh;
  background: #1a2236;
  color: #8b9cb3;
  display: flex;
  flex-direction: column;
  transition: all 0.3s;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.sidebar.collapsed {
  width: 64px;
}

.logo-container {
  padding: 20px;
  display: flex;
  align-items: center;
  height: 64px;
}

.logo {
  width: 32px;
  height: 32px;
  margin-right: 12px;
}

.brand-name {
  color: #fff;
  font-size: 18px;
  font-weight: 600;
  white-space: nowrap;
}

.divider {
  height: 1px;
  background: rgba(255, 255, 255, 0.1);
  margin: 0 16px;
}

.menu {
  flex: 1;
  padding: 16px 0;
  overflow-y: auto;
}

.menu-item {
  display: flex;
  align-items: center;
  height: 40px;
  padding: 0 20px;
  color: inherit;
  text-decoration: none;
  margin-bottom: 8px;
  border-left: 3px solid transparent;
}

.menu-item i {
  font-size: 18px;
  min-width: 24px;
}

.menu-label {
  margin-left: 12px;
  white-space: nowrap;
}

.menu-item:hover {
  background: rgba(255, 255, 255, 0.05);
  color: #fff;
}

.menu-item.active {
  color: #fff;
  background: rgba(255, 255, 255, 0.1);
  border-left-color: #4361ee;
}

.sidebar-footer {
  padding: 16px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.collapse-btn {
  width: 100%;
  background: rgba(255, 255, 255, 0.1);
  border: none;
  color: inherit;
  padding: 8px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.collapse-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}
</style> 