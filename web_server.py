import os
import json
import asyncio
from aiohttp import web, WSCloseCode
import aiohttp_cors
from pathlib import Path
import psutil
from datetime import datetime
from .auth import AuthManager  # 导入认证管理器
import toml  # 导入toml包用于读取配置

class XyBotWebServer:
    def __init__(self, bot_instance, config_path='main_config.toml'):
        self.bot = bot_instance
        
        # 加载配置文件
        self.config = self._load_config(config_path)
        
        # 从配置中获取Web服务器设置
        self.port = self.config.get('web', {}).get('port', 8080)
        self.host = self.config.get('web', {}).get('host', '0.0.0.0')
        self.debug = self.config.get('web', {}).get('debug', False)
        self.static_path = self.config.get('web', {}).get('static_path', 'web_ui/dist')
        
        # 获取认证相关配置
        auth_config = self.config.get('web', {}).get('auth', {})
        token_expire_hours = auth_config.get('token_expire_hours', 24)
        
        self.app = web.Application()
        
        # 使用bot实例提供的Redis客户端初始化认证管理器
        self.redis = bot_instance.api.redis_client
        self.auth_manager = AuthManager(
            redis_client=self.redis,
            token_expire_hours=token_expire_hours
        )
        
        # 安全配置
        security_config = self.config.get('web', {}).get('security', {})
        self.enable_cors = security_config.get('enable_cors', True)
        self.cors_allow_origins = security_config.get('cors_allow_origins', ['*'])
        
        # WebSocket配置
        ws_config = self.config.get('web', {}).get('websocket', {})
        self.ws_enabled = ws_config.get('enabled', True)
        self.ws_ping_interval = ws_config.get('ping_interval', 30)
        self.ws_max_clients = ws_config.get('max_clients', 50)
        self.ws_stats_update_interval = ws_config.get('stats_update_interval', 5000)
        
        self.setup_routes()
        
        if self.enable_cors:
            self.setup_cors()
            
        self.setup_static_files()
        self.ws_clients = set()
        self.ws_tasks = {}
    
    def _load_config(self, config_path):
        """加载配置文件"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return toml.load(f)
        except Exception as e:
            print(f"加载配置文件失败: {str(e)}，使用默认配置")
            return {
                'web': {
                    'port': 8080,
                    'host': '0.0.0.0',
                    'debug': False,
                    'static_path': 'web_ui/dist',
                    'auth': {
                        'token_expire_hours': 24,
                        'auth_config_path': 'config/auth.json'
                    },
                    'security': {
                        'enable_cors': True,
                        'cors_allow_origins': ['*']
                    },
                    'websocket': {
                        'enabled': True,
                        'ping_interval': 30,
                        'max_clients': 50,
                        'stats_update_interval': 5000
                    }
                }
            }
    
    def setup_routes(self):
        """设置API路由"""
        # 认证相关路由
        self.app.router.add_post('/api/auth/login', self.login)
        self.app.router.add_post('/api/auth/logout', self.logout)
        self.app.router.add_get('/api/auth/verify', self.verify_token)
        self.app.router.add_post('/api/auth/change-password', self.change_password)
        
        # 原有路由，添加认证中间件
        self.app.router.add_get('/api/status', self.auth_middleware(self.get_status))
        self.app.router.add_get('/api/plugins', self.auth_middleware(self.get_plugins))
        self.app.router.add_post('/api/plugins/{plugin_id}/toggle', self.auth_middleware(self.toggle_plugin))
        self.app.router.add_get('/api/messages/recent', self.auth_middleware(self.get_recent_messages))
        self.app.router.add_get('/api/system/info', self.auth_middleware(self.get_system_info))
        self.app.router.add_get('/api/plugins/{plugin_id}/config', self.auth_middleware(self.get_plugin_config))
        self.app.router.add_post('/api/plugins/{plugin_id}/config', self.auth_middleware(self.save_plugin_config))
        self.app.router.add_post('/api/plugins/{plugin_id}/reload', self.auth_middleware(self.reload_plugin))
        self.app.router.add_get('/api/plugins/dependency-graph', self.auth_middleware(self.get_plugin_dependency_graph))
        self.app.router.add_get('/api/settings', self.auth_middleware(self.get_system_settings))
        self.app.router.add_post('/api/settings', self.auth_middleware(self.save_system_settings))
        self.app.router.add_get('/api/logs', self.auth_middleware(self.get_logs))
        self.app.router.add_post('/api/system/restart', self.auth_middleware(self.restart_system))
        self.app.router.add_get('/api/ws', self.websocket_handler)
    
    def setup_cors(self):
        """设置跨域资源共享"""
        cors = aiohttp_cors.setup(self.app, defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
            )
        })
        
        # 为所有路由添加CORS支持
        for route in list(self.app.router.routes()):
            cors.add(route)
    
    def setup_static_files(self):
        """设置静态文件服务"""
        static_path = Path(__file__).parent / self.static_path
        if static_path.exists():
            self.app.router.add_static('/dashboard/', path=str(static_path), name='dashboard')
            self.app.router.add_get('/', self.redirect_to_dashboard)
        else:
            os.makedirs(static_path, exist_ok=True)
            # 创建一个临时页面，提示需要构建前端
            with open(static_path / "index.html", "w") as f:
                f.write("<html><body><h1>XyBotV2控制面板</h1><p>前端界面尚未构建，请运行构建命令。</p></body></html>")
    
    async def redirect_to_dashboard(self, request):
        """将根路径重定向到仪表盘"""
        return web.HTTPFound('/dashboard/')
    
    async def auth_middleware(self, handler):
        """认证中间件，修改为异步方法"""
        async def middleware(request):
            auth_header = request.headers.get('Authorization', '')
            token = None
            
            if auth_header.startswith('Bearer '):
                token = auth_header[7:].strip()
            else:
                token = request.query.get('token', '')
            
            if not token:
                return web.json_response(
                    {"error": "未授权访问"},
                    status=401
                )
            
            user = await self.auth_manager.validate_token(token)
            
            if not user:
                return web.json_response(
                    {"error": "无效或过期的令牌"},
                    status=401
                )
            
            # 添加用户信息到请求中
            request['user'] = user
            
            # 调用原始处理程序
            return await handler(request)
        
        return middleware
    
    async def login(self, request):
        """用户登录"""
        try:
            data = await request.json()
            username = data.get('username')
            password = data.get('password')
            
            if not username or not password:
                return web.json_response(
                    {"error": "用户名和密码不能为空"},
                    status=400
                )
            
            auth_result = await self.auth_manager.authenticate(username, password)
            
            if auth_result:
                return web.json_response(auth_result)
            else:
                return web.json_response(
                    {"error": "用户名或密码错误"},
                    status=401
                )
        except Exception as e:
            return web.json_response({"error": str(e)}, status=500)
    
    async def logout(self, request):
        """用户注销"""
        try:
            data = await request.json()
            token = data.get('token')
            
            if not token:
                return web.json_response(
                    {"error": "令牌不能为空"}, 
                    status=400
                )
            
            success = await self.auth_manager.revoke_token(token)
            
            return web.json_response({"success": success})
        except Exception as e:
            return web.json_response({"error": str(e)}, status=500)
    
    async def verify_token(self, request):
        """验证访问令牌"""
        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            token = auth_header[7:].strip()
        else:
            token = request.query.get('token', '')
        
        if not token:
            return web.json_response({"valid": False}, status=401)
        
        user = await self.auth_manager.validate_token(token)
        
        if user:
            return web.json_response({
                "valid": True,
                "username": user.get('username'),
                "role": user.get('role')
            })
        
        return web.json_response({"valid": False}, status=401)
    
    async def change_password(self, request):
        """修改用户密码"""
        try:
            data = await request.json()
            username = data.get('username')
            old_password = data.get('oldPassword')
            new_password = data.get('newPassword')
            
            if not all([username, old_password, new_password]):
                return web.json_response(
                    {"error": "缺少必要参数"},
                    status=400
                )
            
            success = await self.auth_manager.change_password(username, old_password, new_password)
            
            if success:
                return web.json_response({"success": True})
            else:
                return web.json_response(
                    {"error": "密码修改失败，请确认用户名和原密码正确"},
                    status=400
                )
        
        except Exception as e:
            return web.json_response({"error": str(e)}, status=500)
    
    async def get_status(self, request):
        """获取机器人状态"""
        try:
            is_online = await self.bot.is_logged_in()
            status_data = {
                "online": is_online,
                "uptime": self.bot.get_uptime(),
                "last_activity": self.bot.get_last_activity_time(),
                "version": "XyBotV2 " + self.bot.version
            }
            return web.json_response(status_data)
        except Exception as e:
            return web.json_response({"error": str(e)}, status=500)
    
    async def get_plugins(self, request):
        """获取插件列表及状态"""
        try:
            plugins_data = []
            for plugin_id, plugin in self.bot.plugin_manager.plugins.items():
                plugins_data.append({
                    "id": plugin_id,
                    "name": getattr(plugin, "name", plugin_id),
                    "description": getattr(plugin, "description", ""),
                    "author": getattr(plugin, "author", ""),
                    "version": getattr(plugin, "version", "1.0.0"),
                    "enabled": plugin.enabled,
                    "config_path": str(Path(plugin.__module__).parent / "config.toml")
                })
            return web.json_response(plugins_data)
        except Exception as e:
            return web.json_response({"error": str(e)}, status=500)
    
    async def toggle_plugin(self, request):
        """启用或禁用插件"""
        plugin_id = request.match_info.get('plugin_id')
        try:
            data = await request.json()
            enable = data.get('enable', True)
            
            result = await self.bot.plugin_manager.toggle_plugin(plugin_id, enable)
            return web.json_response({"success": result, "enabled": enable})
        except Exception as e:
            return web.json_response({"error": str(e)}, status=500)
    
    async def get_recent_messages(self, request):
        """获取最近消息"""
        try:
            limit = int(request.query.get('limit', 20))
            messages = self.bot.get_recent_messages(limit)
            return web.json_response(messages)
        except Exception as e:
            return web.json_response({"error": str(e)}, status=500)
    
    async def get_system_info(self, request):
        """获取系统信息"""
        try:
            import psutil
            import platform
            
            cpu_percent = psutil.cpu_percent()
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            system_info = {
                "cpu": {
                    "percent": cpu_percent,
                    "cores": psutil.cpu_count()
                },
                "memory": {
                    "total": memory.total,
                    "available": memory.available,
                    "percent": memory.percent
                },
                "disk": {
                    "total": disk.total,
                    "free": disk.free,
                    "percent": disk.percent
                },
                "platform": {
                    "system": platform.system(),
                    "release": platform.release(),
                    "version": platform.version()
                },
                "python": platform.python_version()
            }
            return web.json_response(system_info)
        except Exception as e:
            return web.json_response({"error": str(e)}, status=500)
    
    async def get_plugin_config(self, request):
        """获取插件配置"""
        plugin_id = request.match_info.get('plugin_id')
        try:
            plugin = self.bot.plugin_manager.get_plugin(plugin_id)
            if not plugin:
                return web.json_response({"error": "插件不存在"}, status=404)
            
            config_path = Path(plugin.__module__).parent / "config.toml"
            if not config_path.exists():
                return web.json_response({"error": "配置文件不存在"}, status=404)
            
            with open(config_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            return web.json_response({
                "content": content
            })
        except Exception as e:
            return web.json_response({"error": str(e)}, status=500)
    
    async def save_plugin_config(self, request):
        """保存插件配置"""
        plugin_id = request.match_info.get('plugin_id')
        try:
            data = await request.json()
            content = data.get('content')
            
            if not content:
                return web.json_response({"error": "配置内容不能为空"}, status=400)
            
            plugin = self.bot.plugin_manager.get_plugin(plugin_id)
            if not plugin:
                return web.json_response({"error": "插件不存在"}, status=404)
            
            config_path = Path(plugin.__module__).parent / "config.toml"
            
            # 尝试解析TOML以验证格式是否正确
            try:
                import tomli
                tomli.loads(content)
            except Exception as e:
                return web.json_response({"error": f"配置格式错误: {str(e)}"}, status=400)
            
            # 保存配置
            with open(config_path, "w", encoding="utf-8") as f:
                f.write(content)
            
            return web.json_response({"success": True})
        except Exception as e:
            return web.json_response({"error": str(e)}, status=500)
    
    async def get_system_settings(self, request):
        """获取系统设置"""
        try:
            # 这里应该从配置文件或数据库中读取设置
            # 目前使用示例数据
            settings = {
                "general": {
                    "botName": "XyBotV2",
                    "autoRestart": True,
                    "logLevel": "INFO"
                },
                "webServer": {
                    "enabled": True,
                    "port": 8080,
                    "requireAuth": False
                },
                "notifications": {
                    "statusChange": True,
                    "errors": True,
                    "method": "pushplus"
                }
            }
            return web.json_response(settings)
        except Exception as e:
            return web.json_response({"error": str(e)}, status=500)
    
    async def save_system_settings(self, request):
        """保存系统设置"""
        try:
            # 获取要保存的设置
            data = await request.json()
            
            # 这里应该将设置保存到配置文件或数据库
            # 目前仅返回成功响应
            
            return web.json_response({"success": True})
        except Exception as e:
            return web.json_response({"error": str(e)}, status=500)
    
    async def get_logs(self, request):
        """获取系统日志"""
        try:
            limit = int(request.query.get('limit', 200))
            level = request.query.get('level', None)
            
            # 日志文件路径
            log_path = Path("logs")
            log_files = list(log_path.glob("XYBot_*.log"))
            log_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            
            logs = []
            
            # 读取最新的日志文件
            if log_files:
                current_file = log_files[0]
                with open(current_file, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    # 从末尾开始读取指定数量的行
                    for line in reversed(lines[-limit:]):
                        parts = line.strip().split(" | ", 2)
                        if len(parts) >= 3:
                            timestamp, log_level, message = parts
                            
                            # 如果指定了日志级别过滤
                            if level and log_level != level:
                                continue
                            
                            # 解析元数据（如果存在）
                            metadata = None
                            traceback = None
                            if "[METADATA]" in message:
                                message_parts = message.split("[METADATA]", 1)
                                message = message_parts[0].strip()
                                try:
                                    metadata = json.loads(message_parts[1].strip())
                                except:
                                    metadata = {"raw": message_parts[1].strip()}
                            
                            # 解析traceback（如果存在）
                            if "[TRACEBACK]" in message:
                                message_parts = message.split("[TRACEBACK]", 1)
                                message = message_parts[0].strip()
                                traceback = message_parts[1].strip()
                            
                            log_entry = {
                                "timestamp": timestamp,
                                "level": log_level,
                                "message": message,
                                "metadata": metadata,
                                "traceback": traceback
                            }
                            logs.append(log_entry)
                            
                            # 达到限制数量时停止
                            if len(logs) >= limit:
                                break
            
            # 根据时间戳排序，最新的在前
            logs.sort(key=lambda x: x["timestamp"], reverse=True)
            
            return web.json_response(logs)
        except Exception as e:
            return web.json_response({"error": str(e)}, status=500)
    
    async def restart_system(self, request):
        """重启系统"""
        try:
            await self.bot.restart()
            return web.json_response({"success": True})
        except Exception as e:
            return web.json_response({"error": str(e)}, status=500)
    
    async def websocket_handler(self, request):
        """处理WebSocket连接"""
        # 认证检查
        token = request.query.get('token')
        if not token or not self.auth_manager.validate_token(token):
            return web.Response(status=401, text='未授权访问')
        
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        
        # 将新连接添加到客户端集合
        self.ws_clients.add(ws)
        client_id = id(ws)
        subscriptions = set()
        
        try:
            async for msg in ws:
                if msg.type == web.WSMsgType.TEXT:
                    try:
                        data = json.loads(msg.data)
                        await self._handle_ws_message(ws, data, client_id, subscriptions)
                    except json.JSONDecodeError:
                        await ws.send_json({
                            'type': 'error',
                            'payload': {'message': 'Invalid JSON format'}
                        })
                elif msg.type == web.WSMsgType.ERROR:
                    print(f'WebSocket连接错误: {ws.exception()}')
        finally:
            # 清理连接和相关任务
            self.ws_clients.remove(ws)
            for channel in list(subscriptions):
                await self._unsubscribe(ws, client_id, channel, subscriptions)
            
        return ws
    
    async def _handle_ws_message(self, ws, data, client_id, subscriptions):
        """处理WebSocket消息"""
        msg_type = data.get('type')
        payload = data.get('payload', {})
        
        if msg_type == 'subscribe':
            channel = payload.get('channel')
            interval = payload.get('interval', 5000)  # 默认5秒
            
            if channel:
                await self._subscribe(ws, client_id, channel, interval, subscriptions)
                await ws.send_json({
                    'type': 'subscription_success',
                    'payload': {'channel': channel}
                })
        
        elif msg_type == 'unsubscribe':
            channel = payload.get('channel')
            if channel and channel in subscriptions:
                await self._unsubscribe(ws, client_id, channel, subscriptions)
                await ws.send_json({
                    'type': 'unsubscription_success',
                    'payload': {'channel': channel}
                })
        
        else:
            await ws.send_json({
                'type': 'error',
                'payload': {'message': f'Unknown message type: {msg_type}'}
            })
    
    async def _subscribe(self, ws, client_id, channel, interval, subscriptions):
        """订阅一个通道"""
        # 取消之前的订阅（如果存在）
        await self._unsubscribe(ws, client_id, channel, subscriptions)
        
        # 添加新订阅
        subscriptions.add(channel)
        
        # 创建对应的任务
        task_key = f"{client_id}_{channel}"
        
        if channel == 'system_stats':
            self.ws_tasks[task_key] = asyncio.create_task(
                self._send_system_stats(ws, interval)
            )
        elif channel == 'messages':
            self.ws_tasks[task_key] = asyncio.create_task(
                self._send_recent_messages(ws, interval)
            )
        # 可以添加更多通道类型
    
    async def _unsubscribe(self, ws, client_id, channel, subscriptions):
        """取消订阅一个通道"""
        if channel in subscriptions:
            subscriptions.remove(channel)
        
        # 取消并删除相应的任务
        task_key = f"{client_id}_{channel}"
        if task_key in self.ws_tasks:
            self.ws_tasks[task_key].cancel()
            try:
                await self.ws_tasks[task_key]
            except asyncio.CancelledError:
                pass
            del self.ws_tasks[task_key]
    
    async def _send_system_stats(self, ws, interval):
        """发送系统统计数据，使用配置的更新间隔"""
        try:
            while True:
                # 获取系统信息
                cpu = psutil.cpu_percent(interval=0.5)
                memory = psutil.virtual_memory()
                disk = psutil.disk_usage('/')
                network = psutil.net_io_counters()
                
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
                        'used': disk.used,
                        'free': disk.free,
                        'percent': disk.percent
                    },
                    'network': {
                        'bytes_sent': network.bytes_sent,
                        'bytes_recv': network.bytes_recv
                    },
                    'timestamp': datetime.now().isoformat()
                }
                
                # 发送数据
                await ws.send_json({
                    'type': 'system_stats',
                    'payload': stats
                })
                
                # 使用配置的更新间隔
                await asyncio.sleep(self.ws_stats_update_interval / 1000)  # 转换为秒
        except asyncio.CancelledError:
            # 任务被取消时正常退出
            pass
        except Exception as e:
            print(f"发送系统统计数据时出错: {str(e)}")
            if not ws.closed:
                await ws.send_json({
                    'type': 'error',
                    'payload': {'message': f'System stats error: {str(e)}'}
                })
    
    async def _send_recent_messages(self, ws, interval):
        """发送最近消息"""
        try:
            last_message_time = datetime.now()
            while True:
                # 获取新消息
                recent_messages = await self._get_new_messages(last_message_time)
                
                if recent_messages:
                    last_message_time = datetime.now()
                    await ws.send_json({
                        'type': 'messages',
                        'payload': {'messages': recent_messages}
                    })
                
                # 等待下一次更新
                await asyncio.sleep(interval / 1000)  # 转换为秒
        except asyncio.CancelledError:
            # 任务被取消时正常退出
            pass
        except Exception as e:
            print(f"发送最近消息时出错: {str(e)}")
            if not ws.closed:
                await ws.send_json({
                    'type': 'error',
                    'payload': {'message': f'Recent messages error: {str(e)}'}
                })
    
    async def _get_new_messages(self, since_time):
        """获取指定时间后的新消息"""
        # 这里实现获取最新消息的逻辑
        # 例如从数据库或内存中获取
        return []  # 返回消息列表
    
    async def close_all_ws_connections(self):
        """关闭所有WebSocket连接"""
        for ws in self.ws_clients:
            if not ws.closed:
                await ws.close(code=WSCloseCode.GOING_AWAY, 
                               message=b'Server shutdown')
        self.ws_clients.clear()
        
        # 取消所有任务
        for task in self.ws_tasks.values():
            task.cancel()
        await asyncio.gather(*self.ws_tasks.values(), return_exceptions=True)
        self.ws_tasks.clear()
    
    async def start(self):
        """启动Web服务器，使用配置的主机和端口"""
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, self.host, self.port)
        await site.start()
        print(f"Web管理界面已启动，请访问 http://{self.host if self.host != '0.0.0.0' else 'localhost'}:{self.port}/")
        return runner 