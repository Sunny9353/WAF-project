import os
import re

# Regex pattern to parse Apache access log lines
LOG_PATTERN = re.compile(
    r'(\S+) - - \[.+\] "(GET|POST|PUT|DELETE|HEAD|OPTIONS|PATCH) (\S+) HTTP/[\d.]+" (\d{3}) \d+'
)

def parse_log_line(line):
    match = LOG_PATTERN.match(line)
    if match:
        ip = match.group(1)
        method = match.group(2).lower()
        url = match.group(3).lower()
        status = match.group(4)

        return {
            'ip': ip,
            'method': method,
            'url': url,
            'status': status
        }
    else:
        return None

def clean_logs(input_path, output_path):
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input log file '{input_path}' not found.")
    
    cleaned_logs = []
    with open(input_path, 'r') as file:
        for line in file:
            parsed = parse_log_line(line.strip())
            if parsed:
                cleaned_logs.append(parsed)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as file:
        for log in cleaned_logs:
            file.write(f"{log['ip']}\t{log['method']}\t{log['url']}\t{log['status']}\n")

if __name__ == "__main__":
    input_file = os.path.join('data', 'processed', 'collected_logs.txt')
    output_file = os.path.join('data', 'processed', 'cleaned_logs.txt')
    clean_logs(input_file, output_file)
    print(f"Cleaned logs saved to '{output_file}'")