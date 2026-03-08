import psutil
import time

class Sensors:
    """
    /**
     * @brief      ISO-Standardized Hardware Telemetry Engine.
     * @details    Provides core system metrics for ISO/IEC 25010 performance and 
     * reliability monitoring on Linux environments.
     * @standard   ISO/IEC 25010, ISO/IEC 12207
     */
    """

    def __init__(self, cpu_interval: float = 0.5) -> None:
        """
        @brief Initialize sampling interval for CPU telemetry.
        """
        self.cpu_interval = cpu_interval

    def get_cpu_usage(self) -> float:
        """
        @brief   CPU utilization sampler.
        @details Measures load percentage to provide evidence for Performance Efficiency.
        """
        return psutil.cpu_percent(interval=self.cpu_interval)

    def get_cpu_speed(self) -> float:
        """
        @brief   CPU frequency reporter.
        @details Returns current clock speed in GHz for hardware transparency.
        """
        freq = psutil.cpu_freq()
        if freq:
            return round(freq.current / 1000, 2)
        return 0.0

    def get_ram_details(self) -> dict:
        """
        @brief   RAM telemetry aggregator.
        @details Returns volumetric usage (Used/Total GB) and percentage.
        """
        vm = psutil.virtual_memory()
        return {
            "used": round(vm.used / (1024**3), 1),
            "total": round(vm.total / (1024**3), 1),
            "percent": vm.percent
        }

    def get_network_speed(self) -> dict:
        """
        @brief   Network throughput sampler.
        @details Measures instantaneous delta in I/O counters for bitrate calculation.
        """
        io1 = psutil.net_io_counters()
        time.sleep(0.05)  # Minimal blocking window for responsive threading
        io2 = psutil.net_io_counters()

        # Calculation adjusted for 0.05s window (* 20 to get per second)
        download = (io2.bytes_recv - io1.bytes_recv) * 20
        upload = (io2.bytes_sent - io1.bytes_sent) * 20

        return {
            "down": round(download / 1024, 1),
            "up": round(upload / 1024, 1)
        }

    def get_disk_status(self) -> str:
        """
        @brief   I/O Wait analysis.
        @details Interprets CPU time spent waiting for Disk I/O into qualitative states.
        """
        cpu_times = psutil.cpu_times_percent(interval=None)
        wait = getattr(cpu_times, 'iowait', 0.0)
        
        if wait < 1.0: return "Smooth"
        if wait < 5.0: return "Busy"
        return "Bottleneck"

    def get_uptime(self) -> str:
        """
        @brief   Serviceability tracker.
        @details Translates system boot time into a human-readable duration.
        """
        uptime_seconds = time.time() - psutil.boot_time()
        hours = int(uptime_seconds // 3600)
        minutes = int((uptime_seconds % 3600) // 60)
        return f"{hours}h {minutes}m"

    def get_kernel_processes(self) -> list:
        """
        @brief   Kernel Thread Discovery.
        @details Identifies system-level processes by verifying empty command-line strings.
        """
        kernel_threads = []
        for proc in psutil.process_iter(['pid', 'name', 'status']):
            try:
                # Standard Linux indicator for kernel threads (no cmdline)
                if not proc.cmdline():
                    kernel_threads.append({
                        "pid": proc.info['pid'],
                        "name": proc.info['name'],
                        "status": proc.info['status']
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return kernel_threads
