<template>
  <div class="theme-toggle">
    <button 
      @click="toggleTheme" 
      class="theme-toggle-button"
      :title="buttonTitle"
    >
      <i :class="iconClass"></i>
    </button>
    
    <div v-if="showDropdown" class="theme-options">
      <div 
        class="theme-option" 
        :class="{ active: currentTheme === ThemeMode.LIGHT }"
        @click="setTheme(ThemeMode.LIGHT)"
      >
        <i class="icon-sun"></i>
        <span>浅色</span>
      </div>
      
      <div 
        class="theme-option" 
        :class="{ active: currentTheme === ThemeMode.DARK }"
        @click="setTheme(ThemeMode.DARK)"
      >
        <i class="icon-moon"></i>
        <span>深色</span>
      </div>
      
      <div 
        class="theme-option" 
        :class="{ active: currentTheme === ThemeMode.SYSTEM }"
        @click="setTheme(ThemeMode.SYSTEM)"
      >
        <i class="icon-monitor"></i>
        <span>跟随系统</span>
      </div>
    </div>
  </div>
</template>

<script>
import themeManager, { ThemeMode } from '@/utils/theme';

export default {
  name: 'ThemeToggle',
  data() {
    return {
      currentTheme: themeManager.currentTheme,
      isDarkMode: themeManager.isDarkMode,
      showDropdown: false,
      ThemeMode // 导出到模板中使用
    };
  },
  computed: {
    iconClass() {
      if (this.currentTheme === ThemeMode.SYSTEM) {
        return this.isDarkMode ? 'icon-moon' : 'icon-sun';
      } else {
        return this.isDarkMode ? 'icon-moon' : 'icon-sun';
      }
    },
    buttonTitle() {
      return this.isDarkMode ? '切换到浅色模式' : '切换到深色模式';
    }
  },
  mounted() {
    // 监听主题变化
    themeManager.addListener(this.handleThemeChange);
    
    // 点击外部关闭下拉菜单
    document.addEventListener('click', this.closeDropdown);
  },
  beforeDestroy() {
    themeManager.removeListener(this.handleThemeChange);
    document.removeEventListener('click', this.closeDropdown);
  },
  methods: {
    toggleTheme() {
      if (this.simple) {
        // 简单模式直接切换深浅色
        themeManager.toggleDarkMode();
      } else {
        // 显示选项下拉菜单
        this.showDropdown = !this.showDropdown;
      }
    },
    setTheme(theme) {
      themeManager.setTheme(theme);
      this.showDropdown = false;
    },
    handleThemeChange({ theme, isDarkMode }) {
      this.currentTheme = theme;
      this.isDarkMode = isDarkMode;
    },
    closeDropdown(event) {
      if (!this.$el.contains(event.target)) {
        this.showDropdown = false;
      }
    }
  },
  props: {
    simple: {
      type: Boolean,
      default: false
    }
  }
}
</script>

<style scoped>
.theme-toggle {
  position: relative;
}

.theme-toggle-button {
  background: none;
  border: none;
  padding: 8px;
  cursor: pointer;
  color: var(--text-color);
  font-size: 18px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.2s;
}

.theme-toggle-button:hover {
  background-color: var(--hover-bg);
}

.theme-options {
  position: absolute;
  top: 100%;
  right: 0;
  background: var(--card-bg);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  z-index: 100;
  width: 160px;
  overflow: hidden;
  margin-top: 8px;
}

.theme-option {
  padding: 12px 16px;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.theme-option:hover {
  background-color: var(--hover-bg);
}

.theme-option.active {
  background-color: var(--primary-color-light);
  color: var(--primary-color);
}

.theme-option i {
  font-size: 16px;
}
</style> 