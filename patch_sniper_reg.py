import re

with open('bot_thread.py', 'r', encoding='utf-8') as f:
    content = f.read()

scheduler_reg = '# 19. Binance Listing Monitor (Every 30 mins)'
sniper_job = '''        # 20. Smart Listing Sniper Engine (Every 5 seconds)
        self.scheduler.add_job(
            scheduler_tasks.smart_sniper_engine,
            "interval",
            seconds=5,
            args=[self.app, self.ai_engine],
            id="smart_sniper_engine"
        )
        
'''

if scheduler_reg in content:
    content = content.replace(scheduler_reg, sniper_job + scheduler_reg)
    with open('bot_thread.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patch applied for sniper job.")
else:
    print("Warning: Scheduler insertion point not found.")
