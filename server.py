import socket
import threading

TCP_PORT = 5000
UDP_PORT = 5001
DISCOVERY_PORT = 5002
BUFFER = 4096
ENC = "utf-8"

def _handle_tcp_client(conn, addr):
    """Thread para cada cliente TCP (sem autenticação, só echo/placeholder)."""
    try:
        print(f"[TCP SERVER] Nova conexão de {addr}")

        while True:
            data = conn.recv(BUFFER)
            if not data:
                print(f"[TCP SERVER] Cliente {addr} desconectou.")
                break

            msg = data.decode(ENC).strip()
            print(f"[TCP SERVER] Mensagem de {addr}: {msg}")

            if msg == "QUIT":
                print(f"[TCP SERVER] Cliente {addr} pediu para sair.")
                break

            # Por enquanto só ecoa; depois você troca pela lógica de arquivo/chat
            resposta = f"ECO: {msg}\n"
            conn.sendall(resposta.encode(ENC))

    finally:
        conn.close()
        print(f"[TCP SERVER] Conexão encerrada com {addr}")


def _tcp_server_loop():
    """Loop principal do servidor TCP."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_sock:
        tcp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcp_sock.bind(("", TCP_PORT))
        tcp_sock.listen(5)
        print(f"[TCP SERVER] Ouvindo em 0.0.0.0:{TCP_PORT}")

        while True:
            conn, addr = tcp_sock.accept()
            t = threading.Thread(target=_handle_tcp_client, args=(conn, addr), daemon=True)
            t.start()


# def _udp_server_loop():
#     """Loop do servidor UDP (apenas eco para teste)."""
#     with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_sock:
#         udp_sock.bind(("", UDP_PORT))
#         print(f"[UDP SERVER] Ouvindo em 0.0.0.0:{UDP_PORT}")

#         while True:
#             data, addr = udp_sock.recvfrom(BUFFER)
#             print(f"[UDP SERVER] Recebido de {addr}: {data!r}")
#             udp_sock.sendto(data, addr)  # eco simples


def _discovery_server_loop(server_name: str):
    """Loop de descoberta: responde a broadcasts com info do servidor.

    Protocolo simples:
    - Cliente envia:  "DISCOVER_COMUNIKATE"
    - Servidor responde: "COMUNIKATE_SERVER;<nome>;<tcp_port>"
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as disc_sock:
        disc_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        disc_sock.bind(("", DISCOVERY_PORT))
        print(f"[DISCOVERY SERVER] Ouvindo broadcast em 0.0.0.0:{DISCOVERY_PORT}")

        while True:
            data, addr = disc_sock.recvfrom(BUFFER)
            msg = data.decode(ENC).strip()
            if msg == "DISCOVER_COMUNIKATE":
                resposta = f"COMUNIKATE_SERVER;{server_name};{TCP_PORT}\n"
                disc_sock.sendto(resposta.encode(ENC), addr)


class Server:

    @staticmethod
    def criar_servidor():
        """
        Cria um servidor com:
        - TCP: recebe mensagens e ecoa de volta
        - UDP: recebe datagramas e ecoa de volta
        - DISCOVERY: responde a broadcasts de descoberta de servidores
        """
        print("=== CRIAR SERVIDOR ===")
        server_name = input("Nome do servidor (padrão: Servidor Comunikate): ").strip() or "Servidor Comunikate"
        print(f"Servidor '{server_name}' criado.")
        print(f"Servidor TCP na porta {TCP_PORT}, UDP na porta {UDP_PORT} e discovery na porta {DISCOVERY_PORT}.")
        print("Aguardando conexões... (Ctrl+C para encerrar)")

        t_tcp = threading.Thread(target=_tcp_server_loop, daemon=True)
        # t_udp = threading.Thread(target=_udp_server_loop, daemon=True)
        t_disc = threading.Thread(target=_discovery_server_loop, args=(server_name,), daemon=True)

        t_tcp.start()
        # t_udp.start()
        t_disc.start()

        try:
            while True:
                pass
        except KeyboardInterrupt:
            print("\n[SERVER] Encerrando servidor.")
