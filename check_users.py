import sqlite3

conn = sqlite3.connect("cognicare.db")
rows = conn.execute("SELECT id, email, full_name FROM users").fetchall()
for row in rows:
    print(row)
print(f"Total: {len(rows)} users")