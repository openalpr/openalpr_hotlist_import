# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'parser_item.ui'
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


class Ui_ParserItem(object):
    def setupUi(self, ParserItem):
        if ParserItem.objectName():
            ParserItem.setObjectName(u"ParserItem")
        ParserItem.resize(1105, 100)
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ParserItem.sizePolicy().hasHeightForWidth())
        ParserItem.setSizePolicy(sizePolicy)
        ParserItem.setMinimumSize(QSize(0, 100))
        ParserItem.setMaximumSize(QSize(2000, 100))
        font = QFont()
        font.setPointSize(12)
        ParserItem.setFont(font)
        self.horizontalLayout_4 = QHBoxLayout(ParserItem)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.frame = QFrame(ParserItem)
        self.frame.setObjectName(u"frame")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy1)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(20)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setFont(font)
        self.label.setLayoutDirection(Qt.LeftToRight)
        self.label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.label)

        self.txtName = QLineEdit(self.frame)
        self.txtName.setObjectName(u"txtName")

        self.horizontalLayout.addWidget(self.txtName)

        self.btnHelpName = QToolButton(self.frame)
        self.btnHelpName.setObjectName(u"btnHelpName")
        icon = QIcon(QIcon.fromTheme(u":resources/help-icon.ico"))
        self.btnHelpName.setIcon(icon)
        self.btnHelpName.setIconSize(QSize(22, 22))

        self.horizontalLayout.addWidget(self.btnHelpName)

        self.horizontalSpacer_2 = QSpacerItem(50, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)
        self.label_2.setLayoutDirection(Qt.LeftToRight)
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.label_2)

        self.txtCode = QLineEdit(self.frame)
        self.txtCode.setObjectName(u"txtCode")

        self.horizontalLayout.addWidget(self.txtCode)

        self.btnHelpCode = QToolButton(self.frame)
        self.btnHelpCode.setObjectName(u"btnHelpCode")
        self.btnHelpCode.setIcon(icon)
        self.btnHelpCode.setIconSize(QSize(22, 22))

        self.horizontalLayout.addWidget(self.btnHelpCode)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_4 = QLabel(self.frame)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_2.addWidget(self.label_4)

        self.comboMatchStrategy = QComboBox(self.frame)
        self.comboMatchStrategy.addItem("")
        self.comboMatchStrategy.addItem("")
        self.comboMatchStrategy.setObjectName(u"comboMatchStrategy")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(1)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.comboMatchStrategy.sizePolicy().hasHeightForWidth())
        self.comboMatchStrategy.setSizePolicy(sizePolicy2)
        self.comboMatchStrategy.setMaximumSize(QSize(90, 16777215))

        self.horizontalLayout_2.addWidget(self.comboMatchStrategy)

        self.horizontalSpacer_7 = QSpacerItem(100, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_7)

        self.chkOverride = QCheckBox(self.frame)
        self.chkOverride.setObjectName(u"chkOverride")

        self.horizontalLayout_2.addWidget(self.chkOverride)

        self.btnHelpOverride = QToolButton(self.frame)
        self.btnHelpOverride.setObjectName(u"btnHelpOverride")
        self.btnHelpOverride.setIcon(icon)
        self.btnHelpOverride.setIconSize(QSize(22, 22))

        self.horizontalLayout_2.addWidget(self.btnHelpOverride)

        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font)
        self.label_3.setLayoutDirection(Qt.LeftToRight)
        self.label_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.label_3)

        self.txtHotlistLocation = QLineEdit(self.frame)
        self.txtHotlistLocation.setObjectName(u"txtHotlistLocation")
        self.txtHotlistLocation.setEnabled(False)

        self.horizontalLayout_2.addWidget(self.txtHotlistLocation)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.horizontalLayout_3.addLayout(self.verticalLayout_2)

        self.layoutButtons = QVBoxLayout()
        self.layoutButtons.setSpacing(10)
        self.layoutButtons.setObjectName(u"layoutButtons")
        self.btnRemove = QPushButton(self.frame)
        self.btnRemove.setObjectName(u"btnRemove")

        self.layoutButtons.addWidget(self.btnRemove)


        self.horizontalLayout_3.addLayout(self.layoutButtons)


        self.verticalLayout_4.addLayout(self.horizontalLayout_3)


        self.horizontalLayout_4.addWidget(self.frame)

#if QT_CONFIG(shortcut)
        self.label.setBuddy(self.txtName)
        self.label_2.setBuddy(self.txtCode)
        self.label_4.setBuddy(self.comboMatchStrategy)
        self.label_3.setBuddy(self.txtCode)
#endif // QT_CONFIG(shortcut)
        QWidget.setTabOrder(self.txtName, self.txtCode)

        self.retranslateUi(ParserItem)
        self.txtName.textChanged.connect(ParserItem.changed)
        self.comboMatchStrategy.currentIndexChanged.connect(ParserItem.changed)
        self.txtCode.textChanged.connect(ParserItem.changed)
        self.txtHotlistLocation.textChanged.connect(ParserItem.changed)

        QMetaObject.connectSlotsByName(ParserItem)
    # setupUi

    def retranslateUi(self, ParserItem):
        ParserItem.setWindowTitle(QCoreApplication.translate("ParserItem", u"OpenALPR Hotlist Importer", None))
        self.label.setText(QCoreApplication.translate("ParserItem", u"List &Name", None))
#if QT_CONFIG(tooltip)
        self.txtName.setToolTip(QCoreApplication.translate("ParserItem", u"The name of the alert list that will be pushed to the OpenALPR Web Server", None))
#endif // QT_CONFIG(tooltip)
        self.btnHelpName.setText("")
        self.label_2.setText(QCoreApplication.translate("ParserItem", u"Parse &Code", None))
#if QT_CONFIG(tooltip)
        self.txtCode.setToolTip(QCoreApplication.translate("ParserItem", u"A special keyword that the hotlist parser uses to identify this alert list type in the input hotlist data.", None))
#endif // QT_CONFIG(tooltip)
        self.btnHelpCode.setText("")
        self.label_4.setText(QCoreApplication.translate("ParserItem", u"Match &Strategy", None))
        self.comboMatchStrategy.setItemText(0, QCoreApplication.translate("ParserItem", u"Exact", None))
        self.comboMatchStrategy.setItemText(1, QCoreApplication.translate("ParserItem", u"Lenient", None))

#if QT_CONFIG(tooltip)
        self.chkOverride.setToolTip(QCoreApplication.translate("ParserItem", u"Check to use a different hotlist file than the one defined in the general \"Hotlist Location\"", None))
#endif // QT_CONFIG(tooltip)
        self.chkOverride.setText(QCoreApplication.translate("ParserItem", u"Override", None))
        self.btnHelpOverride.setText("")
        self.label_3.setText(QCoreApplication.translate("ParserItem", u"Hotlist &Location", None))
        self.btnRemove.setText(QCoreApplication.translate("ParserItem", u"Remove", None))
    # retranslateUi

