import pandas as pd
import Montecarlo
from math import log2
from Inciso2 import BAconvertido, convertir, probBA
import Montecarlo

print('\n-------------------------------------- Inciso 3 --------------------------------------\n')

df1 = pd.read_csv('S4_buenosAiresR.csv',header=None,dtype=int) #Señal recibida

s4 = df1[0].values

t1 = BAconvertido #Señal transmitida transformada
t4 = convertir(s4) #Señal recibida transformada

def obtener_matriz_canal(T1, T4):
    # Inicializar un diccionario para contar las ocurrencias
    conteos = {
        'B': {'B': 0, 'M': 0, 'A': 0},
        'M': {'B': 0, 'M': 0, 'A': 0},
        'A': {'B': 0, 'M': 0, 'A': 0}
    }
    
    # Contar las ocurrencias de cada par (entrada, salida)
    for entrada, salida in zip(T1, T4):
        conteos[entrada][salida] += 1

    for entrada in conteos:
        total = sum(conteos[entrada].values())
        for salida in conteos[entrada]:
            conteos[entrada][salida] /= total

    return conteos

matriz_canal = obtener_matriz_canal(t1, t4)
print("Matriz de canal:")

# Función para imprimir el diccionario como matriz
def imprimir_matriz_canal(matriz_canal):
    # Obtener los símbolos de entrada y salida
    entradas = list(matriz_canal.keys())
    salidas = list(matriz_canal[entradas[0]].keys())

    # Imprimir los encabezados de las filas
    print("     " + "       ".join(entradas))

    # Imprimir cada columna
    for salida in salidas:
        fila = [f"{matriz_canal[entrada][salida]:.3f}" for entrada in entradas]
        print(f"{salida}:  " + "  ".join(fila))

imprimir_matriz_canal(matriz_canal)

# Función para calcular la probabilidad marginal
def calcular_probabilidad_marginal(signal):
    conteos = {'B': 0, 'M': 0, 'A': 0}
    for simbolo in signal:
        conteos[simbolo] += 1
    total = len(signal)
    for simbolo in conteos:
        conteos[simbolo] /= total
    return conteos

# Calcular las probabilidades marginales
prob_marginal_t1 = calcular_probabilidad_marginal(t1)
prob_marginal_t4 = calcular_probabilidad_marginal(t4)

# Función para calcular el ruido del canal
def ruido_canal(matriz_canal, prob_marginal_t1):
    H_Y_given_X = 0
    for entrada in matriz_canal:
        for salida in matriz_canal[entrada]:
            if matriz_canal[entrada][salida] > 0:
                H_Y_given_X += prob_marginal_t1[entrada] * matriz_canal[entrada][salida] * log2(1 / matriz_canal[entrada][salida])
    return H_Y_given_X

# Función para calcular la información mutua
def informacion_mutua(matriz_canal, prob_marginal_t1, prob_marginal_t4):
    I = 0
    for entrada in matriz_canal:
        for salida in matriz_canal[entrada]:
            if matriz_canal[entrada][salida] > 0:
                P_x_y = matriz_canal[entrada][salida] * prob_marginal_t1[entrada]
                I += P_x_y * log2(P_x_y / (prob_marginal_t1[entrada] * prob_marginal_t4[salida]))
    return I

# Calcular la información mutua y el ruido del canal
ruido_canal_valor = ruido_canal(matriz_canal, prob_marginal_t1)
informacion_mutua_valor = informacion_mutua(matriz_canal, prob_marginal_t1, prob_marginal_t4)


print("\nRuido del canal:", ruido_canal_valor)
print("\nInformación mutua del canal:", informacion_mutua_valor)


#realizar montecarlo para un j='A' y N=2
Montecarlo.simulate_and_plot('A', 2, matriz_canal, 1e-6, probBA)