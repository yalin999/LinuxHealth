"""
@file cpu_widget.py
@brief UI component for visualizing CPU performance.
@project Linux Health Monitor Pro
@dependencies pyqtgraph, PyQt6
"""

import pyqtgraph as pg
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class CPUWidget(QWidget):
    """
    @class CPUWidget
    @brief A graphical widget displaying real-time CPU utilization.
    @details Features a dynamic line graph using pyqtgraph and a textual 
             overlay showing percentage and clock frequency.
    """

    def __init__(self):
        """
        @brief Initializes UI components and graph settings.
        @details Sets up a 60-point sliding window history for the utilization graph.
        """
        super().__init__()
        # Internal state: 60-second sliding window of utilization data
        self.history = [0] * 60
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 5, 0, 5)

        # Telemetry Text Overlay
        self.label = QLabel("CPU: Loading...")
        self.label.setStyleSheet("font-family: 'Monospace'; font-weight: bold;")
        
        # Graph Configuration
        self.graph = pg.PlotWidget()
        self._configure_graph()
        
        # Data Curve Initialization
        pen = pg.mkPen(color=(0, 255, 0), width=2)
        self.curve = self.graph.plot(self.history, pen=pen)
        
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.graph)

    def _configure_graph(self):
        """
        @brief Internal helper to style the pyqtgraph PlotWidget.
        @details Disables user interaction and hides axes to maintain 
                 a clean dashboard aesthetic.
        """
        self.graph.setBackground('k')  # Black background
        self.graph.setFixedHeight(150)
        self.graph.setYRange(0, 100)
        self.graph.getAxis('bottom').hide()
        self.graph.getViewBox().setMouseEnabled(x=False, y=False)
        self.graph.hideButtons()

    def update_display(self, usage: float, speed: float):
        """
        @brief Updates the visual state of the widget.
        @param usage Current CPU load as a percentage (0.0 - 100.0).
        @param speed Current CPU clock speed in GHz.
        @details Shifts the history buffer and redraws the graph curve.
        """
        # Update textual information
        self.label.setText(f"CPU: {usage}% @ {speed:.2f} GHz")
        
        # Maintain sliding window history
        self.history.pop(0)
        self.history.append(usage)
        
        # Atomic update of the graph data
        self.curve.setData(self.history)