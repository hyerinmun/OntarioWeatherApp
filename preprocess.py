from datetime import datetime
from os import error
import os, ssl
import sys
import shutil
from urllib import request

import subprocess

import csv

import pandas as pd

import time

# import the PostgreSQL adapter for Python

import psycopg2

from psycopg2 import sql




start_time = time.time()


# Section 1
# Downloading the latest weather file from https://dd.weather.gc.ca/nowcasting/matrices


if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

# getting the current date and time saving it to a variable 'now'
now = str(datetime.utcnow())

# saving the month, day, and hour values from the variable 'now' into new variables
month = now[5:7]
day = now[8:10]
hour = now[11:13]

# creating a URL string for the latest weather station file on https://dd.weather.gc.ca/nowcasting/matrices/
url = str('https://dd.weather.gc.ca/nowcasting/matrices/SCRIBE.NWCSTG.' + month + '.' + day + '.' + hour + 'Z.n.Z')


# Deleting 'main' folder and then creating it again
# Main folder contains intermediate files that aren't needed after the script is done
# Wiping this file at the start saves space 

shutil.rmtree('main')
os.makedirs('main')


# file name for locally saved weather station file
local_file = str('main\\' + url[45:])


print("running")


while True:
    try:
        request.urlretrieve(url, local_file)
        break
    except error:
        print("Error: 5min")
        time.sleep(300)
        
        
    

    

    



# Section 2
# Unzipping and renaming the weather file into a txt file

# creating variables to add into the command line code using string manipulation
unzipped = str('"' + local_file.replace(".Z", "") + '"')
txt_file = local_file.replace("n.Z", "txt")
print(txt_file)
txt_file = txt_file[5:]
print(txt_file)
txt_file = str('"' + txt_file + '"')
print(txt_file)
# setting up a command line code to unzip files using 7zip
# the output file path will need to be congifured
one = str('7z e ' + local_file + ' -oC:\project\main')

# setting up a command line code to rename the unzipped file into a txt file
two = str('rename ' + unzipped + " " + txt_file)
print(two)
subprocess.run(one, shell=True)
subprocess.run(two, shell=True)

# example of what the above command line code would look like
# subprocess.run('7z e C:\CollaborativeProject\output\SCRIBE.NWCSTG.05.22.03Z.n.Z  -oC:\CollaborativeProject\output', shell=True)
# subprocess.run('rename "C:\CollaborativeProject\output\SCRIBE.NWCSTG.05.22.03Z.n" "SCRIBE.NWCSTG.05.22.03Z.txt"', shell=True)

# Section 3
# Reading the text file and writing the contents to a new file

# csv to list: https://www.codespeedy.com/csv-to-list-in-python/



with open('on_stn_codes.csv') as stn:
    reader = csv.reader(stn)
    my_list = list(reader)


my_list[0] = ['CYAM']

list2 = str(my_list).replace("[",'').replace("'",'').replace("]",'')


list3 = [i[0] for i in my_list]

list4 = [" " + i for i in list3 if len(i) == 3]
list5 = [i for i in list3 if len(i) == 4]    

list4.extend(list5)


count = 0

txt_file2 = str('main\\' + txt_file.replace('"',""))

print(txt_file2)


# Connect to the PostgreSQL database server

postgresConnection = psycopg2.connect("dbname=ontario_weather user=postgres password='root'")

# Get cursor object from the database connection

cursor = postgresConnection.cursor()
print(txt_file)
name_Table = txt_file.replace(".txt", "").replace(".", "")
print(name_Table)
# Create table statement

#sqlCreateTable = "create table "+name_Table+" (STN VARCHAR(4), DATE VARCHAR(8), HOUR VARCHAR(4), TEMP FLOAT, WIND FLOAT, GEOM GEOMETRY(Point, 4326));"

# Create a table in PostgreSQL database

#cursor.execute(sqlCreateTable)


