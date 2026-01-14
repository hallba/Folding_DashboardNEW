import sqlite3

# Connect to the database
conn = sqlite3.connect('keogh.db')
cursor = conn.cursor()

print("Adding indices to keogh.db for optimal query performance...")

# Add indices on frequently queried columns
indices = [
    ('idx_pdb', 'CREATE INDEX IF NOT EXISTS idx_pdb ON ddg_info(pdb);'),
    ('idx_pdb_residual', 'CREATE INDEX IF NOT EXISTS idx_pdb_residual ON ddg_info(pdb_residual);'),
    ('idx_mut_from', 'CREATE INDEX IF NOT EXISTS idx_mut_from ON ddg_info(mut_from);'),
    ('idx_mut_to', 'CREATE INDEX IF NOT EXISTS idx_mut_to ON ddg_info(mut_to);'),
    ('idx_composite', 'CREATE INDEX IF NOT EXISTS idx_composite ON ddg_info(pdb, pdb_residual, mut_from, mut_to);'),
]

for idx_name, idx_sql in indices:
    try:
        cursor.execute(idx_sql)
        print(f"[OK] Created index: {idx_name}")
    except Exception as e:
        print(f"[ERROR] Error creating {idx_name}: {e}")

conn.commit()
print("\nCommitting changes...")

# Verify indices were created
cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='ddg_info';")
existing_indices = cursor.fetchall()
print(f"\nExisting indices on ddg_info table:")
for idx in existing_indices:
    print(f"  - {idx[0]}")

conn.close()
print("\nDone! Database indices have been added.")
