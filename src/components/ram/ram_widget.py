"""
@file ram_widget.py
@brief UI component for visualizing RAM utilization.
@project Linux Health Monitor Pro
@dependencies pyqtgraph, PyQt6
"""

import pyqtgraph as pg
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class RAMWidget(QWidget):
    """
    @class RAMWidget
    @brief A graphical widget displaying real-time Memory (RAM) statistics.
    @details Provides a time-series line graph of memory load percentage 
             and a header label for absolute volumetric metrics (Used/Total).
    """

    def __init__(self):
        """
        @brief Initializes UI components and history buffers.
        @details Sets up a 60-second sliding window for memory percentage tracking.
        """
        super().__init__()
        
        # Internal state: Sliding window buffer for utilization percentage
        self.history = [0.0] * 60
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 5, 0, 5)

        # Telemetry Text Overlay
        self.label = QLabel("RAM: Loading...")
        self.label.setStyleSheet("font-family: 'Monospace'; font-weight: bold;")
        
        # Graph Configuration
        self.graph = pg.PlotWidget()
        self._configure_graph()
        
        # Visual Encoding: Blue line for RAM utilization
        # (0, 150, 255) provides a distinct contrast to CPU (Green) and Net (Magenta/Cyan)
        pen = pg.mkPen(color=(0, 150, 255), width=2)
        self.curve = self.graph.plot(self.history, pen=pen)
        
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.graph)

    def _configure_graph(self):
        """
        @brief Internal helper to style the pyqtgraph PlotWidget.
        @note Y-axis is fixed to 0-100% as RAM utilization is a bounded metric.
        """
        self.graph.setBackground('k')
        self.graph.setFixedHeight(150)
        self.graph.setYRange(0, 100)
        self.graph.getAxis('bottom').hide()
        self.graph.getViewBox().setMouseEnabled(x=False, y=False)
        self.graph.hideButtons()

    def update_display(self, percent: float, used: float, total: float):
        """
        @brief Updates the visual state with the latest memory samples.
        @param percent Current memory load as a percentage (0.0 - 100.0).
        @param used Current memory consumption in Gigabytes (GB).
        @param total Total system memory capacity in Gigabytes (GB).
        @details Updates the text label and shifts the history buffer 
                 before redrawing the utilization curve.
        """
        # Professional formatting: Ensures fixed-width appearance for stability
        self.label.setText(f"RAM: {used:>4.1f} / {total:>4.1f} GB ({percent:>5.1f}%)")
        
        # Maintain time-series history
        self.history.pop(0)
        self.history.append(percent)
        
        # Refresh the graph curve data
        self.curve.setData(self.history)