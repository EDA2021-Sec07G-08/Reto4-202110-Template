﻿"""
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
 """

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def init():
    analyzer = model.newAnalyzer()
    return analyzer

# Funciones para la carga de datos

def loadData(analyzer):

    loadLandingPoints(analyzer, 'landing_points.csv')
    loadCountry(analyzer, 'countries.csv')
    loadConnection(analyzer, 'connections.csv')
    model.addCountriestoCapitalCity(analyzer)

def loadLandingPoints(analyzer, file):

    file = cf.data_dir + file
    input_file = csv.DictReader(open(file, encoding="utf-8"), delimiter = ",")

    for landing_point in input_file:
        model.addLandingPoint(analyzer, landing_point)
    return analyzer

def loadCountry(analyzer, file):

    file = cf.data_dir + file
    input_file = csv.DictReader(open(file, encoding="utf-8"), delimiter = ",")

    for country in input_file:
        model.addCountry(analyzer, country)
    return analyzer

def loadConnection(analyzer, file):

    file = cf.data_dir + file
    input_file = csv.DictReader(open(file, encoding="utf-8"), delimiter = ",")

    for connection in input_file:
        model.addConnection(analyzer, connection)
    model.addSameOrigin(analyzer)
    return analyzer

def Requerimiento2(analyzer):
    print('entre')
    return model.Requerimiento2(analyzer)

def Requerimiento5(analyzer, landing_point_id):
    return model.Requerimiento5(analyzer,landing_point_id)



# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
