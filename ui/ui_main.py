# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
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


class Ui_OpenALPRHotListImporter(object):
    def setupUi(self, OpenALPRHotListImporter):
        if OpenALPRHotListImporter.objectName():
            OpenALPRHotListImporter.setObjectName(u"OpenALPRHotListImporter")
        OpenALPRHotListImporter.resize(1280, 720)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(OpenALPRHotListImporter.sizePolicy().hasHeightForWidth())
        OpenALPRHotListImporter.setSizePolicy(sizePolicy)
        OpenALPRHotListImporter.setMaximumSize(QSize(1280, 720))
        font = QFont()
        font.setPointSize(12)
        OpenALPRHotListImporter.setFont(font)
        self.verticalLayout_2 = QVBoxLayout(OpenALPRHotListImporter)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_4 = QLabel(OpenALPRHotListImporter)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(200, 0))
        self.label_4.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_11.addWidget(self.label_4)

        self.comboHotlistLocation = QComboBox(OpenALPRHotListImporter)
        self.comboHotlistLocation.addItem("")
        self.comboHotlistLocation.addItem("")
        self.comboHotlistLocation.setObjectName(u"comboHotlistLocation")

        self.horizontalLayout_11.addWidget(self.comboHotlistLocation)

        self.txtHotlistLocation = QLineEdit(OpenALPRHotListImporter)
        self.txtHotlistLocation.setObjectName(u"txtHotlistLocation")

        self.horizontalLayout_11.addWidget(self.txtHotlistLocation)

        self.btnBrowse = QPushButton(OpenALPRHotListImporter)
        self.btnBrowse.setObjectName(u"btnBrowse")

        self.horizontalLayout_11.addWidget(self.btnBrowse)


        self.verticalLayout_4.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_3 = QLabel(OpenALPRHotListImporter)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(200, 0))
        self.label_3.setFont(font)
        self.label_3.setLayoutDirection(Qt.LeftToRight)
        self.label_3.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_9.addWidget(self.label_3)

        self.txtWebServer = QLineEdit(OpenALPRHotListImporter)
        self.txtWebServer.setObjectName(u"txtWebServer")

        self.horizontalLayout_9.addWidget(self.txtWebServer)

        self.btnHelpUrl = QToolButton(OpenALPRHotListImporter)
        self.btnHelpUrl.setObjectName(u"btnHelpUrl")
        icon = QIcon()
        icon.addFile(u"ui/help-icon.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.btnHelpUrl.setIcon(icon)
        self.btnHelpUrl.setIconSize(QSize(22, 22))

        self.horizontalLayout_9.addWidget(self.btnHelpUrl)


        self.verticalLayout_4.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.chkAutoRun = QCheckBox(OpenALPRHotListImporter)
        self.chkAutoRun.setObjectName(u"chkAutoRun")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.chkAutoRun.sizePolicy().hasHeightForWidth())
        self.chkAutoRun.setSizePolicy(sizePolicy1)
        self.chkAutoRun.setMinimumSize(QSize(200, 0))

        self.horizontalLayout_10.addWidget(self.chkAutoRun)

        self.timeAutoRun = QTimeEdit(OpenALPRHotListImporter)
        self.timeAutoRun.setObjectName(u"timeAutoRun")
        self.timeAutoRun.setEnabled(False)
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.timeAutoRun.sizePolicy().hasHeightForWidth())
        self.timeAutoRun.setSizePolicy(sizePolicy2)

        self.horizontalLayout_10.addWidget(self.timeAutoRun)


        self.verticalLayout_4.addLayout(self.horizontalLayout_10)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.verticalSpacer = QSpacerItem(20, 25, QSizePolicy.Minimum, QSizePolicy.Maximum)

        self.horizontalLayout_13.addItem(self.verticalSpacer)


        self.verticalLayout_4.addLayout(self.horizontalLayout_13)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.label_7 = QLabel(OpenALPRHotListImporter)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(200, 0))

        self.horizontalLayout_15.addWidget(self.label_7)

        self.comboParser = QComboBox(OpenALPRHotListImporter)
        self.comboParser.setObjectName(u"comboParser")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.comboParser.sizePolicy().hasHeightForWidth())
        self.comboParser.setSizePolicy(sizePolicy3)

        self.horizontalLayout_15.addWidget(self.comboParser)


        self.verticalLayout_4.addLayout(self.horizontalLayout_15)


        self.horizontalLayout_2.addLayout(self.verticalLayout_4)

        self.horizontalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(OpenALPRHotListImporter)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(110, 0))
        self.label.setFont(font)
        self.label.setLayoutDirection(Qt.LeftToRight)
        self.label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.label)

        self.txtCompanyID = QLineEdit(OpenALPRHotListImporter)
        self.txtCompanyID.setObjectName(u"txtCompanyID")

        self.horizontalLayout.addWidget(self.txtCompanyID)

        self.btnHelpCompanyID = QToolButton(OpenALPRHotListImporter)
        self.btnHelpCompanyID.setObjectName(u"btnHelpCompanyID")
        self.btnHelpCompanyID.setIcon(icon)
        self.btnHelpCompanyID.setIconSize(QSize(22, 22))

        self.horizontalLayout.addWidget(self.btnHelpCompanyID)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_2 = QLabel(OpenALPRHotListImporter)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(110, 0))
        self.label_2.setFont(font)
        self.label_2.setLayoutDirection(Qt.LeftToRight)
        self.label_2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_7.addWidget(self.label_2)

        self.txtAPIKey = QLineEdit(OpenALPRHotListImporter)
        self.txtAPIKey.setObjectName(u"txtAPIKey")

        self.horizontalLayout_7.addWidget(self.txtAPIKey)

        self.btnHelpAPIKey = QToolButton(OpenALPRHotListImporter)
        self.btnHelpAPIKey.setObjectName(u"btnHelpAPIKey")
        self.btnHelpAPIKey.setIcon(icon)
        self.btnHelpAPIKey.setIconSize(QSize(22, 22))

        self.horizontalLayout_7.addWidget(self.btnHelpAPIKey)


        self.verticalLayout_3.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.verticalSpacer_3 = QSpacerItem(20, 25, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.horizontalLayout_8.addItem(self.verticalSpacer_3)


        self.verticalLayout_3.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.label_5 = QLabel(OpenALPRHotListImporter)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(110, 0))

        self.horizontalLayout_14.addWidget(self.label_5)

        self.txtStateImport = QLineEdit(OpenALPRHotListImporter)
        self.txtStateImport.setObjectName(u"txtStateImport")

        self.horizontalLayout_14.addWidget(self.txtStateImport)

        self.btnHelpStateImport = QToolButton(OpenALPRHotListImporter)
        self.btnHelpStateImport.setObjectName(u"btnHelpStateImport")
        self.btnHelpStateImport.setIcon(icon)
        self.btnHelpStateImport.setIconSize(QSize(22, 22))

        self.horizontalLayout_14.addWidget(self.btnHelpStateImport)


        self.verticalLayout_3.addLayout(self.horizontalLayout_14)

        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.label_6 = QLabel(OpenALPRHotListImporter)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(110, 0))

        self.horizontalLayout_16.addWidget(self.label_6)

        self.txtSkipPlates = QLineEdit(OpenALPRHotListImporter)
        self.txtSkipPlates.setObjectName(u"txtSkipPlates")

        self.horizontalLayout_16.addWidget(self.txtSkipPlates)

        self.btnHelpPlatesToSkip = QToolButton(OpenALPRHotListImporter)
        self.btnHelpPlatesToSkip.setObjectName(u"btnHelpPlatesToSkip")
        self.btnHelpPlatesToSkip.setIcon(icon)
        self.btnHelpPlatesToSkip.setIconSize(QSize(22, 22))

        self.horizontalLayout_16.addWidget(self.btnHelpPlatesToSkip)


        self.verticalLayout_3.addLayout(self.horizontalLayout_16)


        self.horizontalLayout_2.addLayout(self.verticalLayout_3)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")

        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.verticalSpacer_2 = QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Maximum)

        self.horizontalLayout_12.addItem(self.verticalSpacer_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout_12)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_8 = QLabel(OpenALPRHotListImporter)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setEnabled(True)
        self.label_8.setFont(font)
        self.label_8.setLayoutDirection(Qt.LeftToRight)
        self.label_8.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.label_8)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_5)

        self.txtExampleFormat = QLineEdit(OpenALPRHotListImporter)
        self.txtExampleFormat.setObjectName(u"txtExampleFormat")
        self.txtExampleFormat.setEnabled(True)
        self.txtExampleFormat.setReadOnly(True)

        self.horizontalLayout_5.addWidget(self.txtExampleFormat)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, -1, -1, 5)
        self.scrollParsers = QScrollArea(OpenALPRHotListImporter)
        self.scrollParsers.setObjectName(u"scrollParsers")
        palette = QPalette()
        brush = QBrush(QColor(0, 0, 0, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        brush1 = QBrush(QColor(255, 255, 255, 255))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Button, brush1)
        palette.setBrush(QPalette.Active, QPalette.Light, brush1)
        palette.setBrush(QPalette.Active, QPalette.Midlight, brush1)
        brush2 = QBrush(QColor(127, 127, 127, 255))
        brush2.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Dark, brush2)
        brush3 = QBrush(QColor(170, 170, 170, 255))
        brush3.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Mid, brush3)
        palette.setBrush(QPalette.Active, QPalette.Text, brush)
        palette.setBrush(QPalette.Active, QPalette.BrightText, brush1)
        palette.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Active, QPalette.Base, brush1)
        palette.setBrush(QPalette.Active, QPalette.Window, brush1)
        palette.setBrush(QPalette.Active, QPalette.Shadow, brush)
        palette.setBrush(QPalette.Active, QPalette.AlternateBase, brush1)
        brush4 = QBrush(QColor(255, 255, 220, 255))
        brush4.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.ToolTipBase, brush4)
        palette.setBrush(QPalette.Active, QPalette.ToolTipText, brush)
        brush5 = QBrush(QColor(0, 0, 0, 128))
        brush5.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Active, QPalette.PlaceholderText, brush5)
