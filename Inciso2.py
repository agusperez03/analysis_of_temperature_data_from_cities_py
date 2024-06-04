
import numpy as np
import random
import matplotlib.pyplot as plt
import pandas as pd
import HuffmanCoding

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

print('La probabilidades de Buenos Aires es:', probBA)
print('La probabilidades de Bogota es:', probBO)
print('La probabilidades de Vancouver es:', probVA)

#se calculara la probabilidad con memoria de 1
def probabilidadMemoria1(signal):
    # Inicializar contadores
    bb = bm = ba = 0
    mb = mm = ma = 0
    ab = am = aa = 0
    
    # Inicializar contadores de estados anteriores
    total_b = total_m = total_a = 0
    
    # Contar transiciones
    for i in range(1, len(signal)):
        if signal[i-1] == 'B':
            total_b += 1
            if signal[i] == 'B':
                bb += 1
            elif signal[i] == 'M':
                bm += 1
            elif signal[i] == 'A':
                ba += 1
        elif signal[i-1] == 'M':
            total_m += 1
            if signal[i] == 'B':
                mb += 1
            elif signal[i] == 'M':
                mm += 1
            elif signal[i] == 'A':
                ma += 1
        elif signal[i-1] == 'A':
            total_a += 1
            if signal[i] == 'B':
                ab += 1
            elif signal[i] == 'M':
                am += 1
            elif signal[i] == 'A':
                aa += 1

    # Calcular probabilidades
    probBB = bb / total_b if total_b != 0 else 0
    probBM = bm / total_b if total_b != 0 else 0
    probBA = ba / total_b if total_b != 0 else 0
    probMB = mb / total_m if total_m != 0 else 0
    probMM = mm / total_m if total_m != 0 else 0
    probMA = ma / total_m if total_m != 0 else 0
    probAB = ab / total_a if total_a != 0 else 0
    probAM = am / total_a if total_a != 0 else 0
    probAA = aa / total_a if total_a != 0 else 0

    salida = [probBB, probBM, probBA, probMB, probMM, probMA, probAB, probAM, probAA]
    
    return salida

probBAMemoria1 = probabilidadMemoria1(BAconvertido)
probBOMemoria1 = probabilidadMemoria1(BOconvertido)
probVAMemoria1 = probabilidadMemoria1(VAconvertido)

print('La probabilidades de Buenos Aires con memoria 1 es:', probBAMemoria1)
print('La probabilidades de Bogota con memoria 1 es:', probBOMemoria1)
print('La probabilidades de Vancouver con memoria 1 es:', probVAMemoria1)

#calculo de la entropia
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

print('La entropia de Buenos Aires es:', entropiaBA)
print('La entropia de Bogota es:', entropiaBO)
print('La entropia de Vancouver es:', entropiaVA)

#con memoria
entropiaBAMemoria1 = entropia(probBAMemoria1)
entropiaBOMemoria1 = entropia(probBOMemoria1)
entropiaVAMemoria1 = entropia(probVAMemoria1)

print('La entropia de Buenos Aires con memoria 1 es:', entropiaBAMemoria1)
print('La entropia de Bogota con memoria 1 es:', entropiaBOMemoria1)
print('La entropia de Vancouver con memoria 1 es:', entropiaVAMemoria1)

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

#ingreso los valores de las distribuciones de probabilidades con memoria a un diccionario con key: 'BB','BM','BA','MB','MM','MA','AB','AM','AA'
p_distBAMemoria1 = {    'BB': probBAMemoria1[0]*probBA[0],
                        'BM': probBAMemoria1[1]*probBA[0],
                        'BA': probBAMemoria1[2]*probBA[0],
                        'MB': probBAMemoria1[3]*probBA[1],
                        'MM': probBAMemoria1[4]*probBA[1],
                        'MA': probBAMemoria1[5]*probBA[1],
                        'AB': probBAMemoria1[6]*probBA[2],
                        'AM': probBAMemoria1[7]*probBA[2],
                        'AA': probBAMemoria1[8]*probBA[2]  }

p_distBOMemoria1 = {    'BB': probBOMemoria1[0]*probBO[0],
                        'BM': probBOMemoria1[1]*probBO[0],
                        'BA': probBOMemoria1[2]*probBO[0],
                        'MB': probBOMemoria1[3]*probBO[1],
                        'MM': probBOMemoria1[4]*probBO[1],
                        'MA': probBOMemoria1[5]*probBO[1],
                        'AB': probBOMemoria1[6]*probBO[2],
                        'AM': probBOMemoria1[7]*probBO[2],
                        'AA': probBOMemoria1[8]*probBO[2]}

p_distVAMemoria1 = {    'BB': probVAMemoria1[0]*probVA[0],
                        'BM': probVAMemoria1[1]*probVA[0],
                        'BA': probVAMemoria1[2]*probVA[0],
                        'MB': probVAMemoria1[3]*probVA[1],
                        'MM': probVAMemoria1[4]*probVA[1],
                        'MA': probVAMemoria1[5]*probVA[1],
                        'AB': probVAMemoria1[6]*probVA[2],
                        'AM': probVAMemoria1[7]*probVA[2],
                        'AA': probVAMemoria1[8]*probVA[2]}

#recorrer el diccionario y mostrar por pantalla la sumatoria acumulada 
print('\nLa distribución de probabilidad de Buenos Aires con memoria 1 es: ')
suma=0
for value in p_distBAMemoria1.items():
    suma += value[1]
print(suma)

print('\nLa distribución de probabilidad de Bogota con memoria 1 es: ')
suma=0
for value in p_distBOMemoria1.items():
    suma += value[1]
print(suma)

print('\nLa distribución de probabilidad de Vancouver con memoria 1 es: ')
suma=0
for value in p_distVAMemoria1.items():
    suma += value[1]
print(suma)


codeBAMemoria1 = HuffmanCoding.Huffman(p_distBAMemoria1)
codeBOMemoria1 = HuffmanCoding.Huffman(p_distBOMemoria1)
codeVAMemoria1 = HuffmanCoding.Huffman(p_distVAMemoria1)

print('\nEl código de Huffman correspondiente a Buenos Aires con memoria 1 es: ' + str(codeBAMemoria1))
print('\nEl código de Huffman correspondiente a Bogota con memoria 1 es: ' + str(codeBOMemoria1))
print('\nEl código de Huffman correspondiente a Vancouver con memoria 1 es: ' + str(codeVAMemoria1))