with open(txt_file2, "r") as file:  
    
    for line in file:

        try:
            if line[5:9] in list4:
                count += 1
                for x in range(10):
                    next(file)
                current = file.readline()
                sqlInsert = sql.SQL("INSERT INTO weather (STN, DATE, HOUR, TEMP, WIND) VALUES({one}, {two}, {three}, {four}, {five})".format(
                    one = ("'"+(line[5:9].replace(" ", ""))+"'"), 
                two = (current[0:8]), three = (current[9:13]), four = (current[65:70].replace(" ", "")), 
                five= (current[81:84].replace(" ", ""))))

                cursor.execute(sqlInsert)
                
        except IndexError:
            for x in range(30):
                next(file)


sqlAlter = "UPDATE weather SET GEOM = ST_SetSRID(ST_MakePoint(ws.lon, ws.lat), 4326) FROM ws WHERE ws.id = weather.stn;"

cursor.execute(sqlAlter)

postgresConnection.commit()


weather_file = txt_file2.replace(".txt", ".csv")


weather_file = weather_file.replace('"',"")


header = ['STN', 'DATE','HR', 'TEMP', 'WIND', 'Y', 'X', 'T1', 'T2', 'T3', 'T4', 'T5', 'W1','W2','W3', 'W4','W5']

df = pd.read_csv('latlon.csv')

first_column = df[df.columns[0]]
second_column = df[df.columns[1]]


count = 0

with open(txt_file2, "r") as file, open(weather_file, "w", encoding='UTF8', newline='') as new_file:  
    
    writer = csv.writer(new_file)
    writer.writerow(header)
    
    for line in file:

        try:
            if line[5:9] in list4:
                
                for x in range(10):
                    
                    next(file)
                
                current = file.readline()
                
                # current hour
                stn = line[5:9]
                date = current[0:8]
                hour = current[9:13]
                temp = current[65:70].replace(" ", "")
                wind = current[81:84].replace(" ", "")
                
                
                

                #1 hour forecast
                next(file) 
                current1 = file.readline()

                t1 = current1[65:70].replace(" ", "")
                w1 = current1[81:84].replace(" ", "")
                
                
                #2 hour forecast
                current2 = file.readline()

                t2 = current2[65:70].replace(" ", "")
                w2 = current2[81:84].replace(" ", "")

               
                #3 hour forecast
                current3 = file.readline()

                t3 = current3[65:70].replace(" ", "")
                w3 = current3[81:84].replace(" ", "")

                #4 hour forecast
                next(file)
                current4 = file.readline()

                t4 = current4[65:70].replace(" ", "")
                w4 = current4[81:84].replace(" ", "")

                #5 hour forecast
                current5 = file.readline()

                t5 = current5[65:70].replace(" ", "")
                w5 = current5[81:84].replace(" ", "")
                
                writer.writerow([stn, date, hour, temp, wind, first_column[count], second_column[count],
                t1, t2,t3,t4,t5,w1, w2, w3,w4,w5])
                count += 1

        except IndexError:
            for x in range(30):
                next(file)



import sys
from qgis.core import *


# Supply path to qgis install location
QgsApplication.setPrefixPath("'C:/OSGEO4~1/apps/qgis'", True)

# Create a reference to the QgsApplication.  Setting the
# second argument to False disables the GUI.
qgs = QgsApplication([], False)

# Load providers
qgs.initQgis()

sys.path.append(r'C:\OSGeo4W64\apps\qgis\python\plugins')

import processing
from processing.core.Processing import Processing
Processing.initialize()



l = weather_file

output = l.replace(".csv", ".gpkg")


# Create points layer from table
alg_params = {
    'INPUT': l,
    'MFIELD': '',
    'OUTPUT': output,
    'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:4326'),
    'XFIELD': 'X',
    'YFIELD': 'Y',
    'ZFIELD': '',
    'OUTPUT': output
}

processing.run('native:createpointslayerfromtable', alg_params)


layer=QgsVectorLayer(output)

from PyQt5.QtCore import QVariant

