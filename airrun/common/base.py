from airtest.core.api import swipe
from airtest.core.helper import logwrap
from poco.drivers.android.uiautomation import AndroidUiautomationPoco

# defined the poco
poco = AndroidUiautomationPoco(use_airtest_input=False, screenshot_each_action=False)


class BaseAirRun(object):
    def __init__(self):
        self.resolution = poco.get_screen_size()  # 获取设备屏幕size
        self.run_time = 0.01  # 定义滑动时间
        self.x = int(self.resolution[0])  # 定义x轴
        self.y = int(self.resolution[1])  # 定义y轴

    def left_swip(self, count):  # 封装左滑方法
        for i in range(0, count):
            swipe((0.95 * self.x, 0.45 * self.y), (0.04 * self.x, 0.45 * self.y), duration=self.run_time)

    def right_swip(self, count):  # 定义右滑方法
        for i in range(0, count):
            swipe((0.04 * self.x, 0.45 * self.y), (0.95 * self.x, 0.45 * self.y), duration=self.run_time)

    def up_swip(self, count):  # 定义上滑方法
        for i in range(0, count):
            swipe((0.5 * self.x, 0.8 * self.y), (0.5 * self.x, 0.1 * self.y), duration=self.run_time)

    def down_swip(self, count):  # 定义下滑方法
        for i in range(0, count):
            swipe((0.5 * self.x, 0.3 * self.y), (0.5 * self.x, 0.8 * self.y), duration=self.run_time)


bar = BaseAirRun()
x = bar.x
y = bar.y


@logwrap
def start_case(case_name):
    # 这里可以将步骤插入到 log 中，用于展示
    pass


@logwrap
def stop_case(case_name):
    # 这里可以将步骤插入到 log 中，用于展示
    pass

