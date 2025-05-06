import threading
import time
from scraper import scrape_vagas
from api import app
import uvicorn

def run_scraper():
    while True:
        print("[*] Iniciando scraping...")
        try:
            scrape_vagas()
        except Exception as e:
            print(f"[!] Erro no scraping: {e}")
        print("[*] Aguardando 2 minutos para a próxima execução...\n")
        time.sleep(120)

def run_api():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    scraper_thread = threading.Thread(target=run_scraper)
    scraper_thread.daemon = True
    scraper_thread.start()
    run_api()