layer_provider=layer.dataProvider()
layer_provider.addAttributes([QgsField("T",QVariant.Double)])
layer_provider.addAttributes([QgsField("TT1",QVariant.Double)])
layer_provider.addAttributes([QgsField("TT2",QVariant.Double)])
layer_provider.addAttributes([QgsField("TT3",QVariant.Double)])
layer_provider.addAttributes([QgsField("TT4",QVariant.Double)])
layer_provider.addAttributes([QgsField("TT5",QVariant.Double)])
layer_provider.addAttributes([QgsField("W",QVariant.Double)])
layer_provider.addAttributes([QgsField("WW1",QVariant.Double)])
layer_provider.addAttributes([QgsField("WW2",QVariant.Double)])
layer_provider.addAttributes([QgsField("WW3",QVariant.Double)])
layer_provider.addAttributes([QgsField("WW4",QVariant.Double)])
layer_provider.addAttributes([QgsField("WW5",QVariant.Double)])
layer.updateFields()
print(layer.fields().names())


expression1 = QgsExpression('"TEMP"')
expression2 = QgsExpression('"WIND"')
expression3 = QgsExpression('"T1"')
expression4 = QgsExpression('"T2"')
expression5 = QgsExpression('"T3"')
expression6 = QgsExpression('"T4"')
expression7 = QgsExpression('"T5"')
expression8 = QgsExpression('"W1"')
expression9 = QgsExpression('"W2"')
expression10 = QgsExpression('"W3"')
expression11 = QgsExpression('"W4"')
expression12 = QgsExpression('"W5"')


context = QgsExpressionContext()
context.appendScopes(\
QgsExpressionContextUtils.globalProjectLayerScopes(layer))



with edit(layer):
    for f in layer.getFeatures():
        context.setFeature(f)
        f['T'] = expression1.evaluate(context)
        f['W'] = expression2.evaluate(context)
        f['TT1'] = expression3.evaluate(context)
        f['TT2'] = expression4.evaluate(context)
        f['TT3'] = expression5.evaluate(context)
        f['TT4'] = expression6.evaluate(context)
        f['TT5'] = expression7.evaluate(context)
        f['WW1'] = expression8.evaluate(context)
        f['WW2'] = expression9.evaluate(context)
        f['WW3'] = expression10.evaluate(context)
        f['WW4'] = expression11.evaluate(context)
        f['WW5'] = expression12.evaluate(context)
        layer.updateFeature(f)
    
raster_t_1 = output.replace(".gpkg", ".tif").replace("SCRIBE", "tSCRIBE")
raster_w_1 = output.replace(".gpkg", ".tif").replace("SCRIBE", "wSCRIBE")       



ontario = output


## Region 1 ##
# temp
c = 18 
for x in range(6):
    globals()[f"raster_t_1{x}"] = raster_t_1.replace('tSCRIBE',str(f'tSCRIBE1{x}'))
    processing.run("qgis:idwinterpolation", 
    {'INTERPOLATION_DATA': ontario + str(f'|layername=SCRIBE::~::0::~::{c}::~::0'),
    'DISTANCE_COEFFICIENT':4,
    'EXTENT':'-91.083442903,-81.959274672,53.134709156,56.992578945 [EPSG:4326]',
    'PIXEL_SIZE':0.04,'OUTPUT': globals()[f"raster_t_1{x}"]})
    c += 1

# wind
c = 24
for x in range(6):
    globals()[f"raster_w_1{x}"] = raster_w_1.replace('wSCRIBE',str(f'wSCRIBE1{x}'))
    processing.run("qgis:idwinterpolation", 
    {'INTERPOLATION_DATA': ontario + str(f'|layername=SCRIBE::~::0::~::{c}::~::0'),
    'DISTANCE_COEFFICIENT':4,
    'EXTENT':'-91.083442903,-81.959274672,53.134709156,56.992578945 [EPSG:4326]',
    'PIXEL_SIZE':0.04,'OUTPUT':globals()[f"raster_w_1{x}"]})
    c += 1










## Region 2 ##
c = 18
for x in range(6):
    globals()[f"raster_t_2{x}"] = raster_t_1.replace('tSCRIBE',str(f'tSCRIBE2{x}'))
    processing.run("qgis:idwinterpolation", 
    {'INTERPOLATION_DATA': ontario + str(f'|layername=SCRIBE::~::0::~::{c}::~::0'),
    'DISTANCE_COEFFICIENT':4,
    'EXTENT':'-95.338390064,-85.739642612,50.930796853,55.857522171 [EPSG:4326]',
    'PIXEL_SIZE':0.04,'OUTPUT':globals()[f"raster_t_2{x}"]})
    c += 1

