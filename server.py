import random
import socket
import hashlib
from time import sleep

# Definir o tempo limite do temporizador (em segundos)
TIMEOUT = 5

# Número de sequência esperado
expected_sequence_number = 0

def calcular_checksum(dados):
    # Calcular o hash MD5 dos dados
    hash_md5 = hashlib.md5()
    hash_md5.update(dados)
    return hash_md5.digest()

def enviar_dados_com_checksum(socket, dados):
    # Calcular o checksum dos dados
    checksum = calcular_checksum(dados)

    # Concatenar número de sequência, checksum e dados
    mensagem = str(expected_sequence_number).encode() + ":" + checksum + ":" + dados

    # Enviar dados
    socket.sendall(mensagem)
    
def receber_dados_com_checksum(socket):
    global expected_sequence_number

    # Receber dados
    dados = socket.recv(1024)  # Tamanho máximo dos dados, ajuste conforme necessário

    # Separar número de sequência, checksum e dados reais
    partes = dados.split(b":", 2)
    for i in range(len(partes)):
        print(partes[i])
    # Verificar se há três partes
    if len(partes) != 3:
        raise Exception("Dados recebidos incompletos")

    # Extrair número de sequência, checksum e dados reais
    numero_sequencia = int(partes[0])
    checksum_recebido = partes[1]
    dados_reais = partes[2]

    # Calcular o checksum dos dados recebidos
    checksum_calculado = calcular_checksum(dados_reais)

    # Verificar se os checksums coincidem
    if checksum_recebido == checksum_calculado:
        # Verificar se o número de sequência é o esperado
        if numero_sequencia == expected_sequence_number:
            expected_sequence_number += 1
            return dados_reais
        else:
            raise Exception("Número de sequência incorreto")
    else:
        raise Exception("Erro de integridade: checksums não coincidem")

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

        while True:
            try:
                # Exemplo de recebimento de dados confiavelmente
                dados_recebidos = receber_dados_com_checksum(conexao)
                print("Dados recebidos:", dados_recebidos.decode())

                # Enviar uma resposta simples de volta ao cliente
                resposta = "Dados recebidos com sucesso"
                conexao.sendall(resposta.encode())
            except:
                conexao.close()
                conexao, endereco_cliente = servidor_socket.accept()
            
            
    except Exception as e:
        print(f"Erro no servidor: {e}")

    finally:
        # Fechar o socket do servidor
        servidor_socket.close()

if __name__ == "__main__":
    main()
