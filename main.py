from src import sensors
import time

# Import necessary functions from src/sensor.py
from src import sensors  # This tells Python: "Go into 'src' and find 'sensors.py'"

# Color function for visual alert system
def get_color(value):
    """Returns a color code based on the percentage value."""
    if value < 50:
        return "\033[92m" # Green
    elif value < 85:
        return "\033[93m" # Yellow
    else:
        return "\033[91m" # Red

# ANSI code to reset color back to normal
RESET = "\033[0m"

# ANSI code to move cursor to row 1, column 1
# This is like 'end="\r"' but for the entire screen
HOME = "\033[H"
RESET = "\033[0m"

# Clear once at the start
print("\033[2J", end="")

# --- Main Execution ---      
try:
    print("Starting Linux Health Monitor... (Press Ctrl+C to stop)")
    # Call functions to measure the current system info
    while True:
        # Move back to top-left instead of clearing
        print(HOME, end="")

        # Get uptime value
        uptime = sensors.get_uptime()

        # Get CPU related values
        cpu_percent = sensors.get_cpu_stats()
        cpu_speed = sensors.get_cpu_speed()
        
        # Get RAM related values
        ram_raw_info = sensors.get_ram_stats()
        ram_percent = ram_raw_info.percent
        ram_used_gb = round(ram_raw_info.used / (1024**3), 1)
        ram_total_gb = round(ram_raw_info.total / (1024**3), 1)

        # Get battery status
        battery_status = sensors.get_battery_stats()
        
        # Choose colors based on usage(%)
        cpu_color = get_color(cpu_percent)
        ram_color = get_color(ram_percent)

        # Print the measured CPU usage, RAM usage and battery status
        print("--- LINUX HEALTH MONITOR ---\n")
        print(f"Uptime: {uptime}\n")
        print(f"CPU: {cpu_color}{cpu_percent}%{RESET} || {cpu_speed}\n")
        print(f"RAM: {ram_color}{ram_percent}%{RESET} || {ram_used_gb} / {ram_total_gb} GB\n")
        print(f"Battery: {battery_status}\n")
        # Wait for 1 second before checking the hardware again
        time.sleep(1)

# If the user presses Ctrl+C, this block catches the 'KeyboardInterrupt' error
except KeyboardInterrupt:
    print(f"\n{RESET}Dashboard closed cleanly. Goodbye!")

