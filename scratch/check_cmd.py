content = open('bot_thread.py', encoding='utf-8').read()
for cmd in ['"report"', '"daily_report"', '"summary"', '"executive_summary"']:
    print(cmd, cmd in content)
