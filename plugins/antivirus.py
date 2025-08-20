import wmi
import logging
from typing import List

def detect_antivirus() -> List[str]:
    """
    Red Team: Detecting AV helps attackers evade or disable defenses.
    Blue Team: Use tamper protection and monitor for AV enumeration attempts.
    """
    try:
        av_ns = wmi.WMI(namespace="root\\SecurityCenter2")
        av_products = av_ns.AntiVirusProduct()
        names = [p.displayName for p in av_products]
        logging.info('Antivirus info detected.')
        return names or ['None']
    except Exception as e:
        logging.warning(f'Antivirus detection failed: {e}')
        return [] 