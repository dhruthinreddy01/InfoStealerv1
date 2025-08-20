# InfoStealer-Analyzer

🛡️ **InfoStealer-Analyzer** is a visually professional, feature-rich, and safe simulation of info-stealer malware detection, built for cybersecurity education and portfolio demonstration. It does NOT collect any real credentials or exfiltrate data—everything is simulated for ethical learning and awareness.

---

## 🚦 Project Overview
InfoStealer-Analyzer simulates how a real info-stealer might operate, but in a safe, defensive, and educational way. It scans for signs of info-stealer malware, suspicious processes, and common attacker behaviors, and presents the results in a modern CLI and web UI.

---

## ✨ Features
- **Modern Bootstrap 5 Web UI** and CLI
- **Simulated Red Team TTPs**: Process, file, and token theft detection (all simulated)
- **Threat Intelligence Mapping**: MITRE ATT&CK techniques for each scan
- **Export Results**: Download findings as JSON, CSV, or Markdown report
- **Input Sanitization**: No real data is accessed or exfiltrated
- **Secure & Clean Code**: Modular, commented, and safe for sandbox use
- **Ethical/Educational Banner**: Always visible

---

## ⚙️ Setup & Usage

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Run the CLI:**
   ```bash
   python main.py
   ```
3. **Run the Web UI:**
   ```bash
   python analyzer_web.py
   ```
4. **Open your browser:**
   Go to [http://127.0.0.1:5001/](http://127.0.0.1:5001/)

---

## 🖼️ Screenshots
- **CLI:**
  ![CLI Screenshot](screenshot-cli.png)
- **Web UI:**
  ![Web UI Screenshot](screenshot-web.png)

---

## 🛠️ How It Works

### 1. Suspicious Process Scan
- Scans running processes for names or paths matching known info-stealer malware (e.g., RedLine, Raccoon, Vidar).
- **Simulated:** No real process is killed or modified.

### 2. Suspicious Directory Scan
- Looks for files with suspicious names (e.g., 'stealer', 'token', 'password') in common drop locations (user home, temp folders).
- **Simulated:** No files are deleted or exfiltrated.

### 3. Browser Data Access Scan
- Simulates detection of browser data access attempts (e.g., open handles to browser files).
- **Simulated:** No browser data is accessed.

### 4. Discord Token Theft Scan
- Simulates detection of Discord token theft attempts.
- **Simulated:** No Discord data is accessed.

### 5. Vulnerable Path Scan
- Lists world-writable or sensitive paths that could be abused by malware.
- **Simulated:** No changes are made to the system.

---

## 🧠 Threat Intelligence Mapping
| Scan Type                  | MITRE ATT&CK Technique(s)         | Description |
|----------------------------|------------------------------------|-------------|
| Suspicious Process Scan    | T1057 (Process Discovery), T1204   | Detects processes matching known malware names |
| Suspicious Directory Scan  | T1083 (File and Directory Discovery) | Looks for suspicious files in common drop locations |
| Browser Data Access Scan   | T1539 (Steal Web Session Cookie), T1114 | Simulates browser data access attempts |
| Discord Token Theft Scan   | T1555 (Credentials from Password Stores) | Simulates Discord token theft attempts |
| Vulnerable Path Scan       | T1574 (Hijack Execution Flow)      | Lists world-writable or sensitive paths |

---

## ⚠️ Ethical Disclaimer
- **This is NOT real malware.** It does not access or exfiltrate any real credentials or sensitive data.
- Use for learning, awareness, and demonstration only.
- Do not use or present as a real attack tool.
- Always disclose the educational nature of this project in your portfolio or interviews.

---

## 📝 License
MIT License. See [LICENSE](LICENSE).

---

## 🚀 Impact & Portfolio Value
- Demonstrates both offensive and defensive cybersecurity skills
- Modular, extensible, and safe for sandbox use
- Ready for submission to internships, CTFs, and portfolio reviews

---

## 📋 Changelog
- v2.0: Refactored for ethical, defensive use. Added web UI, MITRE mapping, and report export.
- v1.0: Initial offensive simulation (now deprecated for safety).

---

## 🆘 Support & Questions
If you have questions or want to add new features, open an issue or contact the author. 