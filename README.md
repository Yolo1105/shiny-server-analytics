## README

### Overview

This project provides a script to monitor and log the usage statistics of Shiny applications on your Shiny server. The script performs the following tasks:
- Counts session logs.
- Determines the number of session logs created in the last month.
- Counts the total number of Shiny applications.
- Identifies unique IPs accessing the server.

The collected statistics are saved in a CSV file and visualized in a bar graph.

### Prerequisites

- Access to the Shiny server.
- SSH access to the server.
- Python installed on the server.
- Required Python libraries: `pandas`, `matplotlib`, `paramiko`.

### Setup Instructions

#### SSH into the Server

To connect to your Shiny server, use the following command:

```sh
ssh ml7612@shiny.bio.nyu.edu
```

#### Uploading the Script

Transfer the `shiny_usage_monitor.py` script from your local machine to the Shiny server using `scp`:

```sh
scp /path/to/local/shiny_usage_monitor.py ml7612@shiny.bio.nyu.edu:/home/shiny_usage_monitor.py
```

#### Making the Script Executable

On the server, make the script executable:

```sh
chmod +x /home/shiny_usage_monitor.py
```

#### Installing Required Python Libraries

Ensure all required Python libraries are installed by running:

```sh
pip install -r requirements.txt
```

### Setting Up the Cron Job

To automate the script to run daily at midnight, you need to set up a cron job. Cron is a time-based job scheduler in Unix-like operating systems. 

1. **Open the crontab file for editing**:

   Use the following command to edit the crontab file:

   ```sh
   crontab -e
   ```

2. **Add the cron job to the crontab file**:

   Add the following line to schedule the script to run daily at midnight:

   ```sh
   0 0 * * * /usr/bin/python3 /home/shiny_usage_monitor.py
   ```

   This line means:
   - `0 0 * * *`: Run the job at 00:00 (midnight) every day.
   - `/usr/bin/python3`: Use Python 3 to execute the script.
   - `/home/shiny_usage_monitor.py`: The path to the script.

3. **Save and exit the crontab editor**:

   Follow the instructions in the editor to save and exit (commonly `Ctrl+O` to save and `Ctrl+X` to exit in nano).

Once the cron job is set up, the script will run automatically every day at midnight. No further action is required for continuous auditing of the Shiny server usage.

### Downloading Generated Files

To view the generated CSV and PNG files on your local machine, use the following `scp` commands:

1. **Download the CSV file**:

   ```sh
   scp ml7612@shiny.bio.nyu.edu:/home/usage_trace/usage_stats_YYYY-MM-DD.csv /local/path/
   ```

2. **Download the PNG file**:

   ```sh
   scp ml7612@shiny.bio.nyu.edu:/home/usage_trace/usage_stats_YYYY-MM-DD.png /local/path/
   ```

Replace `YYYY-MM-DD` with the actual date the files were generated.

### Using Paramiko for Automated File Download

The following function automates the process of downloading files from the Shiny server using Paramiko:

```python
import paramiko
import os

local_directory = '/local/path/to/save'
hostname = 'shiny.bio.nyu.edu'
username = 'ml7612'
password = 'your_password'  # or use key-based authentication

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname, username=username, password=password)
sftp = ssh.open_sftp()

# Replace `csv_file_path` and `image_file_path` with actual paths
csv_file_path = '/home/usage_trace/usage_stats_YYYY-MM-DD.csv'
image_file_path = '/home/usage_trace/usage_stats_YYYY-MM-DD.png'

sftp.get(csv_file_path, os.path.join(local_directory, os.path.basename(csv_file_path)))
sftp.get(image_file_path, os.path.join(local_directory, os.path.basename(image_file_path)))

sftp.close()
ssh.close()
```

### Viewing the Graph

The generated graph images (`usage_stats_YYYY-MM-DD.png`) show the usage statistics and can be viewed using any image viewer on your local machine. The graph includes metrics such as:
- Total number of sessions.
- Sessions in the last month.
- Total applications.
- Unique IPs.

### Summary of Commands

1. **SSH into the server**:
   ```sh
   ssh ml7612@shiny.bio.nyu.edu
   ```

2. **Upload the script**:
   ```sh
   scp /path/to/local/shiny_usage_monitor.py ml7612@shiny.bio.nyu.edu:/home/shiny_usage_monitor.py
   ```

3. **Make the script executable**:
   ```sh
   chmod +x /home/shiny_usage_monitor.py
   ```

4. **Install required Python libraries**:
   ```sh
   pip install -r requirements.txt
   ```

5. **Set up the cron job**:
   ```sh
   crontab -e
   ```

6. **Add the cron job line to run daily at midnight**:
   ```sh
   0 0 * * * /usr/bin/python3 /home/shiny_usage_monitor.py
   ```

7. **Download the CSV and PNG files**:
   ```sh
   scp ml7612@shiny.bio.nyu.edu:/home/usage_trace/usage_stats_YYYY-MM-DD.csv /local/path/
   scp ml7612@shiny.bio.nyu.edu:/home/usage_trace/usage_stats_YYYY-MM-DD.png /local/path/
   ```

By following these steps, you can automate the collection and visualization of usage statistics for your Shiny applications. The script will run automatically once a day at midnight, ensuring that your usage data is consistently updated and available for analysis.