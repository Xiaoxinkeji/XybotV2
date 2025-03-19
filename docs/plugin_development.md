# XYBotV2 插件开发文档

本文档提供了XYBotV2插件系统的详细说明，帮助开发者理解如何创建自己的插件。

## 目录

1. [插件结构](#插件结构)
2. [插件生命周期](#插件生命周期)
3. [事件装饰器](#事件装饰器)
4. [插件配置管理](#插件配置管理)
5. [API接口](#API接口)
6. [开发最佳实践](#开发最佳实践)
7. [示例插件](#示例插件)

## 插件结构

XYBotV2的插件是一个Python包，必须包含以下文件：

```
plugins/YourPlugin/
├── __init__.py   # 插件入口点，可以为空
├── main.py       # 主要逻辑，包含插件类
└── config.toml   # 插件配置文件
```

插件类必须继承自`PluginBase`并提供必要的属性：

```python
from utils.plugin_base import PluginBase

class YourPlugin(PluginBase):
    # 插件描述信息
    description = "这是一个示例插件"
    author = "开发者名称"
    version = "1.0.0"
    
    def __init__(self):
        super().__init__()
        # 初始化代码
```

## 插件生命周期

插件具有以下生命周期方法，您可以重写它们：

```python
async def on_load(self, bot):
    """插件加载时调用"""
    pass
    
async def on_enable(self, bot):
    """插件启用时调用"""
    pass
    
async def on_disable(self):
    """插件禁用时调用"""
    pass
    
async def on_unload(self):
    """插件卸载时调用"""
    pass
```

## 事件装饰器

XYBotV2提供了多种装饰器来处理不同类型的事件：

```python
from utils.decorators import on_text_message, on_image_message, schedule

class YourPlugin(PluginBase):
    @on_text_message
    async def handle_text(self, bot, message):
        """处理文本消息"""
        if message.content == "你好":
            await bot.send_text_message(message.from_user, "你好，我是机器人！")
        return True
    
    @on_image_message
    async def handle_image(self, bot, message):
        """处理图片消息"""
        # 处理逻辑
        return True
    
    @schedule(minutes=5)
    async def scheduled_task(self, bot):
        """定时任务，每5分钟执行一次"""
        # 定时执行的代码
        pass
```

常用的装饰器包括：

- `@on_text_message` - 处理文本消息
- `@on_image_message` - 处理图片消息
- `@on_video_message` - 处理视频消息
- `@on_file_message` - 处理文件消息
- `@on_voice_message` - 处理语音消息
- `@on_friend_request` - 处理好友请求
- `@on_group_invite` - 处理群邀请
- `@schedule` - 创建定时任务

## 插件配置管理

插件可以通过`config.toml`文件进行配置：

```toml
# 示例配置文件
[general]
enabled = true      # 是否启用插件

[settings]
custom_setting = "值"
timeout = 30
max_retries = 3
```

在插件代码中，您可以访问配置：

```python
def __init__(self):
    super().__init__()
    # 加载配置
    self.config = self.load_config()
    self.timeout = self.config.get("settings", {}).get("timeout", 30)
```

## API接口

XYBotV2提供了丰富的API接口，通过`bot`对象访问：

```python
# 发送文本消息
await bot.send_text_message(user_id, "消息内容")

# 发送图片消息
await bot.send_image_message(user_id, image_path)

# 获取用户信息
user_info = await bot.get_user_info(user_id)

# 获取群成员列表
members = await bot.get_group_members(group_id)
```

## 开发最佳实践

1. **异常处理**：始终使用try-except捕获异常，防止插件崩溃影响整个系统
2. **资源管理**：在`on_disable`和`on_unload`中释放资源
3. **并发控制**：使用`asyncio`提供的工具管理并发
4. **日志记录**：使用`self.log()`方法记录插件活动
5. **配置校验**：加载配置时验证参数有效性

```python
# 良好的异常处理示例
@on_text_message
async def handle_message(self, bot, message):
    try:
        # 处理消息
        response = await self.process_message(message.content)
        await bot.send_text_message(message.from_user, response)
        return True
    except Exception as e:
        self.log(f"处理消息时出错: {str(e)}", "ERROR")
        return False
```

## 示例插件

这是一个完整的示例插件，演示了主要功能：

```python
from utils.plugin_base import PluginBase
from utils.decorators import on_text_message, schedule

class EchoPlugin(PluginBase):
    description = "简单的回声插件示例"
    author = "XYBot开发团队"
    version = "1.0.0"
    
    def __init__(self):
        super().__init__()
        self.config = self.load_config()
        self.prefix = self.config.get("settings", {}).get("prefix", "echo:")
        self.stats = {"messages_processed": 0}
    
    async def on_enable(self, bot):
        self.log("回声插件已启用", "INFO")
        await bot.send_text_message(self.config.get("admin_id"), "回声插件已启用")
    
    @on_text_message
    async def handle_echo(self, bot, message):
        if message.content.startswith(self.prefix):
            echo_text = message.content[len(self.prefix):].strip()
            await bot.send_text_message(message.from_user, echo_text)
            self.stats["messages_processed"] += 1
            return True
        return False
    
    @schedule(minutes=60)
    async def report_stats(self, bot):
        """每小时报告统计信息"""
        admin_id = self.config.get("admin_id")
        if admin_id:
            await bot.send_text_message(
                admin_id, 
                f"回声插件统计: 已处理 {self.stats['messages_processed']} 条消息"
            )
    
    async def on_disable(self):
        self.log(f"回声插件已禁用，共处理 {self.stats['messages_processed']} 条消息", "INFO")
```

配置示例 (`config.toml`):

```toml
[general]
enabled = true

[settings]
prefix = "echo:"
admin_id = "admin-wxid"
```

---

有关更多详细信息，请参阅XYBotV2核心API文档或查看示例插件代码。如果您有任何问题，欢迎在GitHub仓库中提出issue。 