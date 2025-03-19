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

# 复制 Redis 配置（如果存在）
COPY redis.conf* /tmp/
RUN if [ -f "/tmp/redis.conf" ]; then \
    mv /tmp/redis.conf /etc/redis/redis.conf; \
    else \
    echo "Redis配置文件不存在，使用默认配置"; \
    fi

# 复制项目文件
COPY . /app/

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir tomli==2.0.1

# 构建Web UI
RUN chmod +x build_web_ui.sh && ./build_web_ui.sh

# 暴露端口 - Web界面和WechatAPI服务器
EXPOSE 8080 9000

# 复制启动脚本（如果存在）
COPY entrypoint.sh* /tmp/
RUN if [ -f "/tmp/entrypoint.sh" ]; then \
    mv /tmp/entrypoint.sh ./entrypoint.sh && \
    chmod +x entrypoint.sh; \
    else \
    echo "entrypoint.sh不存在，将使用直接命令启动"; \
    fi

# 启动命令
CMD if [ -f "entrypoint.sh" ]; then ./entrypoint.sh; else python main.py; fi

