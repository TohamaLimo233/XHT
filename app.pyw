import APP.xht as xht
import sys
from PySide6.QtWidgets import QApplication
import os

work_path = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(work_path, "config")

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
            window = xht.xht(config_path)
            window.show()
            sys.exit(app.exec())
        except Exception as e:
            print(f"程序异常终止: {e}")
            sys.exit(1)