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
from DISClib.ADT import orderedmap as om
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
    taxi_trips = {'viajes': None,
                  'compañia': None,
                  'fechas': None,
                  'grafo': None
                  }

    taxi_trips['viajes'] = m.newMap(numelements=60000,
                                    maptype='PROBING',
                                    comparefunction=compareTrips)

    taxi_trips['compania'] = m.newMap(numelements=60000,
                                      maptype='PROBING',
                                      comparefunction=compareTrips)

    taxi_trips['fechas'] = om.newMap('RBT', comparefunction=compareDates)

    taxi_trips['grafo'] = gr.newGraph(datastructure='ADJ_LIST',
                                      directed=True,
                                      size=1000,
                                      comparefunction=compareTrips)
    return taxi_trips

# ==============================
# Funciones de consulta
# ==============================


def addTrip(taxi_trips, trip):
    m.put(taxi_trips['viajes'], trip['trip_id'], trip)
    updateDateIndex(taxi_trips, trip)
    addCompany(taxi_trips, trip)
    return taxi_trips


def updateDateIndex(taxi_trips, trip):
    occurreddate = trip['trip_start_timestamp'][0:10] + ' ' + \
        trip['trip_start_timestamp'][11:19]
    tripdate = datetime.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M:%S')
    viaje = trip['trip_id']
    if om.contains(taxi_trips['fechas'], tripdate.date()):
        entry = om.get(taxi_trips['fechas'], tripdate.date())
        lt.addLast(entry['value'], viaje)
        om.put(taxi_trips['fechas'], tripdate.date(), entry['value'])
    else:
        ids = lt.newList()
        lt.addFirst(ids, viaje)
        om.put(taxi_trips['fechas'], tripdate.date(), ids)

    return taxi_trips


def addCompany(taxi_trips, trip):
    compania = trip['company']
    if compania == '':
        compania = 'Independent Owner'
    taxi = trip['taxi_id']
    if m.contains(taxi_trips['compania'], compania) is False:
        lista = lt.newList()
        lt.addLast(lista, taxi)
        valor = [lista, 1]  # la cantidad de viajes por empresa
        m.put(taxi_trips['compania'], compania, valor)
    else:
        entry = m.get(taxi_trips['compania'], compania)
        if lt.isPresent(entry['value'][0], taxi) == 0:
            lt.addLast(entry['value'][0], taxi)
        entry['value'][1] += 1
        m.put(taxi_trips['compania'], compania, entry['value'])

    return taxi_trips


'''
PARTE A
'''


def num_taxis(taxi_trips):
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
        i += 1
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
        i += 1
    return retorno


'''
PARTE B
'''


def top_taxis_puntaje(taxi_trips, fecha, num):
    fecha = datetime.datetime.strptime(fecha, '%Y-%m-%d')
    arbol = om.get(taxi_trips['fechas'], fecha.date())
    mapa = m.newMap(numelements=600,
                    maptype='PROBING',
                    comparefunction=compareid)
    if arbol is None:
        return 'No hay viajes en la fecha'
    else:
        iterador = it.newIterator(arbol['value'])
        while it.hasNext(iterador):
            element = it.next(iterador)
            trip = m.get(taxi_trips['viajes'], element)
            if m.contains(mapa, trip['value']['taxi_id']):
                datos = m.get(mapa, trip['value']['taxi_id'])
                if (trip['value']['trip_miles']) != '' and \
                   (trip['value']['trip_total']) != '':
                    if float(trip['value']['trip_miles']) > 0 and \
                       float(trip['value']['trip_total']) > 0:
                        datos['value']['servicios'] += 1
                        tripM = float(trip['value']['trip_miles'])
                        datos['value']['millas'] += tripM
                        tripT = float(trip['value']['trip_total'])
                        datos['value']['costo'] += tripT
                m.put(mapa, trip['value']['taxi_id'], datos['value'])
            else:
                dicc = {'servicios': 0, 'millas': 0, 'costo': 0}
                if (trip['value']['trip_miles']) != '' and \
                   (trip['value']['trip_total']) != '':
                    if float(trip['value']['trip_miles']) > 0 and \
                       float(trip['value']['trip_total']) > 0:
                        dicc['servicios'] += 1
                        dicc['millas'] += float(trip['value']['trip_miles'])
                        dicc['costo'] += float(trip['value']['trip_total'])
                m.put(mapa, trip['value']['taxi_id'], dicc)

    lista = []
    alfas = []
    retorno = []
    iterador = it.newIterator(m.keySet(mapa))
    while it.hasNext(iterador):
        element = it.next(iterador)
        dicc = m.get(mapa, element)
        if dicc['value']['costo'] != 0:
            alfa = dicc['value']['servicios'] * \
                   dicc['value']['millas'] / dicc['value']['costo']
        else:
            alfa = 0
        lista.append(dicc['key'])
        alfas.append(round(alfa, 2))
    i = 0
    while i < num and len(alfas) != 0:
        j = alfas.index(max(alfas))
        retorno.append((lista[j], max(alfas)))
        lista.remove(lista[j])
        alfas.remove(max(alfas))
        i += 1

    return retorno


