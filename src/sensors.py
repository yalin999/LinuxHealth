import psutil
import time

# Function for CPU usage percentage (averaging over 0.5 seconds)
def get_cpu_stats():
    """ Returns the current CPU usage percentage"""
    return psutil.cpu_percent(interval=0.5)

# Function for CPU speed detection
def get_cpu_speed():
    """Returns the current CPU speed in GHz."""
    # freq.current is in MHz, so we divide by 1000 for GHz
    freq = psutil.cpu_freq()
    if freq:
        return f"{round(freq.current / 1000, 2)} GHz"
    else:
        return "N/A"

# Function for system uptime
def get_uptime():
    """Returns how long the system has been running."""
    # Calculate uptime
    boot_time = psutil.boot_time()
    uptime_seconds = time.time() - boot_time
    
    # Conversion to hour and minute
    hours = int(uptime_seconds // 3600)
    minutes = int((uptime_seconds % 3600) // 60)
    
    return f"{hours}h {minutes}m"

# Function for ram usage percentage
def get_ram_stats():
    """Returns raw RAM usage info"""
    # Get raw RAM info
    ram = psutil.virtual_memory()
    return ram

# Function for battery status
def get_battery_stats():
    """Returns the battery status in % and as charging-discharging."""
    # Get raw battery info
    battery_info = psutil.sensors_battery()

    # If the system literally can't find a battery object
    if battery_info is None:
        return "AC Power (No Battery Detected)"

    # If it finds the battery, determine the state
    if battery_info.power_plugged:
        status = "Charging"
    else:
        status = "Discharging"
        
    # Access the .percent attribute and round it to 1 decimal place    
    return f"{round(battery_info.percent, 1)}% ({status})"