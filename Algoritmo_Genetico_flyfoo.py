"""Rascunho2"""
from random import *
from typing import Callable, List, Tuple

import matplotlib.pyplot as plt
import numpy as np

# Ler Matriz de entrada
arq = open("teste.txt", 'r')
linha1 = arq.readline().split()
linhas = int(linha1[0])
colunas = int(linha1[1])
a = []  # lista vazia
pontos_entrega = []
posicao = []
start = []

while len(a) <= linhas-1:
    linha = arq.readline().split()
    a.append(linha)

for i in range(linhas):
    for j in range(colunas):
        if a[i][j] != "0":
            pontos_entrega.append(a[i][j])
            posicao.append((i, j))
            if a[i][j] == "R":
                start.append((i, j))
                xr = i
                yr = j
                pontos_entrega.remove("R")
                posicao.remove((i, j))


def cruzamento_pais(pai1: str, pai2: str, taxa_cruzamento: float) -> Tuple[str, str]:
    """cruzamento de dois individuos"""
    if random() <= taxa_cruzamento:
        ponto_cruzamento = randint(2, len(pai1) - 1)
        filho_aux_1: str = pai1[:ponto_cruzamento]
        offspring_1 = pai2[ponto_cruzamento:]

        filho_aux_2: str = pai2[:ponto_cruzamento]
        offspring_2 = pai1[ponto_cruzamento:]

        filho_1 = filho_aux_1 + (PMX(filho_aux_1, filho_aux_2, offspring_2))
        filho_2 = filho_aux_2 + (PMX(filho_aux_2, filho_aux_1, offspring_1))

        return filho_1, filho_2
    return pai1, pai2


def cruzamento(pais: List[str], taxa_cruzamento: float) -> List[str]:
    """cruzamento de todos os pais"""
    lista_filhos: List[str] = [None] * len(pais)
    for i in range(0, len(pais)-1, 2):
        filho1, filho2 = cruzamento_pais(pais[i], pais[i + 1], taxa_cruzamento)
        lista_filhos[i] = filho1
        lista_filhos[i + 1] = filho2
    return lista_filhos


def busca(lista, alvo):
    tamanho_da_lista = len(lista)
    for atual in range(0, tamanho_da_lista):
        if (lista[atual] == alvo):
            return atual

    return -1


def PMX(filho_aux_1: str, filho_aux_2: str, offspring: str) -> str:
    for i in range(len(offspring)):
        resultado = busca(filho_aux_1, offspring[i])
        if resultado != -1:
            offspring[i] = filho_aux_2[resultado]
    return offspring


def mutacao_individuo(filho: str, taxa_mutacao: float) -> str:
    """mutação de um individuo"""
    filho_mutado = filho
    for i, s in enumerate(filho):
        # pra cada gene
        if random() <= taxa_mutacao:
            found = False
            while found == False:
                posicao_aleatoria = randint(0, len(filho)-1)
                if posicao_aleatoria != i:
                    found = True
            filho_mutado[i], filho_mutado[posicao_aleatoria] = filho_mutado[posicao_aleatoria], filho_mutado[i]

    return filho_mutado


def mutacao(filhos: List[str], taxa_mutacao: float) -> List[str]:
    """Mutação de todos os filhos"""
    for i, ind in enumerate(filhos):
        filhos[i] = mutacao_individuo(ind, taxa_mutacao)
    return filhos


def roleta(apt: List[float]) -> int:
    """Seleção por roleta"""
    soma_roleta: float = sum(apt)
    n_sorteado: float = random() * soma_roleta
    soma_atual: float = 0
    for i, apt in enumerate(apt):
        soma_atual += apt
        if soma_atual >= n_sorteado:
            return i


def selecao_pais(pop: List[str], apt: List[float], sel_func: Callable) -> List[str]:
    """Seleção dos pais"""
    lista_pais: List[str] = [None] * len(pop)
    for i in range(len(pop)):
        idx_selecionado = sel_func(apt)
        lista_pais[i] = pop[idx_selecionado]
    return lista_pais


