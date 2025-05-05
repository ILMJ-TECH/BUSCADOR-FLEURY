import os
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException

JSON_FILE = "urls.json"

def carregar_dados():
    if os.path.exists(JSON_FILE):
        try:
            with open(JSON_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, UnicodeDecodeError):
            print("[!] Erro ao carregar dados: arquivo JSON corrompido ou com codificação inválida. Criando um novo.")
            salvar_dados([])  
            return []
    return []

def salvar_dados(dados):
    try:
        with open(JSON_FILE, "w", encoding="utf-8") as file:
            json.dump(dados, file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"[!] Erro ao salvar dados: {e}")

def configurar_driver():
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        service = Service("/usr/bin/chromedriver")  # Caminho fixo no container
        return webdriver.Chrome(service=service, options=options)
    except Exception as e:
        print(f"[!] Erro ao configurar o driver: {e}")
        raise

def scrape_vagas():
    vagas_existentes = carregar_dados()
    vagas_existentes_set = {(vaga["titulo"], vaga["link"]) for vaga in vagas_existentes}

    driver = configurar_driver()
    print("Carregando vagas do Grupo Fleury...")
    url = "https://www.vagas.com.br/vagas-de-Fleury"
    driver.get(url)
    time.sleep(3)

    try:
        while True:
            try:
                print("[DEBUG] Tentando encontrar o botão 'maisVagas'...")
                botao = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "maisVagas"))
                )
                print("[DEBUG] Botão 'maisVagas' encontrado. Tentando clicar...")
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao)
                time.sleep(1)

                driver.execute_script("arguments[0].click();", botao)

                print("[+] Carregando mais vagas...")
                time.sleep(3)
            except TimeoutException:
                print("[INFO] Botão 'maisVagas' não encontrado. Todas as vagas foram carregadas.")
                break

        base_url = "https://www.vagas.com.br"
        vagas = driver.find_elements(By.CSS_SELECTOR, "h2.cargo a")

        novas_vagas = []
        for vaga in vagas:
            titulo = vaga.text.strip()
            link = vaga.get_attribute("href")
            if link and not link.startswith("http"):
                link = base_url + link

            if (titulo, link) not in vagas_existentes_set:
                novas_vagas.append({"titulo": titulo, "link": link})
                vagas_existentes_set.add((titulo, link))

        vagas_existentes.extend(novas_vagas)
        salvar_dados(vagas_existentes)
        print(f"[+] Total de novas vagas coletadas: {len(novas_vagas)}")

    finally:
        driver.quit()

if __name__ == "__main__":
    tentativas = 0
    max_tentativas = 5
    while tentativas < max_tentativas:
        print("[*] Iniciando scraping...")
        try:
            scrape_vagas()
            tentativas = 0  
        except Exception as e:
            tentativas += 1
            print(f"[!] Erro durante scraping: {e}")
            if tentativas >= max_tentativas:
                print("[!] Número máximo de tentativas atingido. Encerrando.")
                break
        print("[*] Aguardando 2 minutos para a próxima execução...\n")
        time.sleep(120)
