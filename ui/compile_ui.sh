pyside2-uic main.ui > ui_main.py
pyside2-uic parser_item.ui > ui_parser_item.py
pyside2-uic log_dialog.ui > ui_log_dialog.py
pyside2-uic test_result_dialog.ui > ui_test_result_dialog.py
# A bug in PySide2?
sed -i -- "s/QString()/''/g" ui_main.py
sed -i -- "s/QString()/''/g" ui_parser_item.py
sed -i -- "s/QString()/''/g" ui_log_dialog.py
sed -i -- "s/QString()/''/g" ui_test_result_dialog.py

# Icon is not working... path issue... :/
sed -i -- "s/help-icon.ico/ui\/help-icon.ico/g" ui_main.py
sed -i -- "s/help-icon.ico/ui\/help-icon.ico/g" ui_parser_item.py
