import time

from src.sensors import Sensors

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

# Instantiate sensor reader once so we reuse stateful psutil handles when possible
sensors = Sensors()

# --- Main Execution ---      
try:
    print("Starting Linux Health Monitor... (Press Ctrl+C to stop)")
    # Call functions to measure the current system info
    while True:
        # Move back to top-left instead of clearing
        print(HOME, end="")

        # Get Kernel Threads
        k_threads = sensors.get_kernel_threads()

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

        # Get Disk/Pantry health
        disk_health = sensors.get_disk_status()
        io_val = sensors.get_io_wait()

        # Get Network speeds
        net_stats = sensors.get_network_speed()
        down_speed = net_stats["down"]
        up_speed = net_stats["up"]

        # Print CPU usage, RAM usage and battery status
        print("--- LINUX HEALTH MONITOR ---\n")

        # Print uptime
        print(f"Uptime: {uptime}\n")

        # Print CPU usage
        print(f"CPU: {cpu_color}{cpu_percent}%{RESET} || {cpu_speed}\n")

        # Print RAM usage
        print(f"RAM: {ram_color}{ram_percent}%{RESET} || {ram_used_gb} / {ram_total_gb} GB\n")

        # Print battery status
        print(f"Battery: {battery_status}\n")

        # Print network status
        print(f"Network: ↓ {down_speed} KB/s | ↑ {up_speed} KB/s\n")

        # Print disk status
        print(f"Disk Status: {disk_health} [{io_val}% wait]\n")

        # Print zombie list
        zombie_list = sensors.get_zombie_processes()
        
        print(f"Zombies detected: {len(zombie_list)}")
        if zombie_list:
            for z in zombie_list:
                print(f"  -> [PID: {z['pid']}] {z['name']}")

        # Print total active kernel services
        print(f"Kernel Threads (Sample): {', '.join(k_threads)}")
        print(f"Total Active Kernel Services: {len(k_threads)}\n")

        # Wait for 1 second before checking the hardware again
        time.sleep(1)

# If the user presses Ctrl+C, this block catches the 'KeyboardInterrupt' error
except KeyboardInterrupt:
    print(f"\n{RESET}Dashboard closed cleanly. Goodbye!")
