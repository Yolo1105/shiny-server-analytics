import re
from glob import glob
import datetime
import os
import csv

session_log_path_pattern = '/home/*/ShinyApps/log/ShinyApp*log'
app_directory_path_pattern = '/home/*/ShinyApps'
shiny_log_directory = '/var/log/shiny-server'

# Collect existing logs and apps
session_log_files = glob(session_log_path_pattern)
app_directories = glob(f'{app_directory_path_pattern}/*')
total_apps = len(app_directories)

current_time = datetime.datetime.now()
one_month_ago = current_time - datetime.timedelta(days=30)

ip_pattern = re.compile(r'(\d+\.\d+\.\d+\.\d+)') 
date_pattern = re.compile(r'(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})')
error_pattern = re.compile(r'Execution halted')
warning_pattern = re.compile(r'Warning message:\s*(.*)')

unique_ips = set()
session_count_last_month = 0
errors_detected = 0
session_details = []

for log_file in session_log_files:
    session_info = {'file': log_file, 'errors': [], 'warnings': []}
    with open(log_file, 'r') as file:
        content = file.read()
        # Audit sessions from the last month
        date_match = re.search(date_pattern, log_file)
        if date_match and datetime.datetime.strptime(date_match.group(1), '%Y-%m-%d_%H-%M-%S') > one_month_ago:
            session_count_last_month += 1

        session_info['errors'] = error_pattern.findall(content)
        session_info['warnings'] = warning_pattern.findall(content)
        errors_detected += len(session_info['errors'])

        # Collect unique IPs
        unique_ips.update(ip_pattern.findall(content))

    session_details.append(session_info)

output_directory = '/home/ml7612/ShinyApps'
os.makedirs(output_directory, exist_ok=True)
stats_path = os.path.join(output_directory, f'usage_stats_{current_time.strftime("%Y-%m-%d")}.txt')

with open(stats_path, 'w') as file:
    file.write(f"Date: {current_time.strftime('%Y-%m-%d')}\n")
    file.write(f"Total Apps: {total_apps}\n")  # Audit the growth of new apps
    file.write(f"Total Sessions Last Month: {session_count_last_month}\n")  # Audit number of sessions
    file.write(f"Unique IPs: {len(unique_ips)}\n")  # Audit unique IPs
    file.write(f"Errors Detected: {errors_detected}\n")
    for session in session_details:
        file.write(f"Log File: {session['file']}\n")
        file.write(f"Errors: {', '.join(session['errors']) if session['errors'] else 'No errors'}\n")
        file.write(f"Warnings: {', '.join(session['warnings']) if session['warnings'] else 'No warnings'}\n")

csv_path = os.path.join(output_directory, f'usage_stats_{current_time.strftime("%Y-%m-%d")}.csv')
with open(csv_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Date', 'Total Apps', 'Total Sessions Last Month', 'Unique IPs', 'Errors Detected'])
    writer.writerow([current_time.strftime('%Y-%m-%d'), total_apps, session_count_last_month, len(unique_ips), errors_detected])
    writer.writerow(['Log File', 'Errors', 'Warnings'])
    for session in session_details:
        writer.writerow([session['file'], ', '.join(session['errors']) if session['errors'] else 'No errors', ', '.join(session['warnings']) if session['warnings'] else 'No warnings'])

print(f"Total Apps: {total_apps}")
print(f"Total Sessions Last Month: {session_count_last_month}")
print(f"Unique IPs: {len(unique_ips)}")
print(f"Errors Detected: {errors_detected}")
