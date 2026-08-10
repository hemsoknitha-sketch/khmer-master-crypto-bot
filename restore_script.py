import sys

with open('clean_recovered.py', 'r', encoding='utf-8') as f:
    top_half = f.read()

with open('patch_scheduler_end.py', 'r', encoding='utf-8') as f:
    patch = f.read()

rest_of_code = patch.split('rest_of_code = """')[1].split('"""')[0]

with open('scheduler_tasks.py', 'a', encoding='utf-8') as f:
    f.write('\n' + top_half)
    f.write(rest_of_code)

print('Success!')
