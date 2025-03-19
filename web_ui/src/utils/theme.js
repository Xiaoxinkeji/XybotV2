/**
 * 主题管理工具
 */

const THEME_KEY = 'xybot_theme_preference';
const DARK_MODE_CLASS = 'dark-mode';

export const ThemeMode = {
  LIGHT: 'light',
  DARK: 'dark',
  SYSTEM: 'system' // 根据系统设置自动选择
};

/**
 * 主题管理器
 */
class ThemeManager {
  constructor() {
    this._currentTheme = this._getSavedTheme() || ThemeMode.SYSTEM;
    this._listeners = [];
    
    // 监听系统主题变化
    this._setupSystemThemeListener();
    
    // 初始应用主题
    this.applyTheme(this._currentTheme);
  }
  
  /**
   * 获取当前主题模式
   * @returns {string} 主题模式
   */
  get currentTheme() {
    return this._currentTheme;
  }
  
  /**
   * 获取当前是否为深色模式
   * @returns {boolean} 是否为深色模式
   */
  get isDarkMode() {
    if (this._currentTheme === ThemeMode.DARK) {
      return true;
    }
    if (this._currentTheme === ThemeMode.SYSTEM) {
      return this._isSystemDarkMode();
    }
    return false;
  }
  
  /**
   * 设置主题
   * @param {string} theme - 主题模式
   */
  setTheme(theme) {
    if (!Object.values(ThemeMode).includes(theme)) {
      console.error(`无效的主题模式: ${theme}`);
      return;
    }
    
    this._currentTheme = theme;
    this._saveTheme(theme);
    this.applyTheme(theme);
    this._notifyListeners();
  }
  
  /**
   * 切换深色/浅色模式
   */
  toggleDarkMode() {
    const newTheme = this.isDarkMode ? ThemeMode.LIGHT : ThemeMode.DARK;
    this.setTheme(newTheme);
  }
  
  /**
   * 应用主题到页面
   * @param {string} theme - 主题模式
   */
  applyTheme(theme) {
    const shouldUseDarkMode = 
      theme === ThemeMode.DARK || 
      (theme === ThemeMode.SYSTEM && this._isSystemDarkMode());
    
    if (shouldUseDarkMode) {
      document.documentElement.classList.add(DARK_MODE_CLASS);
    } else {
      document.documentElement.classList.remove(DARK_MODE_CLASS);
    }
  }
  
  /**
   * 添加主题变化监听器
   * @param {function} listener - 监听器函数
   */
  addListener(listener) {
    if (typeof listener === 'function' && !this._listeners.includes(listener)) {
      this._listeners.push(listener);
    }
  }
  
  /**
   * 移除主题变化监听器
   * @param {function} listener - 监听器函数
   */
  removeListener(listener) {
    this._listeners = this._listeners.filter(l => l !== listener);
  }
  
  /**
   * 获取保存的主题
   * @returns {string|null} 保存的主题
   * @private
   */
  _getSavedTheme() {
    return localStorage.getItem(THEME_KEY);
  }
  
  /**
   * 保存主题设置
   * @param {string} theme - 主题模式
   * @private
   */
  _saveTheme(theme) {
    localStorage.setItem(THEME_KEY, theme);
  }
  
  /**
   * 检查系统是否使用深色模式
   * @returns {boolean} 是否为深色模式
   * @private
   */
  _isSystemDarkMode() {
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  }
  
  /**
   * 设置系统主题变化监听器
   * @private
   */
  _setupSystemThemeListener() {
    if (window.matchMedia) {
      const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
      
      // 系统主题变化时重新应用主题
      const handleChange = () => {
        if (this._currentTheme === ThemeMode.SYSTEM) {
          this.applyTheme(ThemeMode.SYSTEM);
          this._notifyListeners();
        }
      };
      
      // 兼容新旧API
      if (mediaQuery.addEventListener) {
        mediaQuery.addEventListener('change', handleChange);
      } else if (mediaQuery.addListener) {
        mediaQuery.addListener(handleChange);
      }
    }
  }
  
  /**
   * 通知所有监听器
   * @private
   */
  _notifyListeners() {
    this._listeners.forEach(listener => {
      try {
        listener({
          theme: this._currentTheme,
          isDarkMode: this.isDarkMode
        });
      } catch (error) {
        console.error('主题监听器执行出错:', error);
      }
    });
  }
}

// 创建单例实例
const themeManager = new ThemeManager();
export default themeManager; 