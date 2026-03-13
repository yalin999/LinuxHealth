"""
@file disk_sensor.py
@brief Telemetry engine for disk I/O throughput monitoring.
@project Linux Health Monitor Pro
@license MIT
"""

import psutil
import time
import logging

class DiskSensor:
    """
    @class DiskSensor
    @brief Calculates real-time disk read/write throughput.
    @details Measures performance by calculating the delta between 
             system-wide disk I/O counters over a specific time interval.
    """

    def __init__(self):
        """
        @brief Establishes the initial baseline for disk I/O counters.
        @details Captures current bytes read/written and the current 
                 unix timestamp to enable the first delta calculation.
        """
        try:
            self.last_io = psutil.disk_io_counters()
            self.last_time = time.time()
        except Exception as e:
            logging.error(f"Failed to initialize DiskSensor: {e}")
            self.last_io = None
            self.last_time = time.time()

    def fetch_data(self) -> dict:
        """
        @brief Samples disk I/O and calculates transfer rates.
        @return A dictionary containing:
            - 'read'  (float): Read speed in MB/s.
            - 'write' (float): Write speed in MB/s.
        @note Rates are calculated as: (Current_Bytes - Previous_Bytes) / Elapsed_Time.
        """
        try:
            now = time.time()
            curr_io = psutil.disk_io_counters()
            
            # Prevent division by zero or errors if counters are inaccessible
            elapsed = now - self.last_time
            if elapsed <= 0 or self.last_io is None:
                return {"read": 0.0, "write": 0.0}

            # Calculate raw bytes per second
            read_bps = (curr_io.read_bytes - self.last_io.read_bytes) / elapsed
            write_bps = (curr_io.write_bytes - self.last_io.write_bytes) / elapsed

            # Update internal state for the next sampling cycle
            self.last_io = curr_io
            self.last_time = now

            # Convert Bytes/s to Megabytes/s (MB/s)
            # Standard conversion: Bytes / 1024^2
            return {
                "read": round(read_bps / (1024 * 1024), 2),
                "write": round(write_bps / (1024 * 1024), 2)
            }
        except Exception as e:
            logging.warning(f"Error sampling disk I/O metrics: {e}")
            return {"read": 0.0, "write": 0.0}