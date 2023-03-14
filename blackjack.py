import random

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

# Função para jogar uma rodada
def jogar_rodada(baralho):
    mao_jogador = [baralho.pop(), baralho.pop()]
    mao_crupie = [baralho.pop(), baralho.pop()]
    print(f'Mão do jogador: {mao_jogador}')
    print(f'Mão do crupiê: [{mao_crupie[0]}, ?]')
    while True:
        opcao = input('Deseja pedir mais uma carta? (s/n) ')
        if opcao.lower() == 's':
            mao_jogador.append(baralho.pop())
            print(f'Mão do jogador: {mao_jogador}')
            if valor_mao(mao_jogador) > 21:
                print('Você estourou! Fim de jogo.')
                return -1
        else:
            break
    while valor_mao(mao_crupie) < 17:
        mao_crupie.append(baralho.pop())
    print(f'Mão do jogador: {mao_jogador} (valor {valor_mao(mao_jogador)})')
    print(f'Mão do crupiê: {mao_crupie} (valor {valor_mao(mao_crupie)})')
    if valor_mao(mao_crupie) > 21:
        print('Crupiê estourou! Você ganhou!')
        return 1
    elif valor_mao(mao_jogador) > valor_mao(mao_crupie):
        print('Você ganhou!')
        return 1
    elif valor_mao(mao_jogador) == valor_mao(mao_crupie):
        print('Empate!')
        return 0
    else:
        print('Você perdeu!')
        return -1

# Loop principal do jogo
saldo = 100

while saldo > 0:
    print(f'Seu saldo é de {saldo} fichas.')
    aposta = int(input('Quanto você quer apostar? '))
    if aposta > saldo:
        print('Aposta inválida! Você não tem fichas suficientes.')
     

        continue
    resultado = jogar_rodada(baralho)
    saldo += resultado * aposta
print('Fim de jogo!')
