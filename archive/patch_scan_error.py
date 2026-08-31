import re

with open('bot_thread.py', 'r', encoding='utf-8') as f:
    content = f.read()

target = '''                msg += f"⚡ ប្រើបញ្ជា `/infinity_grid {symbol} 10 1.0 100 <PIN>` ឬ `/scalp {symbol} 100 1.5 <PIN>` ឥឡូវនេះ!"
                
                await update.message.reply_text(msg, parse_mode="Markdown")
            except Exception as e:
                await update.message.reply_text(f"❌ មានបញ្ហាក្នុងការស្កេនទីផ្សារ: {e}")'''

replacement = '''                msg += f"⚡ ប្រើបញ្ជា `/infinity_grid {symbol} 10 1.0 100 <PIN>` ឬ `/scalp {symbol} 100 1.5 <PIN>` ឥឡូវនេះ!"
                
                try:
                    await update.message.reply_text(msg, parse_mode="Markdown")
                except Exception as markdown_err:
                    print(f"Markdown error in /scan: {markdown_err}. Falling back to plain text.")
                    await update.message.reply_text(msg)
            except Exception as e:
                await update.message.reply_text(f"❌ មានបញ្ហាក្នុងការស្កេនទីផ្សារ: {e}")'''

if 'markdown_err' not in content:
    content = content.replace(target, replacement)
    with open('bot_thread.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched /scan command")
else:
    print("Already patched")
