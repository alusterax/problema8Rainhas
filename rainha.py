import random
import matplotlib.pyplot as plt
import numpy
popMax = 1000
genMax = False
numRainha = 8
elitista = False

def fitness(cromossomo):
    colisoesHorizontais = sum([cromossomo.count(queen)-1 for queen in cromossomo])/2
    colisoesDiagonais = 0

    n = len(cromossomo)
    diagonalEsq = [0] * 2*n
    diagonalDir = [0] * 2*n
    for i in range(n):
        diagonalEsq[i + cromossomo[i] - 1] += 1
        diagonalDir[len(cromossomo) - i + cromossomo[i] - 2] += 1

    colisoesDiagonais = 0
    for i in range(2*n-1):
        qtd = 0
        if diagonalEsq[i] > 1:
            qtd += diagonalEsq[i]-1
        if diagonalDir[i] > 1:
            qtd += diagonalDir[i]-1
        colisoesDiagonais += qtd / (n-abs(i-n+1))

    return int(maxFitness - (colisoesHorizontais + colisoesDiagonais)) # 28 <- Valor máximo, a cada colisão diminui 1
    #Ex: 2 colisões = 26
    #    0 colisões = 28 (e acaba o programa)

def evolucao(populacao, fitness):
    porcentagemMutacao = 0.03
    porcentagemParentes = 0.6
    popNew = []
    parentesIniciais = []

    parenteLen = int(porcentagemParentes*len(populacao))

    if (elitista):
        populationSort = sorted(populacao, key=lambda x: fitness(x), reverse=True)
        parentes = populationSort[:parenteLen]
        for p in parentes:
            pai = parentes[random.randint(0,len(parentes)-1)]
            mae = parentes[random.randint(0,len(parentes)-1)]
            filho = reproduzir(pai,mae)
            if random.random() < porcentagemMutacao:
                filho = mutacao(filho)
            popNew.append(filho)
            if fitness(filho) == maxFitness: break
        return popNew
    else:
        prob = [probabilidade(n, fitness) for n in populacao]
        for i in range(len(populacao)):
            pai = roleta(populacao, prob) # Roleta 1
            mae = roleta(populacao, prob) # Roleta 2
            filho = reproduzir(pai, mae)
            if random.random() < porcentagemMutacao:
                filho = mutacao(filho)
            popNew.append(filho)
            if fitness(filho) == maxFitness: break
        return popNew

def criaIndividuo(size): #cria tabuleiros com posicoes aleatorias
    return [ random.randint(1, numRainha) for x in range(numRainha) ]

def roleta(populacao, prob):
    popProb = zip(populacao, prob)
    totalFitnessPop = sum(w for pop, w in popProb)
    pick = random.uniform(0, totalFitnessPop)
    atualSelec = 0
    for pop, w in zip(populacao, prob):
        if atualSelec + w >= pick:
            return pop
        atualSelec += w

def probabilidade(cromossomo, fitness):
    return fitness(cromossomo) / maxFitness

def reproduzir(x, y): #cruzamento, só um ponto de corte aleatorio
    n = len(x)
    c = random.randint(0, n - 1)
    return x[0:c] + y[c:n]

def mutacao(x):  # Mutação simples, troca uma posição do array de 0 pra 1 ou vice-versa
    n = len(x)
    c = random.randint(0, n - 1)
    m = random.randint(1, n)
    x[c] = m
    return x

def plotaGrafico(melhores,geracoes):
    plt.plot(geracoes,melhores)
    if (elitista):
        plt.title('Gerações x Fitness | Método Elitista | Mutação 3%')
    else:
        plt.title('Gerações x Fitness | Método Roleta | Mutação 3%')
    plt.ylabel('Fitness')
    plt.xlabel('Geração')

maxFitness = (numRainha*(numRainha-1))/2  #Valor maximo seria 8*7/2 = 28.
#maxFitness = numRainha  #Valor maximo seria 8*7/2 = 28.
populacao = [criaIndividuo(numRainha) for x in range(popMax)]

gen = 1
melhores = []
geracoes = []
#Rodar até achar
while not maxFitness in [fitness(individuo) for individuo in populacao]:
    populacao = evolucao(populacao, fitness)
    maxFit = max([fitness(n) for n in populacao])
    populationSort = sorted(populacao, key=lambda x: fitness(x), reverse=True)
    best = populacao[0]
    melhores.append(maxFit)
    geracoes.append(gen)
    print(f'Geração {gen} - Melhor: {best} - Fitness: {maxFit}')
    gen += 1

saidaGrafico = []
melhores.append(maxFit)
geracoes.append(gen)
print(f"Achou em {gen} gerações!")
for individuo in populacao:
    if fitness(individuo) == maxFitness:
        saidaGrafico = individuo
        print(f'\nResultado: {individuo}')

tabuleiro = []

#Monta tabuleiro para printar
for x in range(numRainha):
    tabuleiro.append(["x"] * numRainha)

for i in range(numRainha):
    tabuleiro[numRainha-saidaGrafico[i]][i]="Q"


def printaTabuleiro(tabuleiro):
    for row in tabuleiro:
        print (" ".join(row))

#print()
printaTabuleiro(tabuleiro)
plotaGrafico(melhores,geracoes)
