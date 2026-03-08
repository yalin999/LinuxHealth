import sys
from src.sensors import Sensors
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, 
                             QWidget, QListWidget, QTabWidget)
from PyQt6.QtCore import QThread, pyqtSignal

class SensorWorker(QThread):
    """
    /**
     * @brief      Multi-rate Asynchronous Telemetry Engine.
     * @details    Complies with ISO/IEC 25010 Resource Utilization by staggering 
     * I/O intensive kernel scans from real-time metrics.
     */
    """
    data_received = pyqtSignal(dict)

    def __init__(self, sensors):
        super().__init__()
        self.sensors = sensors

    def run(self):
        """
        @process    Execution loop for background data acquisition.
        @logic      Implements a modulo-based counter to separate sampling frequencies.
        """
        kernel_cache = self.sensors.get_kernel_processes()
        count = 1 
        while True:
            try:
                data = {
                    "cpu_usage": self.sensors.get_cpu_usage(),
                    "cpu_speed": self.sensors.get_cpu_speed(),
                    "ram": self.sensors.get_ram_details(),
                    "net": self.sensors.get_network_speed(),
                    "disk": self.sensors.get_disk_status(),
                    "uptime": self.sensors.get_uptime(),
                    "kernel_procs": kernel_cache 
                }
                
                # Update high-latency data every 5 cycles (5 seconds)
                if count % 5 == 0:
                    kernel_cache = self.sensors.get_kernel_processes()
                    data["kernel_procs"] = kernel_cache
                
                self.data_received.emit(data)
                count += 1
            except Exception as e:
                # Error logging supports ISO/IEC 25010 Reliability
                print(f"Sensor Error: {e}")
            self.msleep(1000)

class HealthWindow(QMainWindow):
    """
    /**
     * @brief      Main Presentation Layer with Tabbed Architecture.
     * @details    Implements ISO/IEC 25010 Usability through logical 
     * separation of Dashboard and System Internals.
     */
    """
    def __init__(self):
        super().__init__()
        self.sensors = Sensors()
        self.last_kernel_data = [] # Data state tracking for Smart Refresh
        
        self.setWindowTitle("Linux Health Monitor Pro")
        self.resize(500, 450)

        # ISO/IEC 12207 Componentization: Using a Tab Widget for Modularity
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # --- Dashboard Tab Initialization ---
        self.dash_tab = QWidget()
        dash_layout = QVBoxLayout()
        
        self.cpu_label = QLabel("CPU: Loading...")
        self.ram_label = QLabel("RAM: Loading...")
        self.disk_label = QLabel("Disk Status: Loading...")
        self.net_label = QLabel("Network: Loading...")
        self.uptime_label = QLabel("Uptime: Loading...")
        
        dash_layout.addWidget(self.cpu_label)
        dash_layout.addWidget(self.ram_label)
        dash_layout.addWidget(self.disk_label)
        dash_layout.addWidget(self.net_label)
        dash_layout.addWidget(self.uptime_label)
        self.dash_tab.setLayout(dash_layout)

        # --- Kernel Threads Tab Initialization ---
        self.kernel_tab = QWidget()
        kernel_layout = QVBoxLayout()
        self.kernel_list = QListWidget()
        kernel_layout.addWidget(self.kernel_list)
        self.kernel_tab.setLayout(kernel_layout)

        # UI Hierarchy Construction
        self.tabs.addTab(self.dash_tab, "Dashboard")
        self.tabs.addTab(self.kernel_tab, "Kernel Threads")

        # Async process management
        self.worker = SensorWorker(self.sensors)
        self.worker.data_received.connect(self.display_data)
        self.worker.start()

    def display_data(self, data):
        """
        @brief   UI Synchronizer.
        @details Processes incoming telemetry and applies Smart Refresh logic 
                 to minimize GUI overhead.
        """
        # Data Transformation (Model to View)
        cpu_text = f"CPU: {data['cpu_usage']}% @ {data['cpu_speed']:.2f} GHz"
        self.cpu_label.setText(cpu_text)
        
        ram = data['ram']
        self.ram_label.setText(f"RAM: {ram['used']} / {ram['total']} GB ({ram['percent']}%)")
        self.disk_label.setText(f"Disk Status: {data['disk']}")
        self.net_label.setText(f"Net: ↓ {data['net']['down']} KB/s | ↑ {data['net']['up']} KB/s")
        self.uptime_label.setText(f"Uptime: {data['uptime']}")

        # Conditional Update Logic (Smart Refresh)
        new_kernel_data = data.get('kernel_procs', [])
        if new_kernel_data != self.last_kernel_data:
            self.kernel_list.clear()
            for proc in new_kernel_data:
                self.kernel_list.addItem(f"[{proc['pid']}] {proc['name']} ({proc['status']})")
            self.last_kernel_data = new_kernel_data

if __name__ == "__main__":
    # Application Entry following ISO/IEC 12207 implementation standards
    app = QApplication(sys.argv)
    window = HealthWindow()
    window.show()
    sys.exit(app.exec())