c = 24
for x in range(6):
    globals()[f"raster_w_2{x}"] = raster_w_1.replace('wSCRIBE',str(f'wSCRIBE2{x}'))
    raster_w_2 = raster_w_1.replace('wSCRIBE','wSCRIBE2')
    processing.run("qgis:idwinterpolation", 
    {'INTERPOLATION_DATA': ontario + str(f'|layername=SCRIBE::~::0::~::{c}::~::0'),
    'DISTANCE_COEFFICIENT':4,
    'EXTENT':'-95.338390064,-85.739642612,50.930796853,55.857522171 [EPSG:4326]',
    'PIXEL_SIZE':0.04,'OUTPUT':globals()[f"raster_w_2{x}"]})
    c += 1


# Region 3
c = 18
for x in range(6):
    globals()[f"raster_t_3{x}"] = raster_t_1.replace('tSCRIBE',str(f'tSCRIBE3{x}'))
    processing.run("qgis:idwinterpolation", 
    {'INTERPOLATION_DATA': ontario + str(f'|layername=SCRIBE::~::0::~::{c}::~::0'),
    'DISTANCE_COEFFICIENT':4,
    'EXTENT':'-86.895472648,-79.252450854,49.434341409,54.436559479 [EPSG:4326]',
    'PIXEL_SIZE':0.04,'OUTPUT':globals()[f"raster_t_3{x}"]})
    c += 1

c = 24
for x in range(6):
    globals()[f"raster_w_3{x}"] = raster_w_1.replace('wSCRIBE',str(f'wSCRIBE3{x}'))
    processing.run("qgis:idwinterpolation", 
    {'INTERPOLATION_DATA': ontario + str(f'|layername=SCRIBE::~::0::~::{c}::~::0'),
    'DISTANCE_COEFFICIENT':4,
    'EXTENT':'-86.895472648,-79.252450854,49.434341409,54.436559479 [EPSG:4326]',
    'PIXEL_SIZE':0.04,'OUTPUT':globals()[f"raster_w_3{x}"]})
    c += 1

# Region 4
c = 18
for x in range(6):
    globals()[f"raster_t_4{x}"] = raster_t_1.replace('tSCRIBE',str(f'tSCRIBE4{x}'))
    processing.run("qgis:idwinterpolation", 
    {'INTERPOLATION_DATA': ontario + str(f'|layername=SCRIBE::~::0::~::{c}::~::0'),
    'DISTANCE_COEFFICIENT':4,
    'EXTENT':'-95.648397458,-79.152942308,47.551333535,53.072828043 [EPSG:4326]',
    'PIXEL_SIZE':0.04,'OUTPUT':globals()[f"raster_t_4{x}"]})
    c += 1

c = 24
for x in range(6):
    globals()[f"raster_w_4{x}"] = raster_w_1.replace('wSCRIBE',str(f'wSCRIBE4{x}'))
    processing.run("qgis:idwinterpolation", 
    {'INTERPOLATION_DATA': ontario + str(f'|layername=SCRIBE::~::0::~::{c}::~::0'),
    'DISTANCE_COEFFICIENT':4,
    'EXTENT':'-95.648397458,-79.152942308,47.551333535,53.072828043 [EPSG:4326]',
    'PIXEL_SIZE':0.04,'OUTPUT':globals()[f"raster_w_4{x}"]})
    c += 1

# Region 5
c = 18
for x in range(6):
    globals()[f"raster_t_5{x}"] = raster_t_1.replace('tSCRIBE',str(f'tSCRIBE5{x}'))
    processing.run("qgis:idwinterpolation", 
    {'INTERPOLATION_DATA': ontario + str(f'|layername=SCRIBE::~::0::~::{c}::~::0'),
    'DISTANCE_COEFFICIENT':4,
    'EXTENT':'-95.639946532,-88.307728553,47.761832383,51.846859520 [EPSG:4326]',
    'PIXEL_SIZE':0.04,'OUTPUT':globals()[f"raster_t_5{x}"]})
    c += 1

