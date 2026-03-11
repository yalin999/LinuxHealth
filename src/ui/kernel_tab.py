"""
@file kernel_tab.py
@brief UI container for kernel-space process monitoring.
@project Linux Health Monitor Pro
@license MIT
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout
from src.components.processes.kernel.kernel_widget import KernelWidget

class KernelTab(QWidget):
    """
    @class KernelTab
    @brief A tabbed view dedicated to Linux kernel thread telemetry.
    @details Acts as a high-level container for the KernelWidget, providing 
             an isolated interface for process-specific data updates.
    """

    def __init__(self):
        """
        @brief Initializes the tab and embeds the kernel list view.
        """
        super().__init__()
        layout = QVBoxLayout(self)
        
        # Instantiate the specialized list widget
        self.kernel_view = KernelWidget()
        layout.addWidget(self.kernel_view)

    def update_ui(self, data: list):
        """
        @brief Receives and delegates kernel thread data.
        @param data List of thread dictionaries from the GlobalWorker.
        @details Implementation passes the data directly to the child view 
                 to maintain strict separation of concerns.
        """
        # Ensure data is valid before attempting a display update
        if isinstance(data, list):
            self.kernel_view.update_display(data)