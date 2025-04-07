from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
import sys
import ctypes
import keyboard

from src.utils import is_admin
from src.main_window import MainWindow

if __name__ == '__main__':
    # 检查是否已以管理员身份运行，如果不是，尝试重新启动
    if not is_admin() and sys.platform == 'win32':
        # 显示提示消息
        ctypes.windll.user32.MessageBoxW(0, 
            "全局快捷键功能需要管理员权限。\n程序将尝试以管理员身份重新启动。", 
            "需要管理员权限", 0)
        
        # 获取当前脚本路径
        script = sys.executable
        params = sys.argv
        params.insert(0, script)
        
        # 以管理员权限重新启动程序
        try:
            if sys.executable.endswith("pythonw.exe"):
                # pythonw 隐藏控制台
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join('"'+p+'"' for p in params[1:]), None, 1)
            else:
                # python 显示控制台
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join('"'+p+'"' for p in params[1:]), None, 1)
            sys.exit(0)
        except:
            pass

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