c = 24
for x in range(6):
    globals()[f"raster_w_5{x}"] = raster_w_1.replace('wSCRIBE',str(f'wSCRIBE5{x}'))
    processing.run("qgis:idwinterpolation", 
    {'INTERPOLATION_DATA': ontario + str(f'|layername=SCRIBE::~::0::~::{c}::~::0'),
    'DISTANCE_COEFFICIENT':4,
    'EXTENT':'-95.639946532,-88.307728553,47.761832383,51.846859520 [EPSG:4326]',
    'PIXEL_SIZE':0.04,'OUTPUT':globals()[f"raster_w_5{x}"]})
    c += 1

# Region 6
c = 18
for x in range(6):
    globals()[f"raster_t_6{x}"] = raster_t_1.replace('tSCRIBE',str(f'tSCRIBE6{x}'))
    processing.run("qgis:idwinterpolation", 
    {'INTERPOLATION_DATA': ontario + str(f'|layername=SCRIBE::~::0::~::{c}::~::0'),
    'DISTANCE_COEFFICIENT':4,
    'EXTENT':'-85.945333102,-79.007506740,47.164781106,49.084075150 [EPSG:4326]',
    'PIXEL_SIZE':0.04,'OUTPUT':globals()[f"raster_t_6{x}"]})
    c += 1

c = 24
for x in range(6):
    globals()[f"raster_w_6{x}"] = raster_w_1.replace('wSCRIBE',str(f'wSCRIBE6{x}'))
    processing.run("qgis:idwinterpolation", 
    {'INTERPOLATION_DATA': ontario + str(f'|layername=SCRIBE::~::0::~::{c}::~::0'),
    'DISTANCE_COEFFICIENT':4,
    'EXTENT':'-85.945333102,-79.007506740,47.164781106,49.084075150 [EPSG:4326]',
    'PIXEL_SIZE':0.04,'OUTPUT':globals()[f"raster_w_6{x}"]})
    c += 1

# Region 7
c = 18
for x in range(6):
    globals()[f"raster_t_7{x}"] = raster_t_1.replace('tSCRIBE',str(f'tSCRIBE7{x}'))
    processing.run("qgis:idwinterpolation", 
    {'INTERPOLATION_DATA': ontario + str(f'|layername=SCRIBE::~::0::~::{c}::~::0'),
    'DISTANCE_COEFFICIENT':4,
    'EXTENT':'-85.258684639,-76.387115025,44.705771841,47.271944156 [EPSG:4326]',
    'PIXEL_SIZE':0.04,'OUTPUT':globals()[f"raster_t_7{x}"]})
    c += 1

c = 24
for x in range(6):
    globals()[f"raster_w_7{x}"] = raster_w_1.replace('wSCRIBE',str(f'wSCRIBE7{x}'))
    processing.run("qgis:idwinterpolation", 
    {'INTERPOLATION_DATA': ontario + str(f'|layername=SCRIBE::~::0::~::{c}::~::0'),
    'DISTANCE_COEFFICIENT':4,
    'EXTENT':'-85.258684639,-76.387115025,44.705771841,47.271944156 [EPSG:4326]',
    'PIXEL_SIZE':0.04,'OUTPUT':globals()[f"raster_w_7{x}"]})
    c += 1

# Region 8
c = 18
for x in range(6):
    globals()[f"raster_t_8{x}"] = raster_t_1.replace('tSCRIBE',str(f'tSCRIBE8{x}'))
    processing.run("qgis:idwinterpolation", 
    {'INTERPOLATION_DATA': ontario + str(f'|layername=SCRIBE::~::0::~::{c}::~::0'),
    'DISTANCE_COEFFICIENT':4,
    'EXTENT':'-81.871781098,-73.708038782,43.255243418,46.225190795 [EPSG:4326]',
    'PIXEL_SIZE':0.04,'OUTPUT':globals()[f"raster_t_8{x}"]})
    c += 1

