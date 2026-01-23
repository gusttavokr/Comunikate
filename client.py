# client.py
import socket
import threading

TCP_PORT = 5000
BUFFER = 4096
ENC = "utf-8"


class Client:
    def __init__(self, host="127.0.0.1", tcp_port=TCP_PORT):
        self.host = host
        self.tcp_port = tcp_port
        self.tcp_sock = None

    def conectar_tcp(self):
        if self.tcp_sock is not None:
            self.fechar_tcp()

        self.tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_sock.connect((self.host, self.tcp_port))
        print(f"[CLIENT] Conectado a {self.host}:{self.tcp_port} via TCP.")

    def enviar_tcp(self, msg: str):
        if not self.tcp_sock:
            print("[CLIENT] Erro: não conectado.")
            return
        self.tcp_sock.send(msg.encode(ENC))

    def receber_tcp(self) -> str:
        if not self.tcp_sock:
            print("[CLIENT] Erro: não conectado.")
            return ""
        data = self.tcp_sock.recv(BUFFER)
        return data.decode(ENC) if data else ""

    def fechar_tcp(self):
        if self.tcp_sock:
            self.tcp_sock.close()
        self.tcp_sock = None

    def loop_interativo(self):
        print("[CLIENT] Modo interativo (digite 'QUIT' para sair):\n")
        try:
            while True:
                msg = input("Enviar: ").strip()
                if msg.upper() == "QUIT":
                    break
                self.enviar_tcp(msg)
                resp = self.receber_tcp()
                print(f"Resposta: {resp}")
        finally:
            self.fechar_tcp()
