import random
import socket
import hashlib
import time


# Definir o tempo limite do temporizador (em segundos)
TIMEOUT = 5

# Número de sequência inicial
sequence_number = 0

# Tamanho da janela 
WINDOW_SIZE = 5

def calcular_checksum(dados):
    # Calcular o hash MD5 dos dados
    hash_md5 = hashlib.md5()
    hash_md5.update(dados)
    return hash_md5.digest()

def enviar_dados_com_checksum(socket, dados):
    global sequence_number

    # Adicionar o número de sequência aos dados
    dados = str(sequence_number).encode() + b":" + dados
    sequence_number += 1

    # Calcular o checksum dos dados
    checksum = calcular_checksum(dados)

    # Enviar checksum e dados
    socket.sendall(checksum)
    socket.sendall(dados)
    
# Função para enviar uma janela de dados
def enviar_janela(socket, janela):
    for dados in janela:
        enviar_dados_com_checksum(socket, dados)
        
# Função para simular falha de integridade e/ou perda de mensagens
def simular_falha():
    return random.random() < 0.2  # Probabilidade de 20%

def receber_dados_com_checksum(socket):
    # Receber checksum e dados
    checksum_recebido = socket.recv(16)  # MD5 tem 16 bytes
    dados = socket.recv(1024)  # Tamanho máximo dos dados, ajuste conforme necessário

    # Calcular o checksum dos dados recebidos
    checksum_calculado = calcular_checksum(dados)

    # Verificar se os checksums coincidem
    if checksum_recebido == checksum_calculado:
        return dados
    else:
        raise Exception("Erro de integridade: checksums não coincidem")

# Função para enviar dados confiavelmente (com soma de verificação)
def enviar_dados_confiavelmente(socket, dados):
    try:
        inicio_temporizador = time.time()
        while True:
            enviar_dados_com_checksum(socket, dados)
            print("Dados enviados com sucesso")
            
            # Esperar pela resposta
            socket.settimeout(TIMEOUT)
            resposta = socket.recv(1024)
            if resposta:
                print("Resposta do servidor:", resposta.decode())
                break  # Saia do loop se receber uma resposta
            if time.time() - inicio_temporizador > TIMEOUT:
                raise Exception("Tempo limite excedido ao aguardar resposta do servidor")

    except socket.timeout:
        print("Tempo limite atingido ao aguardar resposta do servidor")
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
            
    except socket.timeout:
        print("Tempo limite atingido ao aguardar dados do cliente")
    except Exception as e:
        print(f"Erro ao receber dados: {e}")

# Função principal do cliente
def main():
    # Configurar host e porta
    host = 'localhost'  # Ou o IP do servidor
    porta = 12345  # Porta para comunicação

    # Criar um socket TCP/IP
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Conectar ao servidor
        cliente_socket.connect((host, porta))

        # Exemplo de envio de dados confiavelmente
        enviar_dados_confiavelmente(cliente_socket, "Dados de teste confiáveis".encode("utf-8"))

        # Exemplo de recebimento de dados confiavelmente
        dados_recebidos = receber_dados_confiavelmente(cliente_socket)
        print("Dados recebidos:", dados_recebidos.decode())

    except Exception as e:
        print(f"Erro ao conectar ao servidor: {e}")

    finally:
        # Fechar o socket
        cliente_socket.close()

if __name__ == "__main__":
    main()