# server.py
import socket
import threading

TCP_PORT = 5000
UDP_PORT = 5001
BUFFER = 4096
ENC = "utf-8"


def _handle_tcp_client(conn, addr):
    try:
        print(f"[TCP SERVER] Nova conexão: {addr}")
        while True:
            data = conn.recv(BUFFER)
            if not data:
                break
            msg = data.decode(ENC).strip()
            print(f"[TCP SERVER] Recebido de {addr}: {msg}")
            # eco simples
            conn.send(f"OK: {msg}".encode(ENC))
    except Exception as e:
        print(f"[TCP SERVER] Erro com cliente {addr}: {e}")
    finally:
        print(f"[TCP SERVER] Conexão encerrada: {addr}")
        conn.close()


def _tcp_server_loop():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # reusa porta
    server.bind(("", TCP_PORT))  # escuta em todas as interfaces
    server.listen(5)

    print(f"[SERVER] TCP ouvindo na porta {TCP_PORT}...")
    print("Aguardando conexões... (Ctrl+C para sair)")

    try:
        while True:
            conn, addr = server.accept()
            t = threading.Thread(target=_handle_tcp_client, args=(conn, addr), daemon=True)
            t.start()
    except KeyboardInterrupt:
        print("\n[SERVER] Encerrando servidor TCP.")
    finally:
        server.close()


class Server:
    @staticmethod
    def criar_servidor():
        _tcp_server_loop()
