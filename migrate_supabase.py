import os
import psycopg2

host = "aws-0-ap-southeast-1.pooler.supabase.com"
port = 5432
user = "postgres.tgqvtmrbwefuouegtsbw"
password = "Theara@@@90"
dbname = "postgres"

schema_file = os.path.join("backend", "supabase", "schema.sql")
with open(schema_file, "r", encoding="utf-8") as f:
    sql = f.read()

print("Connecting to Supabase PostgreSQL...")
conn = psycopg2.connect(
    host=host,
    port=port,
    user=user,
    password=password,
    dbname=dbname,
    connect_timeout=15,
)
conn.autocommit = True
cur = conn.cursor()

print("Applying schema to Supabase...")
# Execute statements
cur.execute(sql)
print("Schema successfully executed!")

# Verify tables created
cur.execute("""
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = 'public'
    ORDER BY table_name;
""")
tables = [row[0] for row in cur.fetchall()]
print(f"Verified {len(tables)} public tables in Supabase:")
for t in tables:
    print(f"  - {t}")

conn.close()

