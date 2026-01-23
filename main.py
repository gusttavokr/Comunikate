from server import Server
from client import Client
from server_save import carregar_servidores

def escolher_servidor():
    """Lista servidores salvos com nome e permite escolher um."""
    servidores = carregar_servidores()
    if not servidores:
        print("Nenhum servidor registrado ainda.")
        print("Dica: em outra máquina, use a opção 'Criar servidor'.")
        return None

    print("\n=== Servidores disponíveis ===")
    for i, s in enumerate(servidores, start=1):
        print(f"{i} - {s['nome']} ({s['ip']}:{s['port']})")

    try:
        idx = int(input("Escolha um servidor: ").strip())
        idx -= 1
        if 0 <= idx < len(servidores):
            return servidores[idx]
        else:
            print("Opção inválida.")
            return None
    except ValueError:
        print("Entrada inválida.")
        return None
