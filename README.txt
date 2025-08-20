# 🕵️ InfoSnare

InfoSnare is a Python-based educational tool designed to simulate the data collection techniques used by info-stealer malware, for use in ethical research and cybersecurity labs. It collects system and user environment data and stores it locally for analysis. **No data is sent over the network.**

## 🚦 Purpose

- For ethical simulation and blue team training
- Demonstrates how attackers might gather information
- All data is stored locally in the `stolen_data/` folder

## 📦 Features

- Collects system information (OS, CPU, boot time, etc.)
- Captures clipboard contents
- Lists top CPU-consuming processes
- Detects installed antivirus
- Fetches WiFi SSID
- Enumerates connected devices
- Takes a screenshot and webcam photo (if available)
- All output is saved as JSON/TXT in `stolen_data/`
- Robust error handling and logging

---

## 🗂 File Structure

```
InfoSnare/
├── main.py                # Main simulation script
├── README.txt             # Documentation
├── requirements.txt       # Python dependencies
├── credits.txt            # Attribution
├── licence.txt            # License (MIT)
├── test_webhook_functionality.py  # Now tests local data output
└── stolen_data/           # All simulated "stolen" data (created at runtime)
```

---

## ⚙️ Requirements

- Python 3.8+
- Windows OS (for full feature support)

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Usage

Run the main script:

```bash
python main.py
```

Data will be periodically saved in the `stolen_data/` directory. Review the logs in `InfoSnare.log` for details.

---

## 🛑 Legal & Ethical Notice

> This project is for **educational and ethical simulation** only. Do **not** use on systems you do not own or without explicit permission. No data leaves your machine. Use responsibly for learning and defense training.

---
