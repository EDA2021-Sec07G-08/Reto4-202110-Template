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


from DISClib.DataStructures.arraylist import newList
from DISClib.DataStructures.chaininghashtable import contains
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.ADT import orderedmap as om
from DISClib.ADT import graph as gr
from DISClib import haversine as hs
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newAnalyzer():

    analyzer = {
                'vertices':None,
                'info_landings': None,
                'landing_points' : None,
                'countries' : None,
                'connections': None,
                'cities_country' : None
                }
    analyzer['vertices'] = lt.newList()

    analyzer['landing_points'] = om.newMap()

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
    dict_landing['cables'] = lt.newList()

    om.put(analyzer['landing_points'], landing_point['landing_point_id'], dict_landing)

def addCountry(analyzer, country):
    mp.put(analyzer['countries'], country['CountryName'], country)
    lista = lt.newList()
    lt.addLast(lista , country['CapitalName'])
    mp.put(analyzer['cities_country'], country['CountryName'], lista)
    dict_capital = {}
    dict_capital['CapitalLatitude'] = country['CapitalLatitude']
    dict_capital['CapitalLongitude'] = country['CapitalLongitude']
    mp.put(analyzer['capitals'], country['CountryName'], dict_capital)

def DistanceHaversine(lp1,lp2, analyzer):

    map_landing = analyzer['landing_points']

    pareja_lp1 = om.get(map_landing, lp1)
    dict_lp1 = me.getValue(pareja_lp1)
    latitude_lp1 = float(dict_lp1['latitude'])
    longitude_lp1 = float(dict_lp1['longitude'])
    
    pareja_lp2 = om.get(map_landing, lp2)
    dict_lp2 = me.getValue(pareja_lp2)
    latitude_lp2 = float(dict_lp2['latitude'])
    longitude_lp2 = float(dict_lp2['longitude'])

    loc_lp1 = (latitude_lp1, longitude_lp1)
    loc_lp2 = (latitude_lp2, longitude_lp2)

    distance = hs.haversine(loc_lp1, loc_lp2)

    return distance

def addConnection(analyzer, connection):
    origin = connection['\ufefforigin']
    destination = connection['destination']
    cable_id = connection['cable_id']
    cable_lenght = DistanceHaversine(origin, destination,analyzer)

    verticeA = "<{}>-<{}>".format(origin, cable_id)
    verticeB = "<{}>-<{}>".format(destination, cable_id)

    listilla = [origin, cable_id, verticeA]

    lt.addLast(analyzer['vertices'], listilla)

    mapa = analyzer['landing_points']
    pareja = om.get(mapa, origin)
    valor = me.getValue(pareja)
    lista_cables = valor['cables']
    lt.addLast(lista_cables, verticeA)

    containsA = gr.containsVertex(analyzer['connections'], verticeA)
    containsB = gr.containsVertex(analyzer['connections'], verticeB)
    if not containsA:
        gr.insertVertex(analyzer['connections'], verticeA)
    if not containsB:
        gr.insertVertex(analyzer['connections'], verticeB)
    
    gr.addEdge(analyzer['connections'], verticeA, verticeB, cable_lenght)

def addSameOrigin(analyzer):

    info = om.valueSet(analyzer['landing_points'])

    for i in range(lt.size(info)):
        diccionario = lt.getElement(info, i)
        lista_cables = diccionario['cables']
        for i in range(lt.size(lista_cables)):
            verticeA = lt.getElement(lista_cables, i)
            cont = 1
            j = i
            while j + cont <= lt.size(lista_cables):
                verticeB = lt.getElement(lista_cables, j + cont)
                if verticeA != verticeB:
                    gr.addEdge(analyzer['connections'], verticeA, verticeB, 100)
                cont += 1

def addCountriestoCapitalCity(analyzer):

    vertices = analyzer['vertices']
    map_landing = analyzer['landing_points']

    for i in range(lt.size(vertices)):
        parejaA = lt.getElement(vertices, i)
        origenA = parejaA[0]
        vertice = parejaA[2]
        pareja = om.get(map_landing, origenA)
        info = me.getValue(pareja)
        pais = info['country']

        contains = gr.containsVertex(analyzer['connections'], pais)
        if not contains:
            gr.insertVertex(analyzer['connections'], pais)
            gr.addEdge(analyzer['connections'], pais, vertice)
            lista_add = analyzer['vertices']
            lt.addLast(lista_add, pais)
        if contains: 
            gr.addEdge(analyzer['connections'], pais, vertice)
  


# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
def Requerimiento2(analyzer):
    vertic = gr.vertices(analyzer['connections'])
    mapaR = mp.newMap()
    listaR = lt.newList()
    
    for i in range (0,lt.size(vertic)):
        vertix = lt.getElement(vertic,i)
        vert_adya = gr.degree(analyzer['connections'],vertix)
        print(vertix)
        print(vert_adya)
        lt.addLast(listaR,(vert_adya,vertix))



