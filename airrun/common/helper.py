import logging
import os
import platform
import sys
from datetime import datetime

import prettytable
from airtest.core.api import exists
from airtest.core.cv import Template

from airrun.config import DefaultConfig

logger = logging.getLogger(__name__)


def show_info_as_table(keys: list, values: list) -> None:
    # keys list; values list(dict) or dict
    table = prettytable.PrettyTable()
    if isinstance(values, list):
        table.field_names = keys
        for v in values:
            if isinstance(v, list):
                row = v
            elif isinstance(v, dict):
                row = v.values()
            table.add_row(row)
    elif isinstance(values, dict):
        table.field_names = ['key', 'value']
        for v in keys:
            row = [v, values.get(v)]
            table.add_row(row)
    logger.info('\n{}'.format(table))


def bytes_to_utf8_gbk(data):
    try:
        result = data.decode('utf-8')
        return result
    except Exception:
        result = data.decode('gbk')
        return result


def deal_with_python_version(data):
    if str(sys.version_info.major) == '3':
        if isinstance(data, list):
            result = [bytes_to_utf8_gbk(d) for d in data]
        else:
            result = bytes_to_utf8_gbk(data)
        return result
    else:
        return data


def time_now_format() -> str:
    date_time_now = datetime.now().strftime('%Y%m%d-%H.%M.%S')
    return date_time_now


def system():
    return platform.system()


def make_log_path(device_name: str = "device") -> str:
    time_now = time_now_format()
    log_path = f"{DefaultConfig.LOG_PATH_ROOT}/{device_name}/{time_now}"
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    return log_path


def make_report_path(log_path: str = "") -> str:
    report_path = f"{log_path}_report"
    if not os.path.exists(report_path):
        os.makedirs(report_path)
    return report_path


def exists_check(template):
    if isinstance(template, Template):
        return exists(template)
    else:
        return template.exists()
