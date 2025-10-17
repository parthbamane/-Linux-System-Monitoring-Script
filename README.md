#!/bin/bash
# ==============================================================
# Linux System Monitoring Script on AWS EC2
# ==============================================================
# This script guides you through setting up system monitoring
# on an AWS EC2 instance using Python to log CPU, memory, and disk usage.
# ==============================================================

# --------------------------------------------------------------
# PREREQUISITES
# --------------------------------------------------------------
# 1. AWS Account
# 2. Basic knowledge of Linux command line
# 3. SSH client / terminal installed on your local system
# --------------------------------------------------------------

# --------------------------------------------------------------
# STEP 1: LAUNCH AN AWS EC2 INSTANCE
# --------------------------------------------------------------
# 1. Open AWS Management Console > EC2 > Launch Instance
# 2. Choose an AMI (Amazon Linux 2 or Ubuntu Server)
# 3. Select instance type: t2.micro (Free Tier eligible)
# 4. Configure default settings for network and storage
# 5. Add a Security Group rule to allow SSH on port 22
# 6. Launch the instance and download the .pem key file
# --------------------------------------------------------------

# --------------------------------------------------------------
# STEP 2: CONNECT TO YOUR EC2 INSTANCE
# --------------------------------------------------------------
# Replace placeholders below with your key file and EC2 public IP

# For Ubuntu Server
ssh -i /path/to/your-key.pem ubuntu@<EC2_PUBLIC_IP>

# For Amazon Linux 2
ssh -i /path/to/your-key.pem ec2-user@<EC2_PUBLIC_IP>
# --------------------------------------------------------------

# --------------------------------------------------------------
# STEP 3: INSTALL PYTHON AND DEPENDENCIES
# --------------------------------------------------------------
# Ensure Python 3 is installed
python3 --version

# Update package lists (for Ubuntu/Debian)
sudo apt update

# Install Python pip and 'psutil' library
sudo apt install python3-pip -y
pip3 install psutil
# --------------------------------------------------------------

# --------------------------------------------------------------
# STEP 4: CREATE THE MONITORING SCRIPT
# --------------------------------------------------------------
# Create and open the monitoring script
nano linux_monitor.py

# Copy the contents below into nano, then save and close (CTRL+O, Enter, CTRL+X)
: '
#!/usr/bin/env python3
import psutil
from datetime import datetime

log_file = "/tmp/system_monitor.log"

def get_usage():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    return cpu, memory, disk

def log_usage():
    cpu, memory, disk = get_usage()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"{timestamp} - CPU: {cpu}% | Memory: {memory}% | Disk: {disk}%\\n"
    with open(log_file, "a") as f:
        f.write(entry)
    print(f"Successfully logged: {entry.strip()}")

if __name__ == "__main__":
    log_usage()
'
# --------------------------------------------------------------

# --------------------------------------------------------------
# STEP 5: TEST THE SCRIPT MANUALLY
# --------------------------------------------------------------
python3 linux_monitor.py
# Expected output example:
# Successfully logged: 2025-10-17 15:10:42 - CPU: 13.1% | Memory: 45.2% | Disk: 72.8%
# --------------------------------------------------------------

# --------------------------------------------------------------
# STEP 6: AUTOMATE USING CRON
# --------------------------------------------------------------
# Open crontab
crontab -e

# Add the line below to schedule the script every 5 minutes
*/5 * * * * /usr/bin/python3 /home/ubuntu/linux_monitor.py
# Explanation:
#   */5 * * * *   → runs every 5 minutes
#   /usr/bin/python3 → full path to Python 3
#   /home/ubuntu/linux_monitor.py → path to your script
# --------------------------------------------------------------

# --------------------------------------------------------------
# VIEWING LOGS
# --------------------------------------------------------------
# View complete log file
cat /tmp/system_monitor.log

# Stream logs in real time
tail -f /tmp/system_monitor.log
# --------------------------------------------------------------

# --------------------------------------------------------------
# OPTIONAL ENHANCEMENTS
# --------------------------------------------------------------
# - Email or Slack alerts when CPU > 90%
# - Send logs to AWS CloudWatch for centralized monitoring
# - Use Grafana, Kibana, or AWS QuickSight for visualization
# - Track additional metrics (network I/O, per-process usage)
# --------------------------------------------------------------

# --------------------------------------------------------------
# REPOSITORY STRUCTURE
# --------------------------------------------------------------
# .
# ├── linux_monitor.py      # Python monitoring script
# └── README.md             # This bash-style setup guide
# --------------------------------------------------------------

# END OF SCRIPT
