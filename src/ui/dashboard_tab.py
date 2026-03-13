"""
@file dashboard_tab.py
@brief Main visualization container for system health metrics.
@project Linux Health Monitor Pro
@dependencies PyQt6
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea
from src.components.cpu.cpu_widget import CPUWidget
from src.components.ram.ram_widget import RAMWidget
from src.components.disk.disk_widget import DiskWidget
from src.components.network.network_widget import NetworkWidget

class DashboardTab(QWidget):
    """
    @class DashboardTab
    @brief Aggregates and manages hardware-specific visualization widgets.
    @details Implements a scrollable layout to host multiple telemetry 
             graphs, ensuring the UI is scalable for future sensor expansions.
    """

    def __init__(self):
        """
        @brief Initializes the tab layout and child widgets.
        @details Sets up a QScrollArea to contain the CPU, RAM, Disk and Network 
                 instrumentation panels.
        """
        super().__init__()
        layout = QVBoxLayout(self)
        
        # Scroll Area configuration to handle vertical overflow
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        
        # Content container for specific sensor widgets
        content = QWidget()
        self.content_layout = QVBoxLayout(content)
        
        # Instantiate instrumentation widgets
        self.cpu_w = CPUWidget()
        self.ram_w = RAMWidget()
        self.disk_w = DiskWidget()
        self.net_w = NetworkWidget()
        
        # Add widgets to the internal vertical layout
        self.content_layout.addWidget(self.cpu_w)
        self.content_layout.addWidget(self.ram_w)
        self.content_layout.addWidget(self.disk_w)
        self.content_layout.addWidget(self.net_w)
        
        # Finalize scroll area setup
        scroll.setWidget(content)
        layout.addWidget(scroll)

    def update_ui(self, data: dict):
        """
        @brief Propagates telemetry data to individual hardware widgets.
        @param data Unified dictionary containing nested sensor readings.
        @details Maps the incoming telemetry packet keys to the corresponding 
                 widget display methods.
        """
        # Distribute CPU metrics
        self.cpu_w.update_display(
            data['cpu']['usage'], 
            data['cpu']['speed']
        )
        
        # Distribute RAM metrics
        self.ram_w.update_display(
            data['ram']['percent'], 
            data['ram']['used'], 
            data['ram']['total']
        )
        
        # Distribute Disk metrics
        self.disk_w.update_display(
            data['disk']['read'], 
            data['disk']['write'], 
        )
        # Distribute Network metrics
        self.net_w.update_display(
            data['net']['down'], 
            data['net']['up']
        )