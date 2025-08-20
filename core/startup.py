def startup_prompt(dry_run: bool = False) -> bool:
    print("""
    =============================
    InfoSnare Ethical Simulation
    =============================
    This tool simulates info-stealer malware for educational and lab use ONLY.
    Do not run on systems you do not own or without explicit permission.
    """)
    if dry_run:
        print("[DRY RUN] No data will be collected. This is a simulation only.")
        return True
    resp = input("Do you have permission to run this tool on this system? (yes/no): ").strip().lower()
    if resp == 'yes':
        print("[OK] Proceeding with data collection.")
        return True
    else:
        print("[ABORTED] You must have explicit permission to proceed.")
        return False 