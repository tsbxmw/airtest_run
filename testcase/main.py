__author__ = "mengwei"
__title__ = "测试"
__desc__ = """
测试用例集合
"""

from airtest.core.api import auto_setup
from airtest.core.settings import Settings
from testcase.test_1 import test_1

Settings.FIND_TIMEOUT = 1
auto_setup(__file__)


test_1()