#endif
        palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Button, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Light, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Midlight, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Dark, brush2)
        palette.setBrush(QPalette.Inactive, QPalette.Mid, brush3)
        palette.setBrush(QPalette.Inactive, QPalette.Text, brush)
        palette.setBrush(QPalette.Inactive, QPalette.BrightText, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Shadow, brush)
        palette.setBrush(QPalette.Inactive, QPalette.AlternateBase, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.ToolTipBase, brush4)
        palette.setBrush(QPalette.Inactive, QPalette.ToolTipText, brush)
        brush6 = QBrush(QColor(0, 0, 0, 128))
        brush6.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush6)
#endif
        palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush2)
        palette.setBrush(QPalette.Disabled, QPalette.Button, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Light, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Midlight, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Dark, brush2)
        palette.setBrush(QPalette.Disabled, QPalette.Mid, brush3)
        palette.setBrush(QPalette.Disabled, QPalette.Text, brush2)
        palette.setBrush(QPalette.Disabled, QPalette.BrightText, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.ButtonText, brush2)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Shadow, brush)
        palette.setBrush(QPalette.Disabled, QPalette.AlternateBase, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.ToolTipBase, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.ToolTipText, brush)
        brush7 = QBrush(QColor(0, 0, 0, 128))
        brush7.setStyle(Qt.NoBrush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush7)
