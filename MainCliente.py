# Função principal do cliente
import socket
from time import sleep
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

        while True:
            sleep(1)
            opcao = client.menu()
            qtd_threads = 5

            if opcao == '1':
                nome = input("Digite o nome do contato: ")
                telefone = input("Digite o telefone do contato: ")

                dadoParaEnviar = client.enviarMsg_add_telefone(nome, telefone)
                client.enviar_dados_confiavelmente(cliente_socket, dadoParaEnviar.encode())
                
               # dados_recebidos = client.receber_dados_confiavelmente(cliente_socket)
                #print("Resposta do servidor:", dados_recebidos.decode())

            elif opcao == '2':
                nome = input("Digite o nome do contato: ")
                telefone = input("Digite o telefone do contato: ")

                dadoParaEnviar = client.enviarMsg_add_telefone(nome, telefone)
                
                client.simulate_integrity_error(cliente_socket, dadoParaEnviar.encode())
                dados_recebidos = client.receber_dados_confiavelmente(cliente_socket)
                print("Resposta do servidor:", dados_recebidos.decode())
            
            elif opcao == '4':
                cliente_socket.close()
                break
            
            elif opcao == '3':
                #digite o nome e o contato para enviar
                nome = input("Digite o nome do contato: ")
                telefone = input("Digite o telefone do contato: ")
                
                
                #enviar varios pacotes ao mesmo tempo
                for i in range(qtd_threads):
                    thread = threading.Thread(target=client.enviar_dados_confiavelmente, args=(cliente_socket, client.enviarMsg_add_telefone(nome, telefone).encode()))
                    thread.start()
            else:
                print("Opção inválida.")

    except Exception as e:
        print(f"Erro ao conectar ao servidor: {e}")
        
    finally:
        # Fechar o socket do cliente
        cliente_socket.close()

if __name__ == "__main__":
    main()

