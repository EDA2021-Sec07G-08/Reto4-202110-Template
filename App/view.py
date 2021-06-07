"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf
from DISClib.ADT import graph as gr
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2 - Requerimiento 1")
    print('3 - Requerimiento 2')
    print('4 - Requerimiento 3')
    print('5 - Requerimiento 4')
    print('6 - Requerimiento 5')

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        analyzer = controller.init()
        data = controller.loadData(analyzer)
        grafo = analyzer['connections']
        grafo_direc = analyzer['connections_directed']
        print('El numero de landing points es: '+str(om.size(analyzer['landing_points'])))
        print('El numero total de paises es: '+ str(mp.size(analyzer['countries'])))
        print('El numero de conexiones entre landing points (arcos) es: '+ str(gr.numEdges(analyzer['connections'])))

    elif int(inputs[0]) == 2:
        landing1 = input('Ingrese el nombre del landing point 1: ')
        landing2 = input('Ingrese el nombre del landing point 2: ')
        controller.Requerimiento1(analyzer,landing1,landing2)
        
    elif int(inputs[0]) == 3:
        ans = controller.Requerimiento2(analyzer)
        j = 0
        for i in lt.iterator(ans):
            j += 1
            if j == 11:
                break
            print(i)


    elif int(inputs[0]) == 4:
        pais_a = input('Ingrese el nombre del país A: ')
        pais_b = input('Ingrese el nombre del país B: ')
        controller.Requerimiento3(analyzer,pais_a,pais_b)

    elif int(inputs[0]) == 5:
        controller.Requerimiento4(analyzer)
    elif int(inputs[0]) == 6:
        landing_point_id = input('Ingrese el landing point id: ')
        controller.Requerimiento5(analyzer, landing_point_id)
    else:
        sys.exit(0)
sys.exit(0)
