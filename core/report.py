import os
import json
from typing import List

def generate_report(data_dir: str = 'stolen_data', output_file: str = 'stolen_data/summary_report.md'):
    """
    Parses all JSON dumps in data_dir and generates a Markdown summary report.
    """
    entries: List[dict] = []
    for fname in os.listdir(data_dir):
        if fname.endswith('.json'):
            with open(os.path.join(data_dir, fname), 'r') as f:
                try:
                    entries.append(json.load(f))
                except Exception:
                    continue
    with open(output_file, 'w') as out:
        out.write('# InfoSnare Data Summary\n\n')
        for entry in entries:
            out.write(f"## Dump at {entry.get('timestamp', 'unknown')}\n")
            for k, v in entry.items():
                if k not in ('timestamp', 'screenshot', 'webcam_image'):
                    out.write(f"- **{k}**: {v}\n")
            if entry.get('screenshot'):
                out.write(f"- Screenshot: {entry['screenshot']}\n")
            if entry.get('webcam_image'):
                out.write(f"- Webcam: {entry['webcam_image']}\n")
            out.write('\n---\n\n') 