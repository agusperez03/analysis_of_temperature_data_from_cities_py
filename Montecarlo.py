#Implementacion del metodo Montecarlo para obtener el Vector Estacionario

import random
epsilon = 0.00001
min_iteraciones = 1000

def vector_estacionario(probabilidad):
    #Crea una matriz de probabilidades que contenga los valores de la lista probabilidad
    prob_acum = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    aux=0
    for i in range(3):
        for j in range(3):
            prob_acum[i][j] = probabilidad[aux]
            aux+=1
    #muestro la matriz de probabilidad
    print("Matriz de probabilidad")
    for i in range(3):
        print(prob_acum[i])
    #Ahora se calcula la probabilidad acumulada
    for i in range(1,3):
        for j in range(0, 3):
            prob_acum[i][j] += prob_acum[i-1][j]
            if prob_acum[i][j] + 0.001 > 1:
                prob_acum[i][j] = 1
    #muesstro la matriz de probabilidad acumulada
    print("Matriz de probabilidad acumulada")
    for i in range(3):
        print(prob_acum[i])

    t_actual = 0
    count = [0,0,0]
    pr_actual = [0, 0, 0]
    pr_ant = [-1, -1, -1]
    s = 1  # Estado inicial

    while not converge(pr_ant, pr_actual) or t_actual < min_iteraciones:
        t_actual += 1
        pr_ant = pr_actual.copy()
        s = getSimb(s, prob_acum)
        pr_ant = pr_actual.copy()
        count[s] += 1
        for i in range(3):
            pr_actual[i] = count[i] / t_actual

    return pr_actual

def getSimb(s_ant, prob_acum):
    r = random.random()
    for i in range(3):
        if r < prob_acum[i][s_ant]:
            return i                     # 0:Baja 1:Media 2:Alta

        
def converge(pr_ant, pr_actual):
    for i in range(3):
        if abs(pr_ant[i] - pr_actual[i]) > epsilon:
            return False
    return True