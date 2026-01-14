"""
Test script to verify database queries work correctly after migration
"""
import sqlite3
import pandas as pd
import time

# Connect to the database
conn = sqlite3.connect('keogh.db', check_same_thread=False)
cursor = conn.cursor()

print("=" * 60)
print("DATABASE MIGRATION VERIFICATION TEST")
print("=" * 60)

# Test 1: Verify table exists and get row count
print("\n[Test 1] Checking ddg_info table...")
cursor.execute("SELECT COUNT(*) FROM ddg_info;")
row_count = cursor.fetchone()[0]
print(f"  Total rows in ddg_info: {row_count:,}")

# Test 2: Verify indices exist
print("\n[Test 2] Checking indices...")
cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='ddg_info';")
indices = cursor.fetchall()
print(f"  Found {len(indices)} indices:")
for idx in indices:
    print(f"    - {idx[0]}")

# Test 3: Sample query (similar to what the app does)
print("\n[Test 3] Testing sample query performance...")
test_pdb = ['1UOL', '2FEJ']  # Sample PDB values
placeholders = ','.join('?' * len(test_pdb))
query = f"""
    SELECT ddg
    FROM ddg_info
    WHERE pdb IN ({placeholders})
    LIMIT 10
"""
start_time = time.time()
cursor.execute(query, test_pdb)
results = cursor.fetchall()
elapsed = time.time() - start_time
print(f"  Query returned {len(results)} rows in {elapsed:.4f} seconds")

# Test 4: Complex query with multiple filters
print("\n[Test 4] Testing complex filtered query...")
query_complex = f"""
    SELECT *
    FROM ddg_info
    WHERE pdb IN ({placeholders})
    AND pdb_residual = ?
    LIMIT 5
"""
start_time = time.time()
cursor.execute(query_complex, (*test_pdb, 100))
columns = [description[0] for description in cursor.description]
results = cursor.fetchall()
elapsed = time.time() - start_time
print(f"  Query returned {len(results)} rows in {elapsed:.4f} seconds")
if results:
    print(f"  Sample row: {dict(zip(columns, results[0]))}")

# Test 5: Verify data integrity
print("\n[Test 5] Verifying data integrity...")
cursor.execute("SELECT COUNT(DISTINCT pdb) FROM ddg_info;")
unique_pdbs = cursor.fetchone()[0]
print(f"  Unique PDB entries: {unique_pdbs:,}")

cursor.execute("SELECT MIN(ddg), MAX(ddg), AVG(ddg) FROM ddg_info;")
min_ddg, max_ddg, avg_ddg = cursor.fetchone()
print(f"  DDG range: {min_ddg:.2f} to {max_ddg:.2f} (avg: {avg_ddg:.2f})")

conn.close()

print("\n" + "=" * 60)
print("ALL TESTS COMPLETED SUCCESSFULLY!")
print("=" * 60)
