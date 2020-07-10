import json
import os
from multiprocessing import Process
from threading import Thread

from airrun.common.helper import time_now_format
from airrun.utils.adb import AdbTool
from airrun.config import DefaultConfig
import logging, time

logger = logging.getLogger(__name__)


class RecordAndroidInfo(Process):
    def __init__(self, queue, device_name, package_name, test_name=None, adb_tool=None, log_root=None):
        super().__init__()
        self.daemon = True
        self.name = f"{device_name}={package_name}"
        self.device_name = device_name
        self.package_name = package_name
        self.test_name = test_name
        self.adb_tool = adb_tool if adb_tool else AdbTool(device_name)
        self.queue = queue
        self.log_path = log_root
        self.all_data = {}

    def reset_bug_report_log(self):
        self.adb_tool.reset_bug_report_log()

    def get_bug_report_log(self, test_name):
        self.adb_tool.get_bug_report_log(f"{self.log_path}/{test_name}_bug_report.txt")

    def write_to_file(self):
        if not os.path.exists(self.log_path):
            os.mkdir(self.log_path)
        with open(f"{self.log_path}/cpu_memory.json", 'w') as f:
            f.write(json.dumps(self.all_data))

    def check_test_name(self):
        # 0 Empty, 1 start, 2...
        if self.queue.empty():
            return 0
        current_test_name = self.test_name
        self.test_name = self.queue.get()
        if self.test_name == DefaultConfig.RECORD_ALL_END_MARK:
            self.get_bug_report_log(current_test_name)
            self.queue.put(DefaultConfig.RECORD_END_RESPONSE)
            return 2
        if self.test_name == DefaultConfig.RECORD_CASE_END_MARK:
            return 3
        return 1

    def run(self):
        self.reset_bug_report_log()
        self.all_data = {}
        while self.check_test_name() == 0:
            time.sleep(0.1)
        flag = True
        while flag:
            wait_flag = False
            current_test_name = self.test_name
            self.all_data[current_test_name] = {
                "name": f"{self.device_name}={self.package_name}={current_test_name}",
                "begin_time": time_now_format(),
                "end_time": time_now_format(),
                "data": {}
            }
            while True:
                check = self.check_test_name()
                if check == 3:  # 结束当前测试
                    self.all_data[current_test_name]["end_time"] = time_now_format()
                    wait_flag = True
                    break
                if check == 2:
                    flag = False
                    break
                current_data = {
                    "heap_size": 0,
                    "heap_alloc": 0,
                    "cpu": 0,
                    "rss": 0
                }
                try:
                    current_data["heap_size"], current_data["heap_alloc"] = self.adb_tool.get_memory_info(self.package_name)
                except Exception as e:
                    logger.error(e)
                try:
                    current_data["cpu"], current_data["rss"] = self.adb_tool.get_cpu(self.package_name, by_pid=True)
                except Exception as e:
                    logger.error(e)
                self.all_data[current_test_name]["data"][time_now_format()] = current_data
                time.sleep(0.1)
            if wait_flag:
                while True:
                    check = self.check_test_name()
                    if check == 0:
                        time.sleep(0.5)
                        continue
                    elif check == 1:
                        break
                    elif check == 2:
                        flag = False
                        break

        self.write_to_file()