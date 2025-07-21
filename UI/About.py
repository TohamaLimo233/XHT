from PySide6.QtCore import (QCoreApplication, QMetaObject, QSize, Qt)
from PySide6.QtGui import (QFont, QPixmap)
from PySide6.QtWidgets import (QHBoxLayout, QLabel, QVBoxLayout, QWidget)

class Ui_AboutWindow(object):
    def setupUi(self, AboutWindow):
        if not AboutWindow.objectName():
            AboutWindow.setObjectName(u"AboutWindow")
        AboutWindow.resize(320, 250)
        AboutWindow.setMinimumSize(QSize(320, 250))
        AboutWindow.setMaximumSize(QSize(320, 250))
        self.centralwidget = QWidget(AboutWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setPixmap(QPixmap(u"res/icon/xht.png"))
        self.label.setScaledContents(False)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(False)

        self.verticalLayout_2.addWidget(self.label)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        font = QFont()
        font.setFamilies([u"Microsoft YaHei UI"])
        font.setPointSize(24)
        font.setBold(True)
        font.setItalic(False)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet(u"")
        self.label_2.setTextFormat(Qt.TextFormat.AutoText)
        self.label_2.setScaledContents(False)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_2.setOpenExternalLinks(True)

        self.verticalLayout.addWidget(self.label_2)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label_3)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setTextFormat(Qt.TextFormat.RichText)
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_5.setOpenExternalLinks(True)

        self.horizontalLayout.addWidget(self.label_5)

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setTextFormat(Qt.TextFormat.RichText)
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_4.setOpenExternalLinks(True)

        self.horizontalLayout.addWidget(self.label_4)

        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setTextFormat(Qt.TextFormat.RichText)
        self.label_6.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_6.setOpenExternalLinks(True)

        self.horizontalLayout.addWidget(self.label_6)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        AboutWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(AboutWindow)

        QMetaObject.connectSlotsByName(AboutWindow)

    def retranslateUi(self, AboutWindow):
        AboutWindow.setWindowTitle(QCoreApplication.translate("AboutWindow", u"\u5173\u4e8e", None))
        self.label.setText("")
        self.label_2.setText(QCoreApplication.translate("AboutWindow", u"\u5c0f\u9ed1\u6761", None))
        self.label_3.setText(QCoreApplication.translate("AboutWindow", u"0.0.1 Dev", None))
        self.label_5.setText(QCoreApplication.translate("AboutWindow", u"<a href=\"https://github.com/TohamaLimo233/XHT\" title=\"Github\">Github</a>", None))
        self.label_4.setText(QCoreApplication.translate("AboutWindow", u"<p><a href=\"https://github.com/TohamaLimo233/XHT/blob/main/LICENSE\" title=\"开源协议\">开源协议</a>", None))
        self.label_6.setText(QCoreApplication.translate("AboutWindow", u"<a href=\"https://classwidgets.rinlit.cn\" title=\"Github\">ClassWidgets(\u53cb\u94fe)</a>", None))