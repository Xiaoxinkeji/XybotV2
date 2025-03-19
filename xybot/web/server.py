"""
Web服务器模块
提供Web管理界面和API服务
"""

import os
import json
import asyncio
from aiohttp import web, WSCloseCode
import aiohttp_cors
from pathlib import Path
import psutil
import logging
from datetime import datetime

from ..auth.manager import AuthManager
from ..utils.config import ConfigManager
from .routes import setup_routes
from .websocket import WebSocketManager

logger = logging.getLogger(__name__)

class WebServer:
    """Web服务器类"""
    
    def __init__(self, bot_instance, config_manager=None):
        """
        初始化Web服务器
        
        Args:
            bot_instance: 机器人实例
            config_manager: 配置管理器实例，如果为None则创建新实例
        """
        self.bot = bot_instance
        
        # 初始化配置
        self.config_manager = config_manager or ConfigManager()
        
        # 加载Web服务器配置
        self.port = self.config_manager.get('web.port', 8080)
        self.host = self.config_manager.get('web.host', '0.0.0.0')
        self.debug = self.config_manager.get('web.debug', False)
        self.static_path = self.config_manager.get('web.static_path', 'web_ui/dist')
        
        # 获取认证相关配置
        token_expire_hours = self.config_manager.get('web.auth.token_expire_hours', 24)
        
        # 创建Web应用
        self.app = web.Application(middlewares=[
            self.error_middleware
        ])
        
        # 初始化认证管理器
        if hasattr(bot_instance, 'api') and hasattr(bot_instance.api, 'redis_client'):
            self.redis = bot_instance.api.redis_client
            self.auth_manager = AuthManager(
                redis_client=self.redis,
                token_expire_hours=token_expire_hours
            )
        else:
            logger.error("Bot实例没有提供Redis客户端，认证功能将不可用")
            self.auth_manager = None
            self.redis = None
        
        # 安全配置
        self.enable_cors = self.config_manager.get('web.security.enable_cors', True)
        self.cors_allow_origins = self.config_manager.get('web.security.cors_allow_origins', ['*'])
        
        # 初始化WebSocket管理器
        ws_config = {
            'enabled': self.config_manager.get('web.websocket.enabled', True),
            'ping_interval': self.config_manager.get('web.websocket.ping_interval', 30),
            'max_clients': self.config_manager.get('web.websocket.max_clients', 50),
            'stats_update_interval': self.config_manager.get('web.websocket.stats_update_interval', 5000)
        }
        self.ws_manager = WebSocketManager(self.bot, ws_config)
        
        # 设置路由
        setup_routes(self)
        
        if self.enable_cors:
            self.setup_cors()
        
        self.setup_static_files()
    
    @web.middleware
    async def error_middleware(self, request, handler):
        """全局错误处理中间件"""
        try:
            return await handler(request)
        except web.HTTPException as ex:
            # 处理HTTP异常
            return web.json_response({
                'error': str(ex),
                'status': ex.status
            }, status=ex.status)
        except Exception as e:
            # 处理所有其他异常
            logger.exception(f"处理请求时出错: {str(e)}")
            return web.json_response({
                'error': '服务器内部错误',
                'message': str(e) if self.debug else None
            }, status=500)
    
    def setup_cors(self):
        """设置CORS"""
        cors = aiohttp_cors.setup(self.app, defaults={
            origin: aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*"
            ) for origin in self.cors_allow_origins
        })
        
        # 为所有路由添加CORS支持
        for route in list(self.app.router.routes()):
            cors.add(route)
    
    def setup_static_files(self):
        """设置静态文件服务"""
        static_path = Path(__file__).parent.parent.parent / self.static_path
        if static_path.exists():
            self.app.router.add_static('/dashboard/', path=str(static_path), name='dashboard')
            # 添加前端路由支持，所有不存在的路由都转到index.html
            self.app.router.add_get('/dashboard/{tail:.*}', self.handle_frontend_routes)
        else:
            logger.warning(f"静态文件目录不存在: {static_path}")
    
    async def handle_frontend_routes(self, request):
        """处理前端路由，支持SPA"""
        index_path = Path(__file__).parent.parent.parent / self.static_path / 'index.html'
        if index_path.exists():
            return web.FileResponse(index_path)
        return web.Response(text="Web UI not found. Please build it first.", content_type='text/html')
    
    async def auth_middleware(self, handler):
        """认证中间件"""
        async def middleware(request):
            if self.auth_manager is None:
                return web.json_response({"error": "认证服务不可用"}, status=500)
                
            auth_header = request.headers.get('Authorization', '')
            token = None
            
            if auth_header.startswith('Bearer '):
                token = auth_header[7:].strip()
            else:
                token = request.query.get('token', '')
            
            if not token:
                return web.json_response({"error": "未授权访问"}, status=401)
            
            user = await self.auth_manager.validate_token(token)
            
            if not user:
                return web.json_response({"error": "无效或过期的令牌"}, status=401)
            
            # 添加用户信息到请求中
            request['user'] = user
            
            # 调用原始处理程序
            return await handler(request)
        
        return middleware
    
    async def start(self):
        """启动Web服务器"""
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, self.host, self.port)
        await site.start()
        logger.info(f"Web管理界面已启动，请访问 http://{self.host if self.host != '0.0.0.0' else 'localhost'}:{self.port}/dashboard/")
        return runner
    
    async def shutdown(self):
        """关闭Web服务器"""
        if hasattr(self, 'ws_manager'):
            await self.ws_manager.close_all_connections() 