#endif
        self.scrollParsers.setPalette(palette)
        self.scrollParsers.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 1258, 359))
        self.scrollParsersLayout = QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.scrollParsersLayout.setObjectName(u"scrollParsersLayout")
        self.scrollParsers.setWidget(self.scrollAreaWidgetContents_2)

        self.verticalLayout.addWidget(self.scrollParsers)

        self.btnAddParser = QPushButton(OpenALPRHotListImporter)
        self.btnAddParser.setObjectName(u"btnAddParser")

        self.verticalLayout.addWidget(self.btnAddParser)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.btnViewLog = QPushButton(OpenALPRHotListImporter)
        self.btnViewLog.setObjectName(u"btnViewLog")

        self.horizontalLayout_6.addWidget(self.btnViewLog)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_6)

        self.btnTest = QPushButton(OpenALPRHotListImporter)
        self.btnTest.setObjectName(u"btnTest")

        self.horizontalLayout_6.addWidget(self.btnTest)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_8)

        self.btnSave = QPushButton(OpenALPRHotListImporter)
        self.btnSave.setObjectName(u"btnSave")

        self.horizontalLayout_6.addWidget(self.btnSave)


        self.verticalLayout_2.addLayout(self.horizontalLayout_6)

#if QT_CONFIG(shortcut)
        self.label_4.setBuddy(self.comboHotlistLocation)
        self.label_3.setBuddy(self.txtWebServer)
        self.label_7.setBuddy(self.comboHotlistLocation)
        self.label.setBuddy(self.txtCompanyID)
        self.label_2.setBuddy(self.txtAPIKey)
        self.label_5.setBuddy(self.txtStateImport)
        self.label_6.setBuddy(self.txtSkipPlates)
        self.label_8.setBuddy(self.txtCompanyID)
#endif // QT_CONFIG(shortcut)

        self.retranslateUi(OpenALPRHotListImporter)

        QMetaObject.connectSlotsByName(OpenALPRHotListImporter)
    # setupUi

    def retranslateUi(self, OpenALPRHotListImporter):
        OpenALPRHotListImporter.setWindowTitle(QCoreApplication.translate("OpenALPRHotListImporter", u"OpenALPR Hotlist Importer", None))
        self.label_4.setText(QCoreApplication.translate("OpenALPRHotListImporter", u"Hotlist &Location", None))
        self.comboHotlistLocation.setItemText(0, QCoreApplication.translate("OpenALPRHotListImporter", u"FILE", None))
        self.comboHotlistLocation.setItemText(1, QCoreApplication.translate("OpenALPRHotListImporter", u"URL", None))

        self.btnBrowse.setText(QCoreApplication.translate("OpenALPRHotListImporter", u"Browse", None))
        self.label_3.setText(QCoreApplication.translate("OpenALPRHotListImporter", u"OpenALPR Web &Server", None))
