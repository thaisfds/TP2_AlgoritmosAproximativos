#Algorithm: Branch and Bound

import numpy as np
from heapq import heappush, heappop

class Node:
    def __init__(self, limit, edgesLimit, cost, solution):
        self.limit = limit
        self.edgesLimit = edgesLimit
        self.cost = cost
        self.solution = solution

    #Nivel do no
    def level(self):
        return len(self.solution)
    
    
    def __lt__(self, outro):
        if len(self.solution) == len(outro.solution):
            return self.limit < outro.limit
        return len(self.solution) > len(outro.solution)

#calcula o limit da raiz
def initialBound(A,n):
    
    limit = 0
    edgesLimit = np.zeros((n, 2), dtype=object)  #armazena os dois menores pesos de cada no

    for i in range(1, n + 1):  
        min1, min2 = np.inf, np.inf #inicia os pesos como infinito

        list = A[i] #não sei pq sõ funciona se jogar ele em uma vairável

        #encontra os dois menores pesos
        for j in list:
            weight = list[j]['weight']

            #se o peso for menor que o menor peso, atualiza o menor peso e o segundo menor peso
            if weight < min1:
                min1, min2 = weight, min1

            #se o peso for menor que o segundo menor peso, atualiza o segundo menor peso
            elif weight < min2:
                min2 = weight

        edgesLimit[i - 1] = [min1, min2]  #armazena os dois menores pesos de cada no

        limit += min1 + min2 #soma os dois menores pesos

    return limit / 2, edgesLimit #divide por 2 para remover repetições


#calcula outros limits
#def bound(A, n, limit, edgesLimit, solution)

def bound(A, n, limit, edgesLimit, solution):
    auxEdges = np.zeros(n, dtype=int)
    newEdges = np.array(edgesLimit)

    weight = A[solution[-2]][solution[-1]]['weight'] #peso da aresta que liga o penultimo ao ultimo no
    sum = limit * 2

    for no in solution[-2:]:
        i = no - 1 

        #atualiza o peso da aresta que liga o no ao primeiro no
        if newEdges[i][0] != weight:
            sum -= newEdges[i][auxEdges[i]]
            sum += weight
            auxEdges[i] += 1

    return sum / 2, newEdges #divide por 2 para remover repetições


#Constuido com base no pseudo-codigo do slide visto em sala de aula
def branchAndBoundTSP(A):
    n = A.number_of_nodes()
    limit, edgesLimit = initialBound(A,n) #Calcula o limite da raiz
    root = Node(limit, edgesLimit, 0, [1])
    heap = []
    heappush(heap, root)
    best = np.inf
    bestSolution = []

    while heap:
        node = heappop(heap)
        level = node.level()
        if level > n:
            if best > node.cost:
                best = node.cost
                bestSolution = node.solution
        else:
            if level < n:
                for k in range(1, n+1):
                    limitWithK, edgesWithK = bound(A, n, limit, edgesLimit, node.solution + [k])
                    if k not in node.solution and limitWithK < best:
                        newNode = Node(limitWithK, edgesWithK, node.cost + A[node.solution[-1]][k]['weight'], node.solution + [k])
                        heappush(heap, newNode)
            else:
                limitWithFirst, edgesWithFirst = bound(A, n, limit, edgesLimit, node.solution + [1])
                if limitWithFirst < best:
                    newNode = Node(limitWithFirst, edgesWithFirst, node.cost + A[node.solution[-1]][1]['weight'], node.solution + [1])
                    heappush(heap, newNode)
    return bestSolution, best

