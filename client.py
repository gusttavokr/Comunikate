import socket
import threading

TCP_PORT = 5000
UDP_PORT = 5001  # reservado para envio de arquivos via UDP
BUFFER = 4096
ENC = "utf-8"

class Client:
    def __init__(self, host="127.0.0.1", tcp_port=TCP_PORT, udp_port=UDP_PORT):
        self.host = host
        self.tcp_port = tcp_port
        self.udp_port = udp_port

        self.tcp_sock: socket.socket | None = None
        self.udp_sock: socket.socket | None = None

        self._tcp_connected = False

    # ========= TCP =========
    def conectar_tcp(self):
        """Abre conexão TCP com o servidor."""
        if self._tcp_connected:
            return

        self.tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_sock.connect((self.host, self.tcp_port))
        self._tcp_connected = True
        print(f"[TCP CLIENT] Conectado em {self.host}:{self.tcp_port}")

    def enviar_tcp(self, msg: str):
        """Envia mensagem via TCP."""
        if not self.esta_conectado_tcp():
            raise RuntimeError("Cliente TCP não está conectado")

        data = (msg + "\n").encode(ENC)
        self.tcp_sock.sendall(data)

    def esta_conectado_tcp(self) -> bool:
        """
        Verifica se o socket TCP ainda está conectado.
        """
        if not self.tcp_sock:
            return False

        try:
            err = self.tcp_sock.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
            if err != 0:
                # houve erro na conexão
                self._tcp_connected = False
                return False
        except OSError:
            self._tcp_connected = False
            return False

        return self._tcp_connected

    @staticmethod
    def descobrir_servidores(timeout: float = 0.5):
        """Descobre servidores Comunikate na rede local via TCP.

        Estratégia simples:
        - Descobre o IP local e assume rede /24 (ex.: 192.168.0.x).
        - Tenta conectar via TCP em cada IP do range na porta TCP_PORT.
        - Ao conectar, envia "HELLO_COMUNIKATE" e espera resposta
          "COMUNIKATE_SERVER;<nome>;<porta>".

        Retorna uma lista de dicionários:
        [{"name": str, "ip": str, "port": int}, ...]
        """
        servidores = []
        lock = threading.Lock()

        # Descobre IP local para inferir o prefixo da rede (ex.: 192.168.0)
        try:
            tmp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            tmp_sock.connect(("8.8.8.8", 80))
            local_ip = tmp_sock.getsockname()[0]
        except OSError:
            # fallback: localhost (pode não achar outros servidores)
            local_ip = "127.0.0.1"
        finally:
            try:
                tmp_sock.close()
            except Exception:
                pass

        partes_ip = local_ip.split(".")
        if len(partes_ip) != 4:
            return []

        prefixo = ".".join(partes_ip[:3])  # assume /24

        def scan_host(ip: str):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(timeout)
            try:
                s.connect((ip, TCP_PORT))
                s.sendall("HELLO_COMUNIKATE\n".encode(ENC))
                data = s.recv(BUFFER)
            except OSError:
                s.close()
                return

            s.close()

            if not data:
                return

            texto = data.decode(ENC).strip()
            if not texto.startswith("COMUNIKATE_SERVER;"):
                return

            partes = texto.split(";")
            if len(partes) != 3:
                return

            _, name, tcp_port_str = partes
            try:
                tcp_port = int(tcp_port_str)
            except ValueError:
                return

            entrada = {"name": name, "ip": ip, "port": tcp_port}
            with lock:
                if entrada not in servidores:
                    servidores.append(entrada)

        threads = []
        for host in range(1, 255):
            ip = f"{prefixo}.{host}"
            t = threading.Thread(target=scan_host, args=(ip,), daemon=True)
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        return servidores
    # ========= UDP (opcional, eco simples) =========
    # def conectar_udp(self):
    #     """Cria socket UDP (sem 'conexão', só bind local opcional)."""
    #     if self.udp_sock:
    #         return
    #     self.udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #     print(f"[UDP CLIENT] UDP pronto para {self.host}:{self.udp_port}")

    # def enviar_udp(self, msg: str):
    #     if not self.udp_sock:
    #         self.conectar_udp()
    #     data = msg.encode(ENC)
    #     self.udp_sock.sendto(data, (self.host, self.udp_port))

    # def receber_udp(self) -> str:
    #     if not self.udp_sock:
    #         raise RuntimeError("Socket UDP não criado")
    #     data, addr = self.udp_sock.recvfrom(BUFFER)
    #     print(f"[UDP CLIENT] Recebido de {addr}: {data!r}")
    #     return data.decode(ENC).strip()

    # def fechar_udp(self):
    #     if self.udp_sock:
    #         self.udp_sock.close()
    #         self.udp_sock = None
    #         print("[UDP CLIENT] Socket UDP fechado")

    # ========= Métodos estáticos auxiliares =========
    # @staticmethod
    # def testar_conexao(host="127.0.0.1", port=TCP_PORT, timeout=2.0) -> bool:
    #     """
    #     Testa se é possível conectar no servidor (sem manter o socket aberto).
    #     Útil para 'pingar' o servidor antes de criar o cliente.
    #     """
    #     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     sock.settimeout(timeout)
    #     try:
    #         sock.connect((host, port))
    #         # se conectou, está aceitando conexões
    #         return True
    #     except OSError:
    #         return False
    #     finally:
    #         sock.close()

