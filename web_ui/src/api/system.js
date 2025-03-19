import axios from 'axios';

// 创建API基础配置
const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// 获取系统状态
export const getStatus = async () => {
  const response = await api.get('/status');
  return response.data;
};

// 获取系统信息
export const getSystemInfo = async () => {
  const response = await api.get('/system/info');
  return response.data;
};

// 重启系统
export const restartSystem = async () => {
  const response = await api.post('/system/restart');
  return response.data;
};

// 获取系统设置
export const getSystemSettings = async () => {
  const response = await api.get('/settings');
  return response.data;
};

// 保存系统设置
export const saveSystemSettings = async (settings) => {
  const response = await api.post('/settings', settings);
  return response.data;
}; 