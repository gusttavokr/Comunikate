import socket
import threading
import time

DISCOVERY_PORT = 54545
ENC = "utf-8"

def get_local_ip():
    """Tenta descobrir o IP real da máquina na rede (ex: 192.168.x.x)"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Não precisa conectar de verdade, só para o OS escolher a interface de saída
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

class Server:
    def __init__(self, port=5000):
        self.ip = get_local_ip()
        self.port = port
        self.tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = False
        self.clients = []

    def _broadcast_loop(self):
        """Envia pacotes UDP repetidamente para que clientes encontrem este servidor."""
        udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
        # Formato que o seu main.py espera: "NOME|IP|PORTA"
        hostname = socket.gethostname()
        mensagem = f"Servidor de {hostname}|{self.ip}|{self.port}"
        
        print(f"[SERVER] Iniciando broadcast de descoberta na porta {DISCOVERY_PORT}...")
        
        while self.running:
            try:
                # Envia para toda a rede (<broadcast>)
                udp_sock.sendto(mensagem.encode(ENC), ('<broadcast>', DISCOVERY_PORT))
                time.sleep(2) # Anuncia a cada 2 segundos
            except Exception as e:
                print(f"[SERVER] Erro no broadcast: {e}")
                time.sleep(5)
        
        udp_sock.close()

    def _client_handler(self, cl_sock, cl_addr):
        """Lida com mensagens de um cliente específico."""
        print(f"[SERVER] Nova conexão de {cl_addr}")
        try:
            while self.running:
                data = cl_sock.recv(1024)
                if not data:
                    break
                msg = data.decode(ENC)
                print(f"[{cl_addr}] disse: {msg}")
                
                if msg.lower() == 'sair':
                    break
                
                # Eco simples (muda isso depois para lógica de chat real)
                cl_sock.sendall(f"Recebido: {msg}".encode(ENC))
        except ConnectionResetError:
            pass
        finally:
            print(f"[SERVER] Cliente {cl_addr} desconectado.")
            cl_sock.close()
            if cl_sock in self.clients:
                self.clients.remove(cl_sock)

    def iniciar(self):
        try:
            # Bind TCP (Conexão do chat)
            self.tcp_sock.bind(("0.0.0.0", self.port))
            self.tcp_sock.listen(5)
            self.running = True

            print(f"[SERVER] TCP ouvindo em {self.ip}:{self.port}")

            # 1. Inicia a thread que "GRITA" na rede (Broadcast UDP)
            retransmissor = threading.Thread(target=self._broadcast_loop, daemon=True)
            retransmissor.start()

            # 2. Loop principal aceitando conexões TCP
            while self.running:
                client_sock, addr = self.tcp_sock.accept()
                self.clients.append(client_sock)
                t_cli = threading.Thread(target=self._client_handler, args=(client_sock, addr), daemon=True)
                t_cli.start()

        except Exception as e:
            print(f"[SERVER] Erro fatal: {e}")
        finally:
            self.running = False
            self.tcp_sock.close()

    @staticmethod
    def criar_servidor():
        s = Server(port=5000)
        s.iniciar()