/**
 * WebSocket API服务
 * 提供实时数据更新功能
 */

class WebSocketService {
  constructor() {
    this.socket = null;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.reconnectInterval = 3000;
    this.listeners = {};
    this.connected = false;
  }

  /**
   * 连接到WebSocket服务器
   * @param {string} token - 认证令牌（可选）
   */
  connect(token = null) {
    if (this.socket && this.connected) {
      return;
    }

    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const host = window.location.host;
    const wsUrl = `${protocol}//${host}/api/ws`;

    // 如果提供了认证令牌，添加到URL参数中
    const url = token ? `${wsUrl}?token=${token}` : wsUrl;

    this.socket = new WebSocket(url);

    this.socket.onopen = () => {
      console.log('WebSocket连接已建立');
      this.connected = true;
      this.reconnectAttempts = 0;
      this._trigger('connect', { connected: true });
    };

    this.socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.type && typeof data.type === 'string') {
          this._trigger(data.type, data.payload || {});
        }
      } catch (error) {
        console.error('WebSocket消息解析错误:', error);
      }
    };

    this.socket.onclose = () => {
      console.log('WebSocket连接已关闭');
      this.connected = false;
      this._trigger('disconnect', { connected: false });
      this._attemptReconnect();
    };

    this.socket.onerror = (error) => {
      console.error('WebSocket错误:', error);
      this._trigger('error', { error });
    };
  }

  /**
   * 尝试重新连接
   * @private
   */
  _attemptReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      console.log(`尝试重新连接 (${this.reconnectAttempts}/${this.maxReconnectAttempts})...`);
      
      setTimeout(() => {
        this.connect();
      }, this.reconnectInterval);
    }
  }

  /**
   * 断开WebSocket连接
   */
  disconnect() {
    if (this.socket) {
      this.socket.close();
      this.socket = null;
      this.connected = false;
    }
  }

  /**
   * 发送消息到服务器
   * @param {string} type - 消息类型
   * @param {object} payload - 消息数据
   */
  send(type, payload = {}) {
    if (!this.socket || !this.connected) {
      console.error('WebSocket未连接，无法发送消息');
      return;
    }

    const message = JSON.stringify({
      type,
      payload
    });

    this.socket.send(message);
  }

  /**
   * 注册事件监听器
   * @param {string} event - 事件类型
   * @param {function} callback - 回调函数
   */
  on(event, callback) {
    if (!this.listeners[event]) {
      this.listeners[event] = [];
    }
    this.listeners[event].push(callback);
  }

  /**
   * 移除事件监听器
   * @param {string} event - 事件类型
   * @param {function} callback - 要移除的回调函数
   */
  off(event, callback) {
    if (!this.listeners[event]) return;
    
    if (callback) {
      this.listeners[event] = this.listeners[event].filter(cb => cb !== callback);
    } else {
      delete this.listeners[event];
    }
  }

  /**
   * 触发事件
   * @param {string} event - 事件类型
   * @param {object} data - 事件数据
   * @private
   */
  _trigger(event, data) {
    if (!this.listeners[event]) return;
    
    this.listeners[event].forEach(callback => {
      try {
        callback(data);
      } catch (error) {
        console.error(`执行${event}事件回调时出错:`, error);
      }
    });
  }
}

// 创建单例实例
const webSocketService = new WebSocketService();
export default webSocketService; 