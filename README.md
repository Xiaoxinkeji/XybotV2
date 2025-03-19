# XYBotV2 (二次开发版)

> **注意**：本项目是基于 [HenryXiaoYang/XYBotV2](https://github.com/HenryXiaoYang/XYBotV2) 的二次开发版本，感谢原作者的工作。

![version](https://img.shields.io/badge/version-2.0.0-blue)
![license](https://img.shields.io/badge/license-MIT-green)

XYBotV2是一个功能强大的微信自动化工具，提供Web管理界面、插件系统和完整的API接口，帮助用户实现微信消息的自动化处理。

## 📚 主要特性

- **微信消息自动化**：接收和发送各类微信消息
- **Web管理平台**：通过浏览器实时管理和监控机器人
- **插件系统**：支持自定义功能扩展
- **数据持久化**：使用SQLite和Redis进行数据存储
- **认证系统**：基于令牌的安全认证机制
- **Docker支持**：提供容器化部署方案

## 🏗️ 系统架构

系统由以下几个核心组件构成：

1. **微信API集成层**：处理与微信客户端的通信
2. **核心处理引擎**：处理消息分发与事件调度
3. **插件管理系统**：加载、管理和执行各种功能插件
4. **Web管理界面**：提供直观的图形化管理控制台
5. **数据存储层**：处理数据持久化需求

## 🚀 快速开始

### 使用Docker部署（推荐）

1. 确保已安装 [Docker](https://www.docker.com/) 和 [Docker Compose](https://docs.docker.com/compose/)

2. 克隆项目
   ```bash
   git clone https://github.com/Xiaoxinkeji/XybotV2.git
   cd XybotV2
   ```

3. 启动容器
   ```bash
   docker-compose up -d
   ```

4. 访问Web管理界面
   ```
   http://localhost:8080
   ```

### 手动安装

1. 确保已安装 Python 3.11 及以上版本

2. 克隆项目
   ```bash
   git clone https://github.com/Xiaoxinkeji/XybotV2.git
   cd XybotV2
   ```

3. 安装依赖
   ```bash
   pip install -r requirements.txt
   ```

4. 构建Web界面
   ```bash
   chmod +x build_web_ui.sh
   ./build_web_ui.sh
   ```

5. 启动服务
   ```bash
   python main.py
   ```

## ⚙️ 配置说明

XYBotV2 使用 TOML 格式的配置文件，主配置文件为 `main_config.toml`，包含以下主要配置项：

```toml
[WechatAPIServer]
port = 9000                # WechatAPI服务器端口
redis-host = "127.0.0.1"   # Redis服务器地址

[XYBot]
version = "v1.0.0"         # 版本号
admins = ["admin-wxid"]    # 管理员微信ID列表

[web]
enabled = true             # 是否启用Web管理界面
port = 8080                # Web服务器端口
```

更多配置选项请参考 `config/default_config.toml` 文件。

## 🔌 插件开发

XYBotV2 提供了强大的插件系统，您可以轻松开发自己的插件。插件结构如下：

```
plugins/YourPlugin/
├── __init__.py   # 插件入口点
├── main.py       # 主要逻辑
└── config.toml   # 插件配置
```

插件开发示例：

```python
from utils.plugin_base import PluginBase
from utils.decorators import on_text_message

class YourPlugin(PluginBase):
    description = "你的插件描述"
    author = "你的名字"
    version = "1.0.0"
    
    def __init__(self):
        super().__init__()
        # 初始化代码
    
    @on_text_message
    async def handle_message(self, bot, message):
        # 处理文本消息
        if message.content == "你好":
            await bot.send_text_message(message.from_user, "你好！")
        return True
```

更多插件开发详情请参考 [插件开发文档](docs/plugin_development.md)。

## 📊 Web管理平台

XYBotV2 提供了现代化的Web管理界面，功能包括：

- 实时监控机器人运行状态
- 插件管理（启用/禁用/配置）
- 消息日志查看与搜索
- 系统设置调整
- 用户认证与权限管理

访问 `http://localhost:8080` 打开管理界面（默认用户名: admin，密码: admin）。

## ❓ 常见问题

**Q: 无法连接到GitHub进行推送怎么办？**
A: 如遇到 "Recv failure: Connection was reset" 错误，请参考以下解决方案：
- 配置代理: `git config --global http.proxy http://127.0.0.1:端口号`
- 增加缓冲区: `git config --global http.postBuffer 524288000`
- 使用SSH方式连接: `git remote set-url origin git@github.com:用户名/仓库名.git`

**Q: 插件加载失败怎么办？**
A: 检查插件代码是否有语法错误，依赖项是否已安装，配置文件格式是否正确。详细错误信息可在日志文件中查看。

**Q: Web界面无法访问怎么办？**
A: 检查端口是否被占用，防火墙是否已放行端口，确认配置文件中Web服务是否已启用。

## 🤝 贡献指南

欢迎贡献代码、修复Bug或提出新功能建议！请遵循以下步骤：

1. Fork 本仓库
2. 创建新分支 (`git checkout -b feature/your-feature`)
3. 提交更改 (`git commit -am 'Add some feature'`)
4. 推送到分支 (`git push origin feature/your-feature`)
5. 创建 Pull Request

## 📜 许可证

本项目采用 MIT 许可证 - 详情见 [LICENSE](LICENSE) 文件。