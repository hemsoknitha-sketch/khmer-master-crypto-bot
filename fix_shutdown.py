import codecs

with codecs.open('bot_thread.py', 'r', 'utf-8') as f:
    text = f.read()

# 1. Restore broadcast_message
start_marker1 = '        async def send_to_all():'
idx1 = text.find(start_marker1)

if idx1 != -1 and 'def broadcast_message' not in text[idx1-200:idx1]:
    broadcast_code = '''
    def broadcast_message(self, text: str, target: str):
        """Called from PyQt GUI to broadcast a message asynchronously."""
        if not self.app or not self.loop:
            self.log_signal.emit("❌ Broadcast failed: Bot is not running.")
            return

        async def send_to_all():
'''
    text = text.replace('        async def send_to_all():\r\n', broadcast_code)
    text = text.replace('        async def send_to_all():\n', broadcast_code)

# 2. Rewrite the stop() method entirely
start_marker2 = '    def stop(self):'
idx2 = text.find(start_marker2)
if idx2 != -1:
    new_stop_code = '''    def stop(self):
        """Safely shutdown the bot service"""
        if self.app and self.loop:
            async def shutdown():
                try:
                    if hasattr(self, 'scheduler') and self.scheduler.running:
                        self.scheduler.shutdown(wait=False)
                    if self.app.updater:
                        await self.app.updater.stop()
                    await self.app.stop()
                    await self.app.shutdown()
                    
                    import asyncio
                    tasks = [t for t in asyncio.all_tasks(self.loop) if t is not asyncio.current_task()]
                    for task in tasks:
                        task.cancel()
                    await asyncio.gather(*tasks, return_exceptions=True)
                except Exception as e:
                    print(f"Error during bot shutdown: {e}")

            import asyncio
            future = asyncio.run_coroutine_threadsafe(shutdown(), self.loop)
            try:
                future.result(timeout=3.0)
            except Exception:
                pass
                
            self.log_signal.emit("🛑 Telegram Bot stopped cleanly.")
            self.loop.call_soon_threadsafe(self.loop.stop)
            
        self.quit()
        self.wait()
'''
    text = text[:idx2] + new_stop_code

with codecs.open('bot_thread.py', 'w', 'utf-8') as f:
    f.write(text)

print("bot_thread.py stop() method and broadcast_message restored successfully.")
