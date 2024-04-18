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

        while True:
            opcao = client.menu()
            qtd_threads = 5

            if opcao == '1':
                nome = input("ADigite o nome do contato: ")
                telefone = input("Digite o telefone do contato: ")

                dadoParaEnviar = client.enviarMsg_add_telefone(nome, telefone)
                client.enviar_dados_confiavelmente(cliente_socket, dadoParaEnviar.encode())
                
                dados_recebidos = client.receber_dados_confiavelmente(cliente_socket)
                print("Resposta do servidor:", dados_recebidos.decode())

            elif opcao == '2':
                nome = input("ADigite o nome do contato: ")
                telefone = input("Digite o telefone do contato: ")

                dadoParaEnviar = client.enviarMsg_add_telefone(nome, telefone)
                
                client.simulate_integrity_error(cliente_socket, dadoParaEnviar.encode())
                dados_recebidos = client.receber_dados_confiavelmente(cliente_socket)
                print("Resposta do servidor:", dados_recebidos.decode())
            
            elif opcao == '3':
                break
            else:
                print("Opção inválida.")

    except Exception as e:
        print(f"Erro ao conectar ao servidor: {e}")

if __name__ == "__main__":
    main()

