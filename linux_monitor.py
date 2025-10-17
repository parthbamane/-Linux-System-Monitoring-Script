#!/usr/bin/env python3
# linux_monitor.py - Linux System Monitoring Script

import psutil
import datetime

# Log file location
LOG_FILE = "/tmp/system_monitor.log"

def get_system_usage():
    cpu_percent = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    usage = (f"CPU Usage: {cpu_percent}% | "
             f"Memory Usage: {mem.percent}% | "
             f"Disk Usage: {disk.percent}%")
    return usage

def log_usage():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    usage = get_system_usage()
    log_line = f"{timestamp} - {usage}\n"

    with open(LOG_FILE, "a") as f:
        f.write(log_line)
    print(log_line.strip())

if __name__ == "__main__":
    log_usage()
