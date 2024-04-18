# Função principal do servidor
import server
import socket
import threading
clients = []
#extrair main para essa classe
def main():
    # Configurar host e porta
    host = 'localhost'  # Ou deixe em branco para todas as interfaces
    porta = 12345  # Porta para comunicação

    recepcao = server.confirmacao_recebimento()

    # Criar um socket TCP/IP
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Vincular o socket à porta
        servidor_socket.bind((host, porta))

        # Escutar conexões
        servidor_socket.listen(5)
            
        print("Servidor pronto para receber conexões...")
        
        if recepcao == "1":
        
            while True:
                conexao, endereco_cliente = servidor_socket.accept()

                # Criar uma thread para lidar com a conexão
                thread = threading.Thread(target=server.handle_client_connection, args=(conexao, endereco_cliente))
                thread.start()
        
        else:
            while True:
                conexao, endereco_cliente = servidor_socket.accept()
                server.handle_client_connection(conexao, endereco_cliente)

    except Exception as e:
        print(f"Erro no servidor: {e}")
    finally:
        # Fechar o socket do servidor
        servidor_socket.close()
        





if __name__ == "__main__":
    main()