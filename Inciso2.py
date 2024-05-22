
import numpy as np
import random
import matplotlib.pyplot as plt
import pandas as pd
import HuffmanCoding
import Montecarlo

#se leen los archivos csv
df1 = pd.read_csv('S1.csv',header=None,dtype=int) #Buenos Aires
df2 = pd.read_csv('S2.csv',header=None,dtype=int) #Bogota
df3 = pd.read_csv('S3.csv',header=None,dtype=int) #Vancouver

#se extraen los valores de las columnas
BuenosAires = df1[0].values
Bogota = df2[0].values
Vancouver = df3[0].values

#convertir todos los enteros de BuenosAires,Bogota y Vancouver a strings dados por los siguientes rangos: B < 10; 10 >= M <20; A>=20
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

print('Las probabilidades de Buenos Aires son:', probBA)
print('Las probabilidades de Bogota son:', probBO)
print('Las probabilidades de Vancouver son:', probVA)

#se calculara la probabilidad con memoria de 1
def probabilidadMemoria1(signal,divisor):
    bb=0
    bm=0
    ba=0
    mb=0
    mm=0
    ma=0
    ab=0
    am=0
    aa=0
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
    probBB = bb/divisor[0]
    probBM = bm/divisor[1]
    if divisor[2]!=0 :
        probBA = ba/divisor[2]
    else:
        probBA = 0
    probMB = mb/divisor[0]
    probMM = mm/divisor[1]
    if divisor[2]!=0 :
        probMA = ma/divisor[2]
    else:
        probMA = 0
    probAB = ab/divisor[0]
    probAM = am/divisor[1]
    if divisor[2]!=0 :
        probAA = aa/divisor[2]
    else:
        probAA = 0
    salida = [probBB, probBM, probBA, probMB, probMM, probMA, probAB, probAM, probAA]
    
    return salida

probBAMemoria1 = probabilidadMemoria1(BAconvertido,recuentoBA)
probBOMemoria1 = probabilidadMemoria1(BOconvertido,recuentoBO)
probVAMemoria1 = probabilidadMemoria1(VAconvertido,recuentoVA)

print('\nLas probabilidades de Buenos Aires con memoria 1 son:', probBAMemoria1)
print('Las probabilidades de Bogota con memoria 1 son:', probBOMemoria1)
print('Las probabilidades de Vancouver con memoria 1 son:', probVAMemoria1)

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

#con memoria
entropiaBAOrden2 = entropia(probBAMemoria1)
entropiaBOOrden2 = entropia(probBOMemoria1)
entropiaVAOrden2 = entropia(probVAMemoria1)

print('\nLa entropia de Buenos Aires con memoria es:', entropiaBAOrden2)
print('La entropia de Bogota con memoria es:', entropiaBOOrden2)
print('La entropia de Vancouver con memoria es:', entropiaVAOrden2)

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

vector_estacionario_BA = Montecarlo.vector_estacionario(probBAMemoria1)
vector_estacionario_BO = Montecarlo.vector_estacionario(probBOMemoria1)
vector_estacionario_VA = Montecarlo.vector_estacionario(probVAMemoria1)

print('\nEl vector estacionario de Buenos Aires es:', vector_estacionario_BA)
print('El vector estacionario de Bogota es:', vector_estacionario_BO)
print('El vector estacionario de Vancouver es:', vector_estacionario_VA)

#ingreso los valores de las distribuciones de probabilidades de orden 2 a un diccionario con key: 'BB','BM','BA','MB','MM','MA','AB','AM','AA'
p_distBAOrden2 = {    'BB': probBAMemoria1[0] * vector_estacionario_BA[0],
                        'BM': probBAMemoria1[1] * vector_estacionario_BA[1],
                        'BA': probBAMemoria1[2] * vector_estacionario_BA[2],
                        'MB': probBAMemoria1[3] * vector_estacionario_BA[0],
                        'MM': probBAMemoria1[4] * vector_estacionario_BA[1],
                        'MA': probBAMemoria1[5] * vector_estacionario_BA[2],
                        'AB': probBAMemoria1[6] * vector_estacionario_BA[0],
                        'AM': probBAMemoria1[7] * vector_estacionario_BA[1],
                        'AA': probBAMemoria1[8] * vector_estacionario_BA[2]  }

p_distBOOrden2 = {    'BB': probBOMemoria1[0] * vector_estacionario_BO[0],
                        'BM': probBOMemoria1[1] * vector_estacionario_BO[1],
                        'BA': probBOMemoria1[2] * vector_estacionario_BO[2],
                        'MB': probBOMemoria1[3] * vector_estacionario_BO[0],
                        'MM': probBOMemoria1[4] * vector_estacionario_BO[1],
                        'MA': probBOMemoria1[5] * vector_estacionario_BO[2],
                        'AB': probBOMemoria1[6] * vector_estacionario_BO[0],
                        'AM': probBOMemoria1[7] * vector_estacionario_BO[1],
                        'AA': probBOMemoria1[8] * vector_estacionario_BO[2] }

p_distVAOrden2 = {    'BB': probVAMemoria1[0] * vector_estacionario_VA[0],
                        'BM': probVAMemoria1[1] * vector_estacionario_VA[1],
                        'BA': probVAMemoria1[2] * vector_estacionario_VA[2],
                        'MB': probVAMemoria1[3] * vector_estacionario_VA[0],
                        'MM': probVAMemoria1[4] * vector_estacionario_VA[1],
                        'MA': probVAMemoria1[5] * vector_estacionario_VA[2],
                        'AB': probVAMemoria1[6] * vector_estacionario_VA[0],
                        'AM': probVAMemoria1[7] * vector_estacionario_VA[1],
                        'AA': probVAMemoria1[8] * vector_estacionario_VA[2] }

codeBAOrden2 = HuffmanCoding.Huffman(p_distBAOrden2)
codeBOOrden2 = HuffmanCoding.Huffman(p_distBOOrden2)
codeVAOrden2 = HuffmanCoding.Huffman(p_distVAOrden2)

print('\nEl código de Huffman correspondiente a Buenos Aires con orden 2 es: ' + str(codeBAOrden2))
print('\nEl código de Huffman correspondiente a Bogota con orden 2 es: ' + str(codeBOOrden2))
print('\nEl código de Huffman correspondiente a Vancouver con orden 2 es: ' + str(codeVAOrden2))

"""
print('\nLa distribución de probabilidad de Buenos Aires con memoria 1 es: ')
suma=0
for value in p_distBAOrden2.items():
    suma += value[1]
print(suma)

print('\nLa distribución de probabilidad de Bogota con memoria 1 es: ')
suma=0
for value in p_distBOOrden2.items():
    suma += value[1]
print(suma)

print('\nLa distribución de probabilidad de Vancouver con memoria 1 es: ')
suma=0
for value in p_distVAOrden2.items():
    suma += value[1]
print(suma)
"""

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

# Verificación del teorema de Shannon para fuentes sin memoria
print('\nVerificación del primer teorema de Shannon para fuentes sin memoria:')
verificacion_BA = verificar_teorema_shannon(entropiaBA, longPromedioBA, 1)
verificacion_BO = verificar_teorema_shannon(entropiaBO, longPromedioBO, 1)
verificacion_VA = verificar_teorema_shannon(entropiaVA, longPromedioVA, 1)

print(f'Buenos Aires: {verificacion_BA}')
print(f'Bogotá: {verificacion_BO}')
print(f'Vancouver: {verificacion_VA}')

#Verificacion del primer teorema de Shannon para las señales de Buenos Aires, Bogota y Vancouver con memoria

