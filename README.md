# Comunikate

Sistema simples de comunicação entre máquinas usando **TCP e UDP** nativos em Python.

## 📋 Requisitos do Projeto

✅ Implementa transmissão de dados com protocolos **TCP e UDP** de fato  
✅ **TCP**: usado para mensagens de texto (conexão confiável)  
✅ **UDP**: usado para envio de arquivos (transferência rápida)  
✅ Ambos os protocolos em um único projeto  
✅ Não usa HTTP/RTSP ou outros protocolos de alto nível  

---

## 🏗️ Arquitetura

### Servidor
- **Porta 5000/TCP**: Recebe e responde mensagens de texto
- **Porta 5001/UDP**: Recebe arquivos e salva no diretório local

### Cliente
- Conecta ao servidor via TCP (mensagens)
- Envia arquivos via UDP (transferência direta)

---

## 🚀 Como Usar

### 1. Instalar
Clone o repositório:

```bash
git clone https://github.com/seu-usuario/Comunikate.git
cd Comunikate
```

**Requisito**: Python 3.10+

### 2. Iniciar o Servidor

Em um terminal:

```bash
python main.py
```

Escolha opção `2` para criar o servidor. Ele ficará escutando nas portas 5000 (TCP) e 5001 (UDP).

### 3. Conectar como Cliente

Em outro terminal (ou máquina na mesma rede):

```bash
python main.py
```

Escolha opção `1` e informe:
- IP do servidor (ex: `localhost` ou `192.168.0.10`)
- Porta TCP (padrão: 5000)

### 4. Testar os Protocolos

No menu do cliente:

- **Opção 1**: Enviar mensagem via **TCP**
- **Opção 2**: Enviar arquivo via **UDP**

---

## 📁 Estrutura do Projeto

```
Comunikate/
├── main.py      # Interface principal (menu)
├── server.py    # Servidor TCP/UDP
├── client.py    # Cliente TCP/UDP
└── README.md    # Este arquivo
```

---

## 🧪 Exemplo de Teste

### Terminal 1 (Servidor):
```
python main.py
→ Escolha: 2
[Servidor TCP] TCP ouvindo na porta 5000...
[Servidor UDP] UDP ouvindo na porta 5001 para receber arquivos...
```

### Terminal 2 (Cliente):
```
python main.py
→ Escolha: 1
IP do servidor: localhost
→ Conectado com sucesso!

Menu:
1 - Enviar mensagem (TCP)
2 - Enviar arquivo (UDP)

→ 1
Digite a mensagem: Olá servidor!
[SERVIDOR] Mensagem recebida: Olá servidor!

→ 2
Caminho do arquivo: teste.txt
Arquivo 'teste.txt' enviado com sucesso! (15 bytes)
```

---

## 🔍 Demonstração dos Protocolos

**TCP (Porta 5000)**:
- Conexão orientada e confiável
- Usado para mensagens de texto
- Mantém estado da conexão

**UDP (Porta 5001)**:
- Sem conexão (connectionless)
- Usado para transferência de arquivos
- Mais rápido, sem garantias de entrega

---

## 📦 Requisitos Técnicos

- Python 3.10+
- Biblioteca padrão (socket, threading, os)
- Máquinas na mesma rede local
- Portas 5000 e 5001 liberadas no firewall

---

## Como usar

### 1. Iniciar o servidor (PC1)

No computador que será o **servidor**:

```bash
python main.py
```

Quando o menu aparecer:

1. Digite `2` para **criar um servidor**.
2. Informe um nome para o servidor (ou pressione Enter para usar o padrão).
3. O servidor começará a escutar TCP em `0.0.0.0:5000`.

Deixe esse terminal aberto e rodando.

### 2. Conectar como cliente (PC2)

No outro computador, na **mesma rede**:

```bash
python main.py
```

Quando o menu aparecer:

1. Digite `1` para **entrar em um servidor**.
2. O cliente vai procurar servidores na rede **via TCP**, varrendo a sub-rede local.
3. Será exibida uma lista semelhante a:

	 ```
	 Servidores encontrados:
	 1 - Servidor Comunikate (192.168.0.10:5000)
	 ```

4. Digite o número do servidor desejado.
5. O cliente abrirá uma conexão **TCP** com o IP/porta escolhidos e exibirá uma mensagem de conexão estabelecida.

> A partir daí você pode evoluir o código (em `client.py` e `server.py`) para enviar mensagens de chat ou arquivos pela conexão TCP.

---

## Fluxo TCP/UDP

- **Descoberta (TCP)**
	- Cliente varre a sub-rede tentando conectar na porta `5000/TCP`.
	- Cliente monta uma lista de servidores disponíveis na LAN.

- **Conexão e dados (TCP)**
	- Após a escolha do servidor, o cliente conecta em `tcp://<ip_servidor>:<porta_tcp>`.
	- Toda troca de dados é feita sobre essa conexão TCP.

Em uma evolução futura, o envio de arquivos será feito via **UDP** usando a porta `5001`, com um protocolo simples para nome/tamanho do arquivo e reenvio em caso de perda de pacotes.

---

## Estrutura do projeto

- `main.py` – Ponto de entrada do CLI (menu inicial, modo cliente/servidor).
- `server.py` – Implementação do servidor TCP (incluindo resposta ao handshake de descoberta) e reserva de porta UDP para arquivos.
- `client.py` – Implementação do cliente TCP e lógica de descoberta de servidores via TCP.

---

## Próximos passos sugeridos

- Implementar envio/recebimento de arquivos via UDP (com barra de progresso, por exemplo).
- Definir um protocolo simples para metadados do arquivo (nome, tamanho, checksum).