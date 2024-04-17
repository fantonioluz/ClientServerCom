import json
import random
import socket
import hashlib
import time

#extrair metodos iguais de server e cliente para ca
class ClasseMae:

    def calcular_checksum(dados):
        # Calcular o hash MD5 dos dados
        hash_md5 = hashlib.md5()
        hash_md5.update(dados)
        return hash_md5.digest()
    
    # Função para simular falha de integridade e/ou perda de mensagens
    def simular_falha():
        return random.random() < 0.2  # Probabilidade de 20%
    
    

