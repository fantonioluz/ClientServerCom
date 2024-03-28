from socket import *

# Create a socket   
serverSocket = socket(AF_INET, SOCK_STREAM)

# Bind the socket to the address and port
serverSocket.bind(('localhost', 12000))

# Listen for incoming connections
serverSocket.listen(1)

print('The server is ready to receive')

while True:
    # Accept incoming connection
    connectionSocket, addr = serverSocket.accept()

    # Receive message from client
    message = connectionSocket.recv(1024).decode()

    # Print the message
    print(message)

    # Send a message to the client
    connectionSocket.send('Hello, client!'.encode())

    # Close the connection
    connectionSocket.close()