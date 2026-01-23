# server_registry.py
import json
from pathlib import Path

REGISTRY_FILE = Path("servers.json")

def carregar_servidores():
    if not REGISTRY_FILE.exists():
        return []
    try:
        with REGISTRY_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def salvar_servidores(lista):
    try:
        with REGISTRY_FILE.open("w", encoding="utf-8") as f:
            json.dump(lista, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Erro ao salvar registro de servidores: {e}")

def registrar_servidor(nome, ip, porta):
    servidores = carregar_servidores()
    servidores.append({"nome": nome, "ip": ip, "port": porta})
    salvar_servidores(servidores)
