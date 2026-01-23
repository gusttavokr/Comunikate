# server.py
import socket
import threading
from server_save import registrar_servidor

TCP_PORT = 5000
BUFFER = 4096
ENC = "utf-8"

class Server:
    @staticmethod
    def criar_servidor():
        """Cria um servidor TCP que escuta e registra nome/IP/porta."""
        nome = input("Nome do servidor: ").strip()
        if not nome:
            nome = "Servidor sem nome"

        # Descobre IP local usado para conexões
        temp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            temp.connect(("8.8.8.8", 80))  # só para descobrir a interface
            ip_local = temp.getsockname()[0]
        except Exception:
            ip_local = "127.0.0.1"
        finally:
            temp.close()

        registrar_servidor(nome, ip_local, TCP_PORT)
        print(f"Servidor '{nome}' registrado em {ip_local}:{TCP_PORT}")

        print("Servidor TCP iniciado...")
        print(f"Aguardando conexões na porta {TCP_PORT}...")

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            server_socket.bind(("", TCP_PORT))
            server_socket.listen(5)
            print("Servidor pronto para aceitar clientes.")

            while True:
                try:
                    conn, addr = server_socket.accept()
                    print(f"Cliente conectado: {addr}")
                    t = threading.Thread(
                        target=Server._handle_client,
                        args=(conn, addr),
                        daemon=True,
                    )
                    t.start()
                except KeyboardInterrupt:
                    print("\nEncerrando servidor...")
                    break
        finally:
            server_socket.close()
            print("Servidor encerrado.")
