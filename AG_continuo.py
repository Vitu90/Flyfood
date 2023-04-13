from random import *
from typing import Callable, List, Tuple

import matplotlib.pyplot as plt

arq = open("wi29.txt", 'r')
matriz = []
for linha in arq:
    linha = linha.split()
    matriz.append(linha)
arq.close()


def get_item(list, i: int, k: int) -> int:
    elemento = list[i][k]
    return elemento


posicao = []
tamanho = len(matriz)
pontos_entrega = list(range(tamanho))
for i in range(tamanho):
    posicao_x = get_item(matriz, i, 1)
    posicao_y = get_item(matriz, i, 2)
    posicao.append((posicao_x, posicao_y))

for i in pontos_entrega:
    pontos_entrega[i] = pontos_entrega[i]+1

pontos_entrega.pop(0)
start = posicao[0]
posicao.pop(0)


def idx(ponto: str) -> int:
    indicie = pontos_entrega.index(ponto)
    return indicie


def calc_dist(a, b):
    indicie_a = idx(a)
    indicie_b = idx(b)
    xa = float(posicao[indicie_a][0])
    xb = float(posicao[indicie_b][0])
    ya = float(posicao[indicie_a][1])
    yb = float(posicao[indicie_b][1])
    dist = ((xa-xb)**2 + (ya-yb)**2)**(1/2)
    return dist


def gerar_pop(n_pop, gene):
    pop = [""] * n_pop
    for i in range(n_pop):
        individuo = sample(gene, len(gene))
        pop[i] = individuo
    return pop


def aptidao(pop):
    """aptidão de uma população"""
    lista_aptidao: list[float] = [0] * len(pop)
    lista_aptidao_aux: list[float] = [0] * len(pop)
    for i, ind in enumerate(pop):
        lista_aptidao_aux[i] = aptidao_individuo(ind)
    soma = sum(lista_aptidao_aux)
    media = soma/len(lista_aptidao_aux)
    for i in range(len(lista_aptidao_aux)):
        lista_aptidao[i] = lista_aptidao_aux[i]/media
    return lista_aptidao


def aptidao_individuo(cromossomo: str) -> float:
    """cálculo da aptidão de um único indivíduo"""
    apt = 1/dist_total(cromossomo)
    return apt


def dist_total(rota):
    aux = dist_rota(rota)
    aux2 = dist_restaurante(start, rota)
    resultado = aux + aux2
    return resultado


def dist_rota(rota):
    dist_percurso = 0
    for i in range(len(rota)-1):
        dist = calc_dist(rota[i], rota[i+1])
        dist_percurso = dist_percurso + dist

    return dist_percurso


def dist_restaurante(start, rota):
    xa = float(start[0][0])
    ya = float(start[0][1])
    inicio = rota[0]
    indicie_inicio = idx(inicio)
    fim = rota[-1]
    indicie_fim = idx(fim)
    x_inicio = float(posicao[indicie_inicio][0])
    y_inicio = float(posicao[indicie_inicio][1])
    x_fim = float(posicao[indicie_fim][0])
    y_fim = float(posicao[indicie_fim][1])
    dist1 = ((xa-x_inicio)**2 + (ya-y_inicio)**2)**1/2
    dist2 = dist = ((xa-x_fim)**2 + (ya-y_fim)**2)**(1/2)
    dist = dist1+dist2
    return dist


def roleta(apt: List[float]) -> int:
    """Seleção por roleta"""
    soma_roleta: float = sum(apt)
    n_sorteado: float = random() * soma_roleta
    soma_atual: float = 0
    for i, apt in enumerate(apt):
        soma_atual += apt
        if soma_atual >= n_sorteado:
            return i


def torneio(apt: List[float]) -> int:
    """Seleção por torneio"""
    pai1 = randint(0, len(apt) - 1)
    pai2 = randint(0, len(apt) - 1)
    return pai1 if apt[pai1] > apt[pai2] else pai2


def selecao_pais(pop, apt, sel_func: Callable):
    """Seleção dos pais"""
    lista_pais = [None] * len(pop)
    for i in range(len(pop)):
        idx_selecionado = sel_func(apt)
        lista_pais[i] = pop[idx_selecionado]
    return lista_pais


