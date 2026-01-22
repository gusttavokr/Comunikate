import socket
import threading

TCP_PORT = 5000
UDP_PORT = 5001  # reservado para envio de arquivos via UDP
BUFFER = 4096
ENC = "utf-8"

SERVER_NAME = "Servidor Comunikate"


def _handle_tcp_client(conn, addr):
    """Thread para cada cliente TCP.

    - Se receber "HELLO_COMUNIKATE": responde com info do servidor e encerra
      (usado para descoberta via TCP).
    - Caso contrário, faz echo simples da mensagem recebida.
    """
    try:
        print(f"[TCP SERVER] Nova conexão de {addr}")

        while True:
            data = conn.recv(BUFFER)
            if not data:
                print(f"[TCP SERVER] Cliente {addr} desconectou.")
                break

            msg = data.decode(ENC).strip()
            print(f"[TCP SERVER] Mensagem de {addr}: {msg}")

            if msg == "HELLO_COMUNIKATE":
                resposta = f"COMUNIKATE_SERVER;{SERVER_NAME};{TCP_PORT}\n"
                conn.sendall(resposta.encode(ENC))
                break

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


    # Aqui no futuro você pode implementar recepção de arquivos via UDP
    # usando a porta UDP_PORT.


class Server:

    @staticmethod
    def criar_servidor():
        """
        Cria um servidor com:
        - TCP: recebe mensagens e ecoa de volta (também usado para descoberta)
        - UDP: reservado para envio/recebimento de arquivos
        """
        print("=== CRIAR SERVIDOR ===")
        global SERVER_NAME
        SERVER_NAME = input("Nome do servidor (padrão: Servidor Comunikate): ").strip() or "Servidor Comunikate"
        print(f"Servidor '{SERVER_NAME}' criado.")
        print(f"Servidor TCP na porta {TCP_PORT} e UDP (arquivos) na porta {UDP_PORT}.")
        print("Aguardando conexões... (Ctrl+C para encerrar)")

        t_tcp = threading.Thread(target=_tcp_server_loop, daemon=True)
        # t_udp = threading.Thread(target=_udp_server_loop, daemon=True)

        t_tcp.start()
        # t_udp.start()

        try:
            while True:
                pass
        except KeyboardInterrupt:
            print("\n[SERVER] Encerrando servidor.")
