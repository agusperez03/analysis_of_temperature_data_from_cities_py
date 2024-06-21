import random
import matplotlib.pyplot as plt

def Sig_dado_Ant(matrizCanal, vectorEstacionario):
    symbols = ['B', 'M', 'A']
    # Genera un símbolo inicial basado en el vectorEstacionario
    initial_symbol = random.choices(symbols, vectorEstacionario)[0]
    # Obtiene la distribución de probabilidad para el próximo símbolo desde el diccionario
    probabilities = [matrizCanal[initial_symbol][symbol] for symbol in symbols]
    # Genera el siguiente símbolo basado en las probabilidades
    return random.choices(symbols, probabilities)[0]

def ProbPrimRec(j, N, matrizCanal, tolerance, vectorEstacionario):
    prob = 0
    prob_ant = -1
    repeticiones = 0
    m = 0
    probs = []
    
    def converge(prob, prob_ant, m, IT_MIN=100000): # Verifica si la probabilidad converge o si se llegó al mínimo de iteraciones
        return abs(prob - prob_ant) < tolerance and m >= IT_MIN
    
    while not converge(prob, prob_ant, m): # Mientras no haya convergencia
        nro_simb = 1
        s = Sig_dado_Ant(matrizCanal, vectorEstacionario) # Genera el primer símbolo
        
        while s != j:   # Mientras no se repita el símbolo j
            s = Sig_dado_Ant(matrizCanal, vectorEstacionario) # Genera el siguiente símbolo
            nro_simb += 1   # Cuenta la cantidad de símbolos generados
            
        if nro_simb <= N:
            repeticiones += 1   # Si se repitió el símbolo j al menos N veces, se cuenta como una repetición
            
        m += 1
        prob_ant = prob
        prob = repeticiones / m
        probs.append(prob)  # Guarda el valor de probabilidad actual para el grafico
        
    return probs, prob

def simulate_and_plot(j, N, matrizCanal, tolerancia, vectorEstacionario):
    probs, final_prob = ProbPrimRec(j, N, matrizCanal, tolerancia, vectorEstacionario)

    print(f'\nProbabilidad de que haya hasta {N} simbolos distintos entre apariciones consecutivas del simbolo {j}: {final_prob}')        
    plt.plot(probs)
    plt.xlabel('Iteration')
    plt.ylabel('Probability')
    plt.title(f'Convergence of Probability for j={j} and N={N}')
    plt.grid(True)
    plt.show()
