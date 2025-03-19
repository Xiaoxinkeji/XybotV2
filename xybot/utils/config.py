"""
配置管理模块
负责加载、验证和提供配置信息
"""

import os
import toml
from pathlib import Path
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_path: str = None):
        """
        初始化配置管理器
        
        Args:
            config_path: 配置文件路径，默认为项目根目录下的config/main_config.toml
        """
        # 确定配置文件路径
        if not config_path:
            # 从当前模块找到项目根目录
            root_dir = Path(__file__).resolve().parent.parent.parent
            config_path = root_dir / "config" / "main_config.toml"
        
        self.config_path = Path(config_path)
        self.default_config_path = self.config_path.parent / "default_config.toml"
        self.config = {}
        self.load_config()
    
    def load_config(self) -> None:
        """加载配置文件"""
        # 首先加载默认配置
        default_config = {}
        if self.default_config_path.exists():
            try:
                with open(self.default_config_path, 'r', encoding='utf-8') as f:
                    default_config = toml.load(f)
                logger.info(f"已加载默认配置文件: {self.default_config_path}")
            except Exception as e:
                logger.error(f"加载默认配置文件出错: {str(e)}")
        
        # 加载用户配置，覆盖默认值
        user_config = {}
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    user_config = toml.load(f)
                logger.info(f"已加载用户配置文件: {self.config_path}")
            else:
                logger.warning(f"用户配置文件不存在: {self.config_path}")
        except Exception as e:
            logger.error(f"加载用户配置文件出错: {str(e)}")
        
        # 合并配置
        self._merge_configs(default_config, user_config)
    
    def _merge_configs(self, default_config: Dict[str, Any], user_config: Dict[str, Any]) -> None:
        """
        深度合并两个配置字典
        
        Args:
            default_config: 默认配置
            user_config: 用户配置
        """
        # 递归合并配置
        self.config = self._deep_merge(default_config, user_config)
    
    def _deep_merge(self, d1: Dict[str, Any], d2: Dict[str, Any]) -> Dict[str, Any]:
        """
        深度合并两个字典
        
        Args:
            d1: 基础字典
            d2: 覆盖字典
            
        Returns:
            合并后的字典
        """
        result = d1.copy()
        
        for k, v in d2.items():
            if k in result and isinstance(result[k], dict) and isinstance(v, dict):
                result[k] = self._deep_merge(result[k], v)
            else:
                result[k] = v
        
        return result
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置值
        
        Args:
            key: 点分隔的配置路径，如 "web.port"
            default: 如果配置不存在时的默认值
            
        Returns:
            配置值或默认值
        """
        parts = key.split('.')
        current = self.config
        
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return default
        
        return current
    
    def save(self) -> bool:
        """
        保存当前配置到文件
        
        Returns:
            是否成功保存
        """
        try:
            # 确保配置目录存在
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            
            # 保存配置
            with open(self.config_path, 'w', encoding='utf-8') as f:
                toml.dump(self.config, f)
            
            logger.info(f"配置已保存到: {self.config_path}")
            return True
        except Exception as e:
            logger.error(f"保存配置文件出错: {str(e)}")
            return False 