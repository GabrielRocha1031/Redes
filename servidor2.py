import socket
import threading
import random

# Definir o host e a porta para o servidor
HOST = '127.0.0.1'  # Endereço IP local
PORT = 5555        # Porta para escutar as conexões (Nao usar 8000)

# Cria um objeto socket TCP/IP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define as opções do socket para permitir reuso de endereços
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Vincula o socket ao host e porta definidos
server_socket.bind((HOST, PORT))

# Aguarda as conexões de clientes
server_socket.listen()

# Função que lida com as conexões de cada cliente
def handle_client(client_socket, client_address):
    print(f"Conexão estabelecida com {client_address}")
    
    # Loop para receber as mensagens do cliente
    while True:
        # Recebe os dados enviados pelo cliente
        data = client_socket.recv(1024)
        
        # Verifica se o cliente encerrou a conexão
        if not data:
            print(f"Conexão encerrada por {client_address}")
            break
        
        # Imprime a mensagem recebida do cliente
        print(f"Mensagem recebida de {client_address}: {data.decode()}")
        
        # Envia uma mensagem de resposta para o cliente
        message = "Mensagem recebida pelo servidor"
        client_socket.send(message.encode())
    
    # Encerra a conexão com o cliente
    client_socket.close()

# Loop principal do servidor
jogadores = int(input("Qual o numero de jogadores: "))
while jogadores != 0:
    # Aguarda uma conexão de cliente
    print("Aguardando conexão de cliente...")
    client_socket, client_address = server_socket.accept()
    
    # Cria uma nova thread para lidar com o cliente
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()
    jogadores-=1