#if QT_CONFIG(tooltip)
        self.txtWebServer.setToolTip(QCoreApplication.translate("OpenALPRHotListImporter", u"The destination address for the OpenALPR web server whose alert lists you wish to update.  Example: https://cloud.openalpr.com", None))
#endif // QT_CONFIG(tooltip)
        self.txtWebServer.setText(QCoreApplication.translate("OpenALPRHotListImporter", u"https://cloud.openalpr.com", None))
        self.btnHelpUrl.setText("")
#if QT_CONFIG(tooltip)
        self.chkAutoRun.setToolTip(QCoreApplication.translate("OpenALPRHotListImporter", u"Enable/disable AutoRun", None))
#endif // QT_CONFIG(tooltip)
        self.chkAutoRun.setText(QCoreApplication.translate("OpenALPRHotListImporter", u"Auto&Run at", None))
        self.timeAutoRun.setDisplayFormat(QCoreApplication.translate("OpenALPRHotListImporter", u"HH:mm", None))
        self.label_7.setText(QCoreApplication.translate("OpenALPRHotListImporter", u"Hotlist &Parser", None))
        self.label.setText(QCoreApplication.translate("OpenALPRHotListImporter", u"Company &ID", None))
#if QT_CONFIG(tooltip)
        self.txtCompanyID.setToolTip(QCoreApplication.translate("OpenALPRHotListImporter", u"The Company ID on the OpenALPR web server.  This can be found on the My Account page: https://cloud.openalpr.com/account/my_account", None))
#endif // QT_CONFIG(tooltip)
        self.btnHelpCompanyID.setText("")
        self.label_2.setText(QCoreApplication.translate("OpenALPRHotListImporter", u"API &Key", None))
#if QT_CONFIG(tooltip)
        self.txtAPIKey.setToolTip(QCoreApplication.translate("OpenALPRHotListImporter", u"The API key used to authenticate with the OpenALPR web server.  This can be found on the My Account page: https://cloud.openalpr.com/account/my_account", None))
#endif // QT_CONFIG(tooltip)
        self.btnHelpAPIKey.setText("")
        self.label_5.setText(QCoreApplication.translate("OpenALPRHotListImporter", u"State &Import", None))
#if QT_CONFIG(tooltip)
        self.txtStateImport.setToolTip(QCoreApplication.translate("OpenALPRHotListImporter", u"List of state license plates (comma separated) to import from the alert list.  Leave blank to import all states.  Example: ca,or,nv,az would limit the import to only plates on the hotlist that correspond do those states.", None))
#endif // QT_CONFIG(tooltip)
        self.txtStateImport.setPlaceholderText("")
        self.btnHelpStateImport.setText("")
        self.label_6.setText(QCoreApplication.translate("OpenALPRHotListImporter", u"Plates to &Skip", None))
#if QT_CONFIG(tooltip)
        self.txtSkipPlates.setToolTip(QCoreApplication.translate("OpenALPRHotListImporter", u"A comma separated list of plates to skip from the alert list.  Example: 000,1111,ABC123 would permanently ignore those plates from import.", None))
#endif // QT_CONFIG(tooltip)
        self.txtSkipPlates.setPlaceholderText("")
        self.btnHelpPlatesToSkip.setText("")
        self.label_8.setText(QCoreApplication.translate("OpenALPRHotListImporter", u"&Example Format", None))
#if QT_CONFIG(tooltip)
        self.txtExampleFormat.setToolTip(QCoreApplication.translate("OpenALPRHotListImporter", u"Example Format", None))
#endif // QT_CONFIG(tooltip)
        self.txtExampleFormat.setPlaceholderText("")
        self.btnAddParser.setText(QCoreApplication.translate("OpenALPRHotListImporter", u"Add &New Parser Item", None))
        self.btnViewLog.setText(QCoreApplication.translate("OpenALPRHotListImporter", u"View Log", None))
        self.btnTest.setText(QCoreApplication.translate("OpenALPRHotListImporter", u"Test", None))
        self.btnSave.setText(QCoreApplication.translate("OpenALPRHotListImporter", u"Save", None))
    # retranslateUi

