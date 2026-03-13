"""
@file process_widget.py
@brief UI component for listing top resource-consuming user processes.
@project Linux Health Monitor Pro
@dependencies PyQt6
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QTableWidget, 
                             QTableWidgetItem, QHeaderView, QAbstractItemView)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont
from src.config import MAX_PROCESSES

class ProcessWidget(QWidget):
    """
    @class ProcessWidget
    @brief Displays a high-performance table of top process consumers.
    @details Utilizes a QTableWidget with optimized updates to show 
             real-time CPU and RAM usage for user-space applications.
    """

    def __init__(self):
        """
        @brief Initializes the table structure and styling.
        """
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Header Label
        self.title = QLabel("Top Resource Consumers")
        self.title.setStyleSheet("font-weight: bold; font-size: 14px; color: #3498db;")
        self.layout.addWidget(self.title)

        # Table Setup
        self.table = QTableWidget(MAX_PROCESSES, 4)  # MAX_PROCESSES rows, 4 columns
        self.table.setHorizontalHeaderLabels(["PID", "Process Name", "CPU %", "RAM (MB)"])
        self._configure_table()
        
        self.layout.addWidget(self.table)

    def _configure_table(self):
        """
        @brief Applies professional styling to the table.
        """
        # Set column stretching: Name takes the most space
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(2, 80)
        self.table.setColumnWidth(3, 100)

        # General Table Styling
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: transparent;
                gridline-color: #333;
                border: none;
            }
            QHeaderView::section {
                background-color: #2c3e50;
                color: white;
                padding: 4px;
                border: 1px solid #1a252f;
            }
        """)

    def update_display(self, process_list: list):
        """
        @brief Refreshes the table content with new telemetry data.
        @param process_list List of dicts containing pid, name, cpu, and ram.
        """
        # Iterate through the list and update rows
        for row, proc in enumerate(process_list):
            if row >= MAX_PROCESSES: break # Safety break

            # PID (Centered)
            self._set_item(row, 0, str(proc['pid']), alignment=Qt.AlignmentFlag.AlignCenter)
            
            # Name
            self._set_item(row, 1, proc['name'])
            
            # CPU % (With color clue)
            cpu_item = self._set_item(row, 2, f"{proc['cpu']}%", alignment=Qt.AlignmentFlag.AlignRight)
            
            # RAM MB (With color clue)
            ram_item = self._set_item(row, 3, f"{proc['ram']:.1f}", alignment=Qt.AlignmentFlag.AlignRight)

    def _set_item(self, row, col, text, alignment=None):
        """
        @brief Helper to create or update a table item efficiently.
        """
        item = self.table.item(row, col)
        if not item:
            item = QTableWidgetItem()
            item.setFont(QFont("Monospace", 9))
            self.table.setItem(row, col, item)
        
        item.setText(text)
        if alignment:
            item.setTextAlignment(alignment)
        return item