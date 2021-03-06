"""
    Common utilities
"""
import glob
import importlib
import inspect
import math
import os
import logging.config
import platform
import subprocess
import sys
import datetime
import operator
from parsers.base import BaseParser

if platform.system() != 'Windows':
    from crontab import CronTab

import gui_settings

_cur_dir = os.path.dirname(os.path.realpath(__file__))

log_file = os.path.expanduser('~/.alpr/alpr_hotlist_importer.log')
os.makedirs(os.path.dirname(log_file), exist_ok=True)

logging.config.fileConfig(os.path.join(_cur_dir, 'logging.ini'))
logger = logging.getLogger('ALPR')


def get_human_file_size(byte_size, units=None):
    if units is None:
        units = [' bytes', 'KB', 'MB', 'GB']
    return str(byte_size) + units[0] if byte_size < 1024 else get_human_file_size(byte_size >> 10, units[1:])


def get_all_parsers():
    parsers = []
    for _file in glob.glob(os.path.join(_cur_dir, os.pardir, 'parsers', '*.py')):
        name = os.path.splitext(os.path.basename(_file))[0]
        # Ignore __ files
        if name.startswith("__"):
            continue
        module = importlib.import_module("parsers." + name)

        for member in dir(module):
            handler_class = getattr(module, member)

            if handler_class and inspect.isclass(handler_class) and issubclass(handler_class, BaseParser):
                cls = handler_class(config_obj={})
                try:
                    parser_name = cls.get_parser_name()
                except NotImplementedError:
                    continue
                if parser_name not in [p.get_parser_name() for p in parsers]:
                    parsers.append(cls)

    return sorted(parsers, key=operator.methodcaller('get_parser_name'))


def read_log():
    with open(log_file) as f:
        lines = f.readlines()
    return ''.join(lines[-500:])


def remove_old_crons():
    if platform.system() != 'Windows':
            return
    if os.path.exists(gui_settings.BAT_FILE):
        os.remove(gui_settings.BAT_FILE)
    if gui_settings.TASK_NAME in os.popen("schtasks.exe").read():
        subprocess.Popen(["schtasks.exe", "/delete", "/tn", gui_settings.TASK_NAME, "/f"])


def set_cron_job(conf_file, autorun_time):
    if platform.system() != 'Windows':
        return
    remove_old_crons()
    py_file = f'{os.path.join(_cur_dir, os.pardir, "hotlistimport.py")}'
    with open(gui_settings.BAT_FILE, 'w') as f:
        f.write(f'"{sys.executable}" "{py_file}" "{conf_file}"{os.linesep}')
    cmd = ["schtasks.exe", "/create", "/tn", gui_settings.TASK_NAME, "/st", autorun_time, "/sc", "daily", "/tr", gui_settings.BAT_FILE]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    logger.info(f'Created schedule:\n\tout: `{stdout}`, \n\terror: `{stderr}`')
    return stdout


def get_cron_setting():
    if os.path.isfile(gui_settings.LINUX_CRON_FILE):
        line = open(gui_settings.LINUX_CRON_FILE).read().strip()
        cron_str = ' '.join(line.split()[:5])
        entry = CronTab(cron_str)
        next_time = datetime.datetime.now() + datetime.timedelta(seconds=math.ceil(entry.next()))
        return next_time


if __name__ == '__main__':
    set_cron_job(conf_file=os.path.expanduser('~/Documents/al_state.yaml'), autorun_time="04:32:00")