def top_taxis_puntaje_rango(taxi_trips, fechain, fechafin, num):
    fechain = datetime.datetime.strptime(fechain, '%Y-%m-%d')
    fechafin = datetime.datetime.strptime(fechafin, '%Y-%m-%d')
    llaves = om.keys(taxi_trips['fechas'], fechain.date(), fechafin.date())
    iterador1 = it.newIterator(llaves)
    mapa = m.newMap(numelements=1000,
                    maptype='PROBING',
                    comparefunction=compareid)
    while it.hasNext(iterador1):
        element1 = it.next(iterador1)
        arbol = om.get(taxi_trips['fechas'], element1)
        iterador = it.newIterator(arbol['value'])
        while it.hasNext(iterador):
            element = it.next(iterador)
            trip = m.get(taxi_trips['viajes'], element)
            if m.contains(mapa, trip['value']['taxi_id']):
                datos = m.get(mapa, trip['value']['taxi_id'])
                if (trip['value']['trip_miles']) != '' and \
                   (trip['value']['trip_total']) != '':
                    if float(trip['value']['trip_miles']) > 0 and \
                       float(trip['value']['trip_total']) > 0:
                        datos['value']['servicios'] += 1
                        tripM = float(trip['value']['trip_miles'])
                        datos['value']['millas'] += tripM
                        tripT = float(trip['value']['trip_total'])
                        datos['value']['costo'] += tripT
                m.put(mapa, trip['value']['taxi_id'], datos['value'])
            else:
                dicc = {'servicios': 0, 'millas': 0, 'costo': 0}
                if (trip['value']['trip_miles']) != '' and \
                   (trip['value']['trip_total']) != '':
                    if float(trip['value']['trip_miles']) > 0 and \
                       float(trip['value']['trip_total']) > 0:
                        dicc['servicios'] += 1
                        dicc['millas'] += float(trip['value']['trip_miles'])
                        dicc['costo'] += float(trip['value']['trip_total'])
                m.put(mapa, trip['value']['taxi_id'], dicc)

    lista = []
    alfas = []
    retorno = []
    iterador = it.newIterator(m.keySet(mapa))
    while it.hasNext(iterador):
        element = it.next(iterador)
        dicc = m.get(mapa, element)
        if dicc['value']['costo'] != 0:
            alfa = dicc['value']['servicios'] * \
                   dicc['value']['millas'] / dicc['value']['costo']
        else:
            alfa = 0
        lista.append(dicc['key'])
        alfas.append(round(alfa, 2))
    i = 0
    while i < num and len(alfas) != 0:
        j = alfas.index(max(alfas))
        retorno.append((lista[j], max(alfas)))
        lista.remove(lista[j])
        alfas.remove(max(alfas))
        i += 1

    return retorno


'''
PARTE C
'''


# ==============================
# Funciones Helper
# ==============================


def totalConnections(analyzer):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(analyzer['grafo'])


def totalStops(analyzer):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return gr.numVertices(analyzer['grafo'])


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


def compareid(id1, id2):
    id2 = id2['key']
    if (id1 == id2):
        return 0
    elif (id1 > id2):
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
