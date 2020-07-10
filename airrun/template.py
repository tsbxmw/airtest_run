import logging
import time

from airtest.core.api import Template, touch, exists, assert_exists, text
from airrun.common.marks import make_current_template

logger = logging.getLogger(__name__)


# 这个模板基类是为了更好地扩展之前 Template 类
# 后面有其他的针对图像识别的各种操作，都可以集成到这个基类里


class TemplateBase(object):
    def __init__(self, template: Template or [], msg="", detail=""):
        if isinstance(template, list):
            self.templates = template
            self.template = template[0]
        else:
            self.templates = []
            self.template = template
        self.msg = msg
        self.detail = detail

    def __repr__(self):
        return self.msg

    # 点击
    # 使用之前一定要 wait for
    def click(self, times=1, **kwargs):
        print(self.template)
        if isinstance(self.template, Template):
            touch(self.template, times, **kwargs)
        else:
            self.template.click()

        time.sleep(kwargs.get("timeout", 0))

    # 监测
    def exists(self):
        if isinstance(self.template, Template):
            return exists(self.template)
        else:
            return self.template.exists()

    # assert
    @make_current_template()
    def assert_exists(self, timeout=20):
        time_start = time.time()
        while True:
            try:
                if self.exists():
                    return
            except Exception as e:
                logger.error(e)
                time.sleep(1)

            if time.time() - time_start > timeout:
                break

        if isinstance(self.template, Template):
            assert_exists(self.template)
        else:
            assert self.exists()

    # 等待进入
    def wait_for(self, timeout=60 * 1, sleep_time=1):
        time_start = time.time()
        while True:
            try:
                if isinstance(self.templates, list) and self.templates:
                    for template in self.templates:
                        self.template = template
                        print(f"try to get {self.template}")
                        if self.exists():
                            return True
                else:
                    if self.exists():
                        break
                time.sleep(0.1)
            except Exception as e:
                logger.error(e)
                time.sleep(sleep_time)

            if time.time() - time_start > timeout:
                return False
        return True

    # type
    def input(self, text_str: str, enter=False):
        if enter or isinstance(self.template, Template):
            text(str(text_str), enter)
            return
        else:
            self.template.set_text(str(text_str))
