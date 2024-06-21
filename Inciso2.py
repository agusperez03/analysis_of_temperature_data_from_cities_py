
import numpy as np
import random
import matplotlib.pyplot as plt
import pandas as pd
import HuffmanCoding
import pprint

print('\n-------------------------------------- Inciso 2 --------------------------------------\n')

#se leen los archivos csv
df1 = pd.read_csv('S1.csv',header=None,dtype=int) #Buenos Aires
df2 = pd.read_csv('S2.csv',header=None,dtype=int) #Bogota
df3 = pd.read_csv('S3.csv',header=None,dtype=int) #Vancouver

#se extraen los valores de las columnas
BuenosAires = df1[0].values
Bogota = df2[0].values
Vancouver = df3[0].values

#convertir todos los enteros de Buenos Aires, Bogota y Vancouver a strings dados por los siguientes rangos: B < 10; 10 >= M <20; A>=20
def convertir(signal):
    aux=[]
    for i in range(0, len(signal)):
        if signal[i] < 10:
            aux.append('B')
        elif signal[i] >= 10 and signal[i] < 20:
            aux.append('M')
        else:
            aux.append('A')
    return aux

BAconvertido= convertir(BuenosAires)
BOconvertido = convertir(Bogota)
VAconvertido = convertir(Vancouver)

#Crear un csv con los valores convertidos
df1 = pd.DataFrame(BAconvertido)
df2 = pd.DataFrame(BOconvertido)
df3 = pd.DataFrame(VAconvertido)

df1.to_csv('S1_convertido.csv', index=False, header=False)
df2.to_csv('S2_convertido.csv', index=False, header=False)
df3.to_csv('S3_convertido.csv', index=False, header=False)

#se calcula la probabilidad de cada rango sobre todas las señales
def probabilidad(signal):
    B=0
    M=0
    A=0
    for i in range(0, len(signal)):
        if signal[i] == 'B':
            B+=1
        elif signal[i] == 'M':
            M+=1
        else:
            A+=1
    probB = B/len(signal)
    probM = M/len(signal)
    probA = A/len(signal)
    salida = [probB, probM, probA]
    recuento = [B,M,A]
    return salida, recuento

probBA,recuentoBA = probabilidad(BAconvertido)
probBO,recuentoBO = probabilidad(BOconvertido)
probVA,recuentoVA = probabilidad(VAconvertido)

print('Las probabilidades de Buenos Aires son (B, M, A):', probBA)
print('Las probabilidades de Bogota son (B, M, A):', probBO)
print('Las probabilidades de Vancouver son (B, M, A):', probVA)

#se calculara la probabilidad con memoria de 1
def probabilidadMemoria1(signal,divisor):
    # Inicializar contadores
    bb = bm = ba = 0
    mb = mm = ma = 0
    ab = am = aa = 0
    
    # Inicializar contadores de estados anteriores
    total_b = total_m = total_a = 0
    
    # Contar transiciones
    for i in range(1, len(signal)):
        if signal[i] == 'B' and signal[i-1] == 'B':
            bb +=1
        elif signal[i] == 'B' and signal[i-1] == 'M':
            bm +=1
        elif signal[i] == 'B' and signal[i-1] == 'A':
            ba +=1
        elif signal[i] == 'M' and signal[i-1] == 'B':
            mb +=1
        elif signal[i] == 'M' and signal[i-1] == 'M':
            mm +=1
        elif signal[i] == 'M' and signal[i-1] == 'A':
            ma +=1
        elif signal[i] == 'A' and signal[i-1] == 'B':
            ab +=1
        elif signal[i] == 'A' and signal[i-1] == 'M':
            am +=1
        elif signal[i] == 'A' and signal[i-1] == 'A':
            aa +=1
    longitud= len(signal)-1
    #probXY probabilidad de x dado y
    probBB = bb/divisor[0]
    probBM = bm/divisor[0]
    probBA = ba/divisor[0]
    probMB = mb/divisor[1]
    probMM = mm/divisor[1]
    probMA = ma/divisor[1]
    if divisor[2]!=0 :
        probAB = ab/divisor[2]
    else:
        probAB = 0
    if divisor[2]!=0 :
        probAM = am/divisor[2]
    else:
        probAM = 0
    if divisor[2]!=0 :
        probAA = aa/divisor[2]
    else:
        probAA = 0
    salida = [probBB, probBM, probBA, probMB, probMM, probMA, probAB, probAM, probAA]
    
    return salida

probBAMemoria1 = probabilidadMemoria1(BAconvertido,recuentoBA)
probBOMemoria1 = probabilidadMemoria1(BOconvertido,recuentoBO)
probVAMemoria1 = probabilidadMemoria1(VAconvertido,recuentoVA)

print('\nLas probabilidades de Buenos Aires con memoria 1 son:')
pprint.pprint(probBAMemoria1)
print('\nLas probabilidades de Bogota con memoria 1 son:')
pprint.pprint(probBOMemoria1)
print('\nLas probabilidades de Vancouver con memoria 1 son:')
pprint.pprint(probVAMemoria1)

#INCISO A

