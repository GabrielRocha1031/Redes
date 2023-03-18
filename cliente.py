import socket

# Definir o host e a porta do servidor
HOST = '127.0.0.1'  # Endereço IP local
PORT = 5555        # Porta usada pelo servidor

# Cria um objeto socket TCP/IP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conecta o socket ao servidor
client_socket.connect((HOST, PORT))



# Loop para enviar mensagens ao servidor
while True:

    # Recebe a resposta do servidor
    data = client_socket.recv(1024)
    
    # Imprime a resposta do servidor
    print(f"{data.decode()}")


    # Lê uma mensagem do usuário
    message = input(": ")
    
    # Envia a mensagem para o servidor
    client_socket.send(message.encode())
    

# Encerra a conexão com o servidor
client_socket.close()
