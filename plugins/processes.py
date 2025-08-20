import psutil
import logging
from typing import List, Dict

def list_top_processes(limit: int = 5) -> List[Dict]:
    """
    Red Team: Monitoring processes can reveal security tools or targets for injection.
    Blue Team: Monitor for unusual process enumeration and restrict access to process info.
    """
    try:
        procs = sorted(psutil.process_iter(['pid', 'name', 'cpu_percent']), key=lambda p: p.info['cpu_percent'], reverse=True)
        top = [{k: p.info[k] for k in p.info} for p in procs[:limit]]
        logging.info('Top processes listed.')
        return top
    except Exception as e:
        logging.error(f'Process listing failed: {e}')
        return [] 