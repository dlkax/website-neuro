from utils.database import get_db

conn = get_db()

conn.execute("""
UPDATE users
SET role = 'Fundador'
WHERE username = 'atlas'
""")

conn.commit()
conn.close()

print("Cargo atualizado!")