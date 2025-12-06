import random
import string
import time
import tracemalloc
import csv

# -------------------------------------------------------------
#                Analizador de algoritmos LCS
# -------------------------------------------------------------
# Este programa implementa tres algoritmos para calcular la
# Subsecuencia Común más Larga (LCS) de dos secuencias:
#   1 - LCSRecursivo: Recursividad directa sin memorización
#   2 - LCSDivide: Divide y vencerás de Hirschberg
#   3 - LCSDinamico: Programación diámica tabular
#
# Al inicio, carga el dataset de prueba contenido en el archivo
# 'dataset.csv' que debe estar en el mismo directorio que este
# código fuente.
# Después, permite ejecutar las pruebas sobre ese dataset para
# después observar los resultados en pantalla y/o exportarlos a
# un archivo 'resultados.csv' para su posterior análisis
# -------------------------------------------------------------


# -------------------------------------------------------------
# Función LCSRecursivo
# -------------------------------------------------------------
# Compara la última letra de cada cadena y se llama recursivamente 
# hacia atrás eliminando caracteres
# 
# param A,B - Cada una de las cadenas a comparar
# param i - Longitud de la cadena A
# param j - Longitud de la cadena B
# 
# return subcadena1 / subcadena2 / <str vacío>
# -------------------------------------------------------------
def LCSRecursivo(A, B, i, j):
    
    # Si la longitud de cualquiera de las cadenas es 0, devuelve una cadena vacía
    if (i==0 or j==0):
        return ""        

    # Si las últimas letras coinciden, están en la LCS -> se devuelve y se llama a sí mismo de
    # manera recursiva con el carácter anterior de cada cadena.
    if(A[i-1] == B[j-1]):
        return LCSRecursivo(A,B,i-1,j-1) + A[i-1]
    else:

        # En caso contrario se prueba dos veces: retrocediendo un carácter en A y retrociendo en B
        subcadena1 = LCSRecursivo(A,B,i-1,j)
        subcadena2 = LCSRecursivo(A,B,i,j-1)

        # Y nos quedamos con la mejor
        if(len(subcadena1) >= len(subcadena2)):
            return subcadena1
        else:
            return subcadena2

# -------------------------------------------------------------
# Función LCSDivide
# -------------------------------------------------------------
# Implementa el algoritmo de Hirschberg:
#   - Divide A en dos mitades A1 y A2
#   - Calcula, para todos los prefijos de B, la longitud de su 
#     LCS con A1 (divideAdelante)
#   - Calcula, para todos los sufijos de B, la longitud de su 
#     LCS con A2 (divideAtras)
#   - Calcula k que maximiza LCS(A1, B[0..k]) + LCS(A2, B[k..m])
#   - Parte B por el punto k y se llama recursivamente sobre 
#     (A1, B1) y (A2, B2)
#
# param A,B - Cada una de las cadenas a comparar
# param i - Longitud de la cadena A
# param j - Longitud de la cadena B
# 
# return resultado1 + resutlado2 - La LCS
# -------------------------------------------------------------
def LCSDivide(A,B,n,m):

    # Caso 1 - Alguna de las cadenas está vacía
    if(n == 0 or m == 0):
        return ""
    
    # Caso 2 - A tiene longitud 1
    # Si el único carácter de A está en B, LCS = A
    # Si no, LCS = ""    
    if(n == 1):
        caracter = A[0]
        for i in B:
            if (i == caracter):
                return caracter
        return ""
    
    # Caso 3 - B tiene longitud 1
    # Caso análogo al caso 2 cambiando A por B
    if(m == 1):
        caracter = B[0]
        for i in A:
            if (i == caracter):
                return caracter
        return ""
    
    # Resto de casos partimos A en dos mitades
    medio = n // 2

    A1 = A[0:medio]
    A2 = A[medio:n]

    # Calculamos los vectores de longitud de LCS hacia adelante y hacia atrás
    arrayAdelante = divideAdelante(A1, B, len(A1), len(B))
    arrayAtras = divideAtras(A2, B, len(A2), len(B))

    
    # Inicializamos los posibles mejor k y valor a 0 y menos infinito
    # Gracias al tipado dinámico, mejorValor se volverá entero tras la primera iteración
    mejorK = 0
    mejorValor = float("-inf")

    # Buscamos el índice k que maximice la suma de las longitudes
    for j in range(0,m+1):
        if((arrayAdelante[j] + arrayAtras[j]) > mejorValor):
            mejorValor = (arrayAdelante[j] + arrayAtras[j])
            mejorK = j

    # Partimos B por el punto k
    B1 = B[0:mejorK]
    B2 = B[mejorK:]

    # Y llamamos de forma recursiva sobre los dos subproblemas
    resultado1 = LCSDivide(A1, B1, len(A1), len(B1))
    resultado2 = LCSDivide(A2, B2, len(A2), len(B2))
    
    return resultado1 + resultado2


