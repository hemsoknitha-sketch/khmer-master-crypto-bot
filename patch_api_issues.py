import os
import sys

def patch_database():
    file_path = "database.py"
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # In set_user_api
    old_set = """    enc_key = security.encrypt_data(api_key)
    enc_secret = security.encrypt_data(api_secret)"""
    new_set = """    enc_key = security.encrypt_data(api_key.strip())
    enc_secret = security.encrypt_data(api_secret.strip())"""
    content = content.replace(old_set, new_set)

    # In get_user_api
    old_get = """        if dec_key and dec_secret:
            return (dec_key, dec_secret)"""
    new_get = """        if dec_key and dec_secret:
            return (dec_key.strip(), dec_secret.strip())"""
    content = content.replace(old_get, new_get)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

def patch_trading_engine():
    file_path = "trading_engine.py"
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Add recvWindow to GET request query strings
    content = content.replace('query_string = f"timestamp={timestamp}"', 'query_string = f"recvWindow=60000&timestamp={timestamp}"')

    # Add recvWindow to POST requests dictionaries
    content = content.replace('"timestamp": (int(time.time() * 1000) + TIME_OFFSET)', '"recvWindow": 60000, "timestamp": (int(time.time() * 1000) + TIME_OFFSET)')

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    patch_database()
    patch_trading_engine()
    print("Patch applied successfully.")
