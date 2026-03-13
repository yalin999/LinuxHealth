"""
@file process_tab.py
@brief Management interface for user-space process telemetry.
@project Linux Health Monitor Pro
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from src.components.processes.user.process_widget import ProcessWidget

class ProcessTab(QWidget):
    """
    @class ProcessTab
    @brief The primary interface for monitoring and sorting system processes.
    @details Houses the ProcessWidget and provides controls for dynamic 
             sorting via the GlobalWorker telemetry stream.
    """

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        
        # --- Control Toolbar ---
        self.toolbar = QHBoxLayout()
        
        self.status_label = QLabel("Sort by:")
        self.status_label.setStyleSheet("font-weight: bold;")
        
        self.btn_sort_cpu = QPushButton("Highest CPU")
        self.btn_sort_ram = QPushButton("Highest RAM")
        
        # Style the buttons to look professional
        btn_style = "padding: 5px 15px; background-color: #2c3e50; color: white; border-radius: 4px;"
        self.btn_sort_cpu.setStyleSheet(btn_style)
        self.btn_sort_ram.setStyleSheet(btn_style)

        self.toolbar.addWidget(self.status_label)
        self.toolbar.addWidget(self.btn_sort_cpu)
        self.toolbar.addWidget(self.btn_sort_ram)
        self.toolbar.addStretch() # Pushes buttons to the left
        
        self.layout.addLayout(self.toolbar)

        # --- The Process Table ---
        self.process_widget = ProcessWidget()
        self.layout.addWidget(self.process_widget)
        
        # State tracking: Default sort
        self.current_sort = "cpu"
        
        # Connect button signals
        self.btn_sort_cpu.clicked.connect(lambda: self.set_sorting("cpu"))
        self.btn_sort_ram.clicked.connect(lambda: self.set_sorting("ram"))

    def set_sorting(self, sort_type: str):
        """
        @brief Updates the internal sorting state and UI feedback.
        """
        self.current_sort = sort_type
        # Update button colors to show which is active
        if sort_type == "cpu":
            self.btn_sort_cpu.setStyleSheet("background-color: #3498db; color: white; border-radius: 4px;")
            self.btn_sort_ram.setStyleSheet("background-color: #2c3e50; color: white; border-radius: 4px;")
        else:
            self.btn_sort_ram.setStyleSheet("background-color: #3498db; color: white; border-radius: 4px;")
            self.btn_sort_cpu.setStyleSheet("background-color: #2c3e50; color: white; border-radius: 4px;")

    def update_ui(self, process_data: list):
        """
        @brief Passes the telemetry packet to the child table widget.
        """
        self.process_widget.update_display(process_data)