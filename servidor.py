import socket
import threading
import random

# Objeto jogador
class Jogador:
    def __init__(self, sock, addr, num, saldo, apostado, cartas, soma_das_cartas, comprando, jogando, Jblackjack):
        self.sock = sock
        self.addr = addr
        self.num = num
        self.saldo = saldo
        self.apostado = apostado
        self.cartas = cartas
        self.soma_das_cartas = soma_das_cartas
        self.comprando = comprando
        self.jogando = jogando

    def exibir_informacoes(self):
        print(f"saldo: {self.saldo}")
        print(f"cartas: {self.cartas}")


# Definição das regras do jogo
valor_cartas = {'A': 11, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10}
baralho = list(valor_cartas.keys()) * 4
random.shuffle(baralho)

# Variaveis do jogo
saldo_do_jogo = 0
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

# Função para calcular o valor de uma mão
def valor_mao(mao):
    valor = sum([valor_cartas[carta] for carta in mao])
    if valor > 21 and 'A' in mao:
        valor -= 10
    return valor

# Informa que jogador fez 21
def blackjack(Jogador):

    message = (f"Mão do jogador: {Jogador.cartas}\nParabéns!!! Você fez 21 e ganhou!")
    Jogador.sock.send(message.encode())

# Futura funcao que define o ganhador
#def ganhador(Jogadores):
#    for Jogador in Jogadores:

    #para fazer comparacoes e premiacoes deve-se ter: soma das cartas de cada jogador e valor apostado

    #if valor_mao(mao_crupie) > 21:
    #    message = ("Crupiê estourou! Você ganhou!")
    #    Jogador.sock.send(message.encode())
    #
    #elif valor_mao(mao_jogador) > valor_mao(mao_crupie):
    #    message = ("Você ganhou!")
    #    Jogador.sock.send(message.encode())
    #elif valor_mao(mao_jogador) == valor_mao(mao_crupie):
    #    print('Empate!')
    #else:
    #    print('Você perdeu!')




# Função para jogar uma rodada
def jogar_rodada(Jogador, baralho):


    Jogador.soma_das_cartas = valor_mao(Jogador.cartas)
    print(f"soma das cartas: {Jogador.soma_das_cartas} Apostado: {Jogador.apostado}")

    #verifica blackjack
    if Jogador.soma_das_cartas == 21:
        blackjack(Jogador)

    Jogador.soma_das_cartas = valor_mao(Jogador.cartas)
    # Envia uma mensagem de resposta para o cliente
    message = (f"Mão do jogador: {Jogador.cartas}\nMão do crupie: [{mao_crupie[0]}, ?] \nDeseja comprar mais cartas? (s/n):")
    Jogador.sock.send(message.encode())
    # Recebe mensagem com a resposta
    opcao = Jogador.sock.recv(1024)
    print(f"{opcao.decode()}")
    # horas foram perdidas graças a este .decode()

    if opcao.decode() == 's':
        Jogador.cartas.append(baralho.pop())
        Jogador.soma_das_cartas = valor_mao(Jogador.cartas)
        if valor_mao(Jogador.cartas) == 21:
             blackjack(Jogador)
        elif valor_mao(Jogador.cartas) > 21:
            message = (f"Mão do jogador: {Jogador.cartas}\nVocê estorou :c que pena...")
            Jogador.sock.send(message.encode())
            resposta = Jogador.sock.recv(1024)
            print(f"{resposta.decode()}")
            Jogador.jogando = 0
            Jogador.comprando = 0
        else:
            message = (f"Mão do jogador: {Jogador.cartas}\nAguarde a proxima rodada... ok? (responder)")
            Jogador.sock.send(message.encode())
            resposta = Jogador.sock.recv(1024)
            print(f"{resposta.decode()}")
            Jogador.comprando = 1
            Jogador.jogando = 1
    else:
        message = ("Você parou, aguarde enquanto os outro jogam...")
        Jogador.sock.send(message.encode())
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
    #######sock, addr, num, saldo, apostado, cartas, soma_das_cartas, comprando, jogando, Jblackjack#######
    Jogadores.append(Jogador(client_socket, client_address, num, 100, 0, [baralho.pop(), baralho.pop()],0,  1, 1, 0))
    nJogadores-=1


# Loop principal do jogo
# Num vai indicar se ainda ha jogadores que podem comprar
while num != 0:
    # Percorre os jogadores ativos na partida
    for Jogador in Jogadores:
        # Chama função de comprar carta
        if Jogador.comprando == 1:
            jogar_rodada(Jogador, baralho)
            print(f"{num}")
            if Jogador.comprando == 0:
                num -= 1

print('Vez do crupie')


#Crupie termina de comprar suas cartas seguindo as regras pre definidas
while valor_mao(mao_crupie) < 17:
    print('Vez do crupie2')
    mao_crupie.append(baralho.pop())

for Jogador in Jogadores:
    message = (f"Mão do crupie: {mao_crupie}")
    Jogador.sock.send(message.encode())

#-----------Programa ta acabando aqui----------------

# Chama a futura funcao que define o ganhador
#ganhador(Jogadores)


    
