#!/bin/bash

# 前端项目目录
FRONTEND_DIR="web_ui"

# 检查目录是否存在
if [ ! -d "$FRONTEND_DIR" ]; then
  echo "前端项目目录不存在，创建..."
  mkdir -p "$FRONTEND_DIR"
fi

# 进入前端目录
cd "$FRONTEND_DIR"

# 检查是否已安装依赖
if [ ! -d "node_modules" ]; then
  echo "安装前端依赖..."
  npm install
fi

# 构建项目
echo "构建前端项目..."
npm run build

echo "前端构建完成！" 