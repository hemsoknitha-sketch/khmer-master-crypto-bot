import re

with open('bot_thread.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the place to insert the scheduler registration
target = "# 6. Sentiment Snipe"
replacement = '''# 6. Flash Crash Defender (Every 10 seconds)
        self.scheduler.add_job(
            scheduler_tasks.flash_crash_defender,
            'interval',
            seconds=10,
            args=[self.app, self.ai_engine],
            id='flash_crash_defender'
        )
        
        # 7. Sentiment Snipe'''

if 'flash_crash_defender' not in content:
    content = content.replace(target, replacement)
    with open('bot_thread.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Registered flash_crash_defender in bot_thread.py")
else:
    print("flash_crash_defender already registered")
