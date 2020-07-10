class DeviceBaseException(Exception):
    '''
    device base exception for device info
    '''
    message_base = 'device exception'


class DeviceNotFoundException(DeviceBaseException):
    def __init__(self, device_name=None):
        self.message = f'device {device_name} not found!'

    def __str__(self):
        return self.message


class DeviceDisconnectedException(DeviceBaseException):
    def __init__(self, device_name=None):
        self.message = f'device {device_name} disconnected!'

    def __str__(self):
        return self.message


class DeviceNotAuthException(DeviceBaseException):
    def __init__(self, device_name=None):
        self.message = f'device {device_name} not auth!'

    def __str__(self):
        return self.message


class LocalPackageNotFoundException(Exception):
    def __init__(self, package=None):
        self.message = f'package {package} not found on local!'

    def __str__(self):
        return self.message


class SetUpErrorException(Exception):
    def __init__(self, err=None):
        self.message = str(err)

    def __str__(self):
        return self.message


class InstallAppException(Exception):
    def __init__(self, err=None):
        self.message = f'install app error : {err}'

    def __str__(self):
        return self.message


class CheckScreenLockedFailed(Exception):
    def __init__(self, err=None):
        self.message = f'screen lock error : {err}'

    def __str__(self):
        return self.message


class ArgsMissingFailed(Exception):
    def __init__(self, param):
        self.message = f'缺少参数 {param}'

    def __str__(self):
        return self.message
