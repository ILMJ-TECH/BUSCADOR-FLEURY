import os
import time
import json
import tempfile
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

JSON_FILE = "urls.json"

def carregar_dados():
    if os.path.exists(JSON_FILE):
        try:
            with open(JSON_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, UnicodeDecodeError):
            print("[!] Erro ao carregar dados. Criando novo arquivo.")
            salvar_dados([])
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
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--remote-debugging-port=0")

        user_data_dir = tempfile.mkdtemp()
        options.add_argument(f"--user-data-dir={user_data_dir}")

        service = Service("/usr/bin/chromedriver")  
        return webdriver.Chrome(service=service, options=options)
    except Exception as e:
        print(f"[!] Erro ao configurar o driver: {e}")
        raise

def scrape_vagas():
    vagas_existentes = carregar_dados()
    vagas_existentes_set = {(vaga["titulo"], vaga["link"]) for vaga in vagas_existentes}

    driver = configurar_driver()
    print("Carregando vagas do Grupo Fleury...")

    try:
        url = "https://www.vagas.com.br/vagas-de-Fleury"
        driver.get(url)
        time.sleep(3)

        vagas = driver.find_elements(By.CSS_SELECTOR, "h2.cargo a")

        while True:
            try:
                print("[DEBUG] Procurando botão 'maisVagas'...")
                botao = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.ID, "maisVagas"))
                )

                if botao.get_attribute("disabled"):
                    print("[INFO] Botão 'maisVagas' desabilitado. Fim da lista.")
                    break

                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao)
                time.sleep(1)
                driver.execute_script("arguments[0].click();", botao)
                time.sleep(2)

                vagas_att = driver.find_elements(By.CSS_SELECTOR, "h2.cargo a")
                if len(vagas) == len(vagas_att):
                    print("[INFO] Nenhuma nova vaga carregada.")
                    break

                vagas = vagas_att
                print("[+] Carregando mais vagas...")
                time.sleep(4.5)

            except TimeoutException:
                print("[INFO] Tempo esgotado. Todas as vagas provavelmente foram carregadas.")
                break

        novas_vagas = []
        base_url = "https://www.vagas.com.br"

        for vaga in vagas:
            titulo = vaga.text.strip()
            link = vaga.get_attribute("href")
            if link and not link.startswith("http"):
                link = base_url + link
            if (titulo, link) not in vagas_existentes_set:
                novas_vagas.append({"titulo": titulo, "link": link})
                print("Adicionando vaga -> " + titulo)
                vagas_existentes_set.add((titulo, link))

        vagas_existentes.extend(novas_vagas)
        salvar_dados(vagas_existentes)
        print(f"[+] Total de novas vagas coletadas: {len(novas_vagas)}")

    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_vagas()
