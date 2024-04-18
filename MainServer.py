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

    #recepcao = server.confirmacao_recebimento()

    # Criar um socket TCP/IP
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Vincular o socket à porta
        servidor_socket.bind((host, porta))

        # Escutar conexões
        servidor_socket.listen(5)
            
        print("Servidor pronto para receber conexões...")
        
        while True:
            conexao, endereco_cliente = servidor_socket.accept()
            
            # Criar uma thread para lidar com a conexão
            thread = threading.Thread(target=server.handle_client_connection, args=(conexao, endereco_cliente))
            thread.start()

    except Exception as e:
        print(f"Erro no servidor: {e}")
    finally:
        # Fechar o socket do servidor
        servidor_socket.close()
        
"""        if recepcao == '2':
            while True:
                print("Servidor pronto para receber conexões...")

                # Aceitar conexões
                conexao, endereco_cliente = servidor_socket.accept()
                print(f"Conexão estabelecida com {endereco_cliente}")

                # Exemplo de recebimento de dados confiavelmente
                dados_recebidos = server.receber_dados_confiavelmente(conexao) #vai receber o dado da conexao que ta la no cliente 

                print("Dados adicionados na lista:", dados_recebidos)

                # Exemplo de envio de dados confiavelmente
                msg = "Resposta do servidor confiável"
                server.enviar_dados_confiavelmente(conexao, msg.encode("utf-8"))
        else:
            while True:
                print("Servidor pronto para receber conexões...")

                # Aceitar conexões
                conexao, endereco_cliente = servidor_socket.accept()
                
                # Iniciar uma nova thread para lidar com a conexão do cliente
                client_thread = threading.Thread(target=server.receber_dados_confiavelmente, args=(conexao, endereco_cliente))
                client_thread.start()
                
    except Exception as e:
        print(f"Erro no servidor: {e}")

    finally:
        # Fechar o socket do servidor
        servidor_socket.close()"""






if __name__ == "__main__":
    main()