'''download the logfile later'''

count = {}
with open('logfile.txt') as f:
    for line in f:
        if 'GET' in line:
            filename = extract_filename(line)
            count[filename] = count.get(filename, 0) + 1

print(count)
