"""
Web路由模块
定义API路由和处理函数
"""

from aiohttp import web
import logging
import json
from datetime import datetime

logger = logging.getLogger(__name__)

def setup_routes(server):
    """
    设置Web服务器路由
    
    Args:
        server: WebServer实例
    """
    app = server.app
    
    # API路由组
    api_routes = web.RouteTableDef()
    
    # 无需认证的API
    @api_routes.post('/api/auth/login')
    async def login(request):
        """用户登录"""
        if server.auth_manager is None:
            return web.json_response({"error": "认证服务不可用"}, status=500)
            
        try:
            data = await request.json()
            username = data.get('username')
            password = data.get('password')
            
            if not username or not password:
                return web.json_response(
                    {"error": "用户名和密码不能为空"}, 
                    status=400
                )
            
            success, result = await server.auth_manager.authenticate(username, password)
            
            if success:
                return web.json_response(result)
            else:
                return web.json_response(result, status=401)
        except Exception as e:
            logger.exception("登录处理出错")
            return web.json_response({"error": str(e)}, status=500)
    
    @api_routes.post('/api/auth/logout')
    async def logout(request):
        """用户注销"""
        if server.auth_manager is None:
            return web.json_response({"error": "认证服务不可用"}, status=500)
            
        try:
            data = await request.json()
            token = data.get('token')
            
            if not token:
                return web.json_response(
                    {"error": "令牌不能为空"}, 
                    status=400
                )
            
            success = await server.auth_manager.revoke_token(token)
            
            return web.json_response({"success": success})
        except Exception as e:
            logger.exception("注销处理出错")
            return web.json_response({"error": str(e)}, status=500)
    
    @api_routes.get('/api/auth/verify')
    async def verify_token(request):
        """验证访问令牌"""
        if server.auth_manager is None:
            return web.json_response({"error": "认证服务不可用"}, status=500)
            
        auth_header = request.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            token = auth_header[7:].strip()
        else:
            token = request.query.get('token', '')
        
        if not token:
            return web.json_response({"valid": False}, status=401)
        
        user = await server.auth_manager.validate_token(token)
        
        if user:
            return web.json_response({
                "valid": True,
                "username": user.get('username'),
                "role": user.get('role')
            })
        
        return web.json_response({"valid": False}, status=401)
    
    # 需要认证的API
    
    # 使用认证中间件创建受保护的API组
    auth_routes = web.RouteTableDef()
    
    @auth_routes.get('/api/system/info')
    async def system_info(request):
        """获取系统信息"""
        import psutil
        import platform
        import os
        
        system_info = {
            'platform': platform.platform(),
            'python': platform.python_version(),
            'cpu_count': psutil.cpu_count(),
            'memory_total': psutil.virtual_memory().total,
            'disk_total': psutil.disk_usage('/').total,
        }
        
        return web.json_response(system_info)
    
    @auth_routes.get('/api/bot/status')
    async def bot_status(request):
        """获取机器人状态"""
        bot = server.bot
        
        status = {
            'version': getattr(bot, 'version', 'unknown'),
            'uptime': getattr(bot, 'uptime', 0),
            'plugins_count': len(getattr(bot, 'plugins', [])),
            'is_running': getattr(bot, 'is_running', False)
        }
        
        return web.json_response(status)
    
    @auth_routes.post('/api/auth/change-password')
    async def change_password(request):
        """修改密码"""
        if server.auth_manager is None:
            return web.json_response({"error": "认证服务不可用"}, status=500)
            
        try:
            data = await request.json()
            username = data.get('username')
            old_password = data.get('oldPassword')
            new_password = data.get('newPassword')
            
            if not all([username, old_password, new_password]):
                return web.json_response(
                    {"error": "所有字段都是必填的"}, 
                    status=400
                )
            
            success = await server.auth_manager.change_password(
                username, old_password, new_password
            )
            
            if success:
                return web.json_response({"success": True})
            else:
                return web.json_response(
                    {"error": "密码修改失败，请确认用户名和原密码正确"},
                    status=400
                )
        
        except Exception as e:
            logger.exception("修改密码处理出错")
            return web.json_response({"error": str(e)}, status=500)
    
    # WebSocket路由
    @auth_routes.get('/api/ws')
    async def websocket_handler(request):
        """WebSocket连接处理"""
        return await server.ws_manager.handle_connection(request)
    
    # 注册路由
    app.add_routes(api_routes)
    
    # 为auth_routes应用认证中间件
    for route in auth_routes:
        route_handler = route.handler
        route._handler = server.auth_middleware(route_handler)
    
    app.add_routes(auth_routes) 