def populacao_inicial(n_pop: int, gene: list[str]) -> list[str]:
    pop: list[str] = [""] * n_pop
    for i in range(n_pop):
        individuo = sample(gene, len(gene))
        pop[i] = individuo
    return pop


def selecao_sobreviventes(
    pop: List[str], apt_pop: List[float], filhos: List[str], apt_filhos: List[float]
):
    """Definição da próxima geração - Substituição geracional sem elitismo"""

    return filhos, apt_filhos


def idx(ponto: str) -> int:
    indicie = pontos_entrega.index(ponto)
    return indicie


def calc_dist(a: str, b: str) -> int:
    indicie_a = idx(a)
    indicie_b = idx(b)
    xa = posicao[indicie_a][0]
    xb = posicao[indicie_b][0]
    ya = posicao[indicie_a][1]
    yb = posicao[indicie_b][1]
    if xa > xb:
        parcela_1 = xa - xb
    else:
        parcela_1 = xb - xa
    if ya > yb:
        parcela_2 = ya - yb
    else:
        parcela_2 = yb - ya

    dist = parcela_1 + parcela_2
    return dist


def dist_r(rota):  # calcula a distancia até o restaurante
    inicio = rota[0]
    fim = rota[-1]
    indicie_inicio = idx(inicio)
    indicie_fim = idx(fim)
    x_inicio = posicao[indicie_inicio][0]
    y_inicio = posicao[indicie_inicio][1]
    x_fim = posicao[indicie_fim][0]
    y_fim = posicao[indicie_fim][1]
    if xr > x_inicio:
        parcela_1 = xr - x_inicio
    else:
        parcela_1 = x_inicio - xr
    if yr > y_inicio:
        parcela_2 = yr - y_inicio
    else:
        parcela_2 = y_inicio - yr
    if xr > x_fim:
        parcela_3 = xr - x_fim
    else:
        parcela_3 = x_fim - xr
    if yr > y_fim:
        parcela_4 = yr - y_fim
    else:
        parcela_4 = y_fim - yr

    distancia_r = parcela_1 + parcela_2 + parcela_3 + parcela_4
    return distancia_r


def dist_rota(rota) -> int:
    dist_percurso = 0
    for i in range(len(rota)-1):
        dist = calc_dist(rota[i], rota[i+1])
        dist_percurso = dist_percurso + dist

    return dist_percurso


def dist_total(rota):
    aux = dist_rota(rota)
    aux2 = dist_r(rota)
    resultado = aux + aux2
    return resultado


def torneio(apt: List[float]) -> int:
    """Seleção por torneio"""
    pai1 = randint(0, len(apt) - 1)
    pai2 = randint(0, len(apt) - 1)
    return pai1 if apt[pai1] > apt[pai2] else pai2


def aptidao_individuo(cromossomo: str) -> float:
    """cálculo da aptidão de um único indivíduo"""
    apt = 1/dist_total(cromossomo)
    return apt


def aptidao(pop: list[str]) -> list[float]:
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


def imprimir_populacao(pop: List[str], apt: List[float], geracao: int) -> None:
    """Imprime cada população e suas aptidoes e também o melhor individuo"""
    for ind, apt_ in zip(pop, apt):
        print(f"rota: {ind}, | função objetivo: {apt_}")
    print(
        f"Melhor solução da geracao {geracao} é {pop[apt.index(max(apt))]} e sua aptidão é {max(apt)}"
    )
    print("*****************************")


geracoes = 10
n_pop = 4
taxa_mutacao = 0.01
taxa_cruzamento = 0.9
gene = pontos_entrega
sel_func = torneio
melhor_fit = 0
ygraph = []
for geracao in range(geracoes):
    pop = populacao_inicial(n_pop, gene)
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


print("o melhor caminho é ", ["R"] + melhor_individuo + ["R"],
      "geracao ", g, "sua apitdão é = ", melhor_fit,
      "a distancia percorrida é ", dist_total(melhor_individuo))


y = ygraph
plt.plot(y)
plt.show()
