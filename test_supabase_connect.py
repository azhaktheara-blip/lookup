import psycopg2

host = "aws-0-ap-southeast-1.pooler.supabase.com"
port = 5432
user = "postgres.tgqvtmrbwefuouegtsbw"
dbname = "postgres"

passwords_to_try = [
    "Theara@@@90",
    "[Theara@@@90]",
]

connected = False
for pwd in passwords_to_try:
    try:
        print(f"Attempting connect with password: {pwd[:3]}*** ...")
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=pwd,
            dbname=dbname,
            connect_timeout=10,
        )
        print("Connected successfully!")
        cur = conn.cursor()
        cur.execute("SELECT version();")
        v = cur.fetchone()
        print("PostgreSQL version:", v[0])
        conn.close()
        connected = True
        break
    except Exception as e:
        print("Connection failed:", e)

if not connected:
    # Also test port 6543 (session mode)
    print("Testing port 6543...")
    for pwd in passwords_to_try:
        try:
            conn = psycopg2.connect(
                host=host,
                port=6543,
                user=user,
                password=pwd,
                dbname=dbname,
                connect_timeout=10,
            )
            print("Connected successfully on port 6543!")
            conn.close()
            connected = True
            break
        except Exception as e:
            print("Port 6543 failed:", e)

