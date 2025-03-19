FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV TZ=Asia/Shanghai
ENV IMAGEIO_FFMPEG_EXE=/usr/bin/ffmpeg
ENV PYTHONUNBUFFERED=1

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    build-essential \
    nodejs \
    npm \
    git \
    ffmpeg \
    redis-server \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 复制 Redis 配置
COPY redis.conf /etc/redis/redis.conf || echo "Redis配置文件不存在，使用默认配置"

# 复制项目文件
COPY . /app/

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 构建Web UI
RUN chmod +x build_web_ui.sh && ./build_web_ui.sh

# 暴露端口 - Web界面和WechatAPI服务器
EXPOSE 8080 9000

# 启动脚本
COPY entrypoint.sh . || echo "entrypoint.sh不存在，将使用直接命令启动"
RUN if [ -f "entrypoint.sh" ]; then chmod +x entrypoint.sh; fi

# 启动命令 - 如果entrypoint.sh存在则使用，否则直接启动python
CMD if [ -f "entrypoint.sh" ]; then ./entrypoint.sh; else python main.py; fi

