# server.py
import socket
import threading
import time

TCP_PORT = 5000
DISCOVERY_PORT = 54545     # porta UDP para discovery
BUFFER = 4096
ENC = "utf-8"

class Server:
    @staticmethod
    def criar_servidor():
        nome = input("Nome do servidor: ").strip()
        if not nome:
            nome = "Servidor sem nome"

        # Descobrir IP local (para anunciar)
        temp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            temp.connect(("8.8.8.8", 80))
            ip_local = temp.getsockname()[0]
        except Exception:
            ip_local = "127.0.0.1"
        finally:
            temp.close()

        print(f"Servidor '{nome}' em {ip_local}:{TCP_PORT}")

        # Inicia thread de broadcast UDP
        t_discovery = threading.Thread(
            target=Server._discovery_broadcast_loop,
            args=(nome, ip_local, TCP_PORT),
            daemon=True,
        )
        t_discovery.start()

        # --- servidor TCP normal ---
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

    @staticmethod
    def _discovery_broadcast_loop(nome, ip, porta):
        """Envia periodicamente anúncios UDP na rede local."""
        msg = f"{nome}|{ip}|{porta}".encode(ENC)

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        addr = ("<broadcast>", DISCOVERY_PORT)

        print(f"[DISCOVERY] Anunciando em broadcast na porta {DISCOVERY_PORT}...")
        try:
            while True:
                sock.sendto(msg, addr)
                time.sleep(1.0)  # 1 anúncio por segundo
        except Exception as e:
            print(f"[DISCOVERY] Erro no broadcast: {e}")
        finally:
            sock.close()

    @staticmethod
    def _handle_client(conn, addr):
        # ... mesmo _handle_client que você já tinha ...
        try:
            while True:
                data = conn.recv(BUFFER)
                if not data:
                    break
                msg = data.decode(ENC)
                print(f"[{addr[0]}:{addr[1]}] {msg}")

                if msg.lower().strip() == "fechar":
                    conn.send("encerrando".encode(ENC))
                    break
                else:
                    conn.send("recebido".encode(ENC))
        finally:
            conn.close()
