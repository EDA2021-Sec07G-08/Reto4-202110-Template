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
        print(gr.numEdges(grafo))
        print(gr.numEdges(grafo_direc))

    elif int(inputs[0]) == 2:
        landing1 = input('Ingrese el nombre del landing point 1: ')
        landing2 = input('Ingrese el nombre del landing point 2: ')
        controller.Requerimiento1(analyzer,landing1,landing2)
        
    elif int(inputs[0]) == 3:
         controller.Requerimiento2(analyzer)

    elif int(inputs[0]) == 5:
        controller.Requerimiento4(analyzer)
    elif int(inputs[0]) == 6:
        landing_point_id = input('Ingrese el landing point id: ')
        controller.Requerimiento5(analyzer, landing_point_id)
    else:
        sys.exit(0)
sys.exit(0)
