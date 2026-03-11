"""
@file network_widget.py
@brief UI component for visualizing dual-stream network throughput.
@project Linux Health Monitor Pro
@dependencies pyqtgraph, PyQt6
"""

import pyqtgraph as pg
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QColor

class NetworkWidget(QWidget):
    """
    @class NetworkWidget
    @brief A dual-stream graph widget for monitoring ingress and egress traffic.
    @details Implements a time-series visualization using two distinct curves
             (Magenta for Download, Cyan for Upload) with an auto-scaling Y-axis.
    """

    def __init__(self):
        """
        @brief Initializes UI components and history buffers.
        @details Sets up two 60-point sliding window buffers to track network activity.
        """
        super().__init__()
        
        # Internal state: Separate buffers for Inbound and Outbound data
        self.down_history = [0.0] * 60
        self.up_history = [0.0] * 60
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 5, 0, 5)

        # Telemetry Text Overlay using HTML for color-coded legibility
        self.label = QLabel("Net: ⇩ 0.0 KB/s | ⇧ 0.0 KB/s")
        self.label.setStyleSheet("font-family: 'Monospace'; font-weight: bold;")
        
        self.graph = pg.PlotWidget()
        self._configure_graph()
        
        # --- Visual Encoding Strategy ---
        
        # Download (Ingress): Magenta curve with semi-transparent area fill
        self.down_curve = self.graph.plot(
            self.down_history, 
            pen=pg.mkPen(color='#FF00FF', width=2),
            fillLevel=0,
            brush=(255, 0, 255, 30)  # Alpha 30 for subtle contrast
        )
        
        # Upload (Egress): Cyan curve, sharp and distinct
        self.up_curve = self.graph.plot(
            self.up_history, 
            pen=pg.mkPen(color='#00FFFF', width=1.5)
        )
        
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.graph)

    def _configure_graph(self):
        """
        @brief Internal helper to style the pyqtgraph PlotWidget.
        @note Y-axis auto-range is enabled to allow the UI to scale between
              low-activity (KB/s) and high-activity (MB/s) states.
        """
        self.graph.setBackground('k')
        self.graph.setFixedHeight(150)
        self.graph.enableAutoRange(axis='y', enable=True)
        self.graph.getAxis('bottom').hide()
        self.graph.getViewBox().setMouseEnabled(x=False, y=False)
        self.graph.hideButtons()

    def update_display(self, down: float, up: float):
        """
        @brief Refreshes the widget with the latest network samples.
        @param down Current download rate in KB/s.
        @param up Current upload rate in KB/s.
        @details Updates the HTML-formatted label and shifts history buffers
                 for both data streams simultaneously.
        """
        # Update text with color clues to match the graph curves
        self.label.setText(
            f'Net: <span style="color:#FF00FF;">⇩ {down:>6.1f} KB/s</span> | '
            f'<span style="color:#00FFFF;">⇧ {up:>6.1f} KB/s</span>'
        )
        
        # Shift sliding windows
        self.down_history.pop(0)
        self.down_history.append(down)
        
        self.up_history.pop(0)
        self.up_history.append(up)
        
        # Push new data to the GPU via pyqtgraph
        self.down_curve.setData(self.down_history)
        self.up_curve.setData(self.up_history)