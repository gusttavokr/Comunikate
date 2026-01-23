# main.py
from server import Server
from client import Client


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
            # Criar cliente sem IP no construtor
            client_app = Client()
            
            # Deixar o cliente escolher e conectar automaticamente
            if client_app.escolher_e_conectar():
                print(f"Conectado com sucesso!")
                menu_cliente(client_app)
            else:
                print("Não foi possível conectar ao servidor.")

        elif op == "2":
            nome_servidor = input("Digite o nome do servidor (ou Enter para usar 'Servidor TCP'): ").strip()
            if not nome_servidor:
                nome_servidor = "Servidor TCP"
            
            print(f"\nCriando servidor: {nome_servidor}")
            print("Pressione Ctrl+C para parar o servidor.")
            # Bloqueante até Ctrl+C
            Server.criar_servidor(nome_servidor)

        else:
            print("Opção inválida. Tente novamente.\n")


if __name__ == "__main__":
    main()
