import axios from 'axios';

// 创建API基础配置
const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// 获取日志列表
export const getLogs = async (params = {}) => {
  const response = await api.get('/logs', { params });
  return response.data;
};

// 下载完整日志
export const downloadFullLogs = async () => {
  const response = await api.get('/logs/download', { 
    responseType: 'blob'
  });
  return response.data;
};

// 清除日志
export const clearLogs = async () => {
  const response = await api.post('/logs/clear');
  return response.data;
}; 