"""
 * Copyright 2020, Departamento de sistemas y Computación,
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
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.ADT import graph as gr
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newAnalyzer():

    analyzer = {
                'landing_points' : None,
                'countries' : None,
                'connections': None,
                'cities_country' : None
                }
    analyzer['landing_points'] = mp.newMap(maptype='PROBING')

    analyzer['countries'] = mp.newMap(maptype= 'PROBING')

    analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST', directed = False)

    analyzer['cities_country'] = mp.newMap(maptype = 'PROBING')

    analyzer['capitals'] = mp.newMap(maptype='PROBING')

    return analyzer

# Funciones para agregar informacion al catalogo

def addLandingPoint(analyzer, landing_point):
    dict_landing = {}
    dict_landing['landing_point_id'] = landing_point['landing_point_id']
    dict_landing['id'] = landing_point['id']
    lista = landing_point['name']
    lista = lista.split(',')
    if len(lista) == 1:
        dict_landing['city'] = lista[0]
        dict_landing['country'] = lista[0]
    elif len(lista) == 2:
        dict_landing['city'] = lista[0]
        dict_landing['country'] = lista[1]
    elif len(lista) == 3:
        dict_landing['city'] = lista[0]
        dict_landing['country'] = lista[2]
    elif len(lista) == 4:
        dict_landing['city'] = lista[0]
        dict_landing['country'] = lista[3]
    dict_landing['latitude'] = landing_point['latitude']
    dict_landing['longitude'] = landing_point['longitude']

    mp.put(analyzer['landing_points'], landing_point['landing_point_id'], dict_landing)

def addCountry(analyzer, country):
    mp.put(analyzer['countries'], country['CountryName'], country)
    lista = lt.newList()
    lt.addLast(lista , country['CapitalName'])
    mp.put(analyzer['cities_country'], country['CountryName'], lista)
    dict_capital = {}
    dict_capital['CapitalLatitude'] = country['CapitalLatitude']
    dict_capital['CapitalLongitude'] = country['CapitalLongitude']
    mp.put(analyzer['capitals'], country['CountryName'], dict_capital)


def addConnection(analyzer, connection):
    origin = connection['\ufefforigin']
    destination = connection['destination']
    cable_id = connection['cable_id']
    cable_lenght = connection['cable_length']

    verticeA = "<{}>-<{}>".format(origin, cable_id)
    verticeB = "<{}>-<{}>".format(destination, cable_id)

    gr.insertVertex(analyzer['connections'], verticeA)
    gr.insertVertex(analyzer['connections'], verticeB)
    gr.addEdge(analyzer['connections'], verticeA, verticeB, cable_lenght)

def addSameOrigin(analyzer):

    vertices = gr.vertices(analyzer['connections'])

    for i in range(lt.size(vertices)):
        verticeA = lt.getElement(vertices, i)
        parejaA = verticeA.replace('<', '').replace('>', '').split('-')
        originA = parejaA[0]
        cableA = parejaA[1]
        for j in range(lt.size(vertices)):
            verticeB = lt.getElement(vertices, j)
            parejaB = verticeB.replace('<', '').replace('>', '').split('-')
            originB = parejaB[0]
            cableB = parejaB[1]
            if originA == originB and cableA != cableB:
                gr.addEdge(analyzer['connections'], verticeA, verticeB, 100)

def addCountriestoCapitalCity(analyzer):

    vertices = gr.vertices(analyzer['connections'])
    map_landing = analyzer['landing_points']

    for i in range(lt.size(vertices)):
        vertice = lt.getElement(vertices, i)
        parejaA = vertice.replace('<', '').replace('>', '').split('-')
        origenA = parejaA[0]
        pareja = mp.get(map_landing, origenA)
        info = me.getValue(pareja)
        pais = info['country']

        contains = gr.containsVertex(analyzer['connections'], pais)
        if not contains:
            gr.insertVertex(analyzer['connections'], pais)
            gr.addEdge(analyzer['connections'], pais, vertice)
        if contains: 
            gr.addEdge(analyzer['connections'], pais, vertice)
  


# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
