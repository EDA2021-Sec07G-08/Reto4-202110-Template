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
from DISClib.Algorithms.Graphs import prim as pr
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.ADT import orderedmap as om
from DISClib.ADT import graph as gr
from DISClib import haversine as hs
assert cf
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as dij
from DISClib.DataStructures import listiterator as it 
from DISClib.Algorithms.Sorting import mergesort as merg
"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newAnalyzer():

    analyzer = {
                'vertices':None,
                'element':None,
                'camino':None,
                'landing_names_id':None,
                'info_landings': None,
                'landing_points' : None,
                'countries' : None,
                'connections': None,
                'connections_directed': None,
                'cities_country' : None
                }
    analyzer['vertices'] = lt.newList()

    analyzer['landing_points'] = om.newMap()

    analyzer['landing_names_id'] = mp.newMap()

    analyzer['countries'] = mp.newMap(maptype= 'PROBING')

    analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST', directed = False)

    analyzer['connections_directed'] = gr.newGraph(datastructure='ADJ_LIST', directed = True)

    analyzer['cities_country'] = mp.newMap(maptype = 'PROBING')

    analyzer['capitals'] = mp.newMap(maptype='PROBING')

    return analyzer

# Funciones para agregar informacion al catalogo

def addLandingPoint(analyzer, landing_point):

    contains_map1 = om.contains(analyzer['landing_points'], landing_point['landing_point_id'])
    if not contains_map1:
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

    contains_map2 = mp.contains(analyzer['landing_names_id'], landing_point['id'])

    if not contains_map2:
        mp.put(analyzer['landing_names_id'], landing_point['name'], landing_point['landing_point_id'])

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
    cable_id = connection['cable_name']
    cable_lenght = DistanceHaversine(origin, destination,analyzer)

    verticeA = "<{}>-<{}>".format(origin, cable_id)
    verticeB = "<{}>-<{}>".format(destination, cable_id)

    containsA = gr.containsVertex(analyzer['connections'], verticeA)
    containsB = gr.containsVertex(analyzer['connections'], verticeB)

    if containsA and containsB:
        gr.addEdge(analyzer['connections'], verticeA, verticeB, cable_lenght)
    if not containsA and not containsB:
        gr.insertVertex(analyzer['connections'], verticeA)
        gr.insertVertex(analyzer['connections'], verticeB)
        gr.addEdge(analyzer['connections'], verticeA, verticeB, cable_lenght)

        listilla = [origin, cable_id, verticeA]

        lt.addLast(analyzer['vertices'], listilla)

        mapa = analyzer['landing_points']
        pareja = om.get(mapa, origin)
        valor = me.getValue(pareja)
        lista_cables = valor['cables']
        lt.addLast(lista_cables, verticeA)

def addConnection_directed(analyzer, connection):
    origin = connection['\ufefforigin']
    destination = connection['destination']
    cable_id = connection['cable_name']
    cable_lenght = DistanceHaversine(origin, destination,analyzer)

    verticeA = "<{}>-<{}>".format(origin, cable_id)
    verticeB = "<{}>-<{}>".format(destination, cable_id)


    containsA = gr.containsVertex(analyzer['connections_directed'], verticeA)
    containsB = gr.containsVertex(analyzer['connections_directed'], verticeB)
    if not containsA and not containsB:
        gr.insertVertex(analyzer['connections_directed'], verticeA)
        gr.insertVertex(analyzer['connections_directed'], verticeB)

        listilla = [origin, cable_id, verticeA]

        lt.addLast(analyzer['vertices'], listilla)

        mapa = analyzer['landing_points']
        pareja = om.get(mapa, origin)
        valor = me.getValue(pareja)
        lista_cables = valor['cables']
        lt.addLast(lista_cables, verticeA)

        gr.addEdge(analyzer['connections_directed'], verticeA, verticeB, cable_lenght)

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

def addSameOrigin_directed(analyzer):

    info = om.valueSet(analyzer['landing_points'])

    for i in range(lt.size(info)):
        diccionario = lt.getElement(info, i)
        lista_cables = diccionario['cables']
        for i in range(lt.size(lista_cables)):
            verticeA = lt.getElement(lista_cables, i)
            cont = 0
            j = 1
            while j + cont <= lt.size(lista_cables):
                verticeB = lt.getElement(lista_cables, j + cont)
                if verticeA != verticeB:
                    gr.addEdge(analyzer['connections_directed'], verticeA, verticeB, 100)
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

