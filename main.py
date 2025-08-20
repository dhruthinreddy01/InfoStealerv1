#!/usr/bin/env python3
"""
InfoStealer-Analyzer: Ethical InfoStealer Detection & Education Tool
Strictly for defensive, educational, and ethical use only.
"""
import os
import sys
import json
import csv
import logging
import argparse
from utils.logger import setup_logger
import psutil
import platform
from datetime import datetime

BANNER = r"""
============================================
   InfoStealer-Analyzer (Defensive Edition)
   For Cybersecurity Education & Awareness
============================================
Strictly for ethical, defensive, and educational use only.
"""

FINDINGS = []
EXPORT_DIR = 'analyzer_results'
os.makedirs(EXPORT_DIR, exist_ok=True)

def scan_suspicious_processes():
    """Detect suspicious processes by name, location, or behavior."""
    suspicious_names = [
        'redline', 'raccoon', 'vidar', 'stealer', 'oski', 'azorult', 'loki', 'agenttesla', 'remcos', 'njrat', 'quasar', 'discordtoken', 'passwordstealer'
    ]
    flagged = []
    for proc in psutil.process_iter(['pid', 'name', 'exe', 'username']):
        try:
            name = proc.info['name'].lower()
            exe = (proc.info['exe'] or '').lower()
            for s in suspicious_names:
                if s in name or s in exe:
                    flagged.append({
                        'type': 'process',
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'exe': proc.info['exe'],
                        'username': proc.info['username'],
                        'reason': f"Suspicious name: {s}"
                    })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    if flagged:
        FINDINGS.extend(flagged)
    return flagged

def scan_suspicious_dirs():
    """Detect suspicious files in common malware drop locations."""
    suspicious_dirs = [
        os.path.expanduser('~'),
        '/tmp', '/var/tmp', '/dev/shm',
        os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming'),
        os.path.join(os.path.expanduser('~'), 'AppData', 'Local', 'Temp'),
    ]
    flagged = []
    for d in suspicious_dirs:
        if os.path.exists(d):
            for fname in os.listdir(d):
                if any(x in fname.lower() for x in ['stealer', 'password', 'discord', 'token', 'log', 'dump']):
                    flagged.append({
                        'type': 'file',
                        'path': os.path.join(d, fname),
                        'reason': 'Suspicious filename in common drop location'
                    })
    if flagged:
        FINDINGS.extend(flagged)
    return flagged

def scan_browser_data_access():
    """Simulate scan for browser data access (placeholder)."""
    # In real use, check for open handles to browser files or known malware files
    flagged = [{
        'type': 'simulation',
        'reason': 'Simulated browser data access scan (educational placeholder)'
    }]
    FINDINGS.extend(flagged)
    return flagged

def scan_discord_token_theft():
    """Simulate scan for Discord token theft (placeholder)."""
    flagged = [{
        'type': 'simulation',
        'reason': 'Simulated Discord token theft scan (educational placeholder)'
    }]
    FINDINGS.extend(flagged)
    return flagged

def scan_vulnerable_paths():
    """List world-writable or sensitive paths (educational)."""
    flagged = []
    paths = [os.path.expanduser('~'), '/tmp', '/var/tmp']
    for p in paths:
        if os.path.exists(p) and os.access(p, os.W_OK):
            flagged.append({'type': 'path', 'path': p, 'reason': 'World-writable'})
    FINDINGS.extend(flagged)
    return flagged

def run_full_scan():
    FINDINGS.clear()
    scan_suspicious_processes()
    scan_suspicious_dirs()
    scan_browser_data_access()
    scan_discord_token_theft()
    scan_vulnerable_paths()
    return FINDINGS

def export_results(fmt='json'):
    now = datetime.now().strftime('%Y%m%d_%H%M%S')
    if fmt == 'json':
        out_path = os.path.join(EXPORT_DIR, f'scan_{now}.json')
        with open(out_path, 'w') as f:
            json.dump(FINDINGS, f, indent=2)
        print(f'[+] Results exported to {out_path}')
    elif fmt == 'csv':
        out_path = os.path.join(EXPORT_DIR, f'scan_{now}.csv')
        if FINDINGS:
            keys = sorted({k for d in FINDINGS for k in d.keys()})
            with open(out_path, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(FINDINGS)
            print(f'[+] Results exported to {out_path}')
        else:
            print('[!] No findings to export.')
    else:
        print('[!] Unknown export format.')

def explain_findings():
    print("\n[Explain Findings] This is a placeholder. In a real tool, this would use OpenAI to explain each finding in plain English.\n")

def main():
    parser = argparse.ArgumentParser(description='InfoStealer-Analyzer: Ethical InfoStealer Detection & Education Tool')
    parser.add_argument('--flask', action='store_true', help='Run the Flask web UI')
    args = parser.parse_args()
    setup_logger()
    print(BANNER)
    if args.flask:
        print('[*] Flask UI not yet implemented. Exiting.')
        sys.exit(0)
    while True:
        print("\n[Menu]")
        print("[1] Scan system for suspicious activity")
        print("[2] Export results (JSON/CSV)")
        print("[3] Explain findings (placeholder)")
        print("[0] Exit")
        choice = input("Select an option: ").strip()
        if choice == '1':
            print("[+] Running full scan...")
            results = run_full_scan()
            print(f"[+] Scan complete. {len(results)} findings.")
            for f in results:
                print(f)
        elif choice == '2':
            fmt = input("Export as [json/csv]: ").strip().lower()
            export_results(fmt)
        elif choice == '3':
            explain_findings()
        elif choice == '0':
            print("[+] Exiting. Stay safe!")
            break
        else:
            print("[!] Invalid option.")

if __name__ == '__main__':
    main()
