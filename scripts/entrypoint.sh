#!/bin/sh

# 可选：打印一些信息 / 环境变量
echo "ENTRYPOINT: starting with arguments: $@"

# 如果 venv 目录不存在，就创建
if [ ! -d "./venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv venv
fi

# 激活虚拟环境
# shellcheck disable=SC1091
source venv/bin/activate

# 升级 pip / setuptools / wheel（可选）
pip install --upgrade pip setuptools wheel

# 安装依赖
if [ -f "requirements.txt" ]; then
  echo "Installing dependencies..."
  pip install -r requirements.txt
fi

# 最后执行传入的命令；如果没有传入命令，用默认启动 app.py
if [ $# -eq 0 ]; then
  echo "No command provided, starting default: python app.py"
  exec python app.py
else
  exec "$@"
fi
