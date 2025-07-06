import xht
import sys
import os
from PySide6.QtGui import QFontDatabase
from PySide6.QtWidgets import QApplication

# 设置不生成 .pyc 文件
sys.dont_write_bytecode = True


if __name__ == '__main__':
        app = QApplication(sys.argv)
        app.setStyleSheet("""
                          QMenu {
                          background-color: black;
                          color: white;
                          border: 1px solid #cccccc;
                          border-radius: 8px;
                          }
                          QMenu::item {
                          padding: 6px 26px;
                          font-size: 12px;
                          }
                          QMenu::item:selected {
                          color: black;
                          font-size: 12px;
                          background-color: #e0e0e0;
                          }""")
        try:
            window = xht.xht()
            window.show()
            sys.exit(app.exec())
        except Exception as e:
            print(f"程序异常终止: {e}")
            sys.exit(1)