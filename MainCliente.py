# Função principal do cliente
import socket
import client
import threading

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

        # Definir parâmetros da janela deslizante
        # window_size = 3  # Tamanho da janela
        # base_sequence_number = 0  # Número de sequência base
        # next_sequence_number = 0  # Próximo número de sequência a ser usado
        # window = {}  # Dicionário para controlar os pacotes na janela
        
        """# Exemplo de envio de dados confiavelmente
        #enviar_dados_confiavelmente(cliente_socket, "Dados de teste confiáveis".encode("utf-8"))
        dadoParaEnviar = client.enviarMsg_add_telefone(cliente_socket, 'teste', '111111111')
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
        cliente_socket.close()"""
        
        while True:
            opcao = client.menu()
            qtd_threads = 5

            if opcao == '1':
                nome = input("ADigite o nome do contato: ")
                telefone = input("Digite o telefone do contato: ")

                dadoParaEnviar = client.enviarMsg_add_telefone(nome, telefone)
                client.enviar_dados_confiavelmente(cliente_socket, dadoParaEnviar.encode())
                
                #while qtd_threads != 5:
                #    thread = threading.Thread(target=client.enviar_dados_confiavelmente, args=(cliente_socket, dadoParaEnviar))
                #    thread.start()
                #    qtd_threads += 1
                    
                # Recebendo confirmação do servidor
                dados_recebidos = client.receber_dados_confiavelmente(cliente_socket)
                print("Resposta do servidor:", dados_recebidos.decode())

            elif opcao == '2':
                
                break
            
            elif opcao == '3':
                cliente_socket.close()
                break
            else:
                print("Opção inválida.")

    except Exception as e:
        print(f"Erro ao conectar ao servidor: {e}")

if __name__ == "__main__":
    main()

