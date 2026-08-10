import re

with open('bot_thread.py', 'r', encoding='utf-8') as f:
    content = f.read()

target1 = '''                    trade_status = f"❌ **បរាជ័យ:** {res.get('error', 'Unknown Error')} (Bot នៅតែរត់ និងរង់ចាំទិញនៅជុំក្រោយ)"'''
replacement1 = '''                    error_msg = res.get('error', res.get('msg', 'Unknown Error'))
                    trade_status = f"❌ **បរាជ័យ:** {error_msg} (Bot នៅតែរត់ និងរង់ចាំទិញនៅជុំក្រោយ)"'''

target2 = '''                    trade_status = f"❌ **បរាជ័យ:** {res.get('error', 'Unknown Error')} (Bot នៅតែរត់ និងរង់ចាំតម្លៃល្អ)"'''
replacement2 = '''                    error_msg = res.get('error', res.get('msg', 'Unknown Error'))
                    trade_status = f"❌ **បរាជ័យ:** {error_msg} (Bot នៅតែរត់ និងរង់ចាំតម្លៃល្អ)"'''

if "error_msg = res.get('error', res.get('msg'" not in content:
    content = content.replace(target1, replacement1)
    content = content.replace(target2, replacement2)
    with open('bot_thread.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed error parsing in bot_thread.py")
else:
    print("Already fixed")
