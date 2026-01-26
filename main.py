# main.py
from server import Server
from client import Client


def menu_cliente(client_app: Client):
    """Menu após o cliente estar conectado."""
    while True:
        print("\n===== MENU DO CLIENTE =====")
        print("1 - Enviar mensagem (TCP)")
        print("2 - Enviar arquivo (UDP)")
        print("3 - Verificar conexão")
        print("0 - Desconectar e voltar")
        opc = input("Escolha: ").strip()

        if opc == "0":
            client_app.desconectar_tcp()
            break

        elif opc == "1":
            msg = input("Digite a mensagem: ")
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
            caminho = input("Caminho do arquivo: ").strip()
            if caminho:
                client_app.enviar_arquivo_udp(caminho)

        elif opc == "3":
            if client_app.esta_conectado():
                print("✓ Ainda conectado ao servidor.")
            else:
                print("✗ Conexão perdida com o servidor.")
                break
        else:
            print("Opção inválida.")


def main():
    while True:
        print("\n=============================")
        print("   Comunikate - TCP & UDP")
        print("=============================")
        print("1 - Conectar a um servidor")
        print("2 - Iniciar servidor")
        print("0 - Sair")

        op = input("\nEscolha: ").strip()

        if op == "0":
            print("Saindo...")
            break

        elif op == "1":
            client_app = Client()
            if client_app.escolher_e_conectar():
                print("✓ Conectado com sucesso!")
                menu_cliente(client_app)
            else:
                print("✗ Não foi possível conectar ao servidor.")

        elif op == "2":
            nome_servidor = input("Nome do servidor (Enter para 'Servidor'): ").strip()
            if not nome_servidor:
                nome_servidor = "Servidor"
            
            print(f"\n[Iniciando {nome_servidor}]")
            print("Porta TCP: 5000 (mensagens)")
            print("Porta UDP: 5001 (arquivos)")
            print("\nPressione Ctrl+C para parar.\n")
            Server.criar_servidor(nome_servidor)

        else:
            print("✗ Opção inválida.\n")


if __name__ == "__main__":
    main()
