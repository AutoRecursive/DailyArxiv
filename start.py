import subprocess
import sys
import os
import signal
import platform
import time


def is_windows():
  return platform.system().lower() == "windows"


def check_dependencies():
  """检查必要的依赖是否安装"""
  try:
    subprocess.run(["python3" if not is_windows() else "python",
                   "--version"], capture_output=True)
    subprocess.run(["npm", "--version"], capture_output=True)
  except FileNotFoundError as e:
    print(f"错误: 缺少必要的依赖: {e}")
    sys.exit(1)


def start_backend():
  """启动后端服务"""
  print("启动后端服务...")

  # 获取项目根目录的绝对路径
  root_dir = os.path.dirname(os.path.abspath(__file__))
  backend_dir = os.path.join(root_dir, "backend")
  venv_dir = os.path.join(backend_dir, "venv")

  # 创建并激活虚拟环境
  if not os.path.exists(venv_dir):
    print("创建虚拟环境...")
    python_cmd = "python3" if not is_windows() else "python"
    subprocess.run([python_cmd, "-m", "venv", venv_dir], check=True)

  # 获取虚拟环境的Python和pip路径
  if is_windows():
    venv_python = os.path.join(venv_dir, "Scripts", "python.exe")
    venv_pip = os.path.join(venv_dir, "Scripts", "pip.exe")
  else:
    venv_python = os.path.join(venv_dir, "bin", "python")
    venv_pip = os.path.join(venv_dir, "bin", "pip")

  # 确保虚拟环境中的 Python 存在
  if not os.path.exists(venv_python):
    print(f"错误: 虚拟环境 Python 不存在: {venv_python}")
    sys.exit(1)

  # 安装依赖
  print("安装后端依赖...")
  requirements_file = os.path.join(backend_dir, "requirements.txt")
  subprocess.run([venv_pip, "install", "-r", requirements_file], check=True)

  # 设置环境变量
  env = os.environ.copy()
  env["PYTHONPATH"] = root_dir

  print("启动后端服务...")
  # 启动后端，并捕获输出
  backend_process = subprocess.Popen(
      [venv_python, "-m", "backend.main"],
      env=env,
      cwd=root_dir,
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE,
      universal_newlines=True
  )

  # 启动一个线程来读取和打印后端输出
  def print_output(process):
    while True:
      output = process.stdout.readline()
      if output:
        print("[Backend]", output.strip())
      error = process.stderr.readline()
      if error:
        print("[Backend Error]", error.strip(), file=sys.stderr)
      if output == '' and error == '' and process.poll() is not None:
        break

  import threading
  threading.Thread(target=print_output, args=(
    backend_process,), daemon=True).start()

  return backend_process


def start_frontend():
  """启动前端服务"""
  print("启动前端服务...")
  root_dir = os.path.dirname(os.path.abspath(__file__))
  frontend_dir = os.path.join(root_dir, "daily-arxiv")

  os.chdir(frontend_dir)

  # 安装依赖
  print("安装前端依赖...")
  subprocess.run(["npm", "install"], check=True)

  print("启动前端服务...")
  # 启动开发服务器
  frontend_process = subprocess.Popen(
      ["npm", "run", "dev"],
      cwd=frontend_dir
  )

  return frontend_process


def main():
  """主函数"""
  try:
    check_dependencies()

    # 启动服务
    backend_process = start_backend()
    time.sleep(2)  # 等待后端启动
    frontend_process = start_frontend()

    print("\n所有服务已启动!")
    print("前端地址: http://localhost:5173")
    print("后端地址: http://localhost:8000")
    print("按 Ctrl+C 停止服务\n")

    try:
      while True:
        time.sleep(1)
    except KeyboardInterrupt:
      print("\n正在停止服务...")
      backend_process.terminate()
      frontend_process.terminate()
      sys.exit(0)

  except Exception as e:
    print(f"\n错误: {e}")
    sys.exit(1)


if __name__ == "__main__":
  main()
