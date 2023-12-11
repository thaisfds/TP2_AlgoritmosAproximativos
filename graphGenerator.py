import tsplib95

#graph generator tsp

def loadTPSProblem(file_path):
    problem = tsplib95.load(file_path)
    graph = problem.get_graph()
    return graph

def otmalSolution(file_path, dataset):
    #procurar pelo nome do dataset no file_path e pegar a linha
    #Formato do .txt é: Dataset : Limiar
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if dataset in line:
                optimal_weight = line.split()[1]
                #retornar int
                return int(optimal_weight)
            

        