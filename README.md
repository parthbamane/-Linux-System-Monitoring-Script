# Linux System Monitoring Script on AWS EC2

This project sets up a Python script to monitor basic system resources (CPU, Memory, Disk) on an AWS EC2 instance and logs the data periodically using cron. Everything is included here — setup, script, and execution.

## Table of Contents

* [Prerequisites](#prerequisites)
* [Step 1: Launch an AWS EC2 Instance](#step-1-launch-an-aws-ec2-instance)
* [Step 2: Connect to Your EC2 Instance](#step-2-connect-to-your-ec2-instance)
* [Step 3: Install Python and Dependencies](#step-3-install-python-and-dependencies)
* [Step 4: Create the Monitoring Script](#step-4-create-the-monitoring-script)
* [Step 5: Test the Script Manually](#step-5-test-the-script-manually)
* [Step 6: Automate with Cron](#step-6-automate-with-cron)
* [Viewing Logs](#viewing-logs)
* [Optional Enhancements](#optional-enhancements)
* [Repository Structure](#repository-structure)

## Prerequisites

* An AWS Account
* Basic knowledge of the Linux command line
* A terminal or SSH client installed on your local machine

## Step 1: Launch an AWS EC2 Instance

```bash
# 1. Navigate to AWS Management Console → EC2 → Launch Instance.
# 2. Choose an AMI, like Amazon Linux 2 or Ubuntu Server.
# 3. Select an instance type, like t2.micro (eligible for the Free Tier).
# 4. Configure network and storage settings (defaults are usually fine).
# 5. Set up a Security Group to allow SSH (port 22) traffic from your IP.
# 6. Launch the instance and download your new .pem key file.
```

## Step 2: Connect to Your EC2 Instance

```bash
# Use the ssh command with your downloaded key to connect.
# Replace the path and public IP with your own.

# Example for an Ubuntu AMI
ssh -i /path/to/your-key.pem ubuntu@<EC2_PUBLIC_IP>

# Example for an Amazon Linux 2 AMI
ssh -i /path/to/your-key.pem ec2-user@<EC2_PUBLIC_IP>
```

## Step 3: Install Python and Dependencies

```bash
# First, verify Python 3 is installed (it usually is).
python3 --version

# Update package lists (for Ubuntu/Debian systems).
sudo apt update

# Install pip for Python 3 and the psutil library.
sudo apt install python3-pip -y
pip3 install psutil
```

**For Amazon Linux 2:**

```bash
# Update package lists
sudo yum update -y

# Install pip for Python 3 and psutil
sudo yum install python3-pip -y
pip3 install psutil
```

## Step 4: Create the Monitoring Script

```bash
# Create and open a new Python file using a text editor like nano.
nano linux_monitor.py
```

**Copy and paste the following Python script into the editor:**

```python
#!/usr/bin/env python3
"""
Linux System Monitoring Script
Monitors CPU, Memory, and Disk usage and logs the data to a file.
"""

import psutil
import datetime

def get_system_metrics():
    """
    Collect system metrics including CPU, Memory, and Disk usage.
    Returns a dictionary with the metrics.
    """
    # Get CPU usage percentage
    cpu_usage = psutil.cpu_percent(interval=1)
    
    # Get Memory usage
    memory = psutil.virtual_memory()
    memory_usage = memory.percent
    
    # Get Disk usage for the root partition
    disk = psutil.disk_usage('/')
    disk_usage = disk.percent
    
    return {
        'cpu': cpu_usage,
        'memory': memory_usage,
        'disk': disk_usage
    }

def log_metrics(metrics, log_file='/tmp/system_monitor.log'):
    """
    Log the system metrics to a file with timestamp.
    """
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = (
        f"{timestamp} - "
        f"CPU Usage: {metrics['cpu']:.1f}% | "
        f"Memory Usage: {metrics['memory']:.1f}% | "
        f"Disk Usage: {metrics['disk']:.1f}%\n"
    )
    
    try:
        with open(log_file, 'a') as f:
            f.write(log_entry)
        print(f"Successfully logged: {log_entry.strip()}")
    except Exception as e:
        print(f"Error writing to log file: {e}")

def main():
    """
    Main function to collect and log system metrics.
    """
    metrics = get_system_metrics()
    log_metrics(metrics)

if __name__ == "__main__":
    main()
```

**Save the file and exit the editor:**
- Press `Ctrl + O` to save
- Press `Enter` to confirm
- Press `Ctrl + X` to exit

**Make the script executable (optional but recommended):**

```bash
chmod +x linux_monitor.py
```

## Step 5: Test the Script Manually

```bash
# Run the script directly from the command line to test it.
python3 linux_monitor.py
```

**You should see output similar to:**

```
Successfully logged: 2025-10-18 14:25:12 - CPU Usage: 12.5% | Memory Usage: 45.3% | Disk Usage: 70.1%
```

**Verify the log file was created:**

```bash
cat /tmp/system_monitor.log
```

## Step 6: Automate with Cron

Use cron to schedule the script to run at a regular interval.

```bash
# Open the crontab editor.
crontab -e
```

**Add the following line to run the script every 5 minutes:**

```bash
*/5 * * * * /usr/bin/python3 /home/ubuntu/linux_monitor.py
```

**Important Notes:**
- `*/5 * * * *`: Runs the command every 5 minutes
- `/usr/bin/python3`: The absolute path to the Python interpreter (verify with `which python3`)
- `/home/ubuntu/linux_monitor.py`: The absolute path to your script (adjust based on your user)

**For Amazon Linux 2, use:**

```bash
*/5 * * * * /usr/bin/python3 /home/ec2-user/linux_monitor.py
```

**To verify your cron job is set up:**

```bash
crontab -l
```

## Viewing Logs

The script appends output to a log file in the `/tmp` directory.

```bash
# View the entire log file from the beginning.
cat /tmp/system_monitor.log

# View the last few lines and follow the file for new updates.
tail -f /tmp/system_monitor.log

# View the last 20 lines only
tail -n 20 /tmp/system_monitor.log
```

**Example log output:**

```
2025-10-18 14:00:01 - CPU Usage: 8.2% | Memory Usage: 42.1% | Disk Usage: 65.3%
2025-10-18 14:05:01 - CPU Usage: 12.5% | Memory Usage: 45.3% | Disk Usage: 65.3%
2025-10-18 14:10:01 - CPU Usage: 6.8% | Memory Usage: 43.7% | Disk Usage: 65.4%
```

## Optional Enhancements

### 1. **Email Alerting**
Modify the script to send an email when usage exceeds a threshold:

```python
import smtplib
from email.mime.text import MIMEText

def send_alert(metric, value, threshold):
    msg = MIMEText(f"Alert: {metric} usage is {value}% (threshold: {threshold}%)")
    msg['Subject'] = f'System Alert: High {metric} Usage'
    msg['From'] = 'monitor@yourserver.com'
    msg['To'] = 'admin@yourcompany.com'
    
    with smtplib.SMTP('localhost') as s:
        s.send_message(msg)
```

### 2. **AWS CloudWatch Integration**
Send metrics to AWS CloudWatch for centralized monitoring:

```bash
pip3 install boto3
```

```python
import boto3

def send_to_cloudwatch(metrics):
    cloudwatch = boto3.client('cloudwatch')
    cloudwatch.put_metric_data(
        Namespace='CustomMetrics',
        MetricData=[
            {
                'MetricName': 'CPUUsage',
                'Value': metrics['cpu'],
                'Unit': 'Percent'
            }
        ]
    )
```

### 3. **Data Visualization**
- Use **Grafana** with Prometheus for real-time dashboards
- Send logs to **AWS CloudWatch Logs** for analysis
- Use **Elasticsearch + Kibana** for log aggregation and visualization

### 4. **Additional Metrics**
Extend the script to monitor:
- Network I/O (`psutil.net_io_counters()`)
- Process information (`psutil.process_iter()`)
- System temperature (`psutil.sensors_temperatures()`)
- Individual CPU core usage

## Repository Structure

```
.
├── linux_monitor.py      # The Python monitoring script
└── README.md             # This setup guide
```

## Troubleshooting

### Script not running via cron?
1. Check cron service is running: `sudo service cron status`
2. Verify Python path: `which python3`
3. Use absolute paths in crontab
4. Check cron logs: `grep CRON /var/log/syslog` (Ubuntu) or `tail -f /var/log/cron` (Amazon Linux)

### Permission issues?
```bash
# Ensure the script has correct permissions
chmod +x linux_monitor.py

# If logging to a different directory, ensure write permissions
sudo chown $USER:$USER /path/to/log/directory
```

### psutil not found?
```bash
# Verify installation
pip3 show psutil

# Reinstall if necessary
pip3 install --upgrade psutil
```

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

---

**Author:** Your Name  
**Created:** October 2025  
**Last Updated:** October 2025
