import sys

from airrun.common.device import DeviceHelper
from airrun.common.exception import ArgsMissingFailed
from airrun.common.helper import make_log_path
from airrun.common.queue import recorder_queue
from airrun.record import RecordAndroidInfo
from airrun.runner import Runner




def main(args):
    '''
    Running the device test here
    '''
    device = DeviceHelper(device_name=args.device)
    log_root = make_log_path(device.device_name)
    record = RecordAndroidInfo(recorder_queue, device.device_name, args.package, log_root=log_root)
    record.start()
    runner = Runner(device.device_name, args.package, device, recorder_queue, log_root=log_root, apk_path=args.apk,
                    install=args.install, uninstall=args.uninstall, script=args.script)
    runner.run()
    record.join()
    print(f'Report Generate at {log_root}_report/main.html')
