from PySide2.QtGui import QPalette
from PySide2 import QtCore
from PySide2.QtWidgets import QMessageBox


def validate_line_edit(widget):
    palette = QPalette()
    palette.setColor(QPalette.Text, QtCore.Qt.black if widget.text() else "#D8000C")
    palette.setColor(QPalette.Background, QtCore.Qt.white if widget.text() else QtCore.Qt.red)
    widget.setPalette(palette)
    return len(widget.text().strip()) > 0


def show_info_dialog(parent, msg):
    dlg = QMessageBox(parent)
    dlg.setIcon(QMessageBox.Information)
    dlg.setText(msg)
    dlg.setWindowTitle("Info")
    dlg.exec_()


def show_error_dialog(parent, msg):
    dlg = QMessageBox(parent)
    dlg.setIcon(QMessageBox.Critical)
    dlg.setText(msg)
    dlg.setWindowTitle("Error")
    dlg.exec_()
