
def Huffman(p_dist):

    code = {key: '' for key in p_dist}          # diccionario con todos los símbolos.
    p_queue = p_distribution_list(p_dist)       # distribución de probabilidades en formato lista.
    p_queue.sort(reverse=True)                  # fila de prioridad: de mayor a menor.

    for i in range(len(p_queue)-1):              # FOR LOOP -> n-1 iteraciones:

        less_likely = p_queue.pop()                             # 1. Seleccionar los dos elementos con la menor probabilidad.
        second_less_likely = p_queue.pop()      

        for i in less_likely[1]:                                # 2. Bifurcarlos entre 0 (izquierda) y 1 (derecha).
            code[i] = '0' + code[i]                             #    Actualizar el diccionario code de todos los símbolos involucrados.
        for i in second_less_likely[1]:
            code[i] = '1' + code[i]                             
            
        p_queue.append(join(less_likely,second_less_likely))    # 3. Combinar ambos elementos sumando su probabilidad y reinsertándo el nuevo elemento en la lista.

        p_queue.sort(reverse=True)                              # 4. Reordenar la lista según las probabilidades actualizadas.

    return code                                 # retorna cada símbolo con su código correspondiente.

def join(s1, s2):                   
    sum = round(s1[0]+s2[0],3)
    symbols = s1[1] + s2[1]   
    return [ sum, symbols ]

def p_distribution_list(p_distribution_dict):
    list = []
    for i in p_distribution_dict:
        element = [p_distribution_dict[i],[i]]
        if element[0] != 0:
            list.append(element)
    if (sum(i[0] for i in list)) < 0.9999999999999998 :
        print("Valores erroneos en la distribución de probabilidades")
        list = []
    return list

def ansi_color_code(color_code):
    return f"\033[38;5;{color_code}m"
RESET = "\033[0m"
LIGHT_PINK = ansi_color_code(218)

#___________________________________________________________________________________________________________________________________________
