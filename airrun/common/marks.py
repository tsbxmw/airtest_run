import logging
import time
import traceback

from airrun.common.base import start_case, stop_case
from airrun.common.helper import exists_check
from airrun.common.queue import recorder_queue
from airrun.config import DefaultConfig

logger = logging.getLogger(__name__)


# 装饰器方法


# 用来启动所有当前测试需要的方法
def airrun_setup(**kwargs):
    # 这里获取 device 信息，可以用于 连接 stf device
    device_name = kwargs.get('device_name')
    app_package = kwargs.get('package_name')
    test_name = kwargs.get('test_name')

    def wrap(func):
        def inner(*args, **kwargs):
            print(f"测试开始 {test_name}")
            start_case(test_name)
            from airtest.core.api import start_app, stop_app
            stop_app(app_package)
            start_app(app_package)
            recorder_queue.put(test_name)  # 这里启动监控
            result = None
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                logger.error(e)
                logger.error(traceback.format_exc())
            recorder_queue.put(DefaultConfig.RECORD_CASE_END_MARK)
            time.sleep(1)
            stop_app(app_package)
            print(f"测试结束 {test_name}")
            stop_case(test_name)
            time.sleep(5)
            return result

        return inner

    return wrap


def make_current_template(*args_out, **kwargs_out):
    def wrap(func):
        def current_template(self, *args, **kwargs):
            if isinstance(self.templates, list) and self.templates:
                self.template = self.templates[0]
                for template in self.templates:
                    if exists_check(template):
                        self.template = template
                        break
            return func(self, *args, **kwargs)

        return current_template

    return wrap
