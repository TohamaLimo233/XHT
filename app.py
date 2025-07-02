import xht
import sys
import win32api
import win32event
import winerror
from PySide6.QtWidgets import QMessageBox,QApplication

if __name__ == '__main__':
    # 单实例检测
    mutex = win32event.CreateMutex(None, False, "XHT_TTATE_MUTEX")
    if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
        QMessageBox.critical(None, "程序已运行", "错误")
        sys.exit(0)
    
    app = QApplication(sys.argv)
    app.setStyleSheet("""
                      QWidget {
                       font-family: Microsoft YaHei UI; 
                      }
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
        QMessageBox.critical("错误", str(e))
        sys.exit(1)