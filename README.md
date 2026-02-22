# Linux Health Monitor 🐧

An advanced, professional-grade system diagnostic tool built for Fedora and other Linux distributions. This project follows **ISO/IEC 25010** quality standards and **ISO/IEC 12207** lifecycle processes to ensure reliability and maintainability.

## 🚀 Features
- **CPU & RAM Monitoring**: Real-time utilization and clock speed tracking.
- **Zombie Detector**: Identifies `defunct` processes (e.g., `zypak-sandbox`) to ensure system hygiene.
- **Disk I/O Analysis**: Detects "Chef/Pantry" bottlenecks using I/O Wait metrics.
- **Network Throughput**: Live download/upload speed tracking in KB/s.
- **Kernel Insights**: Lists active kernel threads and system services.
- **Power Tracking**: Monitors battery percentage and charging status.

## 🛠️ Architecture
The project uses a modular **Engine-UI** split:
- `src/sensors.py`: A stateful Python class for high-performance hardware interrogation using `psutil`.
- `main.py`: A terminal-based dashboard for real-time monitoring.
- `gui.py`: (In Development) A professional PyQt6-based desktop interface.

## 📦 Requirements
- Python 3.12+
- `psutil`
- `PyQt6` (for GUI mode)

## 🔧 Installation
1. Clone the repository:
   ```bash
   git clone [https://github.com/yalin999/LinuxHealth.git](https://github.com/yalin999/LinuxHealth.git)
   cd LinuxHealth