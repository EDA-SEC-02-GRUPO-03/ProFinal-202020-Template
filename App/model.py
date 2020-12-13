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
import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.DataStructures import rbt as rbt
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
import datetime
assert config

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

# -----------------------------------------------------
#                       API
# -----------------------------------------------------

# Funciones para agregar informacion al grafo

def create_analyzer():
    taxi_trips = {'viajes' : None,
                  'compañia' : None,
                  'fechas' : None,
                  'grafo' : None
                  }

    taxi_trips['viajes'] = m.newMap(numelements=60000,
                                    maptype='PROBING',
                                    comparefunction=compareTrips)
    
    taxi_trips['compania'] = m.newMap(numelements=60000,
                                    maptype='PROBING',
                                    comparefunction=compareTrips)
    
    taxi_trips['fechas'] = rbt.newMap(comparefunction=compareDates)

    taxi_trips['grafo'] = gr.newGraph(datastructure='ADJ_LIST',
                                        directed=True,
                                        size=1000,
                                        comparefunction=compareTrips)
    return taxi_trips

# ==============================
# Funciones de consulta
# ==============================

def addTrip(taxi_trips, trip):
    m.put(taxi_trips['viajes'],trip['trip_id'], trip)
    updateDateIndex(taxi_trips, trip)
    addCompany(taxi_trips, trip)
    return taxi_trips

def updateDateIndex(taxi_trips, trip):
    occurreddate = trip['trip_start_timestamp'][0:10] + ' ' + trip['trip_start_timestamp'][11:19]
    tripdate = datetime.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M:%S')
    taxi = trip['taxi_id']
    if rbt.contains(taxi_trips['fechas'], tripdate.date()):
        entry = rbt.get(taxi_trips['fechas'], tripdate.date())
        if lt.isPresent(entry['value'],taxi) == 0:
            lt.addLast(entry['value'],taxi)
            rbt.put(taxi_trips['fechas'],tripdate.date(), entry['value'])

    else:
        ids = lt.newList()
        lt.addFirst(ids, taxi)
        rbt.put(taxi_trips['fechas'], tripdate.date(), ids)

    return taxi_trips

def addCompany(taxi_trips, trip):
    compania = trip['company']
    if compania == '':
        compania = 'Independent Owner'
    taxi = trip['taxi_id']
    if m.contains(taxi_trips['compania'],compania) == False:
        lista = lt.newList()
        lt.addLast(lista,taxi)
        valor = [lista, 1] #la cantidad de viajes por empresa
        m.put(taxi_trips['compania'],compania,valor)
    else:
        entry = m.get(taxi_trips['compania'],compania)
        if lt.isPresent(entry['value'][0],taxi) == 0:
            lt.addLast(entry['value'][0],taxi)
        entry['value'][1] += 1
        m.put(taxi_trips['compania'],compania,entry['value'])

    return taxi_trips
 

# ==============================
# Funciones Helper
# ==============================
'''
PARTE A
'''

def num_taxis (taxi_trips):
    iterador = it.newIterator(m.keySet(taxi_trips['compania']))
    taxis = 0
    while it.hasNext(iterador):
        element = it.next(iterador)
        dicc = m.get(taxi_trips['compania'], element)
        taxis += lt.size(dicc['value'][0])
    return taxis

def num_companias(taxi_trips):
    return lt.size(m.keySet(taxi_trips['compania']))

def top_companias_taxis(taxi_trips, num):
    lista = []
    cantidades = []
    retorno = []
    iterador = it.newIterator(m.keySet(taxi_trips['compania']))
    while it.hasNext(iterador):
        element = it.next(iterador)
        dicc = m.get(taxi_trips['compania'], element)
        afiliados = lt.size(dicc['value'][0])
        valores = {'compania': element, 'afiliados': afiliados}
        lista.append(valores)
        cantidades.append(afiliados)

    i = 0
    while i < num:
        j = cantidades.index(max(cantidades))
        retorno.append(lista[j])
        lista.remove(lista[j])
        cantidades.remove(max(cantidades))
        i+=1
    return retorno


def top_companias_servicios(taxi_trips, num):
    lista = []
    cantidades = []
    retorno = []
    iterador = it.newIterator(m.keySet(taxi_trips['compania']))
    while it.hasNext(iterador):
        element = it.next(iterador)
        dicc = m.get(taxi_trips['compania'], element)
        servicios = dicc['value'][1]
        valores = {'compania': element, 'servicios': servicios}
        lista.append(valores)
        cantidades.append(servicios)

    i = 0
    while i < num:
        j = cantidades.index(max(cantidades))
        retorno.append(lista[j])
        lista.remove(lista[j])
        cantidades.remove(max(cantidades))
        i+=1
    return retorno

'''
PARTE B
''' 


    
# ==============================
# Funciones de Comparacion
# ==============================
def compareDates(date1, date2):
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1

def compareTrips(trip1, trip2):

    trip2 = trip2['key']
    if (trip1 == trip2):
        return 0
    elif (trip1 > trip2):
        return 1
    else:
        return -1