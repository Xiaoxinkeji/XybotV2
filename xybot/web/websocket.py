"""
WebSocket管理模块
处理实时数据传输和连接管理
"""

import asyncio
import json
import logging
import psutil
from datetime import datetime
from aiohttp import web, WSCloseCode

logger = logging.getLogger(__name__)

class WebSocketManager:
    """WebSocket连接管理器"""
    
    def __init__(self, bot_instance, config):
        """
        初始化WebSocket管理器
        
        Args:
            bot_instance: 机器人实例
            config: WebSocket配置
        """
        self.bot = bot_instance
        self.enabled = config.get('enabled', True)
        self.ping_interval = config.get('ping_interval', 30)
        self.max_clients = config.get('max_clients', 50)
        self.stats_update_interval = config.get('stats_update_interval', 5000)
        
        # 连接管理
        self.clients = set()
        self.tasks = {}
    
    async def handle_connection(self, request):
        """
        处理WebSocket连接请求
        
        Args:
            request: 请求对象
            
        Returns:
            WebSocket响应
        """
        if not self.enabled:
            return web.json_response({"error": "WebSocket服务已禁用"}, status=400)
        
        # 限制最大连接数
        if len(self.clients) >= self.max_clients:
            return web.json_response({"error": "达到最大连接数限制"}, status=503)
        
        # 升级到WebSocket连接
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        
        # 获取认证信息
        user = request.get('user', None)
        if not user:
            await ws.close(code=WSCloseCode.POLICY_VIOLATION, message=b'Authentication required')
            return ws
        
        # 保存连接
        self.clients.add(ws)
        client_id = id(ws)
        
        try:
            # 发送欢迎消息
            await ws.send_json({
                'type': 'welcome',
                'payload': {
                    'message': '欢迎连接到XyBotV2 WebSocket服务',
                    'user': user['username'],
                    'timestamp': datetime.now().isoformat()
                }
            })
            
            # 启动系统统计信息发送任务
            stats_task = asyncio.create_task(
                self._send_system_stats(ws, self.stats_update_interval)
            )
            self.tasks[client_id] = stats_task
            
            # 消息处理循环
            async for msg in ws:
                if msg.type == web.WSMsgType.TEXT:
                    try:
                        data = json.loads(msg.data)
                        await self._handle_message(ws, data, user)
                    except json.JSONDecodeError:
                        await ws.send_json({
                            'type': 'error',
                            'payload': {'message': '无效的JSON格式'}
                        })
                elif msg.type == web.WSMsgType.ERROR:
                    logger.error(f'WebSocket连接错误: {ws.exception()}')
                    break
            
        finally:
            # 清理连接
            self.clients.discard(ws)
            if client_id in self.tasks:
                self.tasks[client_id].cancel()
                del self.tasks[client_id]
            
            if not ws.closed:
                await ws.close()
            
            logger.debug(f"WebSocket连接关闭，当前连接数: {len(self.clients)}")
        
        return ws
    
    async def _handle_message(self, ws, data, user):
        """
        处理WebSocket消息
        
        Args:
            ws: WebSocket连接
            data: 消息数据
            user: 用户信息
        """
        msg_type = data.get('type')
        
        if msg_type == 'ping':
            # 处理心跳
            await ws.send_json({
                'type': 'pong',
                'payload': {'timestamp': datetime.now().isoformat()}
            })
        elif msg_type == 'get_bot_status':
            # 发送机器人状态
            await self._send_bot_status(ws)
        else:
            # 未知消息类型
            await ws.send_json({
                'type': 'error',
                'payload': {'message': f'未知的消息类型: {msg_type}'}
            })
    
    async def _send_system_stats(self, ws, interval):
        """
        定时发送系统统计信息
        
        Args:
            ws: WebSocket连接
            interval: 更新间隔（毫秒）
        """
        try:
            while True:
                # 获取系统信息
                cpu = psutil.cpu_percent(interval=0.5)
                memory = psutil.virtual_memory()
                disk = psutil.disk_usage('/')
                
                stats = {
                    'cpu': {
                        'percent': cpu
                    },
                    'memory': {
                        'total': memory.total,
                        'available': memory.available,
                        'percent': memory.percent
                    },
                    'disk': {
                        'total': disk.total,
                        'free': disk.free,
                        'percent': disk.percent
                    },
                    'timestamp': datetime.now().isoformat()
                }
                
                # 发送统计信息
                if not ws.closed:
                    await ws.send_json({
                        'type': 'system_stats',
                        'payload': stats
                    })
                
                # 等待下一次更新
                await asyncio.sleep(interval / 1000)  # 转换为秒
        except asyncio.CancelledError:
            # 任务被取消时正常退出
            pass
        except Exception as e:
            logger.exception(f"发送系统统计数据时出错: {str(e)}")
            if not ws.closed:
                await ws.send_json({
                    'type': 'error',
                    'payload': {'message': f'System stats error: {str(e)}'}
                })
    
    async def _send_bot_status(self, ws):
        """
        发送机器人状态信息
        
        Args:
            ws: WebSocket连接
        """
        try:
            # 获取机器人状态
            bot_status = {
                'version': getattr(self.bot, 'version', 'unknown'),
                'uptime': getattr(self.bot, 'uptime', 0),
                'plugins_count': len(getattr(self.bot, 'plugins', [])),
                'is_running': getattr(self.bot, 'is_running', False),
                'timestamp': datetime.now().isoformat()
            }
            
            # 发送状态信息
            await ws.send_json({
                'type': 'bot_status',
                'payload': bot_status
            })
        except Exception as e:
            logger.exception(f"发送机器人状态数据时出错: {str(e)}")
            if not ws.closed:
                await ws.send_json({
                    'type': 'error',
                    'payload': {'message': f'Bot status error: {str(e)}'}
                })
    
    async def close_all_connections(self):
        """关闭所有WebSocket连接"""
        for ws in self.clients:
            if not ws.closed:
                await ws.close(code=WSCloseCode.GOING_AWAY, 
                               message=b'Server shutdown')
        self.clients.clear()
        
        # 取消所有任务
        for task in self.tasks.values():
            task.cancel()
        
        if self.tasks:
            await asyncio.gather(*self.tasks.values(), return_exceptions=True)
            self.tasks.clear() 