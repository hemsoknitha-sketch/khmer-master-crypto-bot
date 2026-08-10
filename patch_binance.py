import re

with open('bot_thread.py', 'r', encoding='utf-8') as f:
    content = f.read()

scheduler_reg = '# 18. Opportunity Sniper (Every 5 mins)'
listing_job = '''        # 19. Binance Listing Monitor (Every 30 mins)
        self.scheduler.add_job(
            scheduler_tasks.binance_listing_monitor,
            "interval",
            minutes=30,
            args=[self.app, self.ai_engine],
            id="binance_listing_monitor"
        )
        
'''

if scheduler_reg in content:
    content = content.replace(scheduler_reg, listing_job + scheduler_reg)
    with open('bot_thread.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patch applied.")
else:
    print("Warning: Scheduler insertion point not found.")
