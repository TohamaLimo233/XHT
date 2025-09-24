import sys
from PySide6.QtWidgets import QApplication
import os
import platform

import Lib.LogMaker as LogMaker
import Lib.XHTWindow as XHTWindow

#Banner
print("██   ██ ██   ██ ████████ ")
print(" ██ ██  ██   ██    ██    ")
print("  ███   ███████    ██    ")
print(" ██ ██  ██   ██    ██    ")
print("██   ██ ██   ██    ██    ")

log = LogMaker.logger()

log.info(f"""
运行平台：{platform.system()}
OS版本：{platform.release()}
Python版本：{platform.python_version()}
PID：{os.getpid()}""")

class Example(QApplication):
    def __init__(self):
        super().__init__(sys.argv)
        self.setStyleSheet("""
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

    def run(self, window: XHTWindow.Window):
        window.show()
        sys.exit(self.exec())