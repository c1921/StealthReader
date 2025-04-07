from PySide6.QtGui import QColor

class StyleManager:
    @staticmethod
    def get_main_window_style(bg_color, bg_alpha, text_color, text_alpha):
        """获取主窗口样式"""
        return f"""
            QWidget {{
                background: rgba({bg_color.red()}, {bg_color.green()}, {bg_color.blue()}, {bg_alpha});
                border: none;
                border-radius: 5px;
            }}
            QTextEdit {{
                border: none;
                background: transparent;
                color: rgba({text_color.red()}, {text_color.green()}, {text_color.blue()}, {text_alpha});
                selection-background-color: transparent;
                selection-color: inherit;
            }}
        """
    
    @staticmethod
    def get_button_style(bg_color, text_color, text_alpha):
        """获取按钮样式"""
        return f"""
            QPushButton {{
                background-color: rgba({bg_color.red()}, {bg_color.green()}, {bg_color.blue()}, 50);
                color: rgba({text_color.red()}, {text_color.green()}, {text_color.blue()}, {text_alpha});
                border: none;
                border-radius: 3px;
                padding: 5px;
                font-size: 16px;
                min-width: 30px;
                min-height: 30px;
            }}
            QPushButton:hover {{
                background-color: rgba({bg_color.red()}, {bg_color.green()}, {bg_color.blue()}, 100);
            }}
        """ 