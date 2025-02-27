import psycopg2
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://vagas_1ukx_user:gyKqtHfa24cGoojv7SYvVrfbUciqxZtq@dpg-cv06f13tq21c73920oc0-a.oregon-postgres.render.com/vagas_1ukx")

def conectar_bd():
    return psycopg2.connect(DATABASE_URL, sslmode="require")

def criar_tabela():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vagas (
            id SERIAL PRIMARY KEY,
            titulo TEXT UNIQUE,
            link TEXT UNIQUE,
            empresa TEXT
        )
    """)
    conn.commit()
    conn.close()

criar_tabela()

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("user-agent=Mozilla/5.0")
service = Service(ChromeDriverManager().install())

def scrape_vagas():
    conn = conectar_bd()
    cursor = conn.cursor()
    
    driver = webdriver.Chrome(service=service, options=options)
    empresa = "Fleury"
    print("Carregando vagas do Grupo Fleury...")
    url = "https://www.vagas.com.br/vagas-de-Fleury"
    driver.get(url)
    driver.implicitly_wait(5)

    try:
        while True:
            try:
                botao = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "maisVagas")))
                driver.execute_script("arguments[0].scrollIntoView();", botao)
                time.sleep(1)
                driver.execute_script("arguments[0].click();", botao)
                print("[+] Carregando mais vagas...")
                time.sleep(3)
            except (NoSuchElementException, TimeoutException, ElementClickInterceptedException):
                print("[+] Todas as vagas foram carregadas.")
                break

        base_url = "https://www.vagas.com.br"
        vagas = driver.find_elements(By.CSS_SELECTOR, "h2.cargo a")

        total_vagas = 0
        for vaga in vagas:
            titulo = vaga.text.strip()
            link = vaga.get_attribute("href")
            if link.startswith("/"):
                link = base_url + link

            cursor.execute("INSERT INTO vagas (titulo, link, empresa) VALUES (%s, %s, %s) ON CONFLICT (titulo) DO NOTHING",
                           (titulo, link, empresa))
            total_vagas += 1

        conn.commit()
        print(f"[+] Total de vagas coletadas: {total_vagas}")

    finally:
        driver.quit()
        conn.close()

scrape_vagas()
