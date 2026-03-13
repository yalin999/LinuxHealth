"""
@file process_sensor.py
@brief Telemetry engine for monitoring user-space process resource consumption.
@project Linux Health Monitor Pro
@license MIT
"""

import psutil
import logging
from src.config import MAX_PROCESSES

class ProcessSensor:
    """
    @class ProcessSensor
    @brief Aggregates and sorts process-level resource telemetry.
    @details Provides a snapshot of the most resource-intensive user processes.
             Designed to work within a 1Hz sampling loop for accurate CPU delta calculations.
    """

    def __init__(self):
        """
        @brief Initializes the sensor.
        @details No baseline needed here as psutil.process_iter handles 
                 stat persistence for cpu_percent calculations internally.
        """
        pass

    def fetch_data(self, sort_by='cpu') -> list:
        """
        @brief Retrieves a sorted list of top-consuming processes.
        @param sort_by (str): The metric to sort by ('cpu' or 'ram').
        @return A list of dictionaries containing PID, Name, CPU %, and RAM (MB).
        @note Returns a maximum of 15 processes to optimize UI rendering performance.
        """
        processes = []
        try:
            # We iterate through all processes, requesting only specific attributes
            # to minimize context switching between Python and the Kernel.
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
                try:
                    info = proc.info
                    
                    # Process identification and resource metrics
                    pid = info['pid']
                    name = info['name'] or "Unknown"
                    cpu = info['cpu_percent'] or 0.0
                    
                    # RSS (Resident Set Size) represents actual physical memory used
                    ram_mb = 0.0
                    if info['memory_info']:
                        ram_mb = info['memory_info'].rss / (1024 * 1024)

                    processes.append({
                        "pid": pid,
                        "name": name,
                        "cpu": round(cpu, 1),
                        "ram": round(ram_mb, 1)
                    })
                    
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    # These exceptions are common on Linux as processes cycle frequently.
                    # We silently skip them to maintain telemetry stability.
                    continue

            # --- Sorting Logic ---
            # We perform sorting on the background thread to keep the UI responsive.
            # Lambda key allows for dynamic switching between CPU and RAM priorities.
            if sort_by == 'ram':
                processes.sort(key=lambda x: x['ram'], reverse=True)
            else:
                processes.sort(key=lambda x: x['cpu'], reverse=True)

            # Return the "Top 15" consumers (Industry standard for dashboarding)
            return processes[:MAX_PROCESSES]

        except Exception as e:
            logging.error(f"Critical error in ProcessSensor: {e}")
            return []