def Requerimiento1(analyzer,landing1,landing2):
    analyzer['element'] = scc.KosarajuSCC(analyzer['connections_directed'])
    cluster_number = scc.connectedComponents(analyzer['element'])
    get_landing1 = mp.get(analyzer['landing_names_id'],landing1)
    id_landing1 = me.getValue(get_landing1)
    dict_landing_pareja1 = om.get(analyzer['landing_points'], id_landing1)
    dict_landing1 = me.getValue(dict_landing_pareja1)
    lista_cables1 = dict_landing1['cables']
    vectorA = lt.getElement(lista_cables1, 1) 
    get_landing2 = mp.get(analyzer['landing_names_id'],landing2)
    id_landing2 = me.getValue(get_landing2)
    dict_landing_pareja2 = om.get(analyzer['landing_points'], id_landing2)
    dict_landing2 = me.getValue(dict_landing_pareja2)
    lista_cables2 = dict_landing1['cables']
    vectorB = lt.getElement(lista_cables2, 1) 
    inform_cluster = scc.stronglyConnected(analyzer['element'],vectorA, vectorB)

    if inform_cluster == False:
        print('Los landing points consultados no estan en el mismo cluster')
    else:
        print('Los landing points cosnultados se encuentran en el mismo cluster')
        print('El total de clústers presentes en la red es igual a '+ str(cluster_number))

def sorting2(lista,size,cmpfunction_merge):
    sub_list = lt.subList(lista,0, size)
    sub_list = lista.copy()
    sorted_list=merg.sort(sub_list, cmpfunction_merge)
    return  sorted_list

def cmpfunction_merge(vertex1, vertex2):
    return (float(vertex1[1]) > float(vertex2[1]))

def Requerimiento2(analyzer):
    vertic = gr.vertices(analyzer['connections'])
    listaR = lt.newList('SINGLE_LINKED')
    iterator = it.newIterator(vertic)
    while it.hasNext(iterator):
        posi = it.next(iterator)
        vert_adya = gr.degree(analyzer['connections'],posi)
        lt.addLast(listaR,(posi,vert_adya))
    res = sorting2(listaR,10,cmpfunction_merge)
    return res

    
def Requerimiento3 (analyzer,pais_a,pais_b):
    vertice_a = pais_a
    vertice_b = pais_b
    analyzer['caminos'] = dij.Dijkstra(analyzer['connections'],vertice_a)
    ruta = dij.pathTo(analyzer['connection'],vertice_b)
    distancia = dij.distTo(analyzer['connections'],vertice_b)
    return ruta , distancia

def Requerimiento4(analyzer):

    total = 0
    grafo = analyzer['connections']
    mst = pr.PrimMST(grafo)
    map_distTo = mst['distTo']
    values = mp.valueSet(map_distTo)

    for i in range(lt.size(values)):
        value = lt.getElement(values, i)
        total += value

    total = round(total, 2)

    nodos = lt.size(values)

    print('El minimo numero de nodos conectados a la red de expasion minima es: '+str(nodos))
    print('El costo total (en kilometros) de la red de expansion minima es de: ' + str(total) + ' km')
        

def Requerimiento5(analyzer, landing_point_name):

    map_respuesta = mp.newMap()
    #encontrar codigo con nombre

    mapa_codigo = analyzer['landing_names_id']
    pareja_codigo = mp.get(mapa_codigo, landing_point_name)
    codigo = me.getValue(pareja_codigo)

    #sacar vertices de este landing point (unicamente estara conectado a un vertice de pais y es el vertice de su mismo pais)

    mapa_vertices = analyzer['landing_points']
    pareja_vertices = om.get(mapa_vertices, codigo)
    dict_landing = me.getValue(pareja_vertices)
    lista_vertices = dict_landing['cables']

    for i in range(lt.size(lista_vertices)):
        vertice = lt.getElement(lista_vertices, i)
        arcos_vertice = gr.adjacents(analyzer['connections'], vertice)
        for i in range(lt.size(arcos_vertice)):
            vertice2 = lt.getElement(arcos_vertice, i)
            tuple_vertice2 = vertice2.replace('<','').replace('>', '').split('-')
            origen = tuple_vertice2[0]
            contains_landing = om.contains(analyzer['landing_points'], origen)
            if contains_landing:

            #extraer pais del origen

                pareja_origen = om.get(analyzer['landing_points'], origen)
                dict_origen = me.getValue(pareja_origen)
                pais = dict_origen['country']
                contains_country = mp.contains(map_respuesta, pais)
                if not contains_country:
                    mp.put(map_respuesta, pais, 0)

    print(mp.keySet(map_respuesta))
        






