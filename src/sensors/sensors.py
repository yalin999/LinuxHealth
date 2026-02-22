import psutil
import time


class Sensors:
    """
    /**
     * @brief      psutil-based health metric collector.
     * @details    Aggregates process data for ISO/IEC 25010 reliability monitoring.
     *
     * @standard   ISO/IEC 25010, ISO/IEC 12207
     * @author     LinuxHealth
     * @version    1.0.0
     */
    """

    def __init__(self, cpu_interval: float = 0.5) -> None:
        self.cpu_interval = cpu_interval

    def get_kernel_threads(self) -> list:
        """
        /**
         * @brief      Kernel thread identifier.
         * @details    Lists processes without an executable path (typical of kernel threads).
         */
        """
        k_threads = []
        for proc in psutil.process_iter(['pid', 'name', 'exe']):
            try:
                # In Linux, kernel threads don't have an executable path ('exe'), so if it is empty then it is a piece of the Linux Kernel
                if proc.info['exe'] is None:
                    k_threads.append(proc.info['name'])
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return k_threads[:5] # Just show the first 5

    def get_network_speed(self) -> dict:
        """
        /**
         * @brief      Network throughput sampler.
         * @details    Measures bytes sent/received to satisfy ISO/IEC 25010 performance metrics.
         */
        """
        # Get bytes before a tiny sleep
        io1 = psutil.net_io_counters()
        time.sleep(0.1) # Small sample window
        io2 = psutil.net_io_counters()

        # Calculate speed (Bytes per second)
        # We multiply by 10 because our sample window was 0.1s
        download = (io2.bytes_recv - io1.bytes_recv) * 10
        upload = (io2.bytes_sent - io1.bytes_sent) * 10

        return {
            "down": round(download / 1024, 1), # KB/s
            "up": round(upload / 1024, 1)      # KB/s
        }

    def get_io_wait(self) -> float:
        """
        /**
         * @brief      I/O wait sampler.
         * @details    Captures CPU time spent waiting for disk I/O, a key ISO/IEC 25010 efficiency metric.
         */
        """
        # psutil.cpu_times_percent() returns a named tuple including 'iowait'
        cpu_times = psutil.cpu_times_percent(interval=None)
        return getattr(cpu_times, 'iowait', 0.0)

    def get_disk_status(self) -> str:
        """
        /**
         * @brief      Translates raw I/O wait into human-readable categories.
         * @details    Supports ISO/IEC 25010 usability by providing clear system states.
         */
        """
        wait = self.get_io_wait()
        
        if wait < 1.0:
            return "Smooth (Disk is fast enoug)"
        elif wait < 5.0:
            return "Busy (CPU is waiting a bit)"
        else:
            return "Bottleneck! (Disk is slowing the system down)"
    
    def get_network_hogs(self, threshold_bytes: int = 1024) -> list:
        """
        /**
         * @brief      Network usage attribution.
         * @details    Identifies processes with active network connections to detect 'hogs'.
         */
        """
        hogs = []
        for proc in psutil.process_iter(['pid', 'name', 'io_counters']):
            try:
                # We check the I/O counters for read/write bytes
                io = proc.info.get('io_counters')
                if io:
                    # Combining read and write for a general 'usage' stat
                    total_usage = io.read_bytes + io.write_bytes
                    if total_usage > threshold_bytes:
                        hogs.append({
                            "pid": proc.info['pid'],
                            "name": proc.info['name'],
                            "usage_mb": round(total_usage / (1024**2), 2)
                        })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        # Sort by usage so the biggest 'hog' is first
        return sorted(hogs, key=lambda x: x['usage_mb'], reverse=True)[:5]
    
    def get_zombie_processes(self) -> list:
        """
        /**
         * @brief      Zombie process scanner.
         * @details    Identifies 'defunct' processes for ISO/IEC 25010 reliability monitoring.
         */
        """
        zombies = []
        for proc in psutil.process_iter(['pid', 'name', 'status']):
            try:
                if proc.info['status'] == psutil.STATUS_ZOMBIE:
                    # Append the ID and name of zombie processes
                    zombies.append({
                        "pid": proc.info['pid'],
                        "name": proc.info['name']
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return zombies

    def get_cpu_stats(self) -> float:
        """
        /**
         * @brief      CPU utilization sampler.
         * @details    Measures CPU percentage with a configurable interval for ISO/IEC 25010 performance-efficiency evidence.
         */
        """
        return psutil.cpu_percent(interval=self.cpu_interval)

    def get_cpu_speed(self) -> str:
        """
        /**
         * @brief      CPU speed reporter.
         * @details    Provides GHz output or fallback to "N/A" supporting transparency requirements.
         */
        """
        freq = psutil.cpu_freq()
        if freq:
            return f"{round(freq.current / 1000, 2)} GHz"
        return "N/A"

    def get_uptime(self) -> str:
        """
        /**
         * @brief      System uptime formatter.
         * @details    Translates boot time into hours/minutes for ISO/IEC 12207 serviceability tracking.
         */
        """
        boot_time = psutil.boot_time()
        uptime_seconds = time.time() - boot_time
        hours = int(uptime_seconds // 3600)
        minutes = int((uptime_seconds % 3600) // 60)
        return f"{hours}h {minutes}m"

    def get_ram_stats(self):
        """
        /**
         * @brief      RAM statistics fetcher.
         * @details    Returns psutil virtual memory payload for ISO/IEC 25010 resource utilization analysis.
         */
        """
        return psutil.virtual_memory()

    def get_battery_stats(self) -> str:
        """
        /**
         * @brief      Battery availability reporter.
         * @details    Reports state-of-charge and charging status, aligning with ISO/IEC 25010 availability controls.
         */
        """
        battery_info = psutil.sensors_battery()
        if battery_info is None:
            return "AC Power (No Battery Detected)"

        status = "Charging" if battery_info.power_plugged else "Discharging"
        return f"{round(battery_info.percent, 1)}% ({status})"