c = 24
for x in range(6):
    globals()[f"raster_w_8{x}"] = raster_w_1.replace('wSCRIBE',str(f'wSCRIBE8{x}'))
    processing.run("qgis:idwinterpolation", 
    {'INTERPOLATION_DATA': ontario + str(f'|layername=SCRIBE::~::0::~::{c}::~::0'),
    'DISTANCE_COEFFICIENT':4,
    'EXTENT':'-81.871781098,-73.708038782,43.255243418,46.225190795 [EPSG:4326]',
    'PIXEL_SIZE':0.04,'OUTPUT':globals()[f"raster_w_8{x}"]})
    c += 1

# Region 9
c = 18
for x in range(6):
    globals()[f"raster_t_9{x}"] = raster_t_1.replace('tSCRIBE',str(f'tSCRIBE9{x}'))
    processing.run("qgis:idwinterpolation", 
    {'INTERPOLATION_DATA': ontario + str(f'|layername=SCRIBE::~::0::~::{c}::~::0'),
    'DISTANCE_COEFFICIENT':4,
    'EXTENT':'-83.218759443,-78.792542765,41.611438781,43.409489556 [EPSG:4326]',
    'PIXEL_SIZE':0.04,'OUTPUT':globals()[f"raster_t_9{x}"]})
    c += 1

c = 24
for x in range(6):
    globals()[f"raster_w_9{x}"] = raster_w_1.replace('wSCRIBE',str(f'wSCRIBE9{x}'))
    processing.run("qgis:idwinterpolation", 
    {'INTERPOLATION_DATA': ontario + str(f'|layername=SCRIBE::~::0::~::{c}::~::0'),
    'DISTANCE_COEFFICIENT':4,
    'EXTENT':'-83.218759443,-78.792542765,41.611438781,43.409489556 [EPSG:4326]',
    'PIXEL_SIZE':0.04,'OUTPUT':globals()[f"raster_w_9{x}"]})
    c += 1



# Temp Merge
# Current
t_merge0 = 'main\\t_merge0.tif'

processing.run("gdal:merge", 
{'INPUT':[raster_t_10,
raster_t_20,
raster_t_30,
raster_t_40,
raster_t_50,
raster_t_60,
raster_t_70,
raster_t_80,
raster_t_90],
'PCT':False,'SEPARATE':False,'NODATA_INPUT':None,'NODATA_OUTPUT':None,'OPTIONS':'','EXTRA':'',
'DATA_TYPE':5,'OUTPUT':t_merge0})

t_merge1 = 'main\\t_merge1.tif'

processing.run("gdal:merge", 
{'INPUT':[raster_t_11,
raster_t_21,
raster_t_31,
raster_t_41,
raster_t_51,
raster_t_61,
raster_t_71,
raster_t_81,
raster_t_91],
'PCT':False,'SEPARATE':False,'NODATA_INPUT':None,'NODATA_OUTPUT':None,'OPTIONS':'','EXTRA':'',
'DATA_TYPE':5,'OUTPUT':t_merge1})

t_merge2 = 'main\\t_merge2.tif'

processing.run("gdal:merge", 
{'INPUT':[raster_t_12,
raster_t_22,
raster_t_32,
raster_t_42,
raster_t_52,
raster_t_62,
raster_t_72,
raster_t_82,
raster_t_92],
'PCT':False,'SEPARATE':False,'NODATA_INPUT':None,'NODATA_OUTPUT':None,'OPTIONS':'','EXTRA':'',
'DATA_TYPE':5,'OUTPUT':t_merge2})

t_merge3 = 'main\\t_merge3.tif'

processing.run("gdal:merge", 
{'INPUT':[raster_t_13,
raster_t_23,
raster_t_33,
raster_t_43,
raster_t_53,
raster_t_63,
raster_t_73,
raster_t_83,
raster_t_93],
'PCT':False,'SEPARATE':False,'NODATA_INPUT':None,'NODATA_OUTPUT':None,'OPTIONS':'','EXTRA':'',
'DATA_TYPE':5,'OUTPUT':t_merge3})

