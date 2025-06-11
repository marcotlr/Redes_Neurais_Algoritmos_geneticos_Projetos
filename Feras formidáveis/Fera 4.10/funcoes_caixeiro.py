import random
import matplotlib.pyplot as plt


def cria_cidades(n, xy_minimo=0, xy_maximo=300):
    """Cria um dicionário aleatório de cidades com suas posições (x,y).

    Args:
      n: Número de cidades que serão visitadas pelo caixeiro.
      xy_minimo: Valor mínimo possível das coordenadas x e y.
      xy_maximo: Valor máximo possível das coordenadas x e y.

    """
    cidades = {}
    num_digitos = len(str(abs(n)))

    for i in range(n):
        cidades[f"Cidade {i:0>{num_digitos}}"] = (
            random.randint(xy_minimo, xy_maximo),
            random.randint(xy_minimo, xy_maximo),
        )

    return cidades


def plota_cidades(cidades):
    """Plota as cidades do problema do caixeiro viajante

    Nota: código de base criado pelo Google Gemini e modificado aqui.

    Args:
      cidades:
        Dicionário contendo o nome das cidades como chaves e a coordenada no
        plano cartesiano das cidades como valores.

    """
    x = [cidades[cidade][0] for cidade in cidades]
    y = [cidades[cidade][1] for cidade in cidades]

    # plotando as cidades
    plt.scatter(x, y, color="blue")

    # nomes das cidades
    for cidade, (x, y) in cidades.items():
        plt.annotate(
            cidade,
            (x, y),
            textcoords="offset points",
            xytext=(0, 10),
            ha="center",
        )

    plt.xlabel("Coordenada x")
    plt.ylabel("Coordenada y")
    plt.show()


def plota_trajeto(cidades, trajeto):
    """Plota o trajeto do caixeiro

    Nota: código de base criado pelo Google Gemini e modificado aqui.

    Args:
      cidades:
        Dicionário contendo o nome das cidades como chaves e a coordenada no
        plano cartesiano das cidades como valores.
      trajeto: lista contendo a ordem das cidades que foram viszitadas

    """
    x = [cidades[cidade][0] for cidade in cidades]
    y = [cidades[cidade][1] for cidade in cidades]

    # plotando as cidades
    plt.scatter(x, y, color="blue")

    # nomes das cidades
    for cidade, (x, y) in cidades.items():
        plt.annotate(
            cidade,
            (x, y),
            textcoords="offset points",
            xytext=(0, 10),
            ha="center",
        )

    # plotando os trajetos
    for i in range(len(trajeto) - 1):
        cidade1 = trajeto[i]
        cidade2 = trajeto[i + 1]
        plt.plot(
            [cidades[cidade1][0], cidades[cidade2][0]],
            [cidades[cidade1][1], cidades[cidade2][1]],
            color="red",
        )

    # trajeto de volta à cidade inicial
    cidade1 = trajeto[-1]
    cidade2 = trajeto[0]
    plt.plot(
        [cidades[cidade1][0], cidades[cidade2][0]],
        [cidades[cidade1][1], cidades[cidade2][1]],
        color="red",
    )

    plt.xlabel("Coordenada x")
    plt.ylabel("Coordenada y")
    plt.show()


def dist_euclidiana(coord1, coord2):
    """Computa a distância Euclidiana entre dois pontos em R^2

    Args:
      coord1: lista contendo as coordenadas x e y de um ponto.
      coord2: lista contendo as coordenadas x e y do outro ponto.

    """
    x1 = coord1[0]
    x2 = coord2[0]
    y1 = coord1[1]
    y2 = coord2[1]

    distancia = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** (1 / 2)

    return distancia

def repara_trajeto(candidato):
    """
    Garante:
      - Cidade 0 no início
      - Todas as cidades de índice ímpar logo após, na ordem relativa original
      - Depois todas as cidades de índice par (exceto a zero), na ordem relativa original
    """
    def num(cidade):
        return int(cidade.split()[1])
    
    zero = []
    outros = []
    for cidade in candidato:
        if num(cidade) == 0:
            zero.append(cidade)
        else: 
            outros.append(cidade)
    impar = []
    par = []
    for cidade in outros:
        if num(cidade) % 2 == 1:
            impar.append(cidade)
        else: 
            par.append(cidade)
    
    return zero + impar + par

def cria_candidato_caixeiro(cidades):
    """Sorteia um caminho válido para o Caixeiro que prefere cidades ímpares"""
    nomes_cidades = list(cidades.keys())
    caminho = random.sample(nomes_cidades, k=len(nomes_cidades))
    return repara_trajeto(caminho)


def populacao_caixeiro(tamanho_populacao, cidades):
    """Cria uma população no problema do caixeiro viajante

    Args:
      tamanho_populacao: tamanho da população.
      cidades:
        Dicionário contendo o nome das cidades como chaves e a coordenada no
        plano cartesiano das cidades como valores.

    """
    populacao = []

    for _ in range(tamanho_populacao):
        populacao.append(cria_candidato_caixeiro(cidades))

    return populacao


