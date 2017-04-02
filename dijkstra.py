import sys
from grafo import Grafo
from heap import Heap

# def dijkstra(grafo, comeco, fim):
#     tabela = []
#     i = 0
#     anterior = comeco
#
#     # inicializa distancias
#     linha = {}
#     for w in grafo:
#         if w is grafo.getVertice(comeco):
#             linha[w.getId()] = 0
#         else:
#             linha[w.getId()] = sys.maxint
#     tabela.append(linha.copy())
#     i = i + 1
#     marcados = [min(linha, key=linha.get)]
#     naoMarcados = []
#     a = min(linha, key=linha.get)
#     anterior = a
#     for w in grafo:
#         if w not in marcados:
#             naoMarcados.append(w.getId())
#
#     # laco principal
#     # preenche tabela de distancias
#     while naoMarcados:
#         aux = {}
#         for w in naoMarcados:
#             if grafo.getVertice(w) in grafo.getVertice(anterior).getConexoes():
#                 novaDist = linha[anterior] + grafo.getVertice(anterior).getPeso(grafo.getVertice(w))
#                 linha[w] = min(novaDist, tabela[i-1][w])
#                 aux[w] = linha[w]
#         if aux != {}:
#             a = min(aux, key=aux.get)
#         else:
#             a = naoMarcados[0]
#         anterior = a
#         marcados.append(a)
#         naoMarcados.remove(a)
#         tabela.append(linha.copy())
#         i = i + 1
#
#     # backtracking para fazer o caminho mais curto
#     i = marcados.index(fim)
#     j = i
#     caminho = [fim]
#
#     while i > 0:
#         i = i - 1
#
#         if tabela[i][marcados[j]] != tabela[i+1][marcados[j]]:
#             j = i
#             caminho = [marcados[j]] + caminho
#     if caminho[0] is not comeco and caminho[-1] is not fim:
#         return []
#     return caminho

def dijkstra(grafo, comeco, fim):
    h = Heap()
    lista = []

    #inicializa valores de distancia e cria a fila de prioridade
    for v in grafo.vertDict.keys():
        if v is comeco:
            lista.append((v, 0))
        else:
            lista.append((v, sys.maxint))
    h.buildHeap(lista)
    predecessores = {h.heapList[1][0]: None}
    visitados = []
    atual = (None,0)

    #calcula as distancias e guarda de onde foi calculada a menor distancia
    while not h.isEmpty():
        atual = h.delMin()
        visitados.append(atual[0])
        vAtual = grafo.getVertice(atual[0])
        for vProximo in vAtual.getConexoes():
            if vProximo.getId() not in visitados:
                novaDist = atual[1] + vAtual.getPeso(vProximo)
                proximo = [x for j, x in enumerate(h.heapList) if x[0] == vProximo.getId()][0]
                if novaDist < proximo[1]:
                    j = h.heapList.index(proximo)
                    h.heapList[j] = (proximo[0],novaDist)
                    h.percolaAcima(j)
                    predecessores[proximo[0]] = atual[0]

    #backtracking para achar o menor caminho
    a = fim
    caminho = []

    while a:
        if a not in predecessores:
            return []
        caminho = [a] + caminho
        a = predecessores[a]
    return caminho


def kpaths(grafo, comeco, fim, k):
    g = grafo
    caminhos = []
    while k > 0:
        arestas = []
        caminho = dijkstra(g, comeco, fim)
        for i in range(0, len(caminho) - 1):
            arestas.append(g.getAresta(caminho[i], caminho[i+1]))
        if arestas:
            minAresta = min(arestas, key = lambda t: t[2])
            g.removeAresta(minAresta[0], minAresta[1])
            caminhos.append(caminho)
        else:
            minAresta = []
        k = k - 1
        if caminho == []:
            break
    return caminhos


if __name__ == '__main__':

    g = Grafo()

    g.addVertice('a')
    g.addVertice('b')
    g.addVertice('c')
    g.addVertice('d')
    g.addVertice('e')
    g.addVertice('f')

    g.addAresta('a', 'b', 7)
    g.addAresta('a', 'c', 9)
    g.addAresta('a', 'f', 14)
    g.addAresta('b', 'c', 10)
    g.addAresta('b', 'd', 15)
    g.addAresta('c', 'd', 11)
    g.addAresta('c', 'f', 2)
    g.addAresta('d', 'e', 6)
    g.addAresta('e', 'f', 9)

    print dijkstra(g, 'a', 'f')
