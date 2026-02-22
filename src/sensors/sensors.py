import psutil
import time


class Sensors:
    """
    /**
     * @brief      psutil-based health metric collector.
     * @details    Aggregates CPU, memory, uptime, and battery data for ISO/IEC 25010 reliability monitoring.
     *
     * @standard   ISO/IEC 25010, ISO/IEC 12207
     * @author     LinuxHealth
     * @version    1.0.0
     */
    """

    def __init__(self, cpu_interval: float = 0.5) -> None:
        self.cpu_interval = cpu_interval

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