# -------------------------------------------------------------
# Funciones auxiliares para Hirschberg (divide y vencerás)
# -------------------------------------------------------------
# divideAdelante: calcula las longitudes de LCS(A1, B[0..j])
# para todos los j y devuelve un vector de tamaño m+1.
# -------------------------------------------------------------
def divideAdelante(A1, B, n, m):

    previo = 0
    temporal = 0

    # Creamos un array auxiliar de tamaño m+1
    arrayAux = [0] * (m+1)

    # Programación dinámica -> recorremos A1 y B
    for i in range(1, n+1):
        previo = 0
        for j in range(1, m+1):
            temporal = arrayAux[j]
            if (A1[i-1] == B[j-1]):
                arrayAux[j] = previo + 1
            else:
                arrayAux[j] = max(arrayAux[j], arrayAux[j-1])
            previo = temporal    
    return arrayAux

# -------------------------------------------------------------
# divideAtras: Análogo a divideAdelante pero trabajando con 
# cadenas invertidas.
# -------------------------------------------------------------
def divideAtras(A2, B, n, m):

    previo = 0
    temporal = 0

    # Invertimos los dos arrays
    A2Reverso = A2[::-1]
    BReverso = B[::-1]

    # Creamos un array auxiliar de tamaño m+1
    arrayAux = [0] * (m+1)

    for i in range(1, n+1):
        previo = 0
        for j in range(1, m+1):
            temporal = arrayAux[j]
            if(A2Reverso[i-1] == BReverso[j-1]):
                arrayAux[j] = previo + 1
            else:
                arrayAux[j] = max(arrayAux[j], arrayAux[j-1])
            previo = temporal

    # Creamos el array resultado que se devolverá invirtiendo arrayAux
    resultado = [0] * (m+1)

    for k in range(0,m+1):
        resultado[k] = arrayAux[m-k]
    
    return resultado

# -------------------------------------------------------------
# Función LCSDinamico
# -------------------------------------------------------------
# Crea una matriz (n+1) x (m+1) para almacenar la longitud de 
# la LCS acumulada. 
# Reconstruye la LCS recorriendo la matriz desde la esquina 
# inferior derecha hacia atrás.
#
# param A,B - Cada una de las cadenas a comparar
# param i - Longitud de la cadena A
# param j - Longitud de la cadena B
# 
# return resultado - La LCS
# -------------------------------------------------------------
def LCSDinamico(A,B,n,m):

    # Creamos la matriz e inicializamos a 0
    matriz = [[0 for fila in range(n+1)] for columna in range(m+1)]

    # Recorremos la matriz rellenando con la longitud de LCS acumulada
    # en cada casilla
    for i in range(1,n+1):
        for j in range(1,m+1):
            if(A[i-1] == B[j-1]):
                matriz[i][j] = matriz[i-1][j-1] + 1
            else:
                matriz[i][j] = max(matriz[i-1][j], matriz[i][j-1])

    # Calculamos la subsecuencia resultado comenzando en el inferior derecha
    resultado = ""
    i = n
    j = m

    while (i > 0) and (j > 0):
        
        # Si son iguales, nos movemos en diagonal
        if(A[i-1] == B[j-1]):
            resultado = A[i-1] + resultado
            i -= 1
            j -= 1
        
        # Si no, nos movemos en la dirección de mayor valor
        elif matriz[i-1][j] >= matriz[i][j-1]:
            i -= 1
        else:
            j -= 1

    return resultado

