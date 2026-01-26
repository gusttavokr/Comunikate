# server.py
import socket
import threading
import os

TCP_PORT = 5000
UDP_PORT = 5001
BUFFER = 4096
ENC = "utf-8"


def _handle_tcp_client(conn, addr, server_name="Servidor TCP"):
    """Trata mensagens TCP do cliente"""
    try:
        print(f"[{server_name}] Nova conexão TCP: {addr}")
        while True:
            data = conn.recv(BUFFER)
            if not data:
                break
            msg = data.decode(ENC).strip()
            print(f"[{server_name}] TCP recebido de {addr}: {msg}")
            response = f"[{server_name}] Mensagem recebida: {msg}"
            conn.send(response.encode(ENC))
    except Exception as e:
        print(f"[{server_name}] Erro TCP com {addr}: {e}")
    finally:
        print(f"[{server_name}] Conexão TCP encerrada: {addr}")
        conn.close()


def _udp_server_loop(server_name="Servidor UDP"):
    """Recebe arquivos via UDP"""
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    udp_sock.bind(("", UDP_PORT))
    print(f"[{server_name}] UDP ouvindo na porta {UDP_PORT} para receber arquivos...")
    
    try:
        while True:
            data, addr = udp_sock.recvfrom(BUFFER)
            
            # Protocolo simples: primeira mensagem contém o nome do arquivo
            if data.startswith(b"FILE:"):
                filename = data[5:].decode(ENC)
                print(f"[{server_name}] Recebendo arquivo '{filename}' de {addr}")
                
                # Enviar ACK
                udp_sock.sendto(b"ACK", addr)
                
                # Receber conteúdo
                file_data, _ = udp_sock.recvfrom(65535)
                
                # Salvar arquivo
                save_path = f"recebido_{filename}"
                with open(save_path, "wb") as f:
                    f.write(file_data)
                
                print(f"[{server_name}] Arquivo salvo como '{save_path}' ({len(file_data)} bytes)")
                udp_sock.sendto(b"OK", addr)
                
    except KeyboardInterrupt:
        print(f"\n[{server_name}] Encerrando servidor UDP.")
    finally:
        udp_sock.close()


def _tcp_server_loop(server_name="Servidor TCP"):
    """Loop principal do servidor TCP"""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("", TCP_PORT))
    server.listen(5)

    print(f"[{server_name}] TCP ouvindo na porta {TCP_PORT}...")
    print("Aguardando conexões... (Ctrl+C para sair)")

    try:
        while True:
            conn, addr = server.accept()
            t = threading.Thread(target=_handle_tcp_client, args=(conn, addr, server_name), daemon=True)
            t.start()
    except KeyboardInterrupt:
        print(f"\n[{server_name}] Encerrando servidor TCP.")
    finally:
        server.close()


class Server:
    @staticmethod
    def criar_servidor(nome="Servidor"):
        """Inicia servidor TCP e UDP simultaneamente"""
        print(f"Iniciando servidor: {nome}")
        
        # Thread para UDP
        udp_thread = threading.Thread(target=_udp_server_loop, args=(f"{nome} UDP",), daemon=True)
        udp_thread.start()
        
        # TCP roda na thread principal
        _tcp_server_loop(f"{nome} TCP")
