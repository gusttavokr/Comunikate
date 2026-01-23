# server_registry.py
import json
from pathlib import Path

REGISTRY_FILE = Path("servers.json")

def carregar_servidores():
    if not REGISTRY_FILE.exists():
        return []
    try:
        texto = REGISTRY_FILE.read_text(encoding="utf-8").strip()
        if not texto:
            return []  # arquivo vazio
        return json.loads(texto)
    except json.JSONDecodeError:
        print("WARNING: servers.json inválido. Ignorando conteúdo.")
        return []
    except Exception as e:
        print(f"Erro ao ler servers.json: {e}")
        return []

def salvar_servidores(lista):
    try:
        REGISTRY_FILE.write_text(
            json.dumps(lista, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
    except Exception as e:
        print(f"Erro ao salvar registro de servidores: {e}")

def registrar_servidor(nome, ip, porta):
    servidores = carregar_servidores()
    servidores.append({"nome": nome, "ip": ip, "port": porta})
    salvar_servidores(servidores)
    print(f"[REGISTRY] Registrado: {nome} ({ip}:{porta})")
