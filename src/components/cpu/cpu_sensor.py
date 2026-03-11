"""
@file cpu_sensor.py
@brief Hardware abstraction layer for CPU metrics.
@project Linux Health Monitor Pro
@license MIT
"""

import psutil
import logging

class CPUSensor:
    """
    @class CPUSensor
    @brief Core logic for CPU telemetry.
    @details Interface for gathering real-time processor utilization and 
             clock frequency using the psutil cross-platform library.
    """

    def __init__(self):
        """
        @brief Initializes the sensor baseline.
        @note psutil.cpu_percent requires a non-blocking initial call to 
               establish a reference point for future delta calculations.
        """
        try:
            psutil.cpu_percent(interval=None)
        except Exception as e:
            logging.error(f"Failed to initialize CPUSensor: {e}")

    def fetch_data(self) -> dict:
        """
        @brief Samples current CPU performance metrics.
        @return A dictionary containing:
            - 'usage' (float): Total CPU utilization as a percentage.
            - 'speed' (float): Current clock speed in GHz.
        @note Clock speed is converted from MHz to GHz for dashboard readability.
        """
        try:
            # Non-blocking call returns the utilization since the last call
            usage = psutil.cpu_percent(interval=None)
            
            # Fetch frequency; may return None on certain virtualized environments
            freq = psutil.cpu_freq()
            
            # Calculation: Convert MHz (psutil default) to GHz
            speed_ghz = round(freq.current / 1000, 2) if freq else 0.0
            
            return {
                "usage": usage,
                "speed": speed_ghz
            }
        except Exception as e:
            logging.warning(f"Error sampling CPU metrics: {e}")
            return {"usage": 0.0, "speed": 0.0}