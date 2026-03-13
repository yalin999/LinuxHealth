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
from src.components.disk.disk_sensor import DiskSensor
from src.components.network.network_sensor import NetworkSensor
from src.components.processes.kernel.kernel_sensor import KernelSensor
from src.components.processes.user.process_sensor import ProcessSensor

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
        self.disk = DiskSensor()
        self.net = NetworkSensor()
        self.kernel = KernelSensor()
        self.user_processes = ProcessSensor()

        # Operational flag to control loop lifecycle
        self._is_running = True

        self.process_sort_mode = "cpu"

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
                    "disk": self.disk.fetch_data(),
                    "net": self.net.fetch_data(),
                    "user_processes": [],
                    "kernel": [] 
                }
                
                # Fetch User Processes
                try:
                    telemetry_packet["user_processes"] = self.user_processes.fetch_data(
                        sort_by=self.process_sort_mode
                    )
                except Exception as e:
                    logging.warning(f"User process sampling failed: {e}")

                # Fetch Kernel Threads
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
    
    def set_process_sort_mode(self, mode: str):
        """
        @brief Updates the sorting criteria for the next sampling cycle.
        @param mode 'cpu' or 'ram'
        """
        self.process_sort_mode = mode
        
    def stop(self):
        """
        @brief Gracefully terminates the worker thread.
        """
        self._is_running = False
        self.wait() # Block until thread actually exits