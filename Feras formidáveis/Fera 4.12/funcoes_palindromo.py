import random


###############################################################################
#                              Palíndromos                                    #
###############################################################################

def checa_vogal(n_letras, candidato, vogais):
    """Confere a existência de vogal no candidato dos palindromos

    Args:
       n_letras: inteiro que representa o número de letras de cada palindromo.
       candidato: uma lista contendo as letras usadas no palindromo
       vogais: lista contendo as vogais
    """

    if not any(letra in vogais for letra in candidato):
        indice = random.randint(0, n_letras-1)
        vogal = random.choice(vogais)
        candidato[indice] = vogal
        candidato[-indice-1] = vogal

    else:
        pass


def gene_palindromo(letras_possiveis):
    """Sorteia uma letra para o gene do palindromo"""
    
    gene = random.choice(letras_possiveis)
    return gene


def cria_candidato_palindromo(n_letras, letras_possiveis, vogais):
    """Cria uma lista contendo n_letras de letras.
    Args:
       n_letras: inteiro que representa o número de letras de cada palindromo.
       letras_possiveis: letras possíveis de serem sorteadas.
       vogais: lista contendo as vogais
    """
    candidato = []
    for _ in range(n_letras):
        candidato.append(gene_palindromo(letras_possiveis))

    checa_vogal(n_letras, candidato, vogais)
    return candidato


def populacao_palindromo(tamanho_pop, n_letras, letras_possiveis, vogais):
    """Cria uma população para o problema das caixas binárias.

    Args:
      tamanho_pop: tamanho da população
      n_letras: inteiro que representa o número de letras de cada palindromo.
      letras_possiveis: letras possíveis de serem sorteadas.
      vogais: lista contendo as vogais

    """

    populacao = []
    for _ in range(tamanho_pop):
        populacao.append(cria_candidato_palindromo(n_letras, letras_possiveis, vogais))

    return populacao


def funcao_objetivo_palindromo(candidato):
    """Computa a função objetivo no problema do palindromo

    Args:
      candidato: uma lista contendo as letras usadas no palindromo

    """
    distancia = 0 

    for i in range(len(candidato) // 2):
        distancia += abs(ord(candidato[i]) - ord(candidato[-i - 1]))

    return distancia


def funcao_objetivo_pop_palindromo(populacao):
    """Computa a função objetivo para uma população dos palindromos

    Args:
      populacao: lista contendo os individuos do problema

    """
    fitness = []
    for individuo in populacao:
        fitness.append(funcao_objetivo_palindromo(individuo))
    return fitness





###############################################################################
#                                   Seleção                                   #
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


###############################################################################
#                                  Cruzamento                                 #
###############################################################################


def cruzamento_espelhado(pai, mae, chance_de_cruzamento, n_letras, vogais):
    """Realiza cruzamento espelhado 

    Args:
       pai: lista representando um individuo
       mae: lista representando um individuo
       chance_de_cruzamento: float entre 0 e 1 representando a chance de cruzamento
       n_letras: inteiro que representa o número de letras de cada palindromo.
       vogais: lista contendo as vogais
"""

    if random.random() < chance_de_cruzamento:
        
        filho1 = pai.copy()
        filho2 = mae.copy()
        indice_trocado = random.randint(0, len(pai)-1) 

        filho1[indice_trocado], filho1[-indice_trocado-1] = mae[indice_trocado], mae[-indice_trocado-1]
        filho2[indice_trocado], filho2[-indice_trocado-1] = pai[indice_trocado], pai[-indice_trocado-1]

        checa_vogal(n_letras, filho1, vogais)
        checa_vogal(n_letras, filho2, vogais)

        return filho1, filho2
    
    else:
        return pai, mae


###############################################################################
#                                   Mutação                                   #
###############################################################################


def mutacao_espelhada(populacao, chance_de_mutacao, letras_possiveis, vogais, n_letras):
    """Realiza mutação simples

    Args:
       populacao: lista contendo os indivíduos do problema
       chance_de_mutacao: float entre 0 e 1 representando a chance de mutação
       letras_possiveis: lista com todos os valores possíveis dos genes
       n_letras: inteiro que representa o número de letras de cada palindromo.
       vogais: lista contendo as vogais
"""

    for individuo in populacao:  

        if random.random() < chance_de_mutacao:
            gene = random.randint(0, len(individuo) -1)      
            novo_gene = random.choice(letras_possiveis)
            individuo[gene] = novo_gene
            individuo[-gene-1] = novo_gene   

        checa_vogal(n_letras, individuo, vogais)     
        
