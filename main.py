import threading
import time
from scraper import scrape_vagas
from api import app
import uvicorn

# Função para rodar o scraper em um loop
def run_scraper():
    while True:
        print("[*] Iniciando scraping...")
        scrape_vagas()
        print("[*] Aguardando 2 minutos para a próxima execução...")
        time.sleep(120)

# Função para rodar a API
def run_api():
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Threads para rodar scraper e API simultaneamente
if __name__ == "__main__":
    scraper_thread = threading.Thread(target=run_scraper)
    scraper_thread.daemon = True  # Permite encerrar o programa ao fechar a API
    scraper_thread.start()

    run_api()