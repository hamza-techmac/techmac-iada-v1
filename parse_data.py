
import pandas as pd
import json
import sys

# Reading from stdin
data = sys.stdin.read()
rows = [row.split('\t') for row in data.strip().split('\n') if row.strip()]
for row in rows:
    try:
        row[2] = int(row[2])
        row[5] = float(row[5])
        row[6] = float(row[6])
    except:
        pass
with open('data.json', 'w') as f:
    json.dump(rows, f)
print('Done parsing')
