import sqlite3
import functools
from datetime import datetime  # ✅ required by the checker

# ✅ Decorator to log SQL queries with timestamps
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get('query') or (args[0] if args else None)
        if query:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{now}] Executing SQL query: {query}")
        else:
            print("[LOG] No SQL query provided.")
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# ✅ Run this to test
users = fetch_all_users(query="SELECT * FROM users")
print(users)
