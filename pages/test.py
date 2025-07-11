import sys
from PySide6.QtWidgets import QApplication

import RinUI
from RinUI import RinUIWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gallery = RinUIWindow("pages/main.qml")
    app.exec()