# -------------------------------------------------------------
# Función mostrarResultados
# -------------------------------------------------------------
# Recorre la matriz de resultados la muestra en pantalla con el
# formato correcto
#
# param tablaResultados - Matriz que contiene los resultados de 
#                         las pruebas
# -------------------------------------------------------------
def mostrarResultados(tablaResultados):
    
    print("Resultados: ")
    print("------------------------------------------------------------------------------------------")
    print(" Tamaño Array \t |\tAlgoritmo     \t|       Tiempo CPU       \t| \t Memoria")
    print("------------------------------------------------------------------------------------------")
    for i in range(len(tablaResultados)):
        print("\t" + str(tablaResultados[i][0]) + "\t\t" + 
              tablaResultados[i][1] + "\t\t" + 
              str(tablaResultados[i][2]) + "\t\t" +
              str(tablaResultados[i][3]))
    return

# -------------------------------------------------------------
# Función cargarDataset
# -------------------------------------------------------------
# Abre el dataset almacenado en 'dataset.csv' y copia sus datos
# en un array
#
# return dataset - Array con los datos del archivo
# -------------------------------------------------------------
def cargarDataset():

    dataset = []
    with open("dataset.csv", newline="", encoding="utf-8") as archivo:
        lectura = csv.reader(archivo, delimiter=";")
        for fila in lectura:
            dataset.append(fila)
    return dataset

# -------------------------------------------------------------
# Función mostrarMenu
# -------------------------------------------------------------
# Muestra el menú de usuario por pantalla
# -------------------------------------------------------------
def mostrarMenu():
    print("----------------------------------------------------------")
    print("|         Analizador de Algoritmos LCS v1.0              |")
    print("|                                                        |")
    print("|          Autor: Eduardo Robledo Martínez               |")
    print("----------------------------------------------------------")
    print("\n1) Ejecutar pruebas")
    print("2) Mostrar resultados por pantalla")
    print("3) Exportar resultados a un archivo CSV")
    print("4) Salir")
   
    return

# -------------------------------------------------------------
# Función exportarCSV
# -------------------------------------------------------------
# Crea el archivo 'resultados.csv' y copia el contenido de la
# matriz de resultados en el mismo, debidamente formateado.
#
# param tablaResultados - Matriz que contiene los resultados de 
#                         las pruebas
# -------------------------------------------------------------
def exportarCSV(tablaResultados):
    cabeceras = ["Tamaño", "Método", "Tiempo CPU en µs", "Memoria en KB", "lcs"]
    with open("resultados.csv", "w", newline="", encoding="utf-8") as archivoSalida:
        escritura = csv.writer(archivoSalida, delimiter=";")
        escritura.writerow(cabeceras)
        for linea in tablaResultados:
            escritura.writerow([
                linea[0],
                linea[1],
                str(linea[2]).replace(".",","),
                str(linea[3]).replace(".",","),
                linea[4]
            ])
    return

