<template>
  <div class="help-page">
    <div class="page-header">
      <h1>帮助文档</h1>
    </div>
    
    <div class="content-wrapper">
      <div class="navigation">
        <div 
          v-for="(section, index) in sections" 
          :key="index"
          class="nav-item"
          :class="{ 'active': activeSection === index }"
          @click="activeSection = index"
        >
          <i :class="`icon-${section.icon}`"></i>
          <span>{{ section.title }}</span>
        </div>
      </div>
      
      <div class="content">
        <div class="card">
          <component :is="currentComponent" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ApiReference from '@/components/help/ApiReference.vue';
import UserGuide from '@/components/help/UserGuide.vue';
import PluginDev from '@/components/help/PluginDev.vue';
import Troubleshooting from '@/components/help/Troubleshooting.vue';

export default {
  name: 'Help',
  components: {
    ApiReference,
    UserGuide,
    PluginDev,
    Troubleshooting
  },
  data() {
    return {
      activeSection: 0,
      sections: [
        { title: '使用指南', icon: 'book', component: 'UserGuide' },
        { title: 'API参考', icon: 'code', component: 'ApiReference' },
        { title: '插件开发', icon: 'package', component: 'PluginDev' },
        { title: '故障排除', icon: 'alert-triangle', component: 'Troubleshooting' }
      ]
    };
  },
  computed: {
    currentComponent() {
      return this.sections[this.activeSection].component;
    }
  }
}
</script>

<style scoped>
.help-page {
  padding: 20px;
}

.page-header {
  margin-bottom: 24px;
}

.content-wrapper {
  display: flex;
  gap: 20px;
  height: calc(100vh - 180px);
}

.navigation {
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

.content {
  flex: 1;
  overflow: hidden;
}

.card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  padding: 20px;
  height: 100%;
  overflow-y: auto;
}
</style> 