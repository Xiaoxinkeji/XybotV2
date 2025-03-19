import axios from 'axios';

// 创建API基础配置
const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// 获取机器人状态
export const getBotStatus = async () => {
  const response = await api.get('/status');
  return response.data;
};

// 获取系统信息
export const getSystemInfo = async () => {
  const response = await api.get('/system/info');
  return response.data;
};

// 获取插件列表
export const getPlugins = async () => {
  const response = await api.get('/plugins');
  return response.data;
};

// 启用/禁用插件
export const togglePlugin = async (pluginId, enable) => {
  const response = await api.post(`/plugins/${pluginId}/toggle`, { enable });
  return response.data;
};

// 获取最近消息
export const getRecentMessages = async (limit = 20) => {
  const response = await api.get(`/messages/recent?limit=${limit}`);
  return response.data;
};

// 获取最近事件
export const getRecentEvents = async (limit = 20) => {
  // 模拟数据，实际实现时应该从服务器获取
  return [
    { id: 1, type: 'status', message: '机器人已成功启动', time: new Date().toISOString(), level: 'info' },
    { id: 2, type: 'plugin', message: 'BotStatusPush插件已启用', time: new Date().toISOString(), level: 'success' },
    { id: 3, type: 'message', message: '收到新消息: 你好，机器人', time: new Date().toISOString(), level: 'info' },
    { id: 4, type: 'system', message: '系统内存使用率达到75%', time: new Date().toISOString(), level: 'warning' }
  ];
};

// 发送测试推送
export const sendTestNotification = async () => {
  // 模拟成功，实际实现时应该调用服务器API
  return { success: true, message: '测试推送已发送' };
};

// 重启机器人服务
export const restartBot = async () => {
  // 模拟成功，实际实现时应该调用服务器API
  return { success: true };
}; 