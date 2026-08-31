import re

# 1. Fix get_db_connection in database.py
with open('database.py', 'r', encoding='utf-8') as f:
    db_content = f.read()

target = 'DB_FILE = os.path.join(BASE_DIR, "bot_database.db")'
replacement = '''DB_FILE = os.path.join(BASE_DIR, "bot_database.db")

def get_db_connection():
    return sqlite3.connect(DB_FILE, timeout=15.0)
'''

if 'def get_db_connection():' not in db_content:
    db_content = db_content.replace(target, replacement)
    with open('database.py', 'w', encoding='utf-8') as f:
        f.write(db_content)
    print("Fixed get_db_connection in database.py")
else:
    print("get_db_connection already exists.")


# 2. Add generate_response alias to ai_engine.py
with open('ai_engine.py', 'r', encoding='utf-8') as f:
    ai_content = f.read()
    
if 'def generate_response' not in ai_content:
    target_method = '''    def analyze_opportunity(self, user_input: str) -> str:
        """Legacy stateless call (used mostly by automated background tasks)"""
        return self.chat_with_user(user_input, history=[])'''
        
    replacement_method = '''    def analyze_opportunity(self, user_input: str) -> str:
        """Legacy stateless call (used mostly by automated background tasks)"""
        return self.chat_with_user(user_input, history=[])
        
    def generate_response(self, user_input: str, user_lang: str = "auto") -> str:
        """Alias for background tasks that might pass lang"""
        # We can append language instruction if needed, but for now just pass to analyze_opportunity
        prompt = user_input
        if user_lang and user_lang != "auto":
            prompt += f"\\n\\nPlease reply in {user_lang} language."
        return self.analyze_opportunity(prompt)'''
        
    ai_content = ai_content.replace(target_method, replacement_method)
    with open('ai_engine.py', 'w', encoding='utf-8') as f:
        f.write(ai_content)
    print("Added generate_response to ai_engine.py")
else:
    print("generate_response already exists.")
