"""
认证管理模块
处理用户认证、令牌管理和权限控制
使用Redis存储认证数据
"""

import os
import time
import hashlib
import secrets
import json
import base64
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class AuthManager:
    """认证管理器，使用Redis存储认证数据"""
    
    # Redis键前缀
    REDIS_KEY_USERS = "xybot:web:users"
    REDIS_KEY_TOKENS = "xybot:web:tokens"
    REDIS_KEY_SECRET = "xybot:web:secret_key"
    
    def __init__(self, redis_client, token_expire_hours: int = 24):
        """
        初始化认证管理器
        
        Args:
            redis_client: Redis客户端实例
            token_expire_hours: 令牌过期时间（小时）
        """
        self.redis = redis_client
        self.token_expire_hours = token_expire_hours
        
        # 初始化或加载配置
        self._ensure_initialized()
    
    async def _ensure_initialized(self) -> None:
        """确保认证系统已初始化"""
        # 检查Redis中是否已有用户数据和密钥
        has_users = await self.redis.exists(self.REDIS_KEY_USERS)
        has_secret = await self.redis.exists(self.REDIS_KEY_SECRET)
        
        if not has_users or not has_secret:
            await self._create_default_config()
    
    async def _create_default_config(self) -> None:
        """创建默认配置，包括默认管理员账户"""
        # 生成随机密钥
        secret_key = secrets.token_hex(32)
        await self.redis.set(self.REDIS_KEY_SECRET, secret_key)
        
        # 默认管理员账户
        default_password = 'admin123'  # 默认密码
        password_hash = self._hash_password(default_password)
        
        admin_user = {
            'username': 'admin',
            'password_hash': password_hash,
            'role': 'admin',
            'created_at': datetime.now().isoformat()
        }
        
        # 存储到Redis
        await self.redis.hset(self.REDIS_KEY_USERS, 'admin', json.dumps(admin_user))
        
        logger.info("认证系统已初始化，创建了默认管理员账户: admin / admin123")
    
    async def _get_secret_key(self) -> str:
        """获取密钥"""
        secret_key = await self.redis.get(self.REDIS_KEY_SECRET)
        if not secret_key:
            secret_key = secrets.token_hex(32)
            await self.redis.set(self.REDIS_KEY_SECRET, secret_key)
        return secret_key.decode('utf-8') if isinstance(secret_key, bytes) else secret_key
    
    def _hash_password(self, password: str) -> str:
        """
        使用PBKDF2算法哈希密码
        
        Args:
            password: 明文密码
            
        Returns:
            密码哈希值
        """
        # 生成随机盐值
        salt = os.urandom(16)
        
        # 使用PBKDF2算法
        key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000  # 迭代次数
        )
        
        # 将盐值和密钥合并并编码
        return base64.b64encode(salt + key).decode('utf-8')
    
    def _verify_password(self, stored_hash: str, password: str) -> bool:
        """
        验证密码
        
        Args:
            stored_hash: 存储的密码哈希
            password: 要验证的明文密码
            
        Returns:
            密码是否正确
        """
        try:
            # 解码存储的哈希
            decoded = base64.b64decode(stored_hash)
            
            # 提取盐值
            salt = decoded[:16]
            
            # 提取存储的密钥
            stored_key = decoded[16:]
            
            # 使用相同的盐值和算法生成密钥
            key = hashlib.pbkdf2_hmac(
                'sha256',
                password.encode('utf-8'),
                salt,
                100000  # 迭代次数
            )
            
            # 比较密钥
            return secrets.compare_digest(key, stored_key)
            
        except Exception as e:
            logger.error(f"密码验证出错: {str(e)}")
            return False
    
    async def authenticate(self, username: str, password: str) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        认证用户
        
        Args:
            username: 用户名
            password: 密码
            
        Returns:
            (成功与否, 用户信息或错误信息)
        """
        # 获取用户信息
        user_json = await self.redis.hget(self.REDIS_KEY_USERS, username)
        if not user_json:
            return False, {"error": "用户不存在"}
        
        try:
            user = json.loads(user_json)
        except json.JSONDecodeError:
            return False, {"error": "用户数据格式错误"}
        
        # 验证密码
        if not self._verify_password(user['password_hash'], password):
            return False, {"error": "密码不正确"}
        
        # 生成访问令牌
        token = await self._generate_token(username)
        
        # 返回用户信息和令牌
        return True, {
            "username": username,
            "role": user.get('role', 'user'),
            "token": token
        }
    
    async def _generate_token(self, username: str) -> str:
        """
        为用户生成访问令牌
        
        Args:
            username: 用户名
            
        Returns:
            访问令牌
        """
        # 生成随机令牌
        token = secrets.token_hex(32)
        
        # 记录令牌信息
        expires_at = datetime.now() + timedelta(hours=self.token_expire_hours)
        token_info = {
            'username': username,
            'created_at': datetime.now().isoformat(),
            'expires_at': expires_at.isoformat()
        }
        
        # 保存到Redis
        await self.redis.hset(self.REDIS_KEY_TOKENS, token, json.dumps(token_info))
        
        # 设置过期时间
        await self.redis.expire(f"{self.REDIS_KEY_TOKENS}:{token}", int(self.token_expire_hours * 3600))
        
        return token
    
    async def validate_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        验证令牌有效性
        
        Args:
            token: 访问令牌
            
        Returns:
            令牌对应的用户信息或None（如果令牌无效）
        """
        if not token:
            return None
        
        # 获取令牌信息
        token_info_json = await self.redis.hget(self.REDIS_KEY_TOKENS, token)
        if not token_info_json:
            return None
        
        try:
            token_info = json.loads(token_info_json)
        except json.JSONDecodeError:
            return None
        
        # 检查是否过期
        expires_at = datetime.fromisoformat(token_info['expires_at'])
        if datetime.now() > expires_at:
            # 删除过期令牌
            await self.redis.hdel(self.REDIS_KEY_TOKENS, token)
            return None
        
        # 获取用户信息
        username = token_info['username']
        user_json = await self.redis.hget(self.REDIS_KEY_USERS, username)
        if not user_json:
            # 用户不存在，令牌无效
            await self.redis.hdel(self.REDIS_KEY_TOKENS, token)
            return None
        
        user = json.loads(user_json)
        return {
            'username': username,
            'role': user.get('role', 'user')
        }
    
    async def revoke_token(self, token: str) -> bool:
        """
        撤销令牌
        
        Args:
            token: 要撤销的令牌
            
        Returns:
            撤销是否成功
        """
        result = await self.redis.hdel(self.REDIS_KEY_TOKENS, token)
        await self.redis.delete(f"{self.REDIS_KEY_TOKENS}:{token}")
        return result > 0
    
    async def list_users(self) -> Dict[str, Dict[str, Any]]:
        """
        获取所有用户
        
        Returns:
            用户字典
        """
        users_data = await self.redis.hgetall(self.REDIS_KEY_USERS)
        users = {}
        
        for username, user_json in users_data.items():
            try:
                user = json.loads(user_json)
                # 移除敏感信息
                if 'password_hash' in user:
                    del user['password_hash']
                users[username] = user
            except json.JSONDecodeError:
                continue
        
        return users
    
    async def add_user(self, username: str, password: str, role: str = 'user') -> bool:
        """
        添加用户
        
        Args:
            username: 用户名
            password: 密码
            role: 角色
            
        Returns:
            是否成功添加
        """
        # 检查用户是否已存在
        exists = await self.redis.hexists(self.REDIS_KEY_USERS, username)
        if exists:
            return False
        
        # 创建用户
        password_hash = self._hash_password(password)
        user = {
            'username': username,
            'password_hash': password_hash,
            'role': role,
            'created_at': datetime.now().isoformat()
        }
        
        # 保存用户
        await self.redis.hset(self.REDIS_KEY_USERS, username, json.dumps(user))
        return True
    
    async def change_password(self, username: str, old_password: str, new_password: str) -> bool:
        """
        修改用户密码
        
        Args:
            username: 用户名
            old_password: 旧密码
            new_password: 新密码
            
        Returns:
            修改是否成功
        """
        # 获取用户信息
        user_json = await self.redis.hget(self.REDIS_KEY_USERS, username)
        if not user_json:
            return False
        
        user = json.loads(user_json)
        
        # 验证旧密码
        if not self._verify_password(user['password_hash'], old_password):
            return False
        
        # 设置新密码
        user['password_hash'] = self._hash_password(new_password)
        user['updated_at'] = datetime.now().isoformat()
        
        # 更新用户信息
        await self.redis.hset(self.REDIS_KEY_USERS, username, json.dumps(user))
        return True
    
    async def delete_user(self, username: str) -> bool:
        """
        删除用户
        
        Args:
            username: 要删除的用户名
            
        Returns:
            删除是否成功
        """
        # 检查用户是否存在
        exists = await self.redis.hexists(self.REDIS_KEY_USERS, username)
        if not exists:
            return False
        
        # 获取用户信息
        user_json = await self.redis.hget(self.REDIS_KEY_USERS, username)
        user = json.loads(user_json)
        
        # 不允许删除最后一个管理员
        if user['role'] == 'admin':
            # 获取所有用户
            all_users = await self.redis.hgetall(self.REDIS_KEY_USERS)
            admin_count = 0
            
            for u_json in all_users.values():
                u = json.loads(u_json)
                if u['role'] == 'admin':
                    admin_count += 1
            
            if admin_count <= 1:
                return False
        
        # 删除用户
        await self.redis.hdel(self.REDIS_KEY_USERS, username)
        
        # 撤销该用户的所有令牌
        all_tokens = await self.redis.hgetall(self.REDIS_KEY_TOKENS)
        for token, token_info_json in all_tokens.items():
            token_info = json.loads(token_info_json)
            if token_info['username'] == username:
                await self.redis.hdel(self.REDIS_KEY_TOKENS, token)
                await self.redis.delete(f"{self.REDIS_KEY_TOKENS}:expiry:{token}")
        
        return True 