t_merge4 = 'main\\t_merge4.tif'

processing.run("gdal:merge", 
{'INPUT':[raster_t_14,
raster_t_24,
raster_t_34,
raster_t_44,
raster_t_54,
raster_t_64,
raster_t_74,
raster_t_84,
raster_t_94],
'PCT':False,'SEPARATE':False,'NODATA_INPUT':None,'NODATA_OUTPUT':None,'OPTIONS':'','EXTRA':'',
'DATA_TYPE':5,'OUTPUT':t_merge4})

t_merge5 = 'main\\t_merge5.tif'

processing.run("gdal:merge", 
{'INPUT':[raster_t_15,
raster_t_25,
raster_t_35,
raster_t_45,
raster_t_55,
raster_t_65,
raster_t_75,
raster_t_85,
raster_t_95],
'PCT':False,'SEPARATE':False,'NODATA_INPUT':None,'NODATA_OUTPUT':None,'OPTIONS':'','EXTRA':'',
'DATA_TYPE':5,'OUTPUT':t_merge5})









# Wind Merge

w_merge0 = 'main\w_merge0.tif'

processing.run("gdal:merge", 
{'INPUT':[raster_w_10,
raster_w_20,
raster_w_30,
raster_w_40,
raster_w_50,
raster_w_60,
raster_w_70,
raster_w_80,
raster_w_90],
'PCT':False,'SEPARATE':False,'NODATA_INPUT':None,'NODATA_OUTPUT':None,'OPTIONS':'','EXTRA':'',
'DATA_TYPE':5,'OUTPUT':w_merge0})

w_merge1 = 'main\w_merge1.tif'

processing.run("gdal:merge", 
{'INPUT':[raster_w_11,
raster_w_21,
raster_w_31,
raster_w_41,
raster_w_51,
raster_w_61,
raster_w_71,
raster_w_81,
raster_w_91],
'PCT':False,'SEPARATE':False,'NODATA_INPUT':None,'NODATA_OUTPUT':None,'OPTIONS':'','EXTRA':'',
'DATA_TYPE':5,'OUTPUT':w_merge1})

w_merge2 = 'main\w_merge2.tif'

processing.run("gdal:merge", 
{'INPUT':[raster_w_12,
raster_w_22,
raster_w_32,
raster_w_42,
raster_w_52,
raster_w_62,
raster_w_72,
raster_w_82,
raster_w_92],
'PCT':False,'SEPARATE':False,'NODATA_INPUT':None,'NODATA_OUTPUT':None,'OPTIONS':'','EXTRA':'',
'DATA_TYPE':5,'OUTPUT':w_merge2})

w_merge3 = 'main\w_merge3.tif'

processing.run("gdal:merge", 
{'INPUT':[raster_w_13,
raster_w_23,
raster_w_33,
raster_w_43,
raster_w_53,
raster_w_63,
raster_w_73,
raster_w_83,
raster_w_93],
'PCT':False,'SEPARATE':False,'NODATA_INPUT':None,'NODATA_OUTPUT':None,'OPTIONS':'','EXTRA':'',
'DATA_TYPE':5,'OUTPUT':w_merge3})


w_merge4 = 'main\w_merge4.tif'

processing.run("gdal:merge", 
{'INPUT':[raster_w_14,
raster_w_24,
raster_w_34,
raster_w_44,
raster_w_54,
raster_w_64,
raster_w_74,
raster_w_84,
raster_w_94],
'PCT':False,'SEPARATE':False,'NODATA_INPUT':None,'NODATA_OUTPUT':None,'OPTIONS':'','EXTRA':'',
'DATA_TYPE':5,'OUTPUT':w_merge4})

w_merge5 = 'main\w_merge5.tif'

processing.run("gdal:merge", 
{'INPUT':[raster_w_15,
raster_w_25,
raster_w_35,
raster_w_45,
raster_w_55,
raster_w_65,
raster_w_75,
raster_w_85,
raster_w_95],
'PCT':False,'SEPARATE':False,'NODATA_INPUT':None,'NODATA_OUTPUT':None,'OPTIONS':'','EXTRA':'',
'DATA_TYPE':5,'OUTPUT':w_merge5})











