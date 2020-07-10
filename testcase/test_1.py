import logging
import time

from airtest.core.api import *

from airrun.common.marks import airrun_setup
from testcase.config.config import LocalSetting
from testcase.pages import main_page_template

logger = logging.getLogger(__name__)

__author__ = "mengwei"
__title__ = "Case 1"
__desc__ = """
金刚切换 DEMO
"""


# 1
@airrun_setup(package_name=LocalSetting.APP_PACKAGE_NAME, test_name="test_1", login_func=None)
def test_1():
    start_app(LocalSetting.APP_PACKAGE_NAME)
    time.sleep(5)
    main_page_template.dao_hang_template.tmplt_wo_de.assert_exists()
    main_page_template.dao_hang_template.tmplt_wo_de.click()
