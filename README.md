#Modo de uso
Rodar o arquivo MainServer.py em um terminal e o arquivo MainCliente.py em outro.


# 1. Introdução
O projeto desenvolvido para a cadeira de Comunicação de Redes consiste em um sistema de comunicação entre cliente e servidor, implementando funcionalidades básicas de uma lista telefônica digital. O sistema permite adicionar e buscar contatos através de uma interface de rede, utilizando o protocolo TCP/IP para garantir a entrega e a integridade das mensagens.

# 2. Visão Geral dos Arquivos

- ClasseMae: Contém métodos úteis para calcular checksums e simular falhas de integridade.
- classMsgAdd: Define uma mensagem para adicionar contatos.
- classMsgGet: Define uma mensagem para buscar contatos.
- MainClient: Script principal do cliente que gerencia a interface de usuário e a comunicação de rede.
- client: Biblioteca de suporte que implementa a lógica de negócio do cliente.
- MainServer: Script principal do servidor que aceita e gerencia conexões de clientes.
- server: Biblioteca de suporte que implementa a lógica de negócio do servidor.

# 3. Análise Detalhada dos Códigos
## ClasseMae
- Esta classe contém métodos fundamentais para calcular o checksum de dados utilizando MD5, o que é crucial para verificar a integridade dos dados na comunicação de rede. Além disso, inclui um método para simular falhas de integridade, útil para testar a robustez do sistema.

## classMsgAdd e classMsgGet
- Estas classes representam os dois tipos de ações que podem ser executadas no sistema: adicionar e buscar contatos. Ambas são serializáveis em JSON para facilitar a transmissão através da rede.

## MainClient e client
- O MainClient configura a conexão de rede e gere o loop principal onde as ações do usuário são capturadas e processadas. O módulo client contém métodos específicos para enviar e receber mensagens, além de implementar lógicas de garantia de integridade através de checksum.

## MainServer e server
- O MainServer é responsável por configurar o servidor, aceitar conexões de clientes e iniciar threads para gerenciar essas conexões individualmente. O módulo server processa as mensagens recebidas, atualiza a lista telefônica e assegura a resposta ao cliente.

# 4. Comunicação e Integridade de Dados
A integridade dos dados é garantida pelo uso de checksums MD5, que são calculados tanto no envio quanto no recebimento de dados. Além disso, são implementados mecanismos de timeout e retransmissão para lidar com falhas temporárias de rede.

# 5. Fluxo de Mensagens e Tratamento de Erros
O sistema implementa um protocolo robusto onde cada mensagem é validada quanto à sua integridade e sequência correta. Erros são tratados de maneira a informar o usuário e tentar recuperar a operação quando possível.

# 6. Conclusão
O sistema desenvolvido oferece uma base sólida para uma aplicação de lista telefônica digital, com ênfase na confiabilidade e integridade da comunicação entre cliente e servidor.

# 7. Anexos
Os códigos-fonte anexados ao relatório proporcionam uma visão completa das implementações detalhadas acima.
