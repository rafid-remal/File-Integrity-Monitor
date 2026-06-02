<div align="center">

# 🔐 File Integrity Monitor

**A lightweight, Python-based tool to detect unauthorized file changes in real time.**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Linux-orange?style=flat-square&logo=linux)](https://kernel.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)]()

</div>

---

## 📌 Overview

**File Integrity Monitor (FIM)** continuously watches a set of files or directories and alerts you when anything changes — modifications, deletions, or unexpected additions. It works by building a cryptographic **baseline** of your files and comparing future states against it.

> Ideal for security auditing, change detection on sensitive configs, or learning about file system monitoring.

---

## 📁 Project Structure

```
file-integrity-monitor/
│
├── src/
│   ├── monitor.py              # Core monitoring logic
│   ├── database.py             # Baseline storage & retrieval
│   ├── hash_utils.py           # Hashing functions (SHA-256)
│   ├── config.py               # Configuration settings
│   ├── alerts.py               # Notification and alerting systems
│   ├── hashing.py              # File scanning and hash verification
│   ├── realtime_monitor.py     # Live file system event tracking
│   ├── report.py               # Integrity status and audit reporting
│   ├── scheduler.py            # Periodic task and scan scheduler
│   └── webapp.py               # Web dashboard and user interface
│   
├── data/
│   └── baseline.json    # Stored file hashes (auto-generated)
│
├── monitored/
│   └── sample.txt       # Example file being monitored
│
├── reports/             # Generated integrity reports
├── requirements.txt     # Python dependencies
├── .gitignore
└── README.md
```
---

## ⚙️ How It Works

1. Scan monitored files → compute SHA-256 hashes

2. Store hashes in baseline.json (first run)

3. On subsequent runs → compare current hashes to baseline

4. Report: ADDED / MODIFIED / DELETED files

5. Save detailed report to /reports/

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

```bash
git clone https://github.com/rafid-remal/File-Integrity-Monitor.git
cd File-Integrity-Monitor
```
```
pip install -r requirements.txt
```
```
cd file-integrity-monitor
```

### Usage

```bash
python src/monitor.py --baseline
```
```
python src/monitor.py --check
```
```
python src/monitor.py --watch --interval 30
```
```
echo "hello" > monitored/file1.txt
echo "config" > monitored/config.ini
```
```
python3 src/monitor.py
```
## Modify: create/modify/delete files in monitored/ and refresh the browser to see the alerts show up.
## Go to your repo
```
cd ~/File-Integrity-Monitor/file-integrity-monitor
```
```
# create a file
echo "test" > monitored/testfile.txt

# modify it
echo "changed" >> monitored/testfile.txt

# delete it
rm monitored/testfile.txt
```
## ⚙️ Terminal 1
```
python3 src/realtime_monitor.py
```
## ⚙️ Terminal 2
```
python src/webapp.py
```

### Go to any Browser and search
```
http://127.0.0.1:5000
```

---

## 📊 Sample Output

```
[✔] Baseline loaded — 12 files tracked
[!] MODIFIED  →  monitored/config.cfg
[!] DELETED   →  monitored/secrets.txt
[+] NEW FILE  →  monitored/unknown_script.sh
Report saved → reports/report_2025-06-02_14-32.txt
```

---

## 🛠️ Configuration

Edit `src/config.py` to customize behavior:

| Setting            | Default              | Description                    |
|--------------------|----------------------|--------------------------------|
| `MONITORED_DIR`    | `./monitored`        | Directory to watch             |
| `BASELINE_FILE`    | `data/baseline.json` | Where hashes are stored        |
| `REPORT_DIR`       | `./reports`          | Output folder for reports      |
| `HASH_ALGORITHM`   | `sha256`             | Hashing algorithm              |
| `WATCH_INTERVAL`   | `60` (seconds)       | Polling interval in watch mode |

---

## 📦 Dependencies

watchdog
colorama
---

## 🔒 Security Notes

- Baseline file (`baseline.json`) should be stored in a **read-only** or **external** location in production to prevent tampering.
- For best results, run with appropriate permissions to access all monitored files.
- Consider encrypting the baseline for sensitive environments.

---

## 🤝 Contributing

Contributions are welcome!

```bash
git checkout -b feature/your-feature-name
```

Please keep code clean and add comments where necessary.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  Made with 🛡️ on Linux &nbsp;|&nbsp; Built for security-conscious developers
</div>

