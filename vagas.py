import sqlite3
import os

db_path = os.path.abspath("vagas.db")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS vagas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    link TEXT NOT NULL UNIQUE,
    empresa TEXT NOT NULL
)
""")

conn.commit()
conn.close()

print("[+] Banco de dados configurado com sucesso!")