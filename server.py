import random
import socket
import hashlib
import time


# Definir o tempo limite do temporizador (em segundos)
TIMEOUT = 5

# Número de sequência esperado
expected_sequence_number = 0

# Tamanho da janela
WINDOW_SIZE = 5

def calcular_checksum(dados):
    # Calcular o hash MD5 dos dados
    hash_md5 = hashlib.md5()
    hash_md5.update(dados)
    return hash_md5.digest()

def enviar_dados_com_checksum(socket, dados):
    # Calcular o checksum dos dados
    checksum = calcular_checksum(dados)

    # Enviar checksum e dados
    socket.sendall(checksum)
    socket.sendall(dados)

def receber_dados_com_checksum(socket):
    global expected_sequence_number

    # Receber checksum e dados
    checksum_recebido = socket.recv(16)  # MD5 tem 16 bytes
    dados = socket.recv(1024)  # Tamanho máximo dos dados, ajuste conforme necessário

    # Calcular o checksum dos dados recebidos
    checksum_calculado = calcular_checksum(dados)

    # Verificar se os checksums coincidem
    if checksum_recebido == checksum_calculado:
        # Separar número de sequência dos dados
        partes = dados.split(b":", 1)
        numero_sequencia = int(partes[0])
        dados_reais = partes[1]

        # Verificar se o número de sequência é o esperado
        if numero_sequencia == expected_sequence_number:
            expected_sequence_number += 1
            return dados_reais
        else:
            # Enviar NACK para solicitar retransmissão
            socket.sendall(b"NACK")
            raise Exception("Número de sequência incorreto")
    else:
        raise Exception("Erro de integridade: checksums não coincidem")
    
# Função para receber uma janela de dados
def receber_janela(socket):
    janela = []
    for _ in range(WINDOW_SIZE):
        dados = receber_dados_com_checksum(socket)
        janela.append(dados)
    return janela


# Função para simular falha de integridade e/ou perda de mensagens
def simular_falha():
    return random.random() < 0.2  # Probabilidade de 20%

# Função para enviar dados confiavelmente (com soma de verificação)
def enviar_dados_confiavelmente(socket, dados):
    try:
        inicio_temporizador = time.time()
        while True:
            enviar_dados_com_checksum(socket, dados)
            print("Dados enviados com sucesso")
            
            # Esperar pela resposta
            socket.settimeout(TIMEOUT)
            try:
                resposta = socket.recv(1024)
                if resposta:
                    print("Resposta do servidor:", resposta.decode())
                    break  # Saia do loop se receber uma resposta
            except socket.timeout:
                print("Tempo limite atingido. Tentando novamente...")
                if time.time() - inicio_temporizador > TIMEOUT:
                    raise Exception("Tempo limite excedido ao aguardar resposta do servidor")

    except Exception as e:
        print(f"Erro ao enviar dados: {e}")

# Função para receber dados confiavelmente (com soma de verificação)
def receber_dados_confiavelmente(socket):
    try:
        inicio_temporizador = time.time()
        while True:
            dados = receber_dados_com_checksum(socket)
            print("Dados recebidos com sucesso")
            socket.sendall(b"ACK")  # Enviar reconhecimento
            return dados
            
    except Exception as e:
        print(f"Erro ao receber dados: {e}")
        if time.time() - inicio_temporizador > TIMEOUT:
            raise Exception("Tempo limite excedido ao aguardar dados do cliente")

# Função principal do servidor
def main():
    # Configurar host e porta
    host = 'localhost'  # Ou deixe em branco para todas as interfaces
    porta = 12345  # Porta para comunicação

    # Criar um socket TCP/IP
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Vincular o socket à porta
        servidor_socket.bind((host, porta))

        # Escutar conexões
        servidor_socket.listen(5)

        print("Servidor pronto para receber conexões...")

        # Aceitar conexões
        conexao, endereco_cliente = servidor_socket.accept()
        print(f"Conexão estabelecida com {endereco_cliente}")

        # Exemplo de recebimento de dados confiavelmente
        dados_recebidos = receber_dados_confiavelmente(conexao)
        print("Dados recebidos:", dados_recebidos.decode())

        # Exemplo de envio de dados confiavelmente
        enviar_dados_confiavelmente(conexao, "Resposta do servidor confiável".encode("utf-8"))

    except Exception as e:
        print(f"Erro no servidor: {e}")

    finally:
        # Fechar o socket do servidor
        servidor_socket.close()

if __name__ == "__main__":
    main()