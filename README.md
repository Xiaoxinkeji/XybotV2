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

```
XYBotV2/
├── 核心模块
│   ├── WechatAPI服务 - 微信通信接口，基于WechatPad
│   ├── 插件管理系统 - 动态加载和管理插件
│   ├── Web管理平台 - 提供图形化操作界面
│   └── 数据持久化 - 消息和配置存储
├── 插件模块
│   ├── SystemStatusWeb - Web端系统状态监控
│   ├── BotStatusPush - 机器人状态推送
│   └── 自定义插件... - 用户可扩展功能
└── 前端UI
    └── Vue.js应用 - 响应式管理界面
```

## 🔄 自动化部署

本项目配置了GitHub Actions自动构建Docker镜像并推送到Docker Hub。每次提交到主分支时，都会自动触发构建流程。

### GitHub Actions 配置

项目使用GitHub Actions实现自动化CI/CD流程：

```yaml
# .github/workflows/docker-build-on-commit.yml
name: Build and Push Docker image

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2
      
      - name: Login to DockerHub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
      
      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: xiaoxinkeji/xybot:latest,xiaoxinkeji/xybot:${{ github.sha }}
```

### Docker Compose 详细配置

以下是完整的docker-compose.yml配置文件：

```yaml
version: '3'

services:
  xybot:
    build: .
    container_name: xybot
    restart: unless-stopped
    ports:
      - "8080:8080"  # Web界面
      - "9000:9000"  # WechatAPI
    depends_on:
      - redis
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
      - ./plugins:/app/plugins
      - ./config:/app/config
    environment:
      - TZ=Asia/Shanghai

  redis:
    image: redis:6-alpine
    container_name: xybot-redis
    restart: unless-stopped
    volumes:
      - redis-data:/data
    command: redis-server --appendonly yes

volumes:
  redis-data:
```

## 🚀 快速开始

### 使用Docker部署（推荐）

1. **克隆项目**
   ```bash
   git clone https://github.com/Xiaoxinkeji/XybotV2.git
   cd XybotV2
   ```

2. **使用docker-compose启动**
   ```bash
   docker-compose up -d
   ```

3. **访问Web管理界面**
   
   浏览器访问 `http://localhost:8080`，默认管理员账号为 `admin`，密码为 `admin`。

### 手动安装

1. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

2. **构建Web界面**
   ```bash
   chmod +x build_web_ui.sh
   ./build_web_ui.sh
   ```

3. **启动机器人**
   ```bash
   python main.py
   ```

## ⚙️ 配置说明

主配置文件位于 `config/main_config.toml`，包含以下主要配置项：

### 配置示例

以下是default_config.toml的关键配置项：

```toml
# 核心配置
[core]
version = "2.0.0"
name = "XyBot"
timezone = "Asia/Shanghai"
auto_restart = false

# 微信服务配置
[wechat]
port = 9000
mode = "release"
ignore_protection = false

[wechat.redis]
host = "127.0.0.1"
port = 6379
password = ""
db = 0

# Web管理界面配置
[web]
enabled = true
port = 8080
host = "0.0.0.0"
debug = false
static_path = "web_ui/dist"

# 认证配置
[web.auth]
token_expire_hours = 24
allow_api_key = true
api_key_expire_days = 90
max_login_attempts = 5

# 安全配置
[web.security]
enable_cors = true
cors_allow_origins = ["*"]
require_https = false

# 插件系统配置
[plugins]
enabled = true
directory = "plugins"
disabled = []
```

## 🔌 插件系统

XYBotV2提供强大的插件系统，让您能够轻松扩展机器人功能：

### 内置插件

1. **SystemStatusWeb** - Web端系统状态监控插件
   - 提供系统资源、机器人状态监控
   - 实时查看CPU、内存、磁盘使用情况

2. **BotStatusPush** - 机器人状态推送插件
   - 监控机器人在线状态
   - 支持通过PushPlus发送通知

