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
        self.resize(500, 700)

        # Tab Navigation Setup
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # UI Component Initialization
        self.dashboard = DashboardTab()
        self.kernel_tab = KernelTab()
        
        # Add production-ready tabs only
        self.tabs.addTab(self.dashboard, "Dashboard")
        self.tabs.addTab(self.kernel_tab, "Kernel Threads")

        # Telemetry Worker Lifecycle Management
        self.worker = GlobalWorker()
        
        # Signal-Slot Connection: Routing worker data to the distributor
        self.worker.data_received.connect(self.update_all_tabs)
        
        self.worker.start()

    def update_all_tabs(self, data: dict):
        """
        @brief Global data distributor (Signal Handler).
        @param data The telemetry packet received from GlobalWorker.
        @details Distributes specific subsets of the telemetry packet to 
                 their respective tab views.
        """
        try:
            # Update the primary performance dashboard
            self.dashboard.update_ui(data)
            
            # Update the kernel process list if data is present
            if 'kernel' in data:
                self.kernel_tab.update_ui(data['kernel'])
                
        except Exception as e:
            logging.error(f"UI Update Distribution Error: {e}")

    def closeEvent(self, event):
        """
        @brief Overrides the default close event to ensure a clean exit.
        @details Signals the GlobalWorker to stop its loop and waits for 
                 the thread to terminate before closing the application.
        """
        logging.info("Shutting down telemetry worker...")
        self.worker.stop() # Uses the custom stop() method we added to GlobalWorker
        event.accept()

if __name__ == "__main__":
    # Configure global logging for the application session
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    app = QApplication(sys.argv)
    
    # Instance creation and display
    window = MainWindow()
    window.show()
    
    # Execute application event loop
    sys.exit(app.exec())