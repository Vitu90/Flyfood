"""Brute"""
import matplotlib.pyplot as plt

# Ler arquivo de entrada e montar a matriz
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

# Montando a matriz, obtendo os vetores de interesse: posicao, pontos de entrega...
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


def idx(ponto: str) -> int:  # transforma um string em um indicie para obter a posicao
    indicie = pontos_entrega.index(ponto)
    return indicie


def calc_dist(a: str, b: str) -> int:  # calculo da distancia entre dois pontos
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


# calcula a distancia entre os pontos de um percurso sem incluir o restaurante
def dist_rota(rota) -> int:
    dist_percurso = 0
    for i in range(len(rota)-1):
        dist = calc_dist(rota[i], rota[i+1])
        dist_percurso = dist_percurso + dist

    return dist_percurso


def Permutacao(lista):  # faz todas as permutações de uma lista
    if len(lista) == 0:
        return []
    elif len(lista) == 1:
        return [lista]
    else:
        lista_aux = []
        for i in range(len(lista)):
            chave = lista[i]
            elementos_restantes = lista[:i] + lista[i+1:]
            for p in Permutacao(elementos_restantes):
                lista_aux.append([chave] + p)
        return lista_aux


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


"""Algoritmo"""
distancias = []
dist_min = 999999999999999999999999999999999
melhor_rota = []
perms = Permutacao(pontos_entrega)
for i, p in enumerate(perms):
    aux = dist_rota(p)
    aux2 = dist_r(p)
    aux3 = aux + aux2
    distancias.append(aux3)
    if aux3 < dist_min:
        dist_min = aux3
        melhor_rota = ["R"] + p + ["R"]
    print("permutacao ", i, "->", p, '\n')

print("=======================================================")

print("O melhor caminho encontrado foi ", melhor_rota,
      "e a distância percorrida foi de ", dist_min, "unidades")

x_graph = [xr]
y_graph = [yr]


def idx(ponto: str) -> int:
    indicie = pontos_entrega.index(ponto)
    return indicie


for i in range(1, len(melhor_rota)-1):
    indicie = idx(melhor_rota[i])
    x_graph.append(posicao[indicie][0])
    y_graph.append(posicao[indicie][1])

x_graph.append(xr)
y_graph.append(yr)
x = x_graph
y = y_graph

plt.plot(x, y)
plt.show()