def cruzamento(pais, taxa_cruzamento):
    """cruzamento de todos os pais"""
    lista_filhos = [None] * len(pais)
    for i in range(0, len(pais)-1, 2):
        filho1, filho2 = cruzamento_pais(pais[i], pais[i + 1], taxa_cruzamento)
        lista_filhos[i] = filho1
        lista_filhos[i + 1] = filho2
    return lista_filhos


def cruzamento_pais(pai1, pai2, taxa_cruzamento: float):
    """cruzamento de dois individuos"""
    if random() <= taxa_cruzamento:
        ponto_cruzamento = randint(2, len(pai1) - 1)
        filho_aux_1 = pai1[: ponto_cruzamento]
        offspring_1 = pai2[ponto_cruzamento:]

        filho_aux_2 = pai2[: ponto_cruzamento]
        offspring_2 = pai1[ponto_cruzamento:]

        filho_1 = filho_aux_1 + (PMX(filho_aux_1, filho_aux_2, offspring_2))
        filho_2 = filho_aux_2 + (PMX(filho_aux_2, filho_aux_1, offspring_1))

        return filho_1, filho_2
    return pai1, pai2


def busca(lista, alvo):
    tamanho_da_lista = len(lista)
    for atual in range(0, tamanho_da_lista):
        if (lista[atual] == alvo):
            return atual

    return -1


def PMX(filho_aux_1, filho_aux_2, offspring):
    for i in range(len(offspring)):
        resultado = busca(filho_aux_1, offspring[i])
        if resultado != -1:
            offspring[i] = filho_aux_2[resultado]
    return offspring


def mutacao_individuo(filho, taxa_mutacao: float):
    """mutação de um individuo"""
    filho_mutado = filho
    for i in range(len(filho)):
        # pra cada gene
        if random() <= taxa_mutacao:
            found = False
            while found == False:
                posicao_aleatoria = randint(0, len(filho)-1)
                if posicao_aleatoria != i:
                    found = True
            filho_mutado[i], filho_mutado[posicao_aleatoria] = filho_mutado[posicao_aleatoria], filho_mutado[i]

    return filho_mutado


def mutacao(filhos, taxa_mutacao: float):
    """Mutação de todos os filhos"""
    for i, ind in enumerate(filhos):
        filhos[i] = mutacao_individuo(ind, taxa_mutacao)
    return filhos


def selecao_sobreviventes(
    pop, apt_pop, filhos, apt_filhos
):
    """Definição da próxima geração - Substituição geracional sem elitismo"""

    return filhos, apt_filhos


def imprimir_populacao(pop, apt, geracao: int):
    """Imprime cada população e suas aptidoes e também o melhor individuo"""
    for ind, apt_ in zip(pop, apt):
        print(f"rota: {ind}, | função objetivo: {apt_}", )
    print(
        f"Melhor solução da geracao {geracao} é {pop[apt.index(max(apt))]} e sua aptidão é {max(apt)}"
    )
    print("*****************************")


geracoes = 100
n_pop = 20
taxa_mutacao = 0.01
taxa_cruzamento = 0.9
gene = pontos_entrega
sel_func = torneio
melhor_fit = 0
ygraph = []
for geracao in range(geracoes):
    pop = gerar_pop(n_pop, gene)
    apt = aptidao(pop)
    pais = selecao_pais(pop, apt, sel_func)
    filhos = cruzamento(pais, taxa_cruzamento)
    filhos = mutacao(filhos, taxa_mutacao)
    apt_filhos = aptidao(filhos)
    pop, apt = selecao_sobreviventes(pop, apt, filhos, apt_filhos)
    imprimir_populacao(pop, apt, geracao)
    ygraph.append(max(apt))
    if max(apt) > melhor_fit:
        melhor_fit = max(apt)
        melhor_individuo = pop[apt.index(melhor_fit)]
        g = geracao


print("o melhor caminho é ", ["1"] + melhor_individuo + ["1"],
      "geracao ", g, "sua apitdão é = ", melhor_fit,
      "a distancia percorrida é ", dist_total(melhor_individuo))


x = list(range(100))
y = ygraph
plt.plot(x, y)
plt.show()
