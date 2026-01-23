from server import Server
from client import Client
from server_registry import carregar_servidores

def escolher_servidor():
    servidores = carregar_servidores()
    print(f"[DEBUG] servidores carregados: {servidores}")  # debug

    if not servidores:
        print("Nenhum servidor registrado ainda.")
        print("Dica: em outra máquina, use a opção 'Criar servidor'.")
        return None

    print("\n=== Servidores disponíveis ===")
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
