# Função principal do cliente
import socket
import client

#extrair main para essa classe
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
        #enviar_dados_confiavelmente(cliente_socket, "Dados de teste confiáveis".encode("utf-8"))
        dadoParaEnviar = client.enviarMsg_add_telefone(cliente_socket, 'Bruna', '992607551')
        client.enviar_dados_confiavelmente(cliente_socket, dadoParaEnviar.encode() ) #o dado que eu quero que ele mande é o obj serializado

        #dadoParaEnviar2 = client.enviarMsg_add_telefone(cliente_socket, 'Alice', '12345678')
        #client.enviar_dados_confiavelmente(cliente_socket, dadoParaEnviar2.encode() ) #o dado que eu quero que ele mande é o obj serializado

        #dadoParaEnviar3 = client.enviarMsg_pegar_telefone(cliente_socket, 'Alice')
        #client.enviar_dados_confiavelmente(cliente_socket, dadoParaEnviar3.encode() ) #o dado que eu quero que ele mande é o obj serializado

        # Exemplo de recebimento de dados confiavelmente
        dados_recebidos = client.receber_dados_confiavelmente(cliente_socket)
        print("Dados recebidos:", dados_recebidos.decode())

    except Exception as e:
        print(f"Erro ao conectar ao servidor: {e}")

    finally:
        # Fechar o socket
        cliente_socket.close()

if __name__ == "__main__":
    main()