#Calculo de la entropia
def entropia(prob):
    s=0
    for i in range(0, len(prob)):
        if prob[i] != 0:
            s = s + prob[i]*np.log2(prob[i])
    s = -s
    return s

#sin memoria
entropiaBA = entropia(probBA)
entropiaBO = entropia(probBO)
entropiaVA = entropia(probVA)

print('\nLa entropia de Buenos Aires es:', entropiaBA)
print('La entropia de Bogota es:', entropiaBO)
print('La entropia de Vancouver es:', entropiaVA)

#Calculo de la entropia
def entropiaConMemoria(prob):
    entropias = []
    for i in range (0, 3):
        Hcond = 0
        for probabilidad in prob[i*3:i*3+3]:
            if probabilidad > 0:
                Hcond += probabilidad * np.log2(probabilidad)
        entropias.append(-Hcond)
    return entropias

#con memoria
condicionalesBA = entropiaConMemoria(probBAMemoria1)
entropiaBAOrden2 = probBA[0]*condicionalesBA[0] + probBA[1]*condicionalesBA[1] + probBA[2]*condicionalesBA[2]
condicionalesBO = entropiaConMemoria(probBOMemoria1)
entropiaBOOrden2 = probBO[0]*condicionalesBO[0] + probBO[1]*condicionalesBO[1] + probBO[2]*condicionalesBO[2]
condicionalesVA = entropiaConMemoria(probVAMemoria1)
entropiaVAOrden2 = probVA[0]*condicionalesVA[0] + probVA[1]*condicionalesVA[1] + probVA[2]*condicionalesVA[2]

print('\nLa entropia de Buenos Aires con memoria es:', entropiaBAOrden2)
print('La entropia de Bogota con memoria es:', entropiaBOOrden2)
print('La entropia de Vancouver con memoria es:', entropiaVAOrden2)

#INCISO B

#ingreso los valores de las distribuciones de probabilidades sin memoria a un diccionario con key: 'B','M','A'
p_distBA = {    'B': probBA[0],
                'M': probBA[1],
                'A': probBA[2]  }

p_distBO = {    'B': probBO[0],
                'M': probBO[1],
                'A': probBO[2]  }

p_distVA = {    'B': probVA[0],
                'M': probVA[1],
                'A': probVA[2]  }

codeBA = HuffmanCoding.Huffman(p_distBA)
codeBO = HuffmanCoding.Huffman(p_distBO)
codeVA = HuffmanCoding.Huffman(p_distVA)

print('\nEl código de Huffman correspondiente a Buenos Aires es: ' + str(codeBA))
print('\nEl código de Huffman correspondiente a Bogota es: ' + str(codeBO))
print('\nEl código de Huffman correspondiente a Vancouver es: ' + str(codeVA))

#ingreso los valores de las distribuciones de probabilidades de orden 2 a un diccionario con key: 'BB','BM','BA','MB','MM','MA','AB','AM','AA'
p_distBAOrden2 = {    'BB': probBAMemoria1[0] * probBA[0],
                        'BM': probBAMemoria1[1] * probBA[0],
                        'BA': probBAMemoria1[2] * probBA[0],
                        'MB': probBAMemoria1[3] * probBA[1],
                        'MM': probBAMemoria1[4] * probBA[1],
                        'MA': probBAMemoria1[5] * probBA[1],
                        'AB': probBAMemoria1[6] * probBA[2],
                        'AM': probBAMemoria1[7] * probBA[2],
                        'AA': probBAMemoria1[8] * probBA[2]  }

p_distBOOrden2 = {    'BB': probBOMemoria1[0] * probBO[0],
                        'BM': probBOMemoria1[1] * probBO[0],
                        'BA': probBOMemoria1[2] * probBO[0],
                        'MB': probBOMemoria1[3] * probBO[1],
                        'MM': probBOMemoria1[4] * probBO[1],
                        'MA': probBOMemoria1[5] * probBO[1],
                        'AB': probBOMemoria1[6] * probBO[2],
                        'AM': probBOMemoria1[7] * probBO[2],
                        'AA': probBOMemoria1[8] * probBO[2] }

p_distVAOrden2 = {    'BB': probVAMemoria1[0] * probVA[0],
                        'BM': probVAMemoria1[1] * probVA[0],
                        'BA': probVAMemoria1[2] * probVA[0],
                        'MB': probVAMemoria1[3] * probVA[1],
                        'MM': probVAMemoria1[4] * probVA[1],
                        'MA': probVAMemoria1[5] * probVA[1],
                        'AB': probVAMemoria1[6] * probVA[2],
                        'AM': probVAMemoria1[7] * probVA[2],
                        'AA': probVAMemoria1[8] * probVA[2] }

codeBAOrden2 = HuffmanCoding.Huffman(p_distBAOrden2)
codeBOOrden2 = HuffmanCoding.Huffman(p_distBOOrden2)
codeVAOrden2 = HuffmanCoding.Huffman(p_distVAOrden2)

