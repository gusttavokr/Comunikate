import socket

TCP_PORT = 5000
BUFFER = 4096
ENC = "utf-8"

class Client:
    def __init__(self, tcp_port=TCP_PORT):
        self.host = None  # Será definido ao escolher servidor
        self.tcp_port = tcp_port
        self.tcp_socket: socket.socket | None = None
        self.connected = False

    def escolher_e_conectar(self):
        """Escolhe o servidor e conecta automaticamente."""
        print("\n=== Escolher servidor ===")
        ip = input("IP do servidor (ex: localhost, 192.168.0.100): ").strip()
        
        if not ip:
            print("IP obrigatório.")
            return False
            
        porta_str = input(f"Porta TCP (padrão {self.tcp_port}): ").strip()
        
        if porta_str:
            try:
                self.tcp_port = int(porta_str)
            except ValueError:
                print("Porta inválida, usando padrão.")
        
        self.host = ip
        return self.conectar_tcp()

    def conectar_tcp(self):
        """Conecta ao servidor TCP especificado."""
        if not self.host:
            print("Nenhum servidor especificado. Use escolher_e_conectar() primeiro.")
            return False
            
        if self.connected:
            print("Já está conectado.")
            return True

        try:
            self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.tcp_socket.connect((self.host, self.tcp_port))
            self.connected = True
            print(f"Conectado ao servidor {self.host}:{self.tcp_port}")
            return True
        except Exception as e:
            print(f"Falha ao conectar: {e}")
            self.connected = False
            if self.tcp_socket:
                self.tcp_socket.close()
                self.tcp_socket = None
            return False

    def desconectar_tcp(self):
        """Fecha a conexão TCP."""
        if self.tcp_socket:
            try:
                self.tcp_socket.close()
            except Exception:
                pass
            finally:
                self.tcp_socket = None
                self.connected = False
                print("Desconectado do servidor.")

    def esta_conectado(self) -> bool:
        """Verifica se o socket ainda está conectado."""
        if not self.tcp_socket or not self.connected:
            return False

        try:
            self.tcp_socket.send(b"")
            return True
        except OSError:
            self.connected = False
            return False

    def enviar_tcp(self, msg: str) -> bool:
        """Envia uma mensagem TCP para o servidor."""
        if not self.esta_conectado():
            print("Não está conectado ao servidor.")
            return False

        try:
            self.tcp_socket.send(msg.encode(ENC))
            return True
        except Exception as e:
            print(f"Erro ao enviar mensagem: {e}")
            self.desconectar_tcp()
            return False

    def receber_tcp(self) -> str | None:
        """Recebe uma mensagem TCP do servidor."""
        if not self.esta_conectado():
            print("Não está conectado ao servidor.")
            return None

        try:
            data = self.tcp_socket.recv(BUFFER)
            if not data:
                # servidor fechou
                self.desconectar_tcp()
                return None
            return data.decode(ENC)
        except Exception as e:
            print(f"Erro ao receber mensagem: {e}")
            self.desconectar_tcp()
            return None
