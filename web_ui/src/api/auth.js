/**
 * 认证相关API
 */

import axios from 'axios';

// 创建API基础配置
const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// 登录
export const login = async (username, password) => {
  try {
    const response = await api.post('/auth/login', { username, password });
    return response.data;
  } catch (error) {
    if (error.response) {
      throw new Error(error.response.data.error || '登录失败');
    }
    throw error;
  }
};

// 注销
export const logout = async (token) => {
  try {
    const response = await api.post('/auth/logout', { token });
    return response.data;
  } catch (error) {
    if (error.response) {
      throw new Error(error.response.data.error || '注销失败');
    }
    throw error;
  }
};

// 验证令牌
export const verifyToken = async (token) => {
  const response = await api.get('/auth/verify', {
    headers: { Authorization: `Bearer ${token}` }
  });
  return response.data;
};

// 修改密码
export const changePassword = async (username, oldPassword, newPassword) => {
  const response = await api.post('/auth/change-password', {
    username,
    oldPassword,
    newPassword
  });
  return response.data;
};

/**
 * 认证拦截器
 * 为所有请求添加认证令牌，处理认证错误
 */
export const setupAuthInterceptors = (router) => {
  // 请求拦截器
  api.interceptors.request.use(
    (config) => {
      const token = localStorage.getItem('auth_token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );
  
  // 响应拦截器
  api.interceptors.response.use(
    (response) => {
      return response;
    },
    (error) => {
      if (error.response && error.response.status === 401) {
        // 清除本地存储的认证信息
        localStorage.removeItem('auth_token');
        localStorage.removeItem('auth_user');
        
        // 如果不是已经在登录页面，则重定向到登录页
        if (router.currentRoute.path !== '/login') {
          router.push({
            path: '/login',
            query: { redirect: router.currentRoute.fullPath }
          });
        }
      }
      return Promise.reject(error);
    }
  );
  
  return api;
};

export default api; 