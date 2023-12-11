import sys
import time
import csv
import numpy as np
import os
from graphGenerator import *
from christofidesTwiceAroundTheTree import *
from branchAndBound import *
from memory_profiler import memory_usage


def generateCSV(result, dataset, numberNodes, algorithm):
    #criar um unico arquivo csv com os resultados adicionando a coluna ALGORITMO apos o nome do dataset
    #se o arquivo não existir, cria um novo
    # se existir, adiciona uma nova linha
    # Dataset, ExecutionTime, MemoryUsage, Weight, Otimal Threshold, Quality, numberNodes
    #o arquivo não deve ser sobrescrito, mas sim atualizado com novos resultados


    #csv conjunto adicionando a coluna ALGORITMO apos o nome do dataset
    file_name = f'results/resultados.csv'

    #se o arquivo não existir, cria um novo
    if not os.path.isfile(file_name):
        with open(file_name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Dataset', 'Algorithm', 'ExecutionTime', 'MemoryUsage', 'Weight', 'Otimal Threshold', 'Quality', 'numberNodes'])
            writer.writerow([dataset, algorithm, result['ExecutionTime'], result['MemoryUsage'], result['Weight'], result['Otimal Threshold'], result['Quality'], numberNodes])
    else:
        #se existir, adiciona uma nova linha
        with open(file_name, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([dataset, algorithm, result['ExecutionTime'], result['MemoryUsage'], result['Weight'], result['Otimal Threshold'], result['Quality'], numberNodes])


    #arquivo csv para cada algoritmo
    file_name = f'results/resultados_{algorithm}.csv'

    #se o arquivo não existir, cria um novo
    if not os.path.isfile(file_name):
        with open(file_name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Dataset', 'Algorithm', 'ExecutionTime', 'MemoryUsage', 'Weight', 'Otimal Threshold', 'Quality', 'numberNodes'])
            writer.writerow([dataset, algorithm, result['ExecutionTime'], result['MemoryUsage'], result['Weight'], result['Otimal Threshold'], result['Quality'], numberNodes])
    else:
        #se existir, adiciona uma nova linha
        with open(file_name, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([dataset, algorithm, result['ExecutionTime'], result['MemoryUsage'], result['Weight'], result['Otimal Threshold'], result['Quality'], numberNodes])


def runAlgorithm(algorithm, graph, optimal_weight):
    start = time.time() #inicia o cronometro
    maxTime = 1800  # 30*60 = 1800 minutos

    #Formato do resultado para futuras analiseses em csv
    result = {
        'Dataset': algorithm.__name__,
        'ExecutionTime': None,
        'MemoryUsage': None,
        'Weight': None,
        'Otimal Threshold': None,
        'Quality': None
    }

    try:
        MemoryUsage = memory_usage((algorithm, (graph,))) #Pegar a memoria utilizada
        weight = algorithm(graph) #Executar o algoritmo
        end = time.time() #Finaliza o cronometro

        executionTime = end - start #Calcula o tempo de execução

        if executionTime > maxTime:
            raise TimeoutError
        
        #Calcula a qualidade da solução
        quality = weight / optimal_weight

        #Atualiza o resultado
        result.update({
            'ExecutionTime': executionTime,
            'MemoryUsage': np.max(MemoryUsage),
            'Weight': weight,
            'Otimal Threshold': optimal_weight,
            'Quality': quality
        })

        return result
    
    except TimeoutError:
        result['Weight'] = "NA" #se passar de 30 minutos, o peso é NA
        return result


def main():
    #leitura do dataset
    dataset = sys.argv[1] if (len(sys.argv) >1) else 'runAllTests'

    if dataset == 'runAllTests':
        #para cada dataset da pasta datasets executar os algoritmos

        #for dataset in os.listdir('datasets'):
        #para cada dataset em tp2_datasets.txt executar os algoritmos
        with open('others/in.txt', 'r') as file:
            datasets = file.readlines()
            datasets = [dataset.strip() for dataset in datasets]

        for dataset in datasets:        

            #print(f'{dataset}')

            #gerar grafos e pegar o peso otimo do arquivo tp2_datasets
            graph = loadTPSProblem(f'datasets/{dataset}')

            #remover .tsv do nome do arquivo
            dataset = dataset[:-4]

            optimal_weight = otmalSolution('others/threshold.txt', dataset)

            numberNodes = len(graph.nodes)

            #print(f'Executando {dataset}')

            if numberNodes <= 20:
                resultado = runAlgorithm (branchAndBound, graph, optimal_weight)
                generateCSV(resultado, dataset, numberNodes , 'bnb')

            #print('1')

            resultado = runAlgorithm (twiceAroundTheTree, graph, optimal_weight)
            generateCSV(resultado, dataset, numberNodes , 'tatt')

            #print('2')

            resultado = runAlgorithm (christofides, graph, optimal_weight)
            generateCSV(resultado, dataset, numberNodes , 'chr')

            #print('3')
            #print('______________________________')

    else:
        #executar apenas o dataset passado como parametro
        graph = loadTPSProblem(f'datasets/{dataset}.tsp')

        optimal_weight = otmalSolution('others/threshold.txt', dataset)

        numberNodes = len(graph.nodes)

        #print(f'Executando {dataset}')

        if numberNodes <= 20:
            resultado = runAlgorithm (branchAndBound, graph, optimal_weight)
            generateCSV(resultado, dataset, numberNodes , 'bnb')

        resultado = runAlgorithm (twiceAroundTheTree, graph, optimal_weight)
        generateCSV(resultado, dataset, numberNodes , 'tatt')

        resultado = runAlgorithm (christofides, graph, optimal_weight)
        generateCSV(resultado, dataset, numberNodes , 'chr')
    

if __name__ == "__main__":
    main()

