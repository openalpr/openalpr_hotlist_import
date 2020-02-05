# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'test_result_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.14.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *


class Ui_TestResultDialog(object):
    def setupUi(self, TestResultDialog):
        if TestResultDialog.objectName():
            TestResultDialog.setObjectName(u"TestResultDialog")
        TestResultDialog.resize(1000, 475)
        TestResultDialog.setMinimumSize(QSize(1000, 0))
        TestResultDialog.setMaximumSize(QSize(1000, 16777215))
        self.verticalLayout = QVBoxLayout(TestResultDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.scrollArea = QScrollArea(TestResultDialog)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 980, 424))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.txtContent = QLabel(self.scrollAreaWidgetContents)
        self.txtContent.setObjectName(u"txtContent")
        self.txtContent.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.verticalLayout_2.addWidget(self.txtContent)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)

        self.buttonBox = QDialogButtonBox(TestResultDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(TestResultDialog)
        self.buttonBox.accepted.connect(TestResultDialog.accept)
        self.buttonBox.rejected.connect(TestResultDialog.reject)

        QMetaObject.connectSlotsByName(TestResultDialog)
    # setupUi

    def retranslateUi(self, TestResultDialog):
        TestResultDialog.setWindowTitle(QCoreApplication.translate("TestResultDialog", u"Test Result", None))
        self.txtContent.setText("")
    # retranslateUi

