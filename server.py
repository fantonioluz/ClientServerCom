import json
import random
import socket
import hashlib
import time

#Estrutura para Armazenar Lista Telefônica:s
lista_telefonica = {'Alice':'123'}

def showListaTelefonica():
    for chave, valor in lista_telefonica.items():
        print(f'Chave: {chave}, Valor: {valor}')

#método que decode diferenciar a msg de search e add e usar no metodo de recebimento
def decode_msg(respostaCliente): #decofifciar a stri json
    #desserializar a msg antes de decodificar
    mensagem = respostaCliente #debug
    mensagem_Desserializada = json.loads(respostaCliente) #aqui deixa de ser json e passa a ser

    #Verifica o tipo de ação na mensagem e chama o método correspondente
    if mensagem_Desserializada["acao"] == "Get":
       processar_mensagem_get(mensagem_Desserializada["nome"])
    elif mensagem_Desserializada["acao"] == "Add":
       processar_mensagem_add(mensagem_Desserializada["nome"], mensagem_Desserializada["telefone"])
    
    return lista_telefonica
       

def processar_mensagem_get(nome):
        # Processa a mensagem "get" e retorna o telefone correspondente ao nome fornecido
        if nome in lista_telefonica:
            print("Numero encontrado")
            return lista_telefonica
            # Aqui você pode enviar o telefone de volta para o cliente se necessário
        else:
            print(f"Não há número registrado para {nome}")
            return lista_telefonica

def processar_mensagem_add(nome, telefone):
        # Processa a mensagem "add" e adiciona o novo número à lista telefônica
        lista_telefonica[nome] = telefone

        print(f"Número de telefone adicionado para {nome}: {telefone}")

        return lista_telefonica
        

# Definir o tempo limite do temporizador (em segundos)
TIMEOUT = 60

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

            return dados_reais #os dados reais (sem o número de sequência) são retornados para que possam ser processados pelo servidor. 
        
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
            print("Dados recebidos com sucesso:")
            print(dados) #recebeu a string json p decodificar
            socket.sendall(b"ACK")  # Enviar reconhecimento

            msgdecode = decode_msg(dados)

            #tratar os dados aqui
            return msgdecode
            #return dados
            
    except Exception as e:
        print(f"Erro ao receber dados: {e}")
        if time.time() - inicio_temporizador > TIMEOUT:
            raise Exception("Tempo limite excedido ao aguardar dados do cliente")

