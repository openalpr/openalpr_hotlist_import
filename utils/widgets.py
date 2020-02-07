from PySide2.QtCore import Signal, QPoint
from PySide2.QtWidgets import QDialog, QWidget, QToolTip

from ui.ui_log_dialog import Ui_LogDialog
from ui.ui_parser_item import Ui_ParserItem
from ui.ui_test_result_dialog import Ui_TestResultDialog
from utils.ui import validate_line_edit, show_info_dialog


class ParserItemWidget(QWidget):

    changed = Signal()

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = Ui_ParserItem()
        self.ui.setupUi(self)
        self.ui.chkOverride.toggled.connect(self._on_chk_override)
        self.ui.txtName.textChanged.connect(lambda d: validate_line_edit(self.ui.txtName))
        self.ui.txtCode.textChanged.connect(lambda d: validate_line_edit(self.ui.txtCode))
        self.ui.txtHotlistLocation.textChanged.connect(lambda d: validate_line_edit(self.ui.txtHotlistLocation))
        self.ui.btnHelpName.released.connect(lambda: self._on_btn_help(self.ui.txtName))
        self.ui.btnHelpCode.released.connect(lambda: self._on_btn_help(self.ui.txtCode))
        self.ui.btnHelpOverride.released.connect(lambda: self._on_btn_help(self.ui.chkOverride))

    def _on_chk_override(self):
        self.ui.txtHotlistLocation.setEnabled(self.ui.chkOverride.isChecked())

    def validate(self):
        is_valid = validate_line_edit(self.ui.txtName) and validate_line_edit(self.ui.txtCode)
        if self.ui.chkOverride.isChecked():
            is_valid = is_valid and validate_line_edit(self.ui.txtHotlistLocation)
        return is_valid

    def _on_btn_help(self, widget):
        show_info_dialog(parent=self, msg=widget.toolTip())
        # QToolTip.showText(
        #     widget.mapToGlobal(QPoint(0, 0)),
        #     widget.toolTip(),
        #     self,
        #     widget.rect()
        # )


class LogDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_LogDialog()
        self.ui.setupUi(self)

    def set_log(self, log):
        self.ui.lbLog.setText(log)

    def show_bottom(self):
        self.ui.scrollArea.verticalScrollBar().setValue(self.ui.scrollArea.verticalScrollBar().maximum())


class TestResultDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_TestResultDialog()
        self.ui.setupUi(self)

    def clear(self, cmd):
        self.ui.txtContent.setText(cmd)

    def append_result(self, result):
        self.ui.txtContent.setText(self.ui.txtContent.text() + '\n' + result)

    def show_bottom(self):
        self.ui.scrollArea.verticalScrollBar().setValue(self.ui.scrollArea.verticalScrollBar().maximum())
