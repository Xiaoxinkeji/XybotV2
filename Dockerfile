FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 安装依赖
RUN apt-get update && apt-get install -y \
    build-essential \
    nodejs \
    npm \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 复制项目文件
COPY . /app/

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 构建Web UI
RUN chmod +x build_web_ui.sh && ./build_web_ui.sh

# 设置环境变量
ENV PYTHONUNBUFFERED=1

# 暴露端口 - Web界面和WechatAPI服务器
EXPOSE 8080 9000

# 启动命令
CMD ["python", "main.py"]