def funcao_objetivo_caixeiro(candidato, cidades):
    """Funcao objetivo de um candidato no problema do caixeiro viajante

    Args:
      candidato: uma lista contendo o caminho percorrido
      cidades:
        Dicionário contendo o nome das cidades como chaves e a coordenada no
        plano cartesiano das cidades como valores.

    """
    distancia = 0

    for pos in range(len(candidato) - 1):
        coord_cidade_partida = cidades[candidato[pos]]
        coord_cidade_chegada = cidades[candidato[pos + 1]]
        distancia += dist_euclidiana(
            coord_cidade_partida, coord_cidade_chegada
        )

    # distância para retornar à cidade inicial
    coord_cidade_final = cidades[candidato[-1]]
    coord_cidade_inicial = cidades[candidato[0]]
    distancia += dist_euclidiana(coord_cidade_final, coord_cidade_inicial)

    return distancia


def funcao_objetivo_pop_caixeiro(populacao, cidades):
    """Funcao objetivo de uma populacao no problema do caixeiro viajante

    Args:
      populacao: lista contendo os individuos do problema
      cidades:
        Dicionário contendo o nome das cidades como chaves e a coordenada no
        plano cartesiano das cidades como valores.

    """
    fitness = []

    for individuo in populacao:
        fitness.append(funcao_objetivo_caixeiro(individuo, cidades))

    return fitness


###############################################################################
#                                   Caixeiro                                  #
###############################################################################
def selecao_torneio_min(populacao, fitness, tamanho_torneio):
    """Faz a seleção de uma população usando torneio.

    Nota: da forma que está implementada, só funciona em problemas de
    minimização.

    Args:
      populacao: lista contendo os individuos do problema
      fitness: lista contendo os valores computados da funcao objetivo
      tamanho_torneio: quantidade de invíduos que batalham entre si

    """
    selecionados = []

    for _ in range(len(populacao)):
        sorteados = random.sample(populacao, tamanho_torneio)

        fitness_sorteados = []
        for individuo in sorteados:
            indice_individuo = populacao.index(individuo)
            fitness_sorteados.append(fitness[indice_individuo])

        min_fitness = min(fitness_sorteados)
        indice_min_fitness = fitness_sorteados.index(min_fitness)
        individuo_selecionado = sorteados[indice_min_fitness]

        selecionados.append(individuo_selecionado)

    return selecionados



def cruzamento_ordenado(pai, mae, chance_de_cruzamento):
    """Cruzamento ordenado entre 2 indivíduos"""
    
    if random.random() < chance_de_cruzamento:
        tamanho = len(pai)
        
        # pontos de corte
        corte1 = random.randint(0, tamanho - 2)
        corte2 = random.randint(corte1 + 1, tamanho)

        #Filho 1 
        filho1 = [None] * tamanho
        filho1[corte1:corte2] = mae[corte1:corte2]
        pai_ = pai[corte2:] + pai[:corte2]
        pos = corte2 % tamanho
        for gene in pai_:
            if gene not in filho1:
                filho1[pos] = gene
                pos += 1
                pos %= tamanho

        # ---- Filho 2 ----
        filho2 = [None] * tamanho
        filho2[corte1:corte2] = pai[corte1:corte2]
        mae_ = mae[corte2:] + mae[:corte2]
        pos = corte2 % tamanho
        for gene in mae_:
            if gene not in filho2:
                filho2[pos] = gene
                pos += 1
                pos %= tamanho

        # reparo para garantir a ordem desejada
        filho1 = repara_trajeto(filho1)
        filho2 = repara_trajeto(filho2)
        return filho1, filho2
    else:
        return repara_trajeto(pai), repara_trajeto(mae)


###############################################################################
#                              Operador de Mutação                            #
###############################################################################



def mutacao_troca(populacao, chance_de_mutacao):
    """Aplica mutação de troca em um indivíduo

    Args:
        populacao: lista contendo os indivíduos do problema
        chance_de_mutacao: float entre 0 e 1 representando a chance de mutação
    """
    
           
    for posicao, individuo in enumerate(populacao):
        if random.random() < chance_de_mutacao:
            gene1 = random.randint(0, len(individuo) - 1)
            gene2 = random.randint(0, len(individuo) - 1)

            # garante que gene1 e gene2 sejam diferentes
            while gene1 == gene2:
                gene1 = random.randint(0, len(individuo) - 1)
                gene2 = random.randint(0, len(individuo) - 1)

            # realiza a troca
            individuo[gene1], individuo[gene2] = (
                individuo[gene2],
                individuo[gene1],
            )

            # reparo para manter a ordem: Cidade 0 → ímpares → pares
            populacao[posicao] = repara_trajeto(individuo)

    
    
