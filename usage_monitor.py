import re
from collections import defaultdict
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import os
from glob import glob

session_log_path_pattern = '/home/*/ShinyApps/log/ShinyApp*log'
app_directory_path_pattern = '/home/*/ShinyApps'
access_log_path = '/var/log/shiny-server/access.log'

session_log_files = glob(session_log_path_pattern)
total_sessions = len(session_log_files)

current_time = datetime.datetime.now()
one_month_ago = current_time - datetime.timedelta(days=30)

session_count_last_month = 0

for log_file in session_log_files:
    timestamp_match = re.search(r'(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})', log_file)
    if timestamp_match:
        log_time = datetime.datetime.strptime(timestamp_match.group(1), '%Y-%m-%d_%H-%M-%S')
        if log_time > one_month_ago:
            session_count_last_month += 1

app_directories = glob(f'{app_directory_path_pattern}/*')
total_app_count = len(app_directories)

unique_ip_addresses = set()
access_log_pattern = re.compile(r'(\S+) - - \[(\S+ \+\d+)\] "GET /([^/]+)/?.*"')

with open(access_log_path, 'r') as f:
    for line in f:
        match = access_log_pattern.match(line)
        if match:
            ip_address, timestamp, app_name = match.groups()
            unique_ip_addresses.add(ip_address)

print(f"Total Sessions: {total_sessions}")
print(f"Sessions Last Month: {session_count_last_month}")
print(f"Total Apps: {total_app_count}")
print(f"Unique IPs: {len(unique_ip_addresses)}")

data = {
    'Metric': ['Total Sessions', 'Sessions Last Month', 'Total Apps', 'Unique IPs'],
    'Count': [total_sessions, session_count_last_month, total_app_count, len(unique_ip_addresses)]
}
df = pd.DataFrame(data)

current_date = datetime.datetime.now().strftime('%Y-%m-%d')
output_directory = '/home/usage_trace'
os.makedirs(output_directory, exist_ok=True)
csv_file_path = f'{output_directory}/usage_stats_{current_date}.csv'

df.to_csv(csv_file_path, index=False)

df.plot(kind='bar', x='Metric', y='Count', legend=False, figsize=(10, 6))
plt.title('Usage Statistics')
plt.xlabel('Metric')
plt.ylabel('Count')
image_file_path = f'{output_directory}/usage_stats_{current_date}.png'
plt.savefig(image_file_path)
plt.close()

# Uncomment the following lines to automatically download the CSV files to your local computer
# import paramiko
# local_directory = '/local/path/to/save'
# hostname = 'shiny.bio.nyu.edu'
# username = 'ml7612'
# password = 'your_password'  # or use key-based authentication

# ssh = paramiko.SSHClient()
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# ssh.connect(hostname, username=username, password=password)
# sftp = ssh.open_sftp()

# sftp.get(csv_file_path, os.path.join(local_directory, os.path.basename(csv_file_path)))
# sftp.get(image_file_path, os.path.join(local_directory, os.path.basename(image_file_path)))

# sftp.close()
# ssh.close()
