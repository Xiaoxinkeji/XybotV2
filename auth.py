"""
认证与安全模块
管理API访问、令牌生成和验证
使用Redis存储认证数据
"""

import os
import time
import hashlib
import secrets
import json
import base64
from datetime import datetime, timedelta

class AuthManager:
    """认证管理器，负责用户认证和访问控制，使用Redis存储数据"""
    
    # Redis键前缀
    REDIS_KEY_USERS = "xybot:web:users"
    REDIS_KEY_TOKENS = "xybot:web:tokens"
    REDIS_KEY_SECRET = "xybot:web:secret_key"
    
    def __init__(self, redis_client, token_expire_hours=24):
        """
        初始化认证管理器
        
        Args:
            redis_client: Redis客户端实例
            token_expire_hours: 令牌过期时间（小时）
        """
        self.redis = redis_client
        self.token_expire_hours = token_expire_hours
        
        # 初始化或加载配置
        self._load_or_create_config()
    
    async def _load_or_create_config(self):
        """加载现有配置或创建默认配置"""
        # 检查Redis中是否已有用户数据
        has_users = await self.redis.exists(self.REDIS_KEY_USERS)
        has_secret = await self.redis.exists(self.REDIS_KEY_SECRET)
        
        if not has_users or not has_secret:
            await self._create_default_config()
    
    async def _create_default_config(self):
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
        
        print("已创建默认认证配置，默认管理员账户: admin / admin123")
    
    async def _get_secret_key(self):
        """获取密钥"""
        secret_key = await self.redis.get(self.REDIS_KEY_SECRET)
        if not secret_key:
            secret_key = secrets.token_hex(32)
            await self.redis.set(self.REDIS_KEY_SECRET, secret_key)
        return secret_key
    
    def _hash_password(self, password):
        """
        密码哈希
        
        Args:
            password: 原始密码
            
        Returns:
            哈希后的密码
        """
        # 生成随机盐值
        salt = secrets.token_bytes(16)
        
        # 使用PBKDF2算法，带盐值哈希
        key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000  # 迭代次数
        )
        
        # 将盐值和哈希结果编码为Base64字符串
        return base64.b64encode(salt + key).decode('utf-8')
    
    def _verify_password(self, stored_hash, password):
        """
        验证密码
        
        Args:
            stored_hash: 存储的哈希值
            password: 待验证的密码
            
        Returns:
            密码是否匹配
        """
        try:
            # 解码存储的哈希值
            decoded = base64.b64decode(stored_hash)
            
            # 提取盐值和哈希结果
            salt = decoded[:16]
            stored_key = decoded[16:]
            
            # 使用相同的盐值和算法计算哈希
            key = hashlib.pbkdf2_hmac(
                'sha256',
                password.encode('utf-8'),
                salt,
                100000  # 迭代次数
            )
            
            # 比较哈希结果
            return key == stored_key
        except Exception:
            return False
    
    async def authenticate(self, username, password):
        """
        验证用户凭据
        
        Args:
            username: 用户名
            password: 密码
            
        Returns:
            认证成功时返回用户信息和令牌，否则返回None
        """
        user_json = await self.redis.hget(self.REDIS_KEY_USERS, username)
        if not user_json:
            return None
        
        user = json.loads(user_json)
        
        # 验证密码
        if not self._verify_password(user['password_hash'], password):
            return None
        
        # 生成访问令牌
        token = await self._generate_token(username)
        
        return {
            'username': user['username'],
            'role': user['role'],
            'token': token
        }
    
    async def _generate_token(self, username):
        """
        为用户生成访问令牌
        
        Args:
            username: 用户名
            
        Returns:
            访问令牌
        """
        # 生成随机令牌
        token = secrets.token_hex(32)
        
        # 记录令牌信息，使用配置的过期时间
        expires_at = datetime.now() + timedelta(hours=self.token_expire_hours)
        token_info = {
            'username': username,
            'created_at': datetime.now().isoformat(),
            'expires_at': expires_at.isoformat()
        }
        
        # 存储到Redis，设置过期时间
        await self.redis.hset(self.REDIS_KEY_TOKENS, token, json.dumps(token_info))
        
        # 设置令牌过期时间
        ttl_seconds = int(self.token_expire_hours * 3600)
        expiry_key = f"{self.REDIS_KEY_TOKENS}:expiry:{token}"
        await self.redis.set(expiry_key, '1', expire=ttl_seconds)
        
        return token
    
    async def validate_token(self, token):
        """
        验证访问令牌是否有效
        
        Args:
            token: 访问令牌
            
        Returns:
            令牌有效时返回用户信息，否则返回None
        """
        token_info_json = await self.redis.hget(self.REDIS_KEY_TOKENS, token)
        if not token_info_json:
            return None
        
        token_info = json.loads(token_info_json)
        
        # 检查令牌是否过期
        expires_at = datetime.fromisoformat(token_info['expires_at'])
        if datetime.now() > expires_at:
            # 删除过期令牌
            await self.redis.hdel(self.REDIS_KEY_TOKENS, token)
            await self.redis.delete(f"{self.REDIS_KEY_TOKENS}:expiry:{token}")
            return None
        
        # 返回用户信息
        username = token_info['username']
        user_json = await self.redis.hget(self.REDIS_KEY_USERS, username)
        
        if not user_json:
            return None
            
        return json.loads(user_json)
    
    async def revoke_token(self, token):
        """
        撤销访问令牌
        
        Args:
            token: 要撤销的令牌
            
        Returns:
            是否成功撤销
        """
        # 检查令牌是否存在
        exists = await self.redis.hexists(self.REDIS_KEY_TOKENS, token)
        if not exists:
            return False
        
        # 删除令牌
        await self.redis.hdel(self.REDIS_KEY_TOKENS, token)
        await self.redis.delete(f"{self.REDIS_KEY_TOKENS}:expiry:{token}")
        return True
    
    async def create_user(self, username, password, role='user'):
        """
        创建新用户
        
        Args:
            username: 用户名
            password: 密码
            role: 用户角色
            
        Returns:
            创建是否成功
        """
        # 检查用户是否已存在
        exists = await self.redis.hexists(self.REDIS_KEY_USERS, username)
        if exists:
            return False
        
        # 创建新用户
        password_hash = self._hash_password(password)
        user = {
            'username': username,
            'password_hash': password_hash,
            'role': role,
            'created_at': datetime.now().isoformat()
        }
        
        # 存储到Redis
        await self.redis.hset(self.REDIS_KEY_USERS, username, json.dumps(user))
        return True
    
    async def change_password(self, username, old_password, new_password):
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
    
    async def delete_user(self, username):
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