print('\nEl código de Huffman correspondiente a Buenos Aires con orden 2 es: ' + str(codeBAOrden2))
print('\nEl código de Huffman correspondiente a Bogota con orden 2 es: ' + str(codeBOOrden2))
print('\nEl código de Huffman correspondiente a Vancouver con orden 2 es: ' + str(codeVAOrden2))

def longPromedio(code,prob):
    s=0
    for i in code:
        s = s + len(code[i])*prob[i]
    return s

longPromedioBA = longPromedio(codeBA, p_distBA)
longPromedioBO = longPromedio(codeBO, p_distBO)
longPromedioVA = longPromedio(codeVA, p_distVA)

print('\nLa longitud promedio de Buenos Aires es:', longPromedioBA)
print('La longitud promedio de Bogota es:', longPromedioBO)
print('La longitud promedio de Vancouver es:', longPromedioVA)

longPromedioBAOrden2 = longPromedio(codeBAOrden2, p_distBAOrden2)
longPromedioBOOrden2 = longPromedio(codeBOOrden2, p_distBOOrden2)
longPromedioVAOrden2 = longPromedio(codeVAOrden2, p_distVAOrden2)

print('La longitud promedio de Buenos Aires de orden 2 es:', longPromedioBAOrden2)
print('La longitud promedio de Bogota de orden 2 es:', longPromedioBOOrden2)
print('La longitud promedio de Vancouver de orden 2 es:', longPromedioVAOrden2)

#Verificacion del primer teorema de Shannon para las señales de Buenos Aires, Bogota y Vancouver sin memoria
def verificar_teorema_shannon(entropia, longitud_promedio, n):
    if entropia <= longitud_promedio/n < entropia + 1/n:
        return True
    else:
        return False
    
#Verificacion del primer teorema de Shannon para las señales de Buenos Aires, Bogota y Vancouver con memoria
def verificar_teorema_shannon_memoria(entropia, entropia_cond, longitud_promedio, n):
    if entropia/n + entropia_cond/n <= longitud_promedio/n < entropia/n + entropia_cond/n + 1/n:
        return True
    else:
        return False

print('\nVerificación del primer teorema de Shannon para fuentes sin memoria:')
verificacion_BA = verificar_teorema_shannon(entropiaBA, longPromedioBA, 1)
verificacion_BO = verificar_teorema_shannon(entropiaBO, longPromedioBO, 1)
verificacion_VA = verificar_teorema_shannon(entropiaVA, longPromedioVA, 1)

print(f'Buenos Aires: {verificacion_BA}')
print(f'Bogotá: {verificacion_BO}')
print(f'Vancouver: {verificacion_VA}')

print('\nVerificación del primer teorema de Shannon para fuentes con memoria:')
verificacion_BA_mem = verificar_teorema_shannon_memoria(entropiaBA, entropiaBAOrden2, longPromedioBAOrden2, 2)
verificacion_BO_mem = verificar_teorema_shannon_memoria(entropiaBO, entropiaBOOrden2, longPromedioBOOrden2, 2)
verificacion_VA_mem = verificar_teorema_shannon_memoria(entropiaVA, entropiaVAOrden2, longPromedioVAOrden2, 2)

print(f'Buenos Aires: {verificacion_BA_mem}')
print(f'Bogotá: {verificacion_BO_mem}')
print(f'Vancouver: {verificacion_VA_mem}')



# Calculo de la longitud total en bits usando el código de Huffman
def calcular_longitud_total(codigo, señal):
    longitud_total = 0
    for simbolo in señal:
        if simbolo in codigo:
            longitud_total = longitud_total + len(codigo[simbolo])
    return longitud_total

def calcular_longitud_total_orden2(codigo, señal):
    longitud_total = 0
    i=1
    while i < len(señal):
        simbolo = señal[i-1] + señal[i]
        if simbolo in codigo:
            longitud_total += len(codigo[simbolo])
        else:
            print(f"Warning: '{simbolo}' not found in Huffman code.")
        i += 2
    return longitud_total

longitud_total_BA = calcular_longitud_total(codeBA, BAconvertido)
longitud_total_BO = calcular_longitud_total(codeBO, BOconvertido)
longitud_total_VA = calcular_longitud_total(codeVA, VAconvertido)

longitud_total_BA_orden2 = calcular_longitud_total_orden2(codeBAOrden2, BAconvertido)
longitud_total_BO_orden2 = calcular_longitud_total_orden2(codeBOOrden2, BOconvertido)
longitud_total_VA_orden2 = calcular_longitud_total_orden2(codeVAOrden2, VAconvertido)

print('\nLa longitud total en bits de Buenos Aires usando el código de Huffman es:', longitud_total_BA)
print('La longitud total en bits de Bogotá usando el código de Huffman es:', longitud_total_BO)
print('La longitud total en bits de Vancouver usando el código de Huffman es:', longitud_total_VA)

print('\nLa longitud total en bits de Buenos Aires con memoria usando el código de Huffman es:', longitud_total_BA_orden2)
print('La longitud total en bits de Bogotá con memoria usando el código de Huffman es:', longitud_total_BO_orden2)
print('La longitud total en bits de Vancouver con memoria usando el código de Huffman es:', longitud_total_VA_orden2)

