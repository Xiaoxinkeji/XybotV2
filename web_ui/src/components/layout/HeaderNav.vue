<template>
  <header class="header">
    <div class="left-section">
      <div class="page-title">{{ pageTitle }}</div>
    </div>
    
    <div class="right-section">
      <div class="search-box">
        <i class="icon-search"></i>
        <input type="text" placeholder="搜索..." />
      </div>
      
      <div class="notification">
        <i class="icon-bell"></i>
        <span v-if="notificationCount > 0" class="badge">{{ notificationCount }}</span>
      </div>
      
      <div class="dropdown user-dropdown">
        <div class="user-info">
          <span class="username">{{ user.name }}</span>
          <img :src="user.avatar" alt="User" class="avatar" />
        </div>
        
        <div class="dropdown-menu">
          <a href="#" class="dropdown-item">
            <i class="icon-user"></i> 个人资料
          </a>
          <a href="#" class="dropdown-item">
            <i class="icon-settings"></i> 偏好设置
          </a>
          <div class="divider"></div>
          <a href="#" class="dropdown-item">
            <i class="icon-log-out"></i> 退出登录
          </a>
        </div>
      </div>
    </div>
  </header>
</template>

<script>
export default {
  name: 'HeaderNav',
  props: {
    collapsed: {
      type: Boolean,
      default: false
    },
    user: {
      type: Object,
      default: () => ({
        name: 'Admin',
        avatar: require('@/assets/default-avatar.png')
      })
    }
  },
  data() {
    return {
      notificationCount: 3
    };
  },
  computed: {
    pageTitle() {
      switch (this.$route.path) {
        case '/': return '仪表盘';
        case '/plugins': return '插件管理';
        case '/messages': return '消息记录';
        case '/settings': return '系统设置';
        case '/logs': return '运行日志';
        case '/help': return '帮助文档';
        default: return 'XyBotV2';
      }
    }
  }
}
</script>

<style scoped>
.header {
  height: 64px;
  background: white;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
}

.left-section {
  display: flex;
  align-items: center;
}

.page-title {
  font-size: 18px;
  font-weight: 600;
  color: #1a2236;
}

.right-section {
  display: flex;
  align-items: center;
  gap: 16px;
}

.search-box {
  position: relative;
}

.search-box i {
  position: absolute;
  left: 10px;
  top: 50%;
  transform: translateY(-50%);
  color: #8b9cb3;
}

.search-box input {
  border: 1px solid #e1e5eb;
  border-radius: 4px;
  padding: 8px 16px 8px 36px;
  width: 220px;
}

.notification {
  position: relative;
  cursor: pointer;
  padding: 8px;
}

.badge {
  position: absolute;
  top: 2px;
  right: 2px;
  background: #f44336;
  color: white;
  border-radius: 50%;
  width: 16px;
  height: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
}

.user-dropdown {
  position: relative;
}

.user-info {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 8px;
}

.username {
  margin-right: 8px;
  font-weight: 500;
}

.avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  object-fit: cover;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  background: white;
  border-radius: 4px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  width: 200px;
  padding: 8px 0;
  display: none;
  z-index: 100;
}

.user-dropdown:hover .dropdown-menu {
  display: block;
}

.dropdown-item {
  display: flex;
  align-items: center;
  padding: 10px 16px;
  color: #333;
  text-decoration: none;
}

.dropdown-item i {
  margin-right: 12px;
}

.dropdown-item:hover {
  background: #f5f7fa;
}

.divider {
  height: 1px;
  background: #e1e5eb;
  margin: 8px 0;
}
</style> 