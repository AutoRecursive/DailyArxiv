#!/bin/bash

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 检查是否安装了必要的依赖
check_dependencies() {
    command -v python3 >/dev/null 2>&1 || { echo "需要 python3 但未安装"; exit 1; }
    command -v npm >/dev/null 2>&1 || { echo "需要 npm 但未安装"; exit 1; }
}

# 启动后端服务
start_backend() {
    echo "启动后端服务..."
    cd "$SCRIPT_DIR/backend"
    
    # 检查并创建虚拟环境
    if [ ! -d "venv" ]; then
        python3 -m venv venv
    fi
    
    # 激活虚拟环境
    source venv/bin/activate
    
    # 安装依赖
    pip install -r requirements.txt
    
    # 设置 PYTHONPATH 并启动后端
    cd "$SCRIPT_DIR"
    PYTHONPATH="$SCRIPT_DIR" python -m backend.main &
}

# 启动前端服务
start_frontend() {
    echo "启动前端服务..."
    cd "$SCRIPT_DIR/frontend"
    
    # 安装依赖
    npm install
    
    # 启动开发服务器
    npm run dev &
    cd "$SCRIPT_DIR"
}

# 主函数
main() {
    check_dependencies
    start_backend
    sleep 2  # 等待后端启动
    start_frontend
    
    echo "服务已启动!"
    echo "前端地址: http://localhost:5173"
    echo "后端地址: http://localhost:8000"
    echo "按 Ctrl+C 停止服务"
    
    # 等待用户中断
    wait
}

# 清理函数
cleanup() {
    echo "正在停止服务..."
    pkill -f "python -m backend.main"
    pkill -f "vite"
    exit 0
}

# 注册清理函数
trap cleanup SIGINT SIGTERM

# 运行主函数
main 