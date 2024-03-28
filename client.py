from socket import *

# Create a socket
clientSocket = socket(AF_INET, SOCK_STREAM)

# Connect to the server
clientSocket.connect(('localhost', 12000))

# Send a message to the server
clientSocket.send('Hello, server!'.encode())

# Receive message from server
message = clientSocket.recv(1024).decode()

# Print the message
print(message)

# Close the connection
clientSocket.close()

# Run the server and client code
