import logging
import pathlib
import re
import sys
import unittest

"""
/**
 * @brief      Ensure project root is importable when running as a script.
 * @details    Adds repository root to sys.path for ISO/IEC 12207 portability compliance.
 */
"""
PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.sensors import Sensors


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class SensorsTest(unittest.TestCase):
    """
    /**
     * @brief      Unit tests for the Sensors API.
     * @details    Provides ISO/IEC 12207 verification evidence across ISO/IEC 25010 attributes.
     */
    """

    @classmethod
    def setUpClass(cls):
        logging.info("\nSetting up Sensors tests...")
        cls.sensors = Sensors()

    def test_cpu_stats_range(self):
        """
        /**
         * @brief      Validate CPU utilization sampling.
         * @details    Confirms output range for ISO/IEC 25010 performance efficiency.
         */
        """
        logging.info("Testing CPU usage retrieval (ISO/IEC 25010 performance efficiency)...")
        cpu_percent = self.sensors.get_cpu_stats()
        self.assertIsInstance(cpu_percent, (int, float))
        self.assertGreaterEqual(cpu_percent, 0.0)
        self.assertLessEqual(cpu_percent, 100.0)
        logging.info("CPU usage test passed!")

    def test_cpu_speed_format(self):
        """
        /**
         * @brief      Validate CPU speed formatting.
         * @details    Ensures GHz output respects transparency expectations.
         */
        """
        logging.info("Testing CPU speed formatting for transparency...")
        cpu_speed = self.sensors.get_cpu_speed()
        self.assertIsInstance(cpu_speed, str)
        if cpu_speed != "N/A":
            self.assertRegex(cpu_speed, r"^\d+(\.\d+)? GHz$")
        logging.info("CPU speed test passed!")

    def test_uptime_format(self):
        """
        /**
         * @brief      Validate uptime formatting.
         * @details    Ensures textual uptime aids maintainability diagnostics.
         */
        """
        logging.info("Testing uptime format to ensure maintainability cues...")
        uptime = self.sensors.get_uptime()
        self.assertRegex(uptime, r"^\d+h \d+m$")
        logging.info("Uptime test passed!")

    def test_ram_stats_payload(self):
        """
        /**
         * @brief      Validate RAM payload structure.
         * @details    Confirms presence of required psutil attributes for resource reporting.
         */
        """
        logging.info("Testing RAM stats payload for resource reporting...")
        ram_stats = self.sensors.get_ram_stats()
        for attribute in ("total", "used", "percent"):
            self.assertTrue(hasattr(ram_stats, attribute), f"Missing '{attribute}' in RAM stats")
        self.assertGreater(ram_stats.total, 0)
        self.assertGreater(ram_stats.total, ram_stats.used / 2)
        logging.info("RAM stats test passed!")

    def test_battery_stats_response(self):
        """
        /**
         * @brief      Validate battery availability reporting.
         * @details    Ensures the response follows ISO/IEC 25010 availability conventions.
         */
        """
        logging.info("Testing battery stats response (availability attribute)...")
        battery_status = self.sensors.get_battery_stats()
        self.assertIsInstance(battery_status, str)
        if "AC Power" not in battery_status:
            pattern = re.compile(r"^\d+(\.\d+)?% \((Charging|Discharging)\)$")
            self.assertRegex(battery_status, pattern)
        logging.info("Battery stats test passed!")


if __name__ == "__main__":
    unittest.main()
