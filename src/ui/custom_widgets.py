from PySide6.QtWidgets import QTextEdit
from PySide6.QtCore import Qt

class CustomTextEdit(QTextEdit):
    def mousePressEvent(self, event):
        # 禁止鼠标事件传递给文本编辑器
        event.ignore()
    
    def mouseMoveEvent(self, event):
        event.ignore()
    
    def mouseReleaseEvent(self, event):
        event.ignore() 