### 开发自定义插件

创建自定义插件的基本结构：

```
plugins/YourPlugin/
├── __init__.py   # 插件入口
├── main.py       # 主要逻辑
└── config.toml   # 插件配置
```

插件示例：
```python
from xybot.plugin import PluginBase
from xybot.decorators import on_text_message

class YourPlugin(PluginBase):
    description = "你的插件描述"
    author = "你的名字"
    version = "1.0.0"
    
    def __init__(self):
        super().__init__()
        # 初始化代码
        
    @on_text_message
    async def on_message(self, bot, message):
        # 处理消息
        return True
```

## 📊 监控与通知

结合内置的SystemStatusWeb和BotStatusPush插件，XYBotV2提供全面的状态监控和通知功能：

### 系统状态监控

通过Web界面实时监控：
- CPU、内存、磁盘使用率
- 机器人运行状态和上线时间
- 插件加载情况
- 消息处理统计

### 自动故障通知

配置BotStatusPush插件可实现：
- 机器人离线自动通知
- 系统资源异常报警
- 定时运行状态推送
- 多种通知方式支持

### 设置方法

修改插件配置文件启用监控功能：

```toml
# BotStatusPush/config.toml 示例
token = "你的推送token"
check_interval = 0.5
notify_interval = 360
force_push_on_enable = true
```

## 🔒 安全说明

XYBotV2已实现完整的安全机制，包括：

- 基于令牌的认证系统
- Redis存储的会话管理
- 密码哈希与加盐
- 可配置的CORS策略
- API访问权限控制
- 失败登录尝试限制

**强烈建议**在生产环境中配置HTTPS和修改默认密码。

## 🌐 API接口

XYBotV2提供完整的REST API，您可以通过这些接口集成其他系统：

### 认证

```
POST /api/auth/login
{
  "username": "admin",
  "password": "your_password"
}
```

### 机器人控制

```
GET /api/status - 获取机器人状态
POST /api/system/restart - 重启机器人
```

### 插件管理

```
GET /api/plugins - 获取插件列表
POST /api/plugins/{id}/toggle - 启用/禁用插件
```

完整API文档可在Web管理界面的"帮助文档"中查看。

## 📋 常见问题

### 连接重置问题解决方案

如果遇到 `Recv failure: Connection was reset` 错误，可尝试以下解决方法：

1. **配置Git代理**：
   ```bash
   git config --global http.proxy http://127.0.0.1:端口号
   git config --global https.proxy http://127.0.0.1:端口号
   ```

2. **使用SSH替代HTTPS**：
   ```bash
   git remote set-url origin git@github.com:Xiaoxinkeji/XybotV2.git
   ```

3. **增加Git缓冲区**：
   ```bash
   git config --global http.postBuffer 524288000
   ```

### 其他常见问题

- **插件无法加载**：检查插件文件结构和依赖项
- **Web界面无法访问**：确认端口设置和防火墙配置
- **微信连接问题**：检查WechatAPI服务配置和网络连接

## 📞 获取帮助

如有任何问题，可通过以下方式获取帮助：

- 提交GitHub Issues
- 查看Wiki文档
- 加入用户交流群

## 📜 许可证

本项目基于MIT许可证开源，详情请参阅LICENSE文件。

## 🔗 相关链接

- [原始项目](https://github.com/HenryXiaoYang/XYBotV2)
- [项目文档](https://github.com/Xiaoxinkeji/XybotV2/wiki)
- [问题反馈](https://github.com/Xiaoxinkeji/XybotV2/issues)

## 🤝 贡献指南

我们欢迎任何形式的贡献，包括但不限于：

1. 提交问题和建议
2. 提交代码改进
3. 改进文档
4. 开发新插件

提交代码前，请确保遵循项目的代码风格指南。

---

感谢使用XYBotV2！希望它能为您的日常工作和生活带来便利。 