# -------------------------------------------------------------
# Función ejecutarPruebas
# -------------------------------------------------------------
# Ejecuta las pruebas sobre el dataset y almacena los resultados
# de las mismas en la matriz de resultados.
#
# param dataset - Dataset sobre el que realizar las pruebas
# param tablaResultados - Matriz que contiene los resultados de 
#                         las pruebas
# -------------------------------------------------------------
def ejecutarPruebas(dataset, tablaResultados):
    contador = 0
    
    # Recorremos el dataset y, por cada línea, tomamos:
    #  n - Tamaño de las secuencias a probar
    #  A - Primera secuencia
    #  B - Segunda secuencia
    for j in dataset:
        n = int(j[0])
        A = str(j[1])
        B = str(j[2])

        # Por cada iteración se tomarán los valores de uso de memoria y tiempo justo antes y 
        # justo después de la función objetivo. Con esto eliminamos al máximo la contaminación
        # de los datos de prueba.
        for i in range(0,3):
            contador += 1   
            match i:
                case 0:

                # Ajustar este valor para establecer hasta dónde ejecutar recursividad
                # Para recoger datos el valor recomendado es 17, para pruebas bajar a 12 o 13
                    if(n <= 17):
                        tracemalloc.start()
                        tiempoInicial = time.perf_counter()
                        resultado = LCSRecursivo(A,B,len(A),len(B))
                        tiempoFinal = time.perf_counter()
                        actual, maximo = tracemalloc.get_traced_memory()
                    else:
                        resultado = "saltando..."
                        maximo = 0
                        tiempoInicial = 0
                        tiempoFinal = 0
                case 1:
                    tracemalloc.start()
                    tiempoInicial = time.perf_counter()
                    resultado = LCSDivide(A,B,len(A),len(B))
                    tiempoFinal = time.perf_counter()
                    actual, maximo = tracemalloc.get_traced_memory()
                case 2:
                    tracemalloc.start()
                    tiempoInicial = time.perf_counter()
                    resultado = LCSDinamico(A,B,len(A),len(B))
                    tiempoFinal = time.perf_counter()
                    actual, maximo = tracemalloc.get_traced_memory()
                    tracemalloc.stop()
            
            print(f"\rEjecutando prueba " + str(contador) + "/" + str(len(dataset)*3), end="")

            # Almacenamos cada valor en su lugar de la tabla de 
            # resultados, conviritiendo el tiempo en microsegundos 
            # y la memoria en Kilobytes por simple legibilidad
            tablaResultados[contador -1][0] = str(n)
            tablaResultados[contador -1][1] = nombresMetodos[i]
            tablaResultados[contador -1][2] = ((tiempoFinal - tiempoInicial)*1000000)
            tablaResultados[contador -1][3] = (maximo/(1024)) 
            tablaResultados[contador -1][4] = resultado
    return

# -------------------------------------------------------------
# Programa principal
# -------------------------------------------------------------
nombresMetodos = ["Recursividad", "Divide y V.", "Dinámico tab"]
pruebasEjecutadas = False
resultado = ""
seleccion = ""

# Creamos la tabla de resultados para cada uno de las 51 pruebas a realizar
# con 5 campos para los datos que vamos a almacenar y la inicializamos a 0
tablaResultados = [[0 for filas in range(5)] for columnas in range(51)]
dataset = cargarDataset()

while(True):
    mostrarMenu()
    seleccion = input()    
    match (seleccion):
        case "1":
            print("Ejecutando pruebas... (paciencia, puede tardar unos minutos)")
            ejecutarPruebas(dataset, tablaResultados)
            print("\nPuebas ejecutadas")
            pruebasEjecutadas = True
        case "2":
            if(pruebasEjecutadas):
                mostrarResultados(tablaResultados)
                print("Pulse ENTER para continuar...")
                seleccion = input()
            else:
                print("No hay datos que mostrar, debe ejecutar las pruebas primero")
        case "3":
            if(pruebasEjecutadas):
                exportarCSV(tablaResultados)
                print("Datos exportados en el archivo resultados.csv")
            else:
                print("No hay datos que exportar, debe ejecutar las pruebas primero")
        case "4":
            exit()
        case _:
            print("Opción no válida")