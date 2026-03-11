"""
@file ram_sensor.py
@brief Telemetry engine for system memory (RAM) monitoring.
@project Linux Health Monitor Pro
@license MIT
"""

import psutil
import logging

class RAMSensor:
    """
    @class RAMSensor
    @brief Interface for gathering volatile memory utilization.
    @details Accesses system-level virtual memory statistics to provide 
             both percentage-based load and absolute volumetric data.
    """

    def fetch_data(self) -> dict:
        """
        @brief Samples current system memory usage.
        @return A dictionary containing:
            - 'percent' (float): Total memory utilization as a percentage.
            - 'used' (float): Currently occupied RAM in Gigabytes (GB).
            - 'total' (float): Total installed physical RAM in Gigabytes (GB).
        @note Volume calculation uses (1024^3) to convert raw bytes to GiB/GB.
        """
        try:
            # Captures all virtual memory stats (used, free, active, etc.)
            vm = psutil.virtual_memory()
            
            # Binary conversion: 1024^3 = 1,073,741,824 bytes per Gigabyte
            bytes_to_gb = 1024**3
            
            return {
                "percent": vm.percent,
                "used": round(vm.used / bytes_to_gb, 1),
                "total": round(vm.total / bytes_to_gb, 1)
            }
        except Exception as e:
            logging.error(f"Critical error in RAMSensor sampling: {e}")
            # Return safe default values to prevent UI crash
            return {"percent": 0.0, "used": 0.0, "total": 0.0}