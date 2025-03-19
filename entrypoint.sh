#!/bin/bash

# 启动Redis服务器
service redis-server start

# 等待Redis启动
sleep 2

# 检查Redis是否正常运行
redis-cli ping

# 启动应用
python main.py