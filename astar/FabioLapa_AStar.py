import math
import matplotlib.pyplot as plt

def heuristic(src, end):
    # formula heuristica utilizada para calcular a distancia entre dois pontos
    # neste caso, distancia euclidiana
    return math.sqrt((src[0] - end[0])**2 + (src[1] - end[1])**2)

def graphPlot(graph, start, goal, route):
    edges = []
    #separar info
    for num in graph:
        for i in graph[num][1]:
            if (i, num) not in edges:
                edges.append((num, i))
    # plotar arestas
    for a, b in edges:
        plt.plot((graph[a][0][0], graph[b][0][0]), (graph[a][0][1], graph[b][0][1]), c = 'black')
    # plotar nos
    plt.plot([graph[num][0][0] for num in graph], [graph[num][0][1] for num in graph], 'o')
    # plotar rota, inicio e fim
    plt.plot([graph[i][0][0] for i in route], [graph[i][0][1] for i in route], ls='--', c= 'red')
    plt.plot(graph[start][0][0], graph[start][0][1], marker = 's', c = 'green', label='start')
    plt.plot(graph[goal][0][0], graph[goal][0][1], marker = "X", c = 'red', label='goal')
    plt.grid()
    plt.legend()
    plt.show()

def AStar(graph, start, goal):
    G = {} # distancia desde o no inicial para o proximo
    F = {} # distancia estimada ate o destino
    H = {} # distancia heuristica do no N ate o destino
    G[start] = 0
    F[start] = H[start] = heuristic(graph[start][0], graph[goal][0]) # F = G + H, como G = 0, entao F = H
    previous = {}
    visited = set()
    queue = set([start])
    
    while len(queue) > 0:
        thisNode = start
        thisF = float('infinity')
        for i in queue: # percorre a fila atras do menor F
            if F[i] < thisF or thisNode == start:
                thisF = F[i]
                thisNode = i

        # testa se o atual eh o destino
        if thisNode == goal:
            route = [thisNode]
            while thisNode in previous:
                thisNode = previous[thisNode] # se sim, refaz o percurso para registrar a rota e plota o grafico
                route.append(thisNode)
            route.reverse()
            print(route,"\nF: ", F[goal])
            graphPlot(graph, start, goal, route)
            return
 
        queue.remove(thisNode)
        visited.add(thisNode)
        for adj in graph[thisNode][1]: # checa os nos adjacentes
            if adj in visited: # se ja tiver passado por ele, continua
                continue
            # senao, calcula o G
            adjG = G[thisNode] + heuristic(graph[thisNode][0], graph[adj][0])
            # se adjacente nao estiver na fila, o adiciona
            if adj not in queue:
                queue.add(adj)
            # testa se o G atual eh maior que o ja salvo. Se sim, ignora
            elif adjG >= G[adj]:
                continue
            # se nao, atualiza os dados
            previous[adj] = thisNode
            G[adj] = adjG
            # calcula H se ja nao tiver sido calculado antes
            if adj not in H:
                H[adj] = heuristic(graph[adj][0], graph[goal][0])
            F[adj] = G[adj] + H[adj] # calcula e armazena F

# Grafo
# Formato: { no : [(coordenadas), (conexoes)] }
Graph_nodes = {
    'A': [(2, 1), ('B','C')],
    'B': [(2, 3), ('A', 'C', 'D')],
    'C': [(4, 3), ('A', 'B', 'E')],
    'D': [(6, 7), ('B', 'F')],
    'E': [(6, 4), ('C', 'F')],
    'F': [(9, 9), ('D', 'E')]
}
start = 'A'
goal = 'F'
# start = Graph_nodes['A'][0]
# goal = Graph_nodes['F'][0]

AStar(Graph_nodes, start, goal)