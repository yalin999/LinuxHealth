"""
@file disk_widget.py
@brief UI component for visualizing real-time Disk I/O throughput.
@project Linux Health Monitor Pro
@dependencies pyqtgraph, PyQt6
"""

import pyqtgraph as pg
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class DiskWidget(QWidget):
    """
    @class DiskWidget
    @brief A dual-stream graph widget for monitoring disk read and write speeds.
    @details Visualizes hardware throughput using Yellow (Read) and Orange (Write) 
             curves. Optimized for real-time MB/s telemetry.
    """

    def __init__(self):
        """
        @brief Initializes UI components and 60-point history buffers.
        """
        super().__init__()
        
        # Internal state: Tracking history for the last 60 samples
        self.read_history = [0.0] * 60
        self.write_history = [0.0] * 60
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 5, 0, 5)

        # Telemetry Text Overlay using HTML for color-coded legibility
        self.label = QLabel("Disk: R: 0.00 MB/s | W: 0.00 MB/s")
        self.label.setStyleSheet("font-family: 'Monospace'; font-weight: bold;")
        
        self.graph = pg.PlotWidget()
        self._configure_graph()
        
        # --- Visual Encoding Strategy ---
        
        # Read Throughput: Gold/Yellow curve with subtle area fill
        self.read_curve = self.graph.plot(
            self.read_history, 
            pen=pg.mkPen(color='#F1C40F', width=2),
            fillLevel=0,
            brush=(241, 196, 15, 30)  # Alpha 30 for depth
        )
        
        # Write Throughput: Orange curve, distinct and sharp
        self.write_curve = self.graph.plot(
            self.write_history, 
            pen=pg.mkPen(color='#E67E22', width=1.5)
        )
        
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.graph)

    def _configure_graph(self):
        """
        @brief Internal helper to style the pyqtgraph PlotWidget.
        """
        self.graph.setBackground('k')
        self.graph.setFixedHeight(150)
        self.graph.enableAutoRange(axis='y', enable=True)
        self.graph.getAxis('bottom').hide()
        self.graph.getViewBox().setMouseEnabled(x=False, y=False)
        self.graph.hideButtons()

    def update_display(self, read: float, write: float):
        """
        @brief Refreshes the widget with the latest Disk I/O samples.
        @param read Current read rate in MB/s.
        @param write Current write rate in MB/s.
        """
        # Update text with color-coded spans to match the curves
        # Note: Using :>7.2f to handle decimal precision for MB/s
        self.label.setText(
            f'Disk: <span style="color:#F1C40F;">R: {read:>7.2f} MB/s</span> | '
            f'<span style="color:#E67E22;">W: {write:>7.2f} MB/s</span>'
        )
        
        # Shift sliding windows
        self.read_history.pop(0)
        self.read_history.append(read)
        
        self.write_history.pop(0)
        self.write_history.append(write)
        
        # Update GPU-bound curves
        self.read_curve.setData(self.read_history)
        self.write_curve.setData(self.write_history)