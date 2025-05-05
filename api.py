from fastapi import FastAPI
import os
import json
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

JSON_FILE = "urls.json"

def carregar_dados():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return []

@app.get("/vagas")
def get_vagas():
    vagas = carregar_dados()
    return vagas
