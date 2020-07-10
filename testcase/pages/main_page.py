import os

from airtest.core.api import Template

from airrun.template import TemplateBase

current_path = f"{os.path.split(os.path.realpath(__file__))[0]}/resource"


class DaoHangTemplate(object):
    # 导航栏
    def __init__(self, path):
        self.base_path = f"{path}/底部导航"
        # 我的
        self.tmplt_wo_de = TemplateBase(
            Template(f"{self.base_path}/我.png", record_pos=(0.376, 0.918), resolution=(1080, 2160))
        )


class MainPageTemplage(object):
    base_path = f"{current_path}/主页"
    # 主页
    dao_hang_template = DaoHangTemplate(base_path)
