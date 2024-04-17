# Função principal do servidor
import server
import socket

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
        dados_recebidos = server.receber_dados_confiavelmente(conexao) #vai receber o dado da conexao que ta la no cliente 

        print("Dados adicionados na lista:", dados_recebidos)

        # Exemplo de envio de dados confiavelmente
        server.enviar_dados_confiavelmente(conexao, "Resposta do servidor confiável".encode("utf-8"))

    except Exception as e:
        print(f"Erro no servidor: {e}")

    finally:
        # Fechar o socket do servidor
        servidor_socket.close()

if __name__ == "__main__":
    main()