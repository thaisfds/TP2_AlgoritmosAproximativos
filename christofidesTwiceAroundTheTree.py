import networkx as nx

#christofides uzando nx

def christofides(A):
    #Arvore geradora minima
    T = nx.minimum_spanning_tree(A)
    
    #Conjunto de nos de grau impar
    odd_degree_nodes = [node for node, degree in nx.degree(T) if degree % 2 == 1]
    
    #Maching perfeito de peso minimo
    M = nx.subgraph(A, odd_degree_nodes)
    M = nx.min_weight_matching(M)

    #Multigrafo formado com os vertices de v e arestas de M e T
    MT = nx.MultiGraph(T)
    MT.add_edges_from((u, v, A[u][v]) for u, v in M)

    #Circuito euleriano
    #Eliminar vertices duplicados, substituindo u-w-v por u-v

    eulerian_circuit = [edge[0] for edge in nx.eulerian_circuit(MT, 1)]
    aux = dict.fromkeys(eulerian_circuit)
    circuit = list(aux) + [eulerian_circuit[0]]


    #Calcular a soma dos pesos

    weight = 0
    size = len(circuit) -1

    for i in range(size):
        weight += A[circuit[i]][circuit[i + 1]]['weight']

    return weight

#twice-around-the-tree

def twiceAroundTheTree(A):
    #Arvore geradora minima
    T = nx.minimum_spanning_tree(A)

    #Duplicar arestas = percorrer usando DFS
    DFS = nx.dfs_preorder_nodes(T, 1)
    M = list(DFS)
    M.append(M[0]) #adiciona o inicio ao final

    #Calcular a soma dos pesos

    weight = 0
    size = len(M) -1

    for i in range(size):
        weight += A[M[i]][M[i + 1]]['weight']

    return weight