# main.py
import socket
import time
from server import Server
from client import Client

DISCOVERY_PORT = 54545
ENC = "utf-8"

def descobrir_servidores(timeout=3.0):
    """Escuta broadcasts na rede local e retorna lista de servidores."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.settimeout(timeout)

    try:
        sock.bind(("", DISCOVERY_PORT))
    except OSError as e:
        print(f"[DISCOVERY] Erro ao bindar porta {DISCOVERY_PORT}: {e}")
        sock.close()
        return []

    print(f"[DISCOVERY] Procurando servidores por {timeout} segundos...")
    encontrados = {}

    start = time.time()
    while time.time() - start < timeout:
        try:
            data, addr = sock.recvfrom(1024)
        except socket.timeout:
            break
        except Exception as e:
            print(f"[DISCOVERY] Erro ao receber: {e}")
            break
        else:
            try:
                decoded = data.decode(ENC)
                nome, ip, porta_str = decoded.split("|")
                porta = int(porta_str)
            except Exception:
                continue

            # Usa (ip, porta) como chave para evitar duplicados
            key = (ip, porta)
            encontrados[key] = {"nome": nome, "ip": ip, "port": porta}

    sock.close()
    return list(encontrados.values())

def escolher_servidor():
    servidores = descobrir_servidores()
    if not servidores:
        print("Nenhum servidor encontrado na rede.")
        return None

    print("\n=== Servidores disponíveis na rede ===")
    for i, s in enumerate(servidores, start=1):
        print(f"{i} - {s['nome']} ({s['ip']}:{s['port']})")

    try:
        idx = int(input("Escolha um servidor: ").strip()) - 1
        if 0 <= idx < len(servidores):
            return servidores[idx]
        else:
            print("Opção inválida.")
            return None
    except ValueError:
        print("Entrada inválida.")
        return None





def menu_cliente(client_app: Client):
    """Menu após o cliente estar conectado."""
    while True:
        print("\n===== MENU DO CLIENTE =====")
        print("1 - Enviar mensagem")
        print("2 - Verificar se ainda está conectado")
        print("0 - Desconectar e voltar")
        opc = input("Escolha: ").strip()

        if opc == "0":
            client_app.desconectar_tcp()
            break

        elif opc == "1":
            msg = input("Mensagem (digite 'sair' para encerrar no servidor): ")
            if not msg:
                continue

            if not client_app.enviar_tcp(msg):
                print("Falha ao enviar. Provavelmente desconectado.")
                break

            resposta = client_app.receber_tcp()
            if resposta is None:
                print("Servidor encerrou a conexão.")
                break

            print(f"[SERVIDOR] {resposta}")

        elif opc == "2":
            if client_app.esta_conectado():
                print("Ainda conectado ao servidor.")
            else:
                print("Conexão perdida com o servidor.")
                break
        else:
            print("Opção inválida.")


def main():
    while True:
        print("========================")
        print(" Bem-vindo ao Comunikate!")
        print("========================")
        print("Digite:")
        print("1 - Entrar em um servidor")
        print("2 - Criar um servidor")
        print("0 - Sair")

        op = input("Insira: ").strip()

        if op == "0":
            print("Saindo...")
            break

        elif op == "1":
            escolhido = escolher_servidor()
            if not escolhido:
                continue

            host = escolhido["ip"]
            port = int(escolhido["port"])

            client_app = Client(host=host, tcp_port=port)
            client_app.conectar_tcp()

            if client_app.esta_conectado():
                print(f"Conectado a {host}:{port}.")
                menu_cliente(client_app)
            else:
                print("Não foi possível conectar ao servidor.")

        elif op == "2":
            print("\nCriando servidor TCP...")
            # Bloqueante até Ctrl+C
            Server.criar_servidor()

        else:
            print("Opção inválida. Tente novamente.\n")


if __name__ == "__main__":
    main()
