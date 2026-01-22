# Comunikate

Comunikate é um comunicador em linha de comando (CLI) para troca de dados entre máquinas na **mesma rede local**, implementado em **Python** usando **TCP e UDP**.

- **TCP** é usado para a conexão estável entre cliente e servidor **e também para descobrir servidores** na rede (varrendo a sub-rede e fazendo um handshake).
- **UDP** é reservado para o **envio de arquivos** de forma leve/broadcast.

> Estado atual: o projeto já implementa descoberta automática de servidores via **TCP** e conexão TCP entre cliente e servidor. A parte de envio de arquivos via UDP pode ser evoluída em cima dessa base.

---

## Arquitetura

- Servidor
	- Escuta conexões **TCP** na porta padrão `5000`.
	- Responde a mensagens TCP (no momento, um *echo* simples).
	- Reserva a porta `5001/UDP` para envio/recebimento de arquivos (a implementar).

- Cliente
	- Descobre o IP local, assume uma rede /24 (ex.: `192.168.0.x`).
	- Tenta conectar via TCP em cada IP do range na porta `5000`.
	- Monta uma lista com os servidores encontrados (`nome`, IP, porta TCP).
	- O usuário escolhe um servidor pelo índice.
	- O cliente então abre uma conexão **TCP** com o servidor escolhido e pode trocar mensagens/dados por essa conexão.

Essa divisão permite usar **TCP para controle/transferência confiável e descoberta** e **UDP para envio de arquivos** em um formato leve (a implementar).

---

## Requisitos

- Python 3.10+ (ou compatível com *type hints* usados no projeto).
- Máquinas na **mesma rede local** (mesmo Wi‑Fi ou rede cabeada), preferencialmente em uma rede /24 simples (ex.: `192.168.0.x`).
- Permitir tráfego nas portas:
	- `5000/TCP` – conexões cliente-servidor e descoberta.
	- `5001/UDP` – (planejado) envio de arquivos.

---

## Instalação

Clone o repositório e entre na pasta do projeto:

```bash
git clone https://github.com/gusttavokr/Comunikate.git
cd Comunikate
```

Não há dependências externas além da biblioteca padrão do Python.

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