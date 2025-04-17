import subprocess
import os
from pystray import Icon, Menu, MenuItem
from PIL import Image

def create_image():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(base_dir, "icon.ico")
    try:
        return Image.open(icon_path)
    except Exception as e:
        print(f"加载图标失败: {e}")
        raise

def start_robot():
    try:
        main_path = os.path.join(os.path.dirname(__file__), "main.py")
        subprocess.Popen(["python", main_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"启动主程序失败: {e}")

def on_exit(icon, item):
    print("程序已退出")
    icon.stop()

def main():
    start_robot()
    menu = Menu(MenuItem("退出程序", on_exit))
    icon = Icon("问答系统", create_image(), menu=menu)
    icon.run()

if __name__ == "__main__":
    main()