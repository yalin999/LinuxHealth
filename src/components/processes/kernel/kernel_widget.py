"""
@file kernel_widget.py
@brief UI component for listing active Linux kernel threads.
@project Linux Health Monitor Pro
@dependencies PyQt6
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget
from PyQt6.QtCore import Qt

class KernelWidget(QWidget):
    """
    @class KernelWidget
    @brief A dedicated list view for kernel-space processes.
    @details Displays a scrollable list of kernel threads with formatted 
             PID alignment and status indicators, styled with a high-contrast 
             terminal aesthetic.
    """

    def __init__(self):
        """
        @brief Initializes the widget layout and static UI elements.
        @details Applies a global dark-mode stylesheet to the list container.
        """
        super().__init__()
        layout = QVBoxLayout(self)
        
        # Header Label for the list section
        self.label = QLabel("Active Kernel Threads")
        self.label.setStyleSheet("font-weight: bold; color: #00FF00; margin-bottom: 5px;")
        
        # List Container with monospace formatting for tabular alignment
        self.list_widget = QListWidget()
        self._apply_styles()
        
        layout.addWidget(self.label)
        layout.addWidget(self.list_widget)

    def _apply_styles(self):
        """
        @brief Internal helper to encapsulate CSS-like styling.
        @details Sets a dark background (#121212) and terminal green text (#00FF00).
        """
        self.list_widget.setStyleSheet("""
            QListWidget {
                background-color: #121212;
                border: 1px solid #333;
                color: #00FF00;
                font-family: 'Monospace';
                font-size: 12px;
            }
            QListWidget::item:selected {
                background: #333; /* Visual feedback on selection */
            }
        """)

    def update_display(self, threads: list):
        """
        @brief Synchronizes the UI list with current system thread data.
        @param threads A list of dictionaries containing 'pid', 'name', and 'status'.
        @details Implementation uses a 'Clear-and-Rebuild' strategy to ensure 
                 the UI accurately reflects the transient nature of kernel threads.
        """
        # Atomically clear the previous sampling period's data
        self.list_widget.clear()
        
        if not threads:
            self.list_widget.addItem("Searching for kernel threads...")
            return

        for thread in threads:
            # PID Alignment Logic:
            # We rjust to 5 characters to ensure columns line up regardless of PID magnitude.
            # Example: [   2] vs [12345]
            formatted_pid = str(thread['pid']).rjust(5)
            line = f"[{formatted_pid}]  {thread['name']} ({thread['status']})"
            
            self.list_widget.addItem(line)



