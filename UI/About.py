from PySide6.QtCore import (QCoreApplication, QMetaObject, QSize, Qt)
from PySide6.QtGui import (QPixmap)
from PySide6.QtWidgets import (QLabel, QVBoxLayout, QWidget)

class Ui_AboutWindow(object):
    def setupUi(self, AboutWindow):
        if not AboutWindow.objectName():
            AboutWindow.setObjectName(u"AboutWindow")
        AboutWindow.resize(400, 300)
        AboutWindow.setMinimumSize(QSize(400, 300))
        AboutWindow.setMaximumSize(QSize(400, 300))
        self.centralwidget = QWidget(AboutWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setPixmap(QPixmap(u"xhtlogo.ico"))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setTextFormat(Qt.TextFormat.AutoText)
        self.label_2.setScaledContents(False)
        self.label_2.setOpenExternalLinks(True)

        self.verticalLayout.addWidget(self.label_2)

        AboutWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(AboutWindow)

        QMetaObject.connectSlotsByName(AboutWindow)

    def retranslateUi(self, AboutWindow):
        AboutWindow.setWindowTitle(QCoreApplication.translate("AboutWindow", u"\u5173\u4e8e", None))
        self.label.setText("")
        self.label_2.setText(QCoreApplication.translate("AboutWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'.AppleSystemUIFont'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:36pt;\">\u5c0f\u9ed1\u6761</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">0.0.1 Dev</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-bloc"
                        "k-indent:0; text-indent:0px;\"><a href=\"https://github.com/GuzhMtangeroou/XHT/blob/main/LICENSE\"><span style=\" text-decoration: underline; color:#094fd1;\">\u5f00\u6e90\u534f\u8bae</span></a></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"https://github.com/GuzhMtangeroou/XHT\"><span style=\" text-decoration: underline; color:#094fd1;\">Github</span></a></p></body></html>", None))

