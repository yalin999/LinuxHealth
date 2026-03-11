"""
@file worker.py
@brief Centralized background telemetry producer.
@project Linux Health Monitor Pro
@dependencies PyQt6, psutil
"""

import logging
from PyQt6.QtCore import QThread, pyqtSignal
from src.components.cpu.cpu_sensor import CPUSensor
from src.components.ram.ram_sensor import RAMSensor
from src.components.network.network_sensor import NetworkSensor
from src.components.processes.kernel.kernel_sensor import KernelSensor

class GlobalWorker(QThread):
    """
    @class GlobalWorker
    @brief Orchestrates hardware sampling on a background thread.
    @details Prevents GUI freezing by executing blocking I/O (sensor reads) 
             in a separate execution context. Aggregates data from all 
             sub-sensors into a unified telemetry packet.
    """

    # Signal emitted every sampling interval (1Hz)
    # @param dict A telemetry packet containing 'cpu', 'ram', 'net', and 'kernel' keys.
    data_received = pyqtSignal(dict)

    def __init__(self):
        """
        @brief Initializes all hardware sensors and internal state.
        """
        super().__init__()
        self.cpu = CPUSensor()
        self.ram = RAMSensor()
        self.net = NetworkSensor()
        self.kernel = KernelSensor()
        
        # Operational flag to control loop lifecycle
        self._is_running = True

    def run(self):
        """
        @brief Execution loop for the background thread.
        @details Samples hardware every 1000ms. Implements error isolation 
                 to ensure one failing sensor doesn't crash the entire worker.
        """
        while self._is_running:
            try:
                # Construct the unified telemetry packet
                telemetry_packet = {
                    "cpu": self.cpu.fetch_data(),
                    "ram": self.ram.fetch_data(),
                    "net": self.net.fetch_data(),
                    "kernel": [] 
                }
                
                # Independent sampling for Kernel threads due to high I/O cost
                try:
                    telemetry_packet["kernel"] = self.kernel.fetch_data()
                except Exception as e:
                    logging.warning(f"Kernel sensor sampling failed: {e}")

                # Dispatch data to the UI thread via Signal/Slot mechanism
                self.data_received.emit(telemetry_packet)

            except Exception as e:
                logging.error(f"Critical Worker Loop Error: {e}")
                
            # Throttle sampling to 1Hz (1000ms) to maintain low CPU overhead
            self.msleep(1000)

    def stop(self):
        """
        @brief Gracefully terminates the worker thread.
        """
        self._is_running = False
        self.wait() # Block until thread actually exits