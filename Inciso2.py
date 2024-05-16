
import numpy as np
import random
import matplotlib.pyplot as plt
import pandas as pd

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
entropiaBAMemoria1 = entropia(probBAMemoria1)
entropiaBOMemoria1 = entropia(probBOMemoria1)
entropiaVAMemoria1 = entropia(probVAMemoria1)

print('La entropia de Buenos Aires con memoria 1 es:', entropiaBAMemoria1)
print('La entropia de Bogota con memoria 1 es:', entropiaBOMemoria1)
print('La entropia de Vancouver con memoria 1 es:', entropiaVAMemoria1)


prueba=''
prueba = prueba+'A'

print(prueba)

prueba = 'B' +prueba

print(prueba)