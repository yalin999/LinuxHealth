# 🐧 Linux Health Monitor Pro (v2.1)

A high-performance, multithreaded system telemetry suite designed for **Linux-based distributions** (Fedora, Ubuntu, Arch, Debian, etc.). This application implements a decoupled architecture to ensure maximum UI responsiveness and resource efficiency while providing deep visibility into kernel-level operations.

---

## 🏗️ Architectural Overview

Following **ISO/IEC 12207** (Software Life Cycle) and **ISO/IEC 25010** (System Quality) standards, the monitor is built on a modular, three-tier structure:

1. **Hardware Abstraction Layer (`src/sensors.py`)**: A distro-agnostic engine that interfaces with the Linux kernel's `/proc` filesystem via `psutil`.
2. **Asynchronous Telemetry Engine (`SensorWorker`)**: A dedicated `QThread` that manages data acquisition independently of the UI. It utilizes **Staggered Sampling** (1Hz for hardware metrics, 0.2Hz for kernel discovery) to optimize CPU utilization.
3. **Presentation Layer (`HealthWindow`)**: A PyQt6-based interface utilizing a **Tabbed Architecture** and **Smart Refresh** logic to minimize GPU draw calls and enhance user operability.

---

## 🚀 Quality Characteristics (ISO/IEC 25010)

| Characteristic | Implementation Detail |
| --- | --- |
| **Performance Efficiency** | Staggered sampling: Real-time hardware stats vs. heavy kernel scans. |
| **Resource Utilization** | **Smart Refresh**: GUI lists only redraw when the underlying data state changes. |
| **Maintainability** | Decoupled Signal/Slot architecture allows for modular sensor expansion. |
| **Usability** | Tabbed interface separates high-level KPIs from technical process lists. |
| **Portability** | Distro-agnostic logic tested across the Linux kernel ecosystem (v2.6+). |

---

## 🛠️ Installation & Setup

### Prerequisites

* **Linux OS**: Any distribution with a modern Linux Kernel.
* **Python**: Version 3.12 or higher.
* **Privileges**: Standard user (some kernel thread metadata may require elevated permissions).

### Deployment

1. **Clone the Repository**:
```bash
git clone <your-repository-url>
cd LinuxHealth

```


2. **Setup Virtual Environment**:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```


3. **Launch Application**:
```bash
python3 gui.py

```



---

## 📊 Feature Specifications

* **Dashboard Tab**:
* Real-time CPU usage and frequency ($GHz$).
* RAM occupancy (Used/Total GB) with dynamic percentage.
* Instantaneous Network Bitrate (Inbound/Outbound).
* Disk I/O Wait State analysis (Smooth/Busy/Bottleneck).


* **Kernel Threads Tab**:
* Automated discovery of ~200 system threads.
* PID, Name, and Status tracking.
* Exclusion-based filtering of user-space command lines for pure kernel visibility.



---

## 📅 Development Roadmap (ISO/IEC 12207)

* ✅ **Phase 1**: Core sensor development and CLI prototyping.
* ✅ **Phase 2**: PyQt6 GUI integration and Layout Management.
* ✅ **Phase 3**: Multithreading implementation (Asynchronous Worker).
* ✅ **Phase 4**: Performance Optimization (Smart Refresh & Staggered Sampling).
* ⏳ **Phase 5**: Predictive Health Analytics and Alerting System.

