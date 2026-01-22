from server import Server
from client import Client

def main():
    print("========================")
    print("Bem-vindo ao Comunikate!")
    print("========================")
    print("Digite:")
    print("1- Para entrar em um servidor, 2- Para criar um servidor")

    operation = int(input("Insira: "))

    if operation == 1:
        escolhido = escolher_servidor()
        if not escolhido:
            return

        client_app = Client(host=escolhido["ip"], tcp_port=escolhido["port"])
        client_app.conectar_tcp()
        # Exemplo simples: enviar uma mensagem de teste
        # client_app.enviar_tcp("Olá, servidor!")

    if operation == 2:
        Server.criar_servidor()

@staticmethod
def escolher_servidor():
    print("\nProcurando servidores Comunikate na rede...")
    servidores = Client.descobrir_servidores()

    if not servidores:
        print("Nenhum servidor encontrado via broadcast.")
        return None

    print("\nServidores encontrados:")
    for idx, s in enumerate(servidores, start=1):
        print(f"{idx} - {s['name']} ({s['ip']}:{s['port']})")

    while True:
        try:
            escolha = int(input("Escolha o número do servidor: "))
            if 1 <= escolha <= len(servidores):
                return servidores[escolha - 1]
        except ValueError:
            pass
        print("Opção inválida, tente novamente.")

if __name__ == "__main__":
    main()
