Linux System Monitoring Script on AWS EC2

This project sets up a Python script to monitor basic system resources (CPU, Memory, Disk) on an AWS EC2 instance and logs the data periodically using cron. Everything is included here — setup, script, and execution.

Table of Contents

Prerequisites

Step 1: Launch an AWS EC2 Instance

Step 2: Connect to Your EC2 Instance

Step 3: Install Python and Dependencies

Step 4: Create the Monitoring Script

Step 5: Test the Script Manually

Step 6: Automate with Cron

Viewing Logs

Optional Enhancements

Repository Structure

Prerequisites

An AWS Account

Basic knowledge of the Linux command line

A terminal or SSH client installed on your local machine

Step 1: Launch an AWS EC2 Instance

# 1. Navigate to AWS Management Console → EC2 → Launch Instance.
# 2. Choose an AMI, like Amazon Linux 2 or Ubuntu Server.
# 3. Select an instance type, like t2.micro (eligible for the Free Tier).
# 4. Configure network and storage settings (defaults are usually fine).
# 5. Set up a Security Group to allow SSH (port 22) traffic from your IP.
# 6. Launch the instance and download your new .pem key file.


Step 2: Connect to Your EC2 Instance

# Use the ssh command with your downloaded key to connect.
# Replace the path and public IP with your own.

# Example for an Ubuntu AMI
ssh -i /path/to/your-key.pem ubuntu@<EC2_PUBLIC_IP>

# Example for an Amazon Linux 2 AMI
ssh -i /path/to/your-key.pem ec2-user@<EC2_PUBLIC_IP>


Step 3: Install Python and Dependencies

# First, verify Python 3 is installed (it usually is).
python3 --version

# Update package lists (for Ubuntu/Debian systems).
sudo apt update

# Install pip for Python 3 and the psutil library.
sudo apt install python3-pip -y
pip3 install psutil


Step 4: Create the Monitoring Script

# Create and open a new Python file using a text editor like nano.
nano linux_monitor.py


Copy your Python script code into the editor.

# The Python monitoring script should be written here.


Save the file and exit the editor (Ctrl + O, Enter, then Ctrl + X in nano).

Step 5: Test the Script Manually

# Run the script directly from the command line to test it.
python3 linux_monitor.py


You should see a single line of output confirming that the log was written.

# Example Output
Successfully logged: 2025-10-17 14:25:12 - CPU Usage: 12.5% | Memory Usage: 45.3% | Disk Usage: 70.1%


Step 6: Automate with Cron

Use cron to schedule the script to run at a regular interval.

# Open the crontab editor.
crontab -e


Add the following line to the bottom of the file to run the script every 5 minutes. Ensure the path to your script is correct.

*/5 * * * * /usr/bin/python3 /home/ubuntu/linux_monitor.py


*/5 * * * *: Runs the command every 5 minutes.

/usr/bin/python3: The absolute path to the Python interpreter.

/home/ubuntu/linux_monitor.py: The absolute path to your script.

Viewing Logs

The script appends output to a log file in the /tmp directory.

# View the entire log file from the beginning.
cat /tmp/system_monitor.log

# View the last few lines and follow the file for new updates.
tail -f /tmp/system_monitor.log


Optional Enhancements

Alerting: Modify the script to send an email or a Slack notification if usage exceeds a certain threshold (e.g., CPU > 90%).

Centralized Logging: Use a service like AWS CloudWatch Logs to send logs to a central location for easier analysis and long-term storage.

Data Visualization: Ingest the log data into a tool like Grafana, Kibana, or AWS QuickSight to create dashboards and visualize resource trends over time.

More Metrics: Expand the script to monitor other system metrics, such as network I/O, temperature, or individual process resource usage.

Repository Structure

.
├── linux_monitor.py      # The Python monitoring script
└── README.md             # This setup guide
