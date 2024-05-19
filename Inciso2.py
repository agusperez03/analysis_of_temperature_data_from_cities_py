
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
entropiaBAOrden2 = entropia(probBAMemoria1)
entropiaBOOrden2 = entropia(probBOMemoria1)
entropiaVAOrden2 = entropia(probVAMemoria1)

print('La entropia de Buenos Aires con memoria es:', entropiaBAOrden2)
print('La entropia de Bogota con memoria es:', entropiaBOOrden2)
print('La entropia de Vancouver con memoria es:', entropiaVAOrden2)

#se calculara la probabilidad de la extension a orden 2 para realizar el b)
def probabilidadOrden2(signal):
    extension = []
    for i in range(len(signal)):
       for j in range(len(signal)):
            extension.append(signal[i] * signal[j])
    
    return extension

probBAOrden2 = probabilidadOrden2(probBA)
probBOOrden2 = probabilidadOrden2(probBO)
probVAOrden2 = probabilidadOrden2(probVA)

print('La probabilidades de Buenos Aires extendido a orden 2 es:', probBAOrden2)
print('La probabilidades de Bogota extendido a orden 2 es:', probBOOrden2)
print('La probabilidades de Vancouver extendido a orden 2 es:', probVAOrden2)

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
p_distBAOrden2 = {    'BB': probBAOrden2[0],
                        'BM': probBAOrden2[1],
                        'BA': probBAOrden2[2],
                        'MB': probBAOrden2[3],
                        'MM': probBAOrden2[4],
                        'MA': probBAOrden2[5],
                        'AB': probBAOrden2[6],
                        'AM': probBAOrden2[7],
                        'AA': probBAOrden2[8]  }

p_distBOOrden2 = {    'BB': probBOOrden2[0],
                        'BM': probBOOrden2[1],
                        'BA': probBOOrden2[2],
                        'MB': probBOOrden2[3],
                        'MM': probBOOrden2[4],
                        'MA': probBOOrden2[5],
                        'AB': probBOOrden2[6],
                        'AM': probBOOrden2[7],
                        'AA': probBOOrden2[8]  }

p_distVAOrden2 = {    'BB': probVAOrden2[0],
                        'BM': probVAOrden2[1],
                        'BA': probVAOrden2[2],
                        'MB': probVAOrden2[3],
                        'MM': probVAOrden2[4],
                        'MA': probVAOrden2[5],
                        'AB': probVAOrden2[6],
                        'AM': probVAOrden2[7],
                        'AA': probVAOrden2[8]  }

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

print('La longitud promedio de Buenos Aires es:', longPromedioBA)
print('La longitud promedio de Bogota es:', longPromedioBO)
print('La longitud promedio de Vancouver es:', longPromedioVA)

longPromedioBAOrden2 = longPromedio(codeBAOrden2, p_distBAOrden2)
longPromedioBOOrden2 = longPromedio(codeBOOrden2, p_distBOOrden2)
longPromedioVAOrden2 = longPromedio(codeVAOrden2, p_distVAOrden2)

print('La longitud promedio de Buenos Aires de orden 2 es:', longPromedioBAOrden2)
print('La longitud promedio de Bogota de orden 2 es:', longPromedioBOOrden2)
print('La longitud promedio de Vancouver de orden 2 es:', longPromedioVAOrden2)

#Verificacion del primer teorema de Shannon para las señales de Buenos Aires, Bogota y Vancouver sin memoria

#Verificacion del primer teorema de Shannon para las señales de Buenos Aires, Bogota y Vancouver con memoria