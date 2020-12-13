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
    print("Bienvenido al analizador de Servicios de Taxis en Chicago")
    print("------------------------------------------------------\n")
    print("1- Inicializar Analizador")
    print("2- Cargar información")
    print("3- Reporte general")
    print("4- Sistema de puntos y premios ")
    print("5- Desplazarse en el menor tiempo entre dos “CommunityAreas”")
    print("0- Salir")
    print("------------------------------------------------------")


def optionTwo():
    controller.loadTrips(cont)
    # numedges = controller.totalConnections(cont)
    # numvertex = controller.totalStops(cont)
    # print('Número de vértices: ' + str(numvertex))
    # print('Número de arcos: ' + str(numedges))


def optionThree():
    pass


def optionFour():
    pass


def optionFive():
    pass


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
