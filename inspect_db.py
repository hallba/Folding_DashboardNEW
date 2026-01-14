import sqlite3

conn = sqlite3.connect('keogh.db')
cursor = conn.cursor()

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print('Tables:', tables)

# Get ddg_info schema
cursor.execute("PRAGMA table_info(ddg_info);")
schema = cursor.fetchall()
print('\nddg_info schema:')
for col in schema:
    print(f"  {col[1]} ({col[2]})")

# Get row count
cursor.execute("SELECT COUNT(*) FROM ddg_info;")
print(f'\nRow count: {cursor.fetchone()[0]:,}')

# Get sample row
cursor.execute("SELECT * FROM ddg_info LIMIT 1;")
sample = cursor.fetchone()
print(f'\nSample row: {sample}')

# Check for indices
cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='index' AND tbl_name='ddg_info';")
indices = cursor.fetchall()
print(f'\nIndices on ddg_info:')
for idx in indices:
    print(f"  {idx[0]}: {idx[1]}")

conn.close()
