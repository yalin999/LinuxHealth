# Linux Health Monitor

A modular, real-time system monitoring tool built for Linux. This project provides a terminal-based dashboard with live updates on hardware performance and resource-intensive processes.

## 🚀 Features
* **Live Hardware Metrics**: Real-time tracking of CPU usage (%) and current clock frequency (GHz).
* **Memory Management**: Detailed RAM usage monitoring (Used/Total GB) with dynamic color-coding.
* **Process Tracking**: A dynamic list of the Top 5 CPU-intensive applications.
* **Smart Battery Detection**: Handles AC Power/Docking station states gracefully.
* **Modular Architecture**: Clean separation between hardware logic (`sensors.py`) and UI logic (`main.py`).

## 🛠️ Project Structure
```text
LinuxHealth/
├── main.py            # Entry point & Dashboard UI
├── src/
│   ├── __init__.py    # Python package marker
│   └── sensors.py     # Hardware logic & psutil calls
└── requirements.txt   # Project dependencies