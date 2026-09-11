import asyncio
import re
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/..")
import scheduler_tasks

async def main():
    msg, kb = await scheduler_tasks.build_executive_summary_report(859271875)
    
    # Remove inline code blocks
    without_code = re.sub(r"`[^`]*`", "", msg)
    underscores = [i for i, c in enumerate(without_code) if c == '_']
    print(f"Total underscores outside backticks: {len(underscores)}")
    print(f"Is count ODD? {len(underscores) % 2 != 0}")
    for i in underscores:
        print("Underscore context:", repr(without_code[max(0, i-15):min(len(without_code), i+20)]))

if __name__ == "__main__":
    asyncio.run(main())
