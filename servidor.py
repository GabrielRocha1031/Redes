import socket
import threading
import random

class Jogador:
    def __init__(self, sock, addr, num, fichas, cartas, comprando, jogando):
        self.sock = sock
        self.addr = addr
        self.num = num
        self.fichas = fichas
        self.cartas = cartas
        self.comprando = comprando
        self.jogando = jogando

    def exibir_informacoes(self):
        print(f"fichas: {self.fichas}")
        print(f"cartas: {self.cartas}")


# Definição das regras do jogo
valor_cartas = {'A': 11, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10}
baralho = list(valor_cartas.keys()) * 4
random.shuffle(baralho)

# Função para calcular o valor de uma mão
def valor_mao(mao):
    valor = sum([valor_cartas[carta] for carta in mao])
    if valor > 21 and 'A' in mao:
        valor -= 10
    return valor


Jogadores = []
mao_crupie = [baralho.pop(), baralho.pop()]

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




# Função para jogar uma rodada
def jogar_rodada(Jogador, baralho):
    print('teste')
    # Envia uma mensagem de resposta para o cliente
    message = (f"Mão do jogador: {Jogador.cartas}\n Mão do crupie: [{mao_crupie[0]}, ?] \n Deseja comprar mais cartas? (s/n):")
    Jogador.sock.send(message.encode())
    # Recebe mensagem com a resposta
    opcao = Jogador.sock.recv(1024)
    if opcao.lower() == 's':
        Jogador.cartas.append(baralho.pop())
        message = (f"Mão do jogador: {Jogador.cartas}")
        if valor_mao(Jogador.cartas) > 21:
            print('Você estourou! Fim de jogo.')
            Jogador.jogando = 0
            Jogador.comprando = 0
        else:
            Jogador.comprando = 1
            Jogador.jogando = 1
    else:
        Jogador.comprando = 0
        Jogador.jogando = 1
             



# Loop principal do servidor
nJogadores = int(input("Qual o numero de jogadores (1 ate 5): "))
num = 0
while nJogadores != 0:
    # Aguarda uma conexão de cliente
    print("Aguardando conexão de cliente...")
    client_socket, client_address = server_socket.accept()
    print(f"Conexão estabelecida com {client_address}")
    num += 1
    Jogadores.append(Jogador(client_socket, client_address, num, 100, [baralho.pop(), baralho.pop()], 1, 1))
    nJogadores-=1


# Loop principal do jogo
# Num vai indicar se ainda ha jogadores que podem comprar
while num != 0:
    print(f"{num}")
    # Percorre os jogadores ativos na partida
    for Jogador in Jogadores:
        # Chama função de comprar carta
        jogar_rodada(Jogador, baralho)
        if Jogador.comprando == 0:
            num -= 1

print('Vez do crupie')




while valor_mao(mao_crupie) < 17:
    print('Vez do crupie2')
    mao_crupie.append(baralho.pop())
    for Jogador in Jogadores:
        message = (f"Mão do crupie: {mao_crupie}")
        Jogador.sock.send(message.encode())
#if valor_mao(mao_crupie) > 21:
#    print('Crupiê estourou! Você ganhou!')
#elif valor_mao(mao_jogador) > valor_mao(mao_crupie):
#    print('Você ganhou!')
#elif valor_mao(mao_jogador) == valor_mao(mao_crupie):
#    print('Empate!')
#else:
#    print('Você perdeu!')