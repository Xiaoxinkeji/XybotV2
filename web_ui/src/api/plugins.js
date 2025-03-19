import axios from 'axios';

// 创建API基础配置
const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// 获取插件列表
export const getPlugins = async () => {
  const response = await api.get('/plugins');
  return response.data;
};

// 切换插件状态（启用/禁用）
export const togglePlugin = async (pluginId, enable) => {
  const response = await api.post(`/plugins/${pluginId}/toggle`, { enable });
  return response.data;
};

// 获取插件配置内容
export const getPluginConfig = async (pluginId) => {
  const response = await api.get(`/plugins/${pluginId}/config`);
  return response.data.content;
};

// 保存插件配置
export const savePluginConfig = async (pluginId, content) => {
  const response = await api.post(`/plugins/${pluginId}/config`, { content });
  return response.data;
};

// 重新加载插件
export const reloadPlugin = async (pluginId) => {
  const response = await api.post(`/plugins/${pluginId}/reload`);
  return response.data;
};

// 获取插件依赖图
export const getPluginDependencyGraph = async () => {
  const response = await api.get('/plugins/dependency-graph');
  return response.data;
}; 