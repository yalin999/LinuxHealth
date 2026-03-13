"""
@file main.py
@brief Application entry point and UI-Worker orchestrator.
@project Linux Health Monitor Pro
@version 1.0.0
@license MIT
"""

import sys
import logging
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget
from PyQt6.QtGui import QIcon

from src.ui.dashboard_tab import DashboardTab
from src.ui.kernel_tab import KernelTab
from src.ui.process_tab import ProcessTab
from src.core.worker import GlobalWorker

class MainWindow(QMainWindow):
    """
    @class MainWindow
    @brief The primary window for the Linux Health Monitor Pro.
    @details Manages the lifecycle of the background telemetry worker and 
             coordinates data distribution between the worker and UI tabs.
    """

    def __init__(self):
        """
        @brief Initializes the main window, UI components, and worker thread.
        """
        super().__init__()
        
        # Window Configuration
        self.setWindowTitle("Linux Health Monitor Pro")
        self.resize(900, 900)  # Increased size slightly for better table visibility

        # Tab Navigation Setup
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # UI Component Initialization
        self.dashboard = DashboardTab()
        self.kernel_tab = KernelTab()
        self.process_monitor = ProcessTab()
        
        # Add production-ready tabs
        self.tabs.addTab(self.dashboard, "Dashboard")
        self.tabs.addTab(self.process_monitor, "Process Monitor")
        self.tabs.addTab(self.kernel_tab, "Kernel Threads")

        # Telemetry Worker Lifecycle Management
        self.worker = GlobalWorker()
        
        # --- Signal-Slot Connections ---
        
        # 1. Routing worker data to the distributor
        self.worker.data_received.connect(self.update_all_tabs)
        
        # 2. Connecting Process sorting buttons to Worker logic
        # These lambda functions tell the worker which sorting mode to use
        self.process_monitor.btn_sort_cpu.clicked.connect(
            lambda: self.worker.set_process_sort_mode("cpu")
        )
        self.process_monitor.btn_sort_ram.clicked.connect(
            lambda: self.worker.set_process_sort_mode("ram")
        )
        
        self.worker.start()

    def update_all_tabs(self, data: dict):
        """
        @brief Global data distributor (Signal Handler).
        @param data The telemetry packet received from GlobalWorker.
        """
        try:
            # Update hardware sensors (CPU, RAM, Net, Disk)
            self.dashboard.update_ui(data)
            
            # Update the User Process list
            if 'user_processes' in data:
                self.process_monitor.update_ui(data['user_processes'])
            
            # Update the Kernel thread list
            if 'kernel' in data:
                self.kernel_tab.update_ui(data['kernel'])
                
        except Exception as e:
            logging.error(f"UI Update Distribution Error: {e}")

    def closeEvent(self, event):
        """
        @brief Overrides the default close event to ensure a clean exit.
        """
        logging.info("Shutting down telemetry worker...")
        self.worker.stop() 
        event.accept()

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())