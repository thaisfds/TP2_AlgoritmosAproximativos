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

#calcula outros limits

def bound(A, n, limit, edgesLimit, solution, type):

    if type == 1: 
        sum = 2 * limit
        edgesLimit = np.array(edgesLimit)
        auxEdges = np.zeros(n, dtype=int)
        for no in solution[-2:]:
            i = no-1 
            #atualiza o peso da aresta que liga o no ao primeiro no
            if edgesLimit[i][0] != A[solution[-2]][solution[-1]]['weight']:
                sum = sum - edgesLimit[i][auxEdges[i]]
                sum = sum + A[solution[-2]][solution[-1]]['weight']
                auxEdges[i] = auxEdges[i] + 1
    
    else:

        newSize = n+1
        edgesLimit = np.zeros((n, 2), dtype=object)  #armazena os dois menores pesos de cada no
        sum = 0

        for i in range(1, newSize):  
            edges1, edges2 = np.inf, np.inf #inicia os pesos como infinito
            #encontra os dois menores pesos
            for j in A[i]:
                #se o peso for menor que o menor peso, atualiza o menor peso e o segundo menor peso
                if A[i][j]['weight'] < edges1:
                    edges1, edges2 = A[i][j]['weight'], edges1
                #se o peso for menor que o segundo menor peso, atualiza o segundo menor peso
                elif A[i][j]['weight'] < edges2:
                    edges2 = A[i][j]['weight']
            
            sum = sum + edges1 + edges2 #soma os dois menores pesos
            edgesLimit[i-1] = [edges1, edges2]  #armazena os dois menores pesos de cada no
            
            
        
    return limit / 2, edgesLimit #divide por 2 para remover repetições


#Constuido com base no pseudo-codigo do slide visto em sala de aula
def branchAndBound(A):
    n = A.number_of_nodes()
    limit, edgesLimit = bound(A,n,0,0,0,0) #Calcula o limite da raiz
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
                    limitWithK, edgesWithK = bound(A, n, limit, edgesLimit, node.solution + [k],1)
                    if k not in node.solution and limitWithK < best:
                        newNode = Node(limitWithK, edgesWithK, node.cost + A[node.solution[-1]][k]['weight'], node.solution + [k])
                        heappush(heap, newNode)
            else:
                limitWithFirst, edgesWithFirst = bound(A, n, limit, edgesLimit, node.solution + [1],1)
                if limitWithFirst < best:
                    newNode = Node(limitWithFirst, edgesWithFirst, node.cost + A[node.solution[-1]][1]['weight'], node.solution + [1])
                    heappush(heap, newNode)
    return bestSolution, best

