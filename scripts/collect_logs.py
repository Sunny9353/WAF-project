import os

def collect_logs(file_path):
    """
    Reads Apache access log file and returns a list of log entries (lines).
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Log file '{file_path}' not found.")
    
    with open(file_path, 'r') as file:
        logs = file.readlines()
    return logs
def store_logs(logs, output_path):
    """
    Stores collected logs in a text file for further use.
    """


    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as file:
        for log in logs:
            file.write(log)

if __name__ == "__main__":
    # Construct file paths relative to project root
    input_log_file = os.path.join('data', 'raw', 'sample_access.log')
    output_log_file = os.path.join('data', 'processed', 'collected_logs.txt')

    logs = collect_logs(input_log_file)
    print(f"Collected {len(logs)} log entries from '{input_log_file}'")

    # Store logs in processed folder
    store_logs(logs, output_log_file)
    print(f"Stored collected logs in '{output_log_file}'")