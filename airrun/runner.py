import time
import traceback
from argparse import Namespace

from airtest.cli.runner import run_script
from airtest.core.api import install, uninstall

from airrun.config import DefaultConfig
from airrun.common.device import DeviceHelper
from airrun.report.report import main as report_generate


class Runner(object):
    def __init__(self, device_name, package_name='', stf_device: DeviceHelper = None, queue_record=None,
                 log_root=None, apk_path=DefaultConfig.APK_DEFAULT_PATH, install=False, uninstall=False,
                 script=None):
        super().__init__()
        self.device_name = device_name
        if not stf_device:
            stf_device = DeviceHelper(self.device_name)
        self.stf_device = stf_device
        self.package_name = package_name
        self.queue_record = queue_record
        self.log = log_root
        self.report = f"{self.log}_report"
        self.apk_path = apk_path
        self.install = install
        self.uninstall = uninstall
        self.script = script

    def run_airtest(self):
        try:
            args = Namespace()
            args.device = f"Android:///{self.stf_device.device_name}"
            args.log = self.log
            args.script = DefaultConfig.SCRIPT_MAIN_PATH if not self.script else self.script
            args.compress = 10
            args.recording = None
            args.action = 'run'
            try:
                run_script(args)
            except Exception as e:
                print(e)
                traceback.print_exc()
        except Exception as ee:
            print(ee)
            traceback.print_exc()

    def run_report(self):
        try:
            args = Namespace()
            args.lang = 'en'
            args.script = DefaultConfig.SCRIPT_MAIN_PATH
            args.package = self.package_name
            args.outfile = "main.html"
            args.device = self.device_name if not self.stf_device.device_model else self.stf_device.device_model
            args.log_root = self.log
            args.export = self.report
            args.record = []
            args.plugins = None
            args.test_name = "test_4"
            args.static_root = None
            args.package_version = self.stf_device.adb_tool.get_package_version(self.package_name)
            try:
                report_generate(args)
            except Exception as e:
                print(e)
                traceback.print_exc()

        except Exception as e:
            print(e)
            traceback.print_exc()

    def install_app(self):
        try:
            install(self.apk_path)
        except Exception as e:
            print(e)

    def uninstall_app(self):
        try:
            uninstall(self.package_name)
        except Exception as e:
            print(e)

    def run(self):
        self.stf_device.connect()
        if self.uninstall:
            self.uninstall_app()
        if self.install:
            self.install_app()
        time.sleep(5)
        self.run_airtest()
        time.sleep(1)
        self.queue_record.put(DefaultConfig.RECORD_ALL_END_MARK)
        time.sleep(10)
        if self.check_record():
            self.run_report()
        self.stf_device.disconnect()

    def check_record(self):
        while True:
            if self.queue_record.empty():
                time.sleep(1)
                continue
            if self.queue_record.get() == DefaultConfig.RECORD_END_RESPONSE:
                return 1