# raster sample one
name_Table = name_Table.replace('"', '')


#t1
sample_output1 = str("main\i"+ name_Table + ".gpkg")

sample_param1 = {'INPUT':'ref_layers\grid_join.gpkg',
'RASTERCOPY':t_merge0,
'COLUMN_PREFIX':'t0','OUTPUT':sample_output1}

processing.run("native:rastersampling", sample_param1)

#t2
sample_output2 = str("main\ii"+ name_Table + ".gpkg")
processing.run("native:rastersampling", {'INPUT':sample_output1,
'RASTERCOPY':t_merge1,
'COLUMN_PREFIX':'t1','OUTPUT':sample_output2})

#t3
sample_output3 = str("main\iii"+ name_Table + ".gpkg")
processing.run("native:rastersampling", {'INPUT':sample_output2,
'RASTERCOPY':t_merge2,
'COLUMN_PREFIX':'t2','OUTPUT':sample_output3})

#t4
sample_output4 = str("main\iiii"+ name_Table + ".gpkg")
processing.run("native:rastersampling", {'INPUT':sample_output3,
'RASTERCOPY':t_merge3,
'COLUMN_PREFIX':'t3','OUTPUT':sample_output4})

#t5
sample_output5 = str("main\iiiii"+ name_Table + ".gpkg")
processing.run("native:rastersampling", {'INPUT':sample_output4,
'RASTERCOPY':t_merge4,
'COLUMN_PREFIX':'t4','OUTPUT':sample_output5})

#t6
sample_output6 = str("main\iiiiii"+ name_Table + ".gpkg")
processing.run("native:rastersampling", {'INPUT':sample_output5,
'RASTERCOPY':t_merge5,
'COLUMN_PREFIX':'t5','OUTPUT':sample_output6})

#w0
sample_output7 = str("main\iiiiiiw"+ name_Table + ".gpkg")
processing.run("native:rastersampling", {'INPUT':sample_output6,
'RASTERCOPY':w_merge0,
'COLUMN_PREFIX':'w0','OUTPUT':sample_output7})

#w1
sample_output8 = str("main\iiiiiiww"+ name_Table + ".gpkg")
processing.run("native:rastersampling", {'INPUT':sample_output7,
'RASTERCOPY':w_merge1,
'COLUMN_PREFIX':'w1','OUTPUT':sample_output8})

#w2
sample_output9 = str("main\iiiiiiwww"+ name_Table + ".gpkg")
processing.run("native:rastersampling", {'INPUT':sample_output8,
'RASTERCOPY':w_merge2,
'COLUMN_PREFIX':'w2','OUTPUT':sample_output9})

#w3
sample_output10 = str("main\iiiiiiwwww"+ name_Table + ".gpkg")
processing.run("native:rastersampling", {'INPUT':sample_output9,
'RASTERCOPY':w_merge3,
'COLUMN_PREFIX':'w3','OUTPUT':sample_output10})

#w4
sample_output11 = str("main\iiiiiiwwwww"+ name_Table + ".gpkg")
processing.run("native:rastersampling", {'INPUT':sample_output10,
'RASTERCOPY':w_merge4,
'COLUMN_PREFIX':'w4','OUTPUT':sample_output11})

#w5
sample_output12 = str("main\iiiiiiwwwwww"+ name_Table + ".gpkg")
processing.run("native:rastersampling", {'INPUT':sample_output11,
'RASTERCOPY':w_merge5,
'COLUMN_PREFIX':'w5','OUTPUT':sample_output12})




# vector split into geojson files for the website
processing.run("native:splitvectorlayer", 
{'INPUT': sample_output12,
'FIELD':'grid_tilename','FILE_TYPE':8,
'OUTPUT':'C:\Apache24\htdocs\documents'})



# tile_layer=QgsVectorLayer("results\grid3_clip.gpkg")

# point_layer = QgsVectorLayer("results\sampled_points\samplePP_test.gpkg")






qgs.exitQgis()



print("--- %s seconds ---" % (time.time() - start_time))