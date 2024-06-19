#en este codigo se implementara la media, el desvio y el factor de correlacion cruzada de las 3 señales pasadas por csv

#se importan las librerias necesarias
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

print('\n-------------------------------------- Inciso 1 --------------------------------------\n')

#se leen los archivos csv
df1 = pd.read_csv('S1.csv',header=None,dtype=int) #Buenos Aires
df2 = pd.read_csv('S2.csv',header=None,dtype=int) #Bogota
df3 = pd.read_csv('S3.csv',header=None,dtype=int) #Vancouver

#se extraen los valores de las columnas
BuenosAires = df1[0].values
Bogota = df2[0].values
Vancouver = df3[0].values

#se crea el algoritmo para calcular la media
def media(signal):
    s=0
    for i in range(0, len(signal)):
        s = s + signal[i]
    media = s/len(signal)
    return media

#se calcula la media de las señales
mediaBA = media(BuenosAires)
mediaBO = media(Bogota)
mediaVA = media(Vancouver)

print('La media de Buenos Aires es:', mediaBA)
print('La media de Bogota es:', mediaBO)
print('La media de Vancouver es:', mediaVA)

#se crea el algoritmo para calcular el desvio
def desvio(signal, media):
    s=0
    for i in range(0, len(signal)):
        s =s+ (signal[i] - media)**2
    desvio = np.sqrt(s/len(signal))
    return desvio

#se calcula el desvio de las señales
desvioBA = desvio(BuenosAires, mediaBA)
desvioBO = desvio(Bogota, mediaBO)
desvioVA = desvio(Vancouver, mediaVA)

print('El desvio de Buenos Aires es:', desvioBA)
print('El desvio de Bogota es:', desvioBO)
print('El desvio de Vancouver es:', desvioVA)

#se crea el algoritmo para calcular el factor de correlacion cruzada
def correlacion(signal1, signal2):
    s=0
    for i in range(0, len(signal1)):
        s = s + (signal1[i] - media(signal1))*(signal2[i] - media(signal2))
    factor = s/(len(signal1)*desvio(signal1, media(signal1))*desvio(signal2, media(signal2)))
    return factor

#se calcula el factor de correlacion cruzada de las señales
correlacionBA_BO = correlacion(BuenosAires, Bogota)
correlacionBA_VA = correlacion(BuenosAires, Vancouver)
correlacionBO_VA = correlacion(Bogota, Vancouver)

print('El factor de correlacion cruzada entre Buenos Aires y Bogota es:', correlacionBA_BO)
print('El factor de correlacion cruzada entre Buenos Aires y Vancouver es:', correlacionBA_VA)
print('El factor de correlacion cruzada entre Bogota y Vancouver es:', correlacionBO_VA)

#se grafican las señales
plt.plot(BuenosAires, label='Temperatura en Buenos Aires')
plt.plot(Bogota, label='Temperatura en Bogota')
plt.plot(Vancouver, label='Temperatura en Vancouver')
plt.legend()
plt.grid()
plt.show()

#se grafican las señales normalizadas
plt.plot((BuenosAires - mediaBA)/desvioBA, label='Temperatura en Buenos Aires')
plt.plot((Bogota - mediaBO)/desvioBO, label='Temperatura en Bogota')
plt.plot((Vancouver - mediaVA)/desvioVA, label='Temperatura en Vancouver')
plt.legend()
plt.grid()
plt.show()

#se grafican las señales normalizadas con media 0
plt.plot((BuenosAires - mediaBA), label='Temperatura en Buenos Aires')
plt.plot((Bogota - mediaBO), label='Temperatura en Bogota')
plt.plot((Vancouver - mediaVA), label='Temperatura en Vancouver')
plt.legend()
plt.grid()
plt.show()

#se grafican las señales normalizadas con desvio 1
plt.plot((BuenosAires/desvioBA), label='Temperatura en Buenos Aires')
plt.plot((Bogota/desvioBO), label='Temperatura en Bogota')
plt.plot((Vancouver/desvioVA), label='Temperatura en Vancouver')
plt.legend()
plt.grid()
plt.show()



