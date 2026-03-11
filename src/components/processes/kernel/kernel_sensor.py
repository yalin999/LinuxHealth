"""
@file kernel_sensor.py
@brief Intelligence engine for identifying Linux kernel threads.
@project Linux Health Monitor Pro
@license MIT
"""

import psutil
import logging

class KernelSensor:
    """
    @class KernelSensor
    @brief Scans and filters the system process tree for kernel-space threads.
    @details On Linux systems, kernel threads are typically spawned by 'kthreadd' (PID 2).
             This class identifies such processes to provide visibility into 
             low-level system operations.
    """

    def fetch_data(self) -> list:
        """
        @brief Performs a point-in-time scan of the process table.
        @return A list of dictionaries, each containing:
            - 'pid' (int): The Process ID.
            - 'name' (str): The kernel thread identifier (e.g., kworker, migration).
            - 'status' (str): Current execution state (running, sleeping, etc.).
        @note Requires access to /proc; some threads may be omitted if 
              permissions are insufficient, though PID 2 check is generally robust.
        """
        threads = []
        
        # We iterate over the process table requesting only specific attributes
        # to minimize overhead during high-frequency sampling.
        attrs = ['pid', 'name', 'status', 'ppid']
        
        for proc in psutil.process_iter(attrs):
            try:
                # Industry Logic:
                # In the Linux process hierarchy, PID 2 is kthreadd.
                # Any process whose Parent PID (ppid) is 2 is a kernel thread.
                # We also include PID 2 itself as the root of the kernel tree.
                if proc.info['ppid'] == 2 or proc.info['pid'] == 2:
                    threads.append({
                        "pid": proc.info['pid'],
                        "name": proc.info['name'],
                        "status": proc.info['status']
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                # Processes can terminate between the iterator and access call.
                # AccessDenied is handled gracefully for non-root users.
                continue
            except Exception as e:
                logging.error(f"Unexpected error in KernelSensor: {e}")
                continue

        # Sort by PID to ensure UI consistency and prevent 'flicker' during updates.
        return sorted(threads, key=lambda x: x['pid'])
