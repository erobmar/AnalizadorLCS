import csv
import string
import random

def generaCadena(tamanyo):
    cadena = ""
    charset = string.ascii_uppercase
    caracter = ""
    for i in range(tamanyo):
        cadena = cadena + random.choice(charset)
    return cadena

tamanyosCadena = [8,9,10,11,12,13,14,15,16,17,20,40,50,100,200,1000,2000]

with open("dataset.csv", "w", newline="", encoding="utf-8") as archivo:
    escritura = csv.writer(archivo, delimiter=";")
    for elemento in tamanyosCadena:
        A = generaCadena(elemento)
        B = generaCadena(elemento)
        escritura.writerow([elemento,A,B])