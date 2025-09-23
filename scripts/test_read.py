print("Starting test")

with open('data/raw/sample_access.log', 'r') as f:
    lines = f.readlines()
print(f"Read {len(lines)} lines")
print("Sample line:", lines[0].strip())