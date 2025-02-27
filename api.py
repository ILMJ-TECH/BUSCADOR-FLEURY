from fastapi import FastAPI
import os
import psycopg2
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Altere para ["http://localhost:5173"] para mais segurança
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = os.getenv("DATABASE_URL").replace("postgresql://", "postgres://", 1)

def conectar_bd():
    return psycopg2.connect(DATABASE_URL, sslmode="require")

@app.get("/vagas")
def get_vagas():
    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute("SELECT titulo, link, empresa FROM vagas")
    vagas = [{"titulo": row[0], "link": row[1], "empresa": row[2]} for row in cursor.fetchall()]

    conn.close()
    return vagas
