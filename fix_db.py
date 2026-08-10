import os

file_path = 'database.py'
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# The user activity log comment was at line 221 (index 220).
# The duplicate user activity log comment is at line 416 (index 415).
# We want to remove lines from index 220 to 414.

del lines[220:415]

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("database.py fixed.")
