/**
 * 格式化日期时间
 * @param {string|number|Date} timestamp - 时间戳或日期对象
 * @param {boolean} showSeconds - 是否显示秒
 * @returns {string} 格式化后的时间字符串
 */
export const formatDateTime = (timestamp, showSeconds = true) => {
  const date = timestamp instanceof Date ? timestamp : new Date(timestamp);
  
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  const hours = String(date.getHours()).padStart(2, '0');
  const minutes = String(date.getMinutes()).padStart(2, '0');
  
  let result = `${year}-${month}-${day} ${hours}:${minutes}`;
  
  if (showSeconds) {
    const seconds = String(date.getSeconds()).padStart(2, '0');
    result += `:${seconds}`;
  }
  
  return result;
};

/**
 * 格式化日期
 * @param {string|number|Date} timestamp - 时间戳或日期对象
 * @returns {string} 格式化后的日期字符串
 */
export const formatDate = (timestamp) => {
  const date = timestamp instanceof Date ? timestamp : new Date(timestamp);
  
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  
  return `${year}-${month}-${day}`;
};

/**
 * 格式化时间
 * @param {string|number|Date} timestamp - 时间戳或日期对象
 * @param {boolean} showSeconds - 是否显示秒
 * @returns {string} 格式化后的时间字符串
 */
export const formatTime = (timestamp, showSeconds = true) => {
  const date = timestamp instanceof Date ? timestamp : new Date(timestamp);
  
  const hours = String(date.getHours()).padStart(2, '0');
  const minutes = String(date.getMinutes()).padStart(2, '0');
  
  let result = `${hours}:${minutes}`;
  
  if (showSeconds) {
    const seconds = String(date.getSeconds()).padStart(2, '0');
    result += `:${seconds}`;
  }
  
  return result;
};

/**
 * 格式化持续时间（秒）
 * @param {number} seconds - 持续时间（秒）
 * @returns {string} 格式化后的持续时间字符串
 */
export const formatDuration = (seconds) => {
  if (!seconds || seconds <= 0) {
    return '0秒';
  }
  
  const days = Math.floor(seconds / 86400);
  const hours = Math.floor((seconds % 86400) / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const remainingSeconds = Math.floor(seconds % 60);
  
  const parts = [];
  
  if (days > 0) {
    parts.push(`${days}天`);
  }
  
  if (hours > 0) {
    parts.push(`${hours}小时`);
  }
  
  if (minutes > 0) {
    parts.push(`${minutes}分钟`);
  }
  
  if (remainingSeconds > 0 && parts.length < 2) {
    parts.push(`${remainingSeconds}秒`);
  }
  
  return parts.join(' ');
};

/**
 * 格式化相对时间
 * @param {string|number|Date} timestamp - 时间戳或日期对象
 * @returns {string} 格式化后的相对时间字符串
 */
export const formatRelativeTime = (timestamp) => {
  const now = new Date();
  const date = timestamp instanceof Date ? timestamp : new Date(timestamp);
  const diff = (now - date) / 1000; // 转换为秒
  
  if (diff < 60) {
    return '刚刚';
  }
  
  if (diff < 3600) {
    const minutes = Math.floor(diff / 60);
    return `${minutes}分钟前`;
  }
  
  if (diff < 86400) {
    const hours = Math.floor(diff / 3600);
    return `${hours}小时前`;
  }
  
  if (diff < 2592000) { // 30天
    const days = Math.floor(diff / 86400);
    return `${days}天前`;
  }
  
  if (diff < 31536000) { // 365天
    const months = Math.floor(diff / 2592000);
    return `${months}个月前`;
  }
  
  const years = Math.floor(diff / 31536000);
  return `${years}年前`;
}; 