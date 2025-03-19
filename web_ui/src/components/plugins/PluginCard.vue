<template>
  <div class="plugin-card" :class="{ 'disabled': !plugin.enabled }">
    <div class="plugin-header">
      <div class="plugin-title">
        <h3>{{ plugin.name }}</h3>
        <span class="plugin-version">v{{ plugin.version }}</span>
      </div>
      
      <div class="switch-container">
        <label class="switch">
          <input type="checkbox" :checked="plugin.enabled" @change="togglePlugin">
          <span class="slider round"></span>
        </label>
      </div>
    </div>
    
    <p class="plugin-description">{{ plugin.description || '暂无描述' }}</p>
    
    <div class="plugin-meta">
      <span class="author">
        <i class="icon-user"></i> {{ plugin.author || '未知作者' }}
      </span>
    </div>
    
    <div class="plugin-actions">
      <button @click="$emit('view-config', plugin)" class="btn-action">
        <i class="icon-settings"></i> 配置
      </button>
      <button class="btn-action">
        <i class="icon-info"></i> 详情
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PluginCard',
  props: {
    plugin: {
      type: Object,
      required: true
    }
  },
  methods: {
    togglePlugin() {
      this.$emit('toggle', this.plugin);
    }
  }
}
</script>

<style scoped>
.plugin-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  padding: 16px;
  transition: all 0.3s;
  border: 1px solid transparent;
}

.plugin-card:hover {
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.plugin-card.disabled {
  opacity: 0.7;
  background: #f7f9fc;
  border-color: #e1e5eb;
}

.plugin-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.plugin-title {
  display: flex;
  align-items: baseline;
  gap: 8px;
}

.plugin-title h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
}

.plugin-version {
  font-size: 12px;
  color: #8b9cb3;
}

.plugin-description {
  color: #4a5568;
  margin-bottom: 12px;
  font-size: 14px;
  line-height: 1.5;
  height: 42px;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.plugin-meta {
  font-size: 12px;
  color: #8b9cb3;
  margin-bottom: 12px;
}

.author {
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.plugin-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}

.btn-action {
  background: none;
  border: 1px solid #e1e5eb;
  border-radius: 4px;
  padding: 6px 12px;
  color: #4a5568;
  font-size: 12px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.btn-action:hover {
  background: #f5f7fa;
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