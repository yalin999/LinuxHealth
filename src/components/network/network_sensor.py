"""
@file network_sensor.py
@brief Telemetry engine for network throughput monitoring.
@project Linux Health Monitor Pro
@license MIT
"""

import psutil
import time
import logging

class NetworkSensor:
    """
    @class NetworkSensor
    @brief Calculates real-time network bandwidth utilization.
    @details Measures throughput by calculating the delta between 
             system-wide I/O counters over a specific time interval.
    """

    def __init__(self):
        """
        @brief Establishes the initial baseline for I/O counters.
        @details Captures current bytes sent/received and the current 
                 unix timestamp to enable the first delta calculation.
        """
        try:
            self.last_net = psutil.net_io_counters()
            self.last_time = time.time()
        except Exception as e:
            logging.error(f"Failed to initialize NetworkSensor: {e}")
            self.last_net = None
            self.last_time = time.time()

    def fetch_data(self) -> dict:
        """
        @brief Samples network I/O and calculates transfer rates.
        @return A dictionary containing:
            - 'down' (float): Download speed in KB/s.
            - 'up'   (float): Upload speed in KB/s.
        @note Rates are calculated as: (Current_Bytes - Previous_Bytes) / Elapsed_Time.
        """
        try:
            now = time.time()
            curr_net = psutil.net_io_counters()
            
            # Prevent division by zero if calls happen too rapidly
            elapsed = now - self.last_time
            if elapsed <= 0 or self.last_net is None:
                return {"down": 0.0, "up": 0.0}

            # Calculate raw bytes per second
            down_bps = (curr_net.bytes_recv - self.last_net.bytes_recv) / elapsed
            up_bps = (curr_net.bytes_sent - self.last_net.bytes_sent) / elapsed

            # Update internal state for the next sampling cycle
            self.last_net = curr_net
            self.last_time = now

            # Convert Bytes/s to Kilobytes/s (KB/s)
            return {
                "down": round(down_bps / 1024, 1),
                "up": round(up_bps / 1024, 1)
            }
        except Exception as e:
            logging.warning(f"Error sampling network metrics: {e}")
            return {"down": 0.0, "up": 0.0}