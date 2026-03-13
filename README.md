# 🐧 Linux Health Monitor Pro

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Framework: PyQt6](https://img.shields.io/badge/UI-PyQt6-green.svg)](https://www.riverbankcomputing.com/software/pyqt/)

A high-performance, multithreaded system telemetry suite designed for **Linux-based distributions**. This application implements a decoupled architecture to ensure maximum UI responsiveness and resource efficiency while providing deep visibility into hardware, user-space applications, and kernel-level operations.

---

## 🏗️ Architectural Design (ISO/IEC 25010)

The project follows a **Modular Component Architecture**, ensuring that hardware logic is strictly separated from the presentation layer:

* **Core Orchestrator (`src/core/`)**: Manages the `GlobalWorker` thread, handling asynchronous telemetry sampling at 1Hz to prevent GUI blocking.
* **Hardware Abstraction Layer (`src/components/`)**: Discrete sensor engines for CPU, RAM, Disk, and Network that interface with the Linux kernel via `psutil`.
* **Centralized Configuration (`src/config.py`)**: Global constants (e.g., `MAX_PROCESSES`) ensuring consistency across sensors and UI widgets.
* **UI Layer (`src/ui/`)**: A tabbed interface designed for high-density data visualization using `pyqtgraph` for GPU-accelerated plotting and `QTableWidget` for process tracking.

---

## 📊 Feature Specifications

| Component | Metrics Tracked | Visual Encoding |
| :--- | :--- | :--- |
| **CPU** | Utilization (%) & Clock Speed (GHz) | Green Trendline (0-100% scale) |
| **RAM** | Used/Total GB & Virtual Memory % | Blue Trendline (0-100% scale) |
| **Disk** | Read (R) & Write (W) in MB/s | Dual-stream (Yellow/Orange) with Area Fill |
| **Network** | Ingress (⇩) & Egress (⇧) in KB/s | Dual-stream (Magenta/Cyan) with Area Fill |
| **Processes** | Top Consumers (PID, Name, CPU, RAM) | **Dynamic Sorting (CPU/RAM Toggle)** |
| **Kernel** | PID 2 (`kthreadd`) Child Processes | Monospaced Alignment & Status Tracking |

---

## 🛠️ Installation & Deployment

### Prerequisites
* **Operating System**: Linux (Fedora, Ubuntu, Arch, etc.)
* **Python**: v3.12 or higher recommended.
* **Dependencies**: Listed in `requirements.txt`.

### Setup Instructions
1.  **Clone the Repository**:
    ```bash
    git clone [https://github.com/yalin999/LinuxHealth.git](https://github.com/yalin999/LinuxHealth.git)
    cd LinuxHealth
    ```

2.  **Initialize Virtual Environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Launch the Application**:
    ```bash
    python3 main.py
    ```

---

## 📁 Project Structure

```text
.
├── main.py                 # Application Entry Point
├── requirements.txt        # Dependency Manifest
├── .gitignore              # Version Control Exclusions
├── src/
│   ├── config.py           # Global Constants & Thresholds
│   ├── core/
│   │   └── worker.py       # Asynchronous Telemetry Engine
│   ├── ui/
│   │   ├── dashboard_tab.py# Hardware Telemetry View
│   │   ├── process_tab.py  # User-Space Process Monitor
│   │   └── kernel_tab.py   # Kernel Thread View
│   └── components/
│       ├── cpu/            # CPU Sensor & Widget
│       ├── disk/           # Disk Sensor & Widget
│       ├── ram/            # RAM Sensor & Widget
│       ├── network/        # Network Sensor & Widget
│       └── processes/      
│           ├── kernel/     # Kernel Thread Logic
│           └── user/       # Top Consumer Sensor & Widget
