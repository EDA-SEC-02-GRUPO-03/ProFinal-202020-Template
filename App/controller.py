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

import config as cf
import model
import csv
import os

"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________


def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # analyzer es utilizado para interactuar con el modelo
    analyzer = model.create_analyzer()
    return analyzer

# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________


def loadTrips(taxi_trips, size):
    for filename in os.listdir(cf.data_dir):
        if filename.endswith('.csv') and size in filename:
            print('⏳ Cargando archivo: ' + filename)
            loadFile(taxi_trips, filename)
    print(taxi_trips['horas'])

    return taxi_trips


def loadFile(taxi_trips, tripfile):
    tripfile = cf.data_dir + tripfile
    input_file = csv.DictReader(open(tripfile, encoding="utf-8"),
                                delimiter=",")
    for trip in input_file:
        model.addTrip(taxi_trips, trip)
    print('✔ Done!')
    return taxi_trips

# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________

'''
PARTE A
'''

def ejec_num_taxis(taxi_trips):
    resul = model.num_taxis(taxi_trips)
    return resul


def ejec_num_companias(taxi_trips):
    resul = model.num_companias(taxi_trips)
    return resul


def ejec_top_companias_taxis(taxi_trips, num):
    resul = model.top_companias_taxis(taxi_trips, num)
    return resul


def ejec_top_companias_servicios(taxi_trips, num):
    resul = model.top_companias_servicios(taxi_trips, num)
    return resul

'''
PARTE B
'''

def ejec_top_taxis_puntaje(taxi_trips, fecha, num):
    resul = model.top_taxis_puntaje(taxi_trips, fecha, num)
    return resul


def ejec_top_taxis_rango(taxi_trips, fechain, fechafin, num):
    resul = model.top_taxis_puntaje_rango(taxi_trips, fechain, fechafin, num)
    return resul

'''
PARTE C
'''

def ejec_mejor_horario(cont, c_a1, c_a2, t1, t2):
    resul = model.mejor_horario(cont, c_a1, c_a2, t1, t2)
    return resul


def totalConnections(analyzer):
    """
    Total de enlaces entre las paradas
    """
    return model.totalConnections(analyzer)


def totalStops(analyzer):
    """
    Total de paradas de autobus
    """
    return model.totalStops(analyzer)
