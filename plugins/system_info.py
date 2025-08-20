import platform
import psutil
import datetime
import logging
from typing import Dict

def collect_system_info() -> Dict[str, str]:
    """
    Red Team: System info helps attackers tailor exploits and evade detection.
    Blue Team: Limit user access to system details and monitor for enumeration tools.
    """
    try:
        boot_time = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d %H:%M:%S')
        info = {
            'os': platform.system(),
            'hostname': platform.node(),
            'architecture': platform.machine(),
            'cpu': platform.processor(),
            'boot_time': boot_time
        }
        logging.info('System info collected.')
        return info
    except Exception as e:
        logging.error(f'System info collection failed: {e}')
        return {} 