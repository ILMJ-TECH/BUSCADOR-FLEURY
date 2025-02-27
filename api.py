from fastapi import FastAPI
import psycopg2
import os

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://vagas_1ukx_user:gyKqtHfa24cGoojv7SYvVrfbUciqxZtq@dpg-cv06f13tq21c73920oc0-a.oregon-postgres.render.com/vagas_1ukx")

def conectar_bd():
    return psycopg2.connect(DATABASE_URL, sslmode="require")

@app.get("/vagas")
def get_vagas():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT titulo, link, empresa FROM vagas ORDER BY id DESC")
    vagas = cursor.fetchall()
    conn.close()

    return [{"titulo": v[0], "link": v[1], "empresa": v[2]} for v in vagas]
