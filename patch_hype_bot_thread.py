import re

with open('bot_thread.py', 'r', encoding='utf-8') as f:
    content = f.read()

target = "# 7. Sentiment Snipe"
replacement = '''# 7. AI Social Hype Predictor (Every 10 minutes)
        self.scheduler.add_job(
            scheduler_tasks.check_social_hype,
            'interval',
            minutes=10,
            args=[self.app, self.ai_engine],
            id='check_social_hype'
        )
        
        # 8. Sentiment Snipe'''

if 'check_social_hype' not in content:
    content = content.replace(target, replacement)
    with open('bot_thread.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Registered check_social_hype in bot_thread.py")
else:
    print("check_social_hype already registered")
