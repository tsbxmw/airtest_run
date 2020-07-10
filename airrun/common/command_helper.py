import logging
import subprocess
import sys
import traceback

logger = logging.getLogger(__name__)


def command_execute(cmd):
    try:
        if not cmd:
            return False
        logger.info(cmd)
        if sys.platform == 'darwin':
            command_process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                               executable="/bin/bash")
        elif sys.platform == 'win32':
            command_process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return command_process
    except Exception as e:
        logger.error(e)
        traceback.print_exc()
