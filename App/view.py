"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """


import sys
import config
from App import controller
from App import model
from DISClib.ADT import stack
import timeit
assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""
recursionLimit = 20000
sys.setrecursionlimit(recursionLimit)
# ___________________________________________________
#  Variables
# ___________________________________________________

# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("\n")
    print("------------------------------------------------------")
    print("🚖 Bienvenido al analizador de Servicios de Taxis en Chicago 🚖")
    print("------------------------------------------------------\n")
    print("1- Inicializar Analizador")
    print("2- Cargar información")
    print("3- Reporte general")
    print("4- Sistema de puntos y premios ")
    print("5- Desplazarse en el menor tiempo entre dos “CommunityAreas”")
    print("0- Salir")
    print("------------------------------------------------------")


def optionTwo():
    try:
        size = input('Tamaño de los datos (small, medium, large): ')
        controller.loadTrips(cont, size)
    except:
        print('❌ No se pudo cargar los datos')
    # numedges = controller.totalConnections(cont)
    # numvertex = controller.totalStops(cont)
    # print('Número de vértices: ' + str(numvertex))
    # print('Número de arcos: ' + str(numedges))


def optionThree():
    n_taxis = int(input('✔ Ingrese la cantidad de compañias para el top por taxis: '))
    n_servi = int(input('✔ Ingrese la cantidad de compañias para el top por servicios: '))

    try:
        numero_taxis = controller.ejec_num_taxis(cont)
        print('Número de taxis: ')
        print (numero_taxis)
    except:
        print('❌ No se pudo encontrar la cantidad de taxis')

    try:
        numero_companias = controller.ejec_num_companias(cont)
        print('Numero de compañias: ')
        print(numero_companias)
    except:
        print('❌ No se pudo encontrar la cantidad de compañias')

    try:
        top_com_t = controller.ejec_top_companias_taxis(cont, n_taxis)
        print('🏆 Top de compañias por taxis:')
        for i in top_com_t:
            print('-', i)
    except:
        print('❌ No se pudo encontrar el top por taxis')

    try:
        top_com_s = controller.ejec_top_companias_servicios(cont, n_servi)
        print('🏆 Top de compañias por servicios:')
        for i in top_com_s:
            print('-',i)
    except:
        print('❌ No se pudo encontrar el top por servicios')


def optionFour():
    taxis = int(input('✔ Ingrese la cantidad de taxis para el top por puntaje:'))
    f = input('📅 ingrese la fecha para para el top por puntos (formato: yyyy-mm-dd):')
    taxis_f = int(input('✔ Ingrese la cantidad de taxis para el top por puntaje en un rango: '))
    f_i = input('📅 ingrese la fecha inicial para el top en rango por puntos (formato: yyyy-mm-dd):')
    f_f = input('📅 ingrese la fecha final para el top en rango por puntos (formato: yyyy-mm-dd):')

    try:
        resul = controller.ejec_top_taxis_puntaje(cont, f, taxis)
        print ('En la fecha ', f)
        for i in resul:
            print('-',i)

    except:
        print('❌ No se pudo encontrar el top por puntaje en esta fecha')

    try:
        resul = controller.ejec_top_taxis_rango(cont, f_i, f_f, taxis_f)
        print ('En el rango de fechas entre ', f_i, ' y ', f_f)
        for i in resul:
            print('-',i)
    except:
        print('❌ No se pudo encontrar el top por puntaje en este rango')


def optionFive():
    c_a1 = input('📍 Ingrese el community area inicial: ')
    c_a2 = input('📍 Ingrese el community area final: ')
    t1 = input('⏱ Ingrese la hora inicial para el recorrido: ')
    t2 = input('⏱ Ingrese la hora final para el recorrido: ')

    # try:
    resul = controller.ejec_mejor_horario(cont, c_a1, c_a2, t1, t2)
    print('Tiempo estimado:', resul[1])
    print('Hora ideal de salida:', resul[2])
    print('Ruta:')
    for i in resul[0]:
        print('-', i)  # hace falta separar según los distintos resultados
    # except:
    #     print('❌ No se pudo encontrar la mejor ruta')


"""
Menu principal
"""

while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()

    elif int(inputs[0]) == 2:

        executiontime = timeit.timeit(optionTwo, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 3:
        executiontime = timeit.timeit(optionThree, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 4:
        executiontime = timeit.timeit(optionFour, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 5:
        executiontime = timeit.timeit(optionFive, number=1)
        print("Tiempo de ejecución: " + str(executiontime))
    else:
        sys.exit(0)
sys.exit(0)
