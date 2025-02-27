import sqlite3
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException

# Configuração do banco de dados SQLite
db_path = os.path.abspath("vagas.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Criar tabela se não existir
cursor.execute("""
    CREATE TABLE IF NOT EXISTS vagas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT UNIQUE,
        link TEXT UNIQUE,
        empresa TEXT
    )
""")
conn.commit()

# Configurar o navegador Selenium
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Rodar em modo headless (sem abrir o navegador)
options.add_argument("user-agent=Mozilla/5.0")  # Definir User-Agent
options.add_argument("--start-maximized")  # Maximizar janela
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

def remover_iframes():
    driver.execute_script("""
        var iframes = document.getElementsByTagName('iframe');
        for (var i = 0; i < iframes.length; i++) {
            iframes[i].parentNode.removeChild(iframes[i]);
        }
    """)

total_vagas_encontradas = 0
INTERVALO_VERIFICACAO = 600

def carregar_vagas_vagas():
    global total_vagas_encontradas
    empresa = "Fleury"
    print("Carregando vagas do Grupo Fleury...")
    url = "https://www.vagas.com.br/vagas-de-Fleury"
    driver.get(url)
    driver.implicitly_wait(5)

    while True:
        try:
            remover_iframes()  # Remove iframes antes de clicar
            botao = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "maisVagas")))
            driver.execute_script("arguments[0].scrollIntoView();", botao)
            time.sleep(1)  # Pequeno delay para evitar erro
            driver.execute_script("arguments[0].click();", botao)
            print("[+] Carregando mais vagas...")
            time.sleep(3)
        except (NoSuchElementException, TimeoutException, ElementClickInterceptedException):
            print("[+] Todas as vagas foram carregadas ou botão inacessível.")
            break

    base_url = "https://www.vagas.com.br"
    vagas = driver.find_elements(By.CSS_SELECTOR, "h2.cargo a")

    total_vagas = 0
    for vaga in vagas:
        titulo = vaga.text.strip()
        link = vaga.get_attribute("href")
        if link.startswith("/"):
            link = base_url + link

        cursor.execute("INSERT OR IGNORE INTO vagas (titulo, link, empresa) VALUES (?, ?, ?)", (titulo, link, empresa))
        print(f"[+] {titulo} - {link} ({empresa})")
        total_vagas += 1

    total_vagas_encontradas += total_vagas
    print(f"[+] Total de vagas coletadas do Grupo Fleury: {total_vagas}")


    
def Countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(f"\r[+] Próxima verificação em {timer}", end="", flush=True)
        time.sleep(1)
        t -= 1
    print("\n")

# Executar as funções de scraping
carregar_vagas_vagas()


Countdown(300)

while True:
    print("\n[+] Iniciando nova verificação...")

    carregar_vagas_vagas()
    print("[+] Verificação concluída. Aguardando próxima execução...\n")
    Countdown(INTERVALO_VERIFICACAO)

# Salvar e fechar conexões
conn.commit()
conn.close()
driver.quit()

print("[+] Scraping finalizado e dados salvos no banco de dados!")

