from datetime import datetime
import os
import platform
# import qdarkstyle
import sys
import tempfile
from functools import partial
import yaml

from PySide2 import QtCore
from PySide2.QtCore import QTime, Qt, QPoint
from PySide2.QtWidgets import QApplication, QWidget, QFileDialog, QLabel, QToolTip

import gui_settings

from ui.ui_main import Ui_OpenALPRHotListImporter
import ui.ui_resources

from utils.common import get_cron_setting, get_all_parsers, read_log, set_cron_job, remove_old_crons
from utils.ui import validate_line_edit, show_error_dialog, show_info_dialog
from utils.widgets import ParserItemWidget, LogDialog, TestResultDialog


_cur_dir = os.path.dirname(os.path.realpath(__file__))

class OpenALPRHotListImporterApp(QWidget):

    def __init__(self, scale_ratio=1.0, parent=None):
        QWidget.__init__(self, parent)
        self.ui = Ui_OpenALPRHotListImporter()
        self.ui.setupUi(self)
        self.resize(gui_settings.WIDTH*scale_ratio, gui_settings.HEIGHT*scale_ratio)

        # Connect signals
        self.ui.comboHotlistLocation.currentIndexChanged.connect(self._on_hotlist_location_changed)
        self.ui.comboParser.currentIndexChanged.connect(self._on_parser_changed)
        self.ui.btnBrowse.released.connect(self._on_btn_browse)
        self.ui.btnViewLog.released.connect(self._on_btn_view_log)
        self.ui.btnTest.released.connect(self._on_btn_test)
        self.ui.btnSave.released.connect(self._on_btn_save)
        self.ui.chkAutoRun.toggled.connect(self._on_chk_autorun)
        self.ui.btnAddParser.released.connect(self._on_btn_add_parser_item)
        self.ui.txtCompanyID.textChanged.connect(lambda: validate_line_edit(self.ui.txtCompanyID))
        self.ui.txtAPIKey.textChanged.connect(lambda: validate_line_edit(self.ui.txtAPIKey))
        self.ui.txtHotlistLocation.textChanged.connect(lambda: validate_line_edit(self.ui.txtHotlistLocation))
        self.ui.txtWebServer.textChanged.connect(lambda: validate_line_edit(self.ui.txtWebServer))
        self.ui.btnHelpCompanyID.released.connect(lambda: self._on_btn_help(self.ui.txtCompanyID))
        self.ui.btnHelpAPIKey.released.connect(lambda: self._on_btn_help(self.ui.txtAPIKey))
        self.ui.btnHelpUrl.released.connect(lambda: self._on_btn_help(self.ui.txtWebServer))
        self.ui.btnHelpStateImport.released.connect(lambda: self._on_btn_help(self.ui.txtStateImport))
        self.ui.btnHelpPlatesToSkip.released.connect(lambda: self._on_btn_help(self.ui.txtSkipPlates))

        # Custom initializations
        self.ui.scrollParsersLayout.setAlignment(Qt.AlignTop)
        self.parsers = get_all_parsers()
        self._test_result_dlg = TestResultDialog()
        self._test_process = QtCore.QProcess(self)
        self._test_process.setProcessChannelMode(QtCore.QProcess.MergedChannels)
        self._test_process.readyReadStandardOutput.connect(self._on_test_data_ready)
        self._initialize()

    def _initialize(self):
        if platform.system() == 'Linux':

            if os.geteuid() != 0:

                show_error_dialog(parent=self, msg="You must run with root privileges in order to save any configuration")


            self.ui.chkAutoRun.setEnabled(False)
            self.ui.timeAutoRun.setEnabled(False)
            cron_val = get_cron_setting()
            if cron_val:
                self.ui.timeAutoRun.setTime(QTime(cron_val.hour, cron_val.minute))
        for p in self.parsers:
            self.ui.comboParser.addItem(p.get_parser_name())
        
        # Populate UI with YAML data
        if os.path.isfile(gui_settings.CONFIG_FILE):
            with open(gui_settings.CONFIG_FILE, 'r') as stream:
                config_data = yaml.load(stream)
            try:
                self.ui.txtCompanyID.setText(config_data['company_id'])
                self.ui.txtAPIKey.setText(config_data['api_key'])
                self.ui.txtHotlistLocation.setText(config_data['hotlist_path'])
                self.ui.txtWebServer.setText(config_data['server_base_url'])
                parser_idx = [i for i, p in enumerate(self.parsers) 
                              if p.__class__.__module__.split('.')[-1] == config_data['hotlist_parser']][0]
                self.ui.comboParser.setCurrentIndex(parser_idx)
                if platform.system() == 'Windows':
                    tasks = os.popen("schtasks.exe").read()
                    if gui_settings.TASK_NAME in tasks:
                        openalpr_task = [t for t in tasks.splitlines() if gui_settings.TASK_NAME in t]
                        if len(openalpr_task) == 0:
                            raise RuntimeError(f'Could not locate {gui_settings.TASK_NAME} in scheduled tasks')
                        time_str = ''.join(openalpr_task[0].split()[2:4])
                        scheduled_time = datetime.strptime(time_str, '%I:%M:%S%p')
                        self.ui.chkAutoRun.setChecked(True)
                        self.ui.timeAutoRun.setTime(QTime(scheduled_time.hour, scheduled_time.minute))
                if 'state_import' in config_data:
                    self.ui.txtStateImport.setText(','.join([s for s in config_data['state_import']]))
                if 'skip_list' in config_data:
                    self.ui.txtSkipPlates.setText(','.join([p for p in config_data['skip_list']]))
            except KeyError as exc:
                raise RuntimeError(f'Malformed YAML missing {exc} key')

    def _on_hotlist_location_changed(self):
        if self.ui.comboHotlistLocation.currentText() == "FILE":
            self.ui.btnBrowse.setEnabled(True)
        else:
            self.ui.btnBrowse.setEnabled(False)
            self.ui.txtHotlistLocation.setText("")

    def _on_parser_changed(self):
        self._cur_parser = self.parsers[self.ui.comboParser.currentIndex()]
        self.ui.txtExampleFormat.setText(self._cur_parser.get_example_format())
        # Clear current parser items
        while self.ui.scrollParsersLayout.count():
            child = self.ui.scrollParsersLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        # Add parser items
        parsers = self._cur_parser.get_default_lists()
        if parsers:
            for i, p in enumerate(parsers):
                item = ParserItemWidget()
                item.ui.txtName.setText(p['name'])
                item.ui.txtCode.setText(p['parse_code'])
                item.ui.btnRemove.released.connect(partial(self._on_remove_parser_item, item))
                self.ui.scrollParsersLayout.addWidget(item)
            # Add "blank" labels
            # for _ in range(max(3 - len(parsers), 0)):
            #     self.ui.scrollParsersLayout.addWidget(QLabel())
        else:
            label = QLabel("No Parser Found")
            label.setAlignment(Qt.AlignCenter)
            self.ui.scrollParsersLayout.addWidget(label)

    def _on_btn_add_parser_item(self):
        item = ParserItemWidget()
        item.ui.btnRemove.released.connect(partial(self._on_remove_parser_item, item))
        self.ui.scrollParsersLayout.addWidget(item)

    @staticmethod
    def _on_remove_parser_item(item):
        try:
            item.deleteLater()
        except RuntimeError:
            pass

    def _is_parser_changed(self):
        lists = self._cur_parser.get_default_lists()
        is_changed = True
        if self.ui.scrollParsersLayout.count() == len(lists):
            is_changed = False
            for i, p in enumerate(lists):
                item = self.ui.scrollParsersLayout.itemAt(i).widget()
                if item.ui.txtName.text() != p['name'] or item.ui.txtCode.text() != p['parse_code'] or \
                        item.ui.chkOverride.isChecked() or item.ui.comboMatchStrategy.currentText() != 'Exact':
                    is_changed = True
                    break
        return is_changed

    def _on_btn_browse(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Hotlist Location File", "",
                                                   "All Files (*)", options=options)
        if file_name:
            self.ui.txtHotlistLocation.setText(file_name)

    def _on_chk_autorun(self):
        self.ui.timeAutoRun.setEnabled(self.ui.chkAutoRun.isChecked())

    def _on_btn_view_log(self):
        dlg = LogDialog(self)
        dlg.set_log(read_log())
        dlg.show()
        dlg.show_bottom()

    def is_valid(self):
        _is_valid = True
        for k in {"txtCompanyID", "txtAPIKey", "txtHotlistLocation", "txtWebServer"}:
            _is_valid = _is_valid and validate_line_edit(getattr(self.ui, k))
        for i in range(self.ui.scrollParsersLayout.count()):
            child = self.ui.scrollParsersLayout.itemAt(i)
            if child and isinstance(child.widget(), ParserItemWidget):
                _is_valid = _is_valid and child.widget().validate()
        return _is_valid

    def _on_test_data_ready(self):
        self._test_result_dlg.append_result(self._test_process.readAllStandardOutput().data().decode())
        self._test_result_dlg.show_bottom()

    def _on_btn_test(self):
        if self.is_valid():
            temp_config_file = os.path.join(tempfile.gettempdir(), 'test_hotlist.yaml')
            conf_file = self.__generate_config_file(temp_config_file)
            args = [os.path.join(_cur_dir, "hotlistimport.py"), conf_file, "--foreground"]
            if not self.ui.chkUpload.isChecked():
                args.append("--skip_upload")
            self._test_result_dlg.clear(f"{sys.executable} {' '.join(args)}\n{'=' * 30}")
            self._test_process.start(sys.executable, args)
            self._test_result_dlg.show()
            self._test_result_dlg.show_bottom()
        else:
            show_error_dialog(parent=self, msg="Please input correct values")

    def _on_btn_save(self):
        if self.is_valid():
            conf_file = self.__generate_config_file(gui_settings.CONFIG_FILE)
            msg = f"Config file is saved as {conf_file}"
            remove_old_crons()
            if self.ui.chkAutoRun.isChecked():
                autorun_time = self.ui.timeAutoRun.text()
                set_cron_job(conf_file, autorun_time)
                msg += f' and will run at {autorun_time}'
            show_info_dialog(parent=self, msg=msg)
        else:
            show_error_dialog(parent=self, msg="Please input correct values")

    def __generate_config_file(self, target_path):

        result_name = self._cur_parser.__class__.__module__.split('.')[-1]
        result_file = target_path

        lines = [
            f"server_base_url: {self.ui.txtWebServer.text()}",
            f"company_id: {self.ui.txtCompanyID.text()}",
            f"api_key: {self.ui.txtAPIKey.text()}",
            f"hotlist_parser: {result_name}",
            f"hotlist_path: {self.ui.txtHotlistLocation.text()}",
            f"temp_dat_file: {os.path.join(tempfile.gettempdir(), 'hotlistimport.dat')}",
            f"temp_csv_file: {os.path.join(tempfile.gettempdir(), 'hotlistimport.csv')}",
            f"log_file: {gui_settings.LOG_FILE}",
            "log_archives: 5",
            "log_max_size_mb: 100",
        ]
        state_import = self.ui.txtStateImport.text().strip()
        if state_import:
            lines.append('state_import:')
            for s in state_import.split(','):
                lines.append(f'  - {s}')
        skip_plates = self.ui.txtSkipPlates.text().strip()
        if skip_plates:
            lines.append('skip_list:')
            for s in skip_plates.split(','):
                lines.append(f"  - '{s}'")
        title_added = False
        for i in range(self.ui.scrollParsersLayout.count()):
            w = self.ui.scrollParsersLayout.itemAt(i).widget()
            if isinstance(w, ParserItemWidget):
                if not title_added:
                    lines.append('alert_types:')
                    title_added = True
                lines.append(f"  - name: {w.ui.txtName.text()}")
                lines.append(f"    parse_code: {w.ui.txtCode.text()}")
                lines.append(f"    match_strategy: {w.ui.comboMatchStrategy.currentText().lower()}")
                if w.ui.chkOverride.isChecked():
                    lines.append(f"    hotlist_path: {w.ui.txtHotlistLocation.text()}")
        with open(result_file, 'w') as f:
            f.write('\n'.join(lines))

        return result_file

    def _on_btn_help(self, widget):
        show_info_dialog(parent=self, msg=widget.toolTip())
        # QToolTip.showText(
        #     widget.mapToGlobal(QPoint(50, -15)),
        #     widget.toolTip(),
        #     self,
        #     widget.rect()
        # )

def main():

    os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'
    app = QApplication(sys.argv)
    form = OpenALPRHotListImporterApp()
    form.showMaximized()
    app.exec_()

if __name__ == '__main__':
    main()
