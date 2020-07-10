import logging
import time

from airtest.core.api import connect_device

from airrun.common.command_helper import command_execute
from airrun.utils.adb import AdbTool

logger = logging.getLogger(__file__)


#  每个 STF 都负责以下内容
#  获取日志、性能信息、连接设备、断开设备


class DeviceHelper(object):
    def __init__(self, device_name: str = ''):
        if device_name:
            self.adb_tool = AdbTool(device_name)
            self.device_name = device_name

    def constructor(self, device_info: dict):
        try:
            # response info to ->
            self.qtt_id = device_info.get('id')
            self.brandId = device_info.get('brandId')
            self.serial = device_info.get('serial')
            self.relSerial = device_info.get('relSerial')
            self.tcpIp = device_info.get('tcpIp')
            self.name = device_info.get('name')
            self.model = device_info.get('model')
            self.platform = device_info.get('platform')
            self.hostIp = device_info.get('hostIp')
            self.osVersion = device_info.get('osVersion')
            self.px = device_info.get('px')
            self.scoketUrl = device_info.get('scoketUrl')
            self.free = device_info.get('free')
            self.connect_ = device_info.get('connect')
            self.adbkitPort = device_info.get('adbkitPort')
            self.networkType = device_info.get('networkType')
            self.lock = device_info.get('lock')
            self.userName = device_info.get('userName')
            self.adb_remote_port = str(int(device_info['scoketUrl'].split('/')[-2]) + 1)
            self.adb_remote_ip_port = f"{self.hostIp}:{self.adb_remote_port}"
            self.device_name = self.adb_remote_ip_port
            self.adb_tool = AdbTool(self.device_name)
        except Exception as e:
            print(e)

    def connect(self, retry_times: int = 10):
        connect_device(f"Android:///{self.device_name}")
        times = 1
        while times < retry_times:
            if self.check_connect():
                logger.info(f'({self.device_name}): 连接设备成功')
                self.device_model = self.adb_tool.get_device_model()
                return True
            else:
                logger.error(f"({self.device_name}): 连接失败 {results}")
            logger.info(f'({self.device_name}): 尝试连接设备：[{self.device_name}] <{times}>')
            cmd = f'{self.adb_tool.command_path} connect {self.device_name}'
            p = command_execute(cmd)
            results = self.adb_tool.output(p)
            time.sleep(1)
            times += 1
        return False

    def check_connect(self):
        logger.info(f'({self.device_name}): 检查设备是否在线')
        devices = self.adb_tool.get_device_list()
        print(devices)
        if self.device_name in devices:
            logger.info(f'({self.device_name}): 设备在线')
            return True
        return False

    def reconnect(self, try_times=10):
        times = 1
        while times < try_times:
            logger.info(f'({self.device_name}): 设备正在重连 {times}')
            if self.check_connect():
                logger.info(f'({self.device_name}): 设备在线')
                break
            else:
                logger.info(f'({self.device_name}): 设备不在线')
                self.connect()
            times += 1

    def disconnect(self, retry_times=10):
        times = 1
        while times < retry_times:
            logger.info(f'({self.device_name}): 设备尝试断开中 {times}')
            cmd = f"{self.adb_tool.command_path} disconnect {self.device_name}"
            p = command_execute(cmd)
            results = self.adb_tool.output(p)
            if not self.check_connect():
                logger.info(f'({self.device_name}): 设备已断开')
                break
            time.sleep(1)
            times += 1
