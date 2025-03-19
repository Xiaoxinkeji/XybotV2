<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-header">
        <div class="logo">
          <img src="@/assets/logo.png" alt="XyBotV2 Logo">
        </div>
        <h1>XyBotV2 管理平台</h1>
      </div>
      
      <div class="login-form">
        <div class="form-group">
          <label for="username">用户名</label>
          <input 
            type="text" 
            id="username" 
            v-model="username" 
            placeholder="请输入用户名"
            :disabled="isLoading"
            @keyup.enter="handleLogin"
          >
        </div>
        
        <div class="form-group">
          <label for="password">密码</label>
          <div class="password-input">
            <input 
              :type="showPassword ? 'text' : 'password'" 
              id="password" 
              v-model="password" 
              placeholder="请输入密码"
              :disabled="isLoading"
              @keyup.enter="handleLogin"
            >
            <button 
              type="button" 
              class="toggle-password" 
              @click="showPassword = !showPassword"
            >
              <i :class="showPassword ? 'icon-eye-off' : 'icon-eye'"></i>
            </button>
          </div>
        </div>
        
        <div class="form-options">
          <label class="remember-me">
            <input type="checkbox" v-model="rememberMe">
            <span>记住我</span>
          </label>
        </div>
        
        <div v-if="error" class="error-message">
          {{ error }}
        </div>
        
        <button 
          type="button" 
          class="login-button" 
          @click="handleLogin" 
          :disabled="isLoading || !isFormValid"
        >
          <span v-if="!isLoading">登录</span>
          <span v-else class="loading-spinner"></span>
        </button>
      </div>
      
      <div class="login-footer">
        <p>© {{ new Date().getFullYear() }} XyBotV2. 保留所有权利。</p>
      </div>
    </div>
  </div>
</template>

<script>
import { login } from '@/api/auth';
import { saveAuth } from '@/utils/auth';

export default {
  name: 'Login',
  data() {
    return {
      username: '',
      password: '',
      showPassword: false,
      rememberMe: false,
      isLoading: false,
      error: ''
    };
  },
  computed: {
    isFormValid() {
      return this.username.trim() && this.password.trim();
    }
  },
  methods: {
    async handleLogin() {
      if (!this.isFormValid || this.isLoading) return;
      
      this.isLoading = true;
      this.error = '';
      
      try {
        const response = await login(this.username, this.password);
        
        if (response && response.token) {
          // 保存认证信息
          saveAuth(response);
          
          // 重定向到之前尝试访问的页面或仪表盘
          const redirectPath = this.$route.query.redirect || '/dashboard';
          this.$router.push(redirectPath);
        } else {
          this.error = '登录失败，请检查您的凭据';
        }
      } catch (error) {
        console.error('登录出错:', error);
        this.error = error.response?.data?.error || '登录时发生错误，请稍后重试';
      } finally {
        this.isLoading = false;
      }
    }
  },
  // 进入页面时检查存储的用户名
  mounted() {
    const savedUsername = localStorage.getItem('saved_username');
    if (savedUsername) {
      this.username = savedUsername;
      this.rememberMe = true;
    }
  },
  // 离开页面时保存用户名
  beforeDestroy() {
    if (this.rememberMe) {
      localStorage.setItem('saved_username', this.username);
    } else {
      localStorage.removeItem('saved_username');
    }
  }
}
</script>

<style scoped>
.login-page {
  display: flex;
  min-height: 100vh;
  justify-content: center;
  align-items: center;
  background-color: var(--bg-color);
  padding: 20px;
}

.login-container {
  width: 100%;
  max-width: 400px;
  background-color: var(--card-bg);
  border-radius: 10px;
  box-shadow: var(--shadow-lg);
  overflow: hidden;
}

.login-header {
  text-align: center;
  padding: 30px 20px;
}

.logo {
  margin-bottom: 16px;
}

.logo img {
  width: 80px;
  height: auto;
}

.login-header h1 {
  font-size: 24px;
  color: var(--text-color);
  margin: 0;
}

.login-form {
  padding: 0 30px 30px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: var(--text-color-secondary);
}

.form-group input {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  background-color: var(--bg-color);
  color: var(--text-color);
  font-size: 16px;
  transition: border-color 0.2s;
}

.form-group input:focus {
  border-color: var(--primary-color);
  outline: none;
}

.password-input {
  position: relative;
}

.toggle-password {
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  color: var(--text-color-tertiary);
}

.form-options {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.remember-me {
  display: flex;
  align-items: center;
  cursor: pointer;
  user-select: none;
}

.remember-me input {
  margin-right: 8px;
}

.error-message {
  padding: 10px;
  border-radius: 4px;
  background-color: rgba(239, 68, 68, 0.1);
  color: var(--error-color);
  margin-bottom: 20px;
}

.login-button {
  width: 100%;
  padding: 12px;
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
  display: flex;
  justify-content: center;
  align-items: center;
}

.login-button:hover:not(:disabled) {
  background-color: var(--primary-color-dark);
}

.login-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.loading-spinner {
  display: inline-block;
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.login-footer {
  padding: 20px;
  text-align: center;
  border-top: 1px solid var(--border-color);
}

.login-footer p {
  margin: 0;
  color: var(--text-color-tertiary);
  font-size: 14px;
}
</style> 