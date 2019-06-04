#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 25/05/2019 21:13
# @Author: Yangyang Li
# @File  : toXML.py

# -*- coding: utf-8 -*- trabajo_xml
import pandas as pd
import xml.dom.minidom
import pymysql
import os

# connect to database
connection = pymysql.connect(
    host='localhost',
    user='root',
    passwd="yangyang9099",
    db='proyectoBD',
    port=3306)

# get all table names
curs = connection.cursor()
curs.execute("select TABLE_NAME from information_schema.tables where TABLE_SCHEMA='proyectoBD';")
result = curs.fetchall()
result = list(result)
# transformar a xml

doc = xml.dom.minidom.Document()
root = doc.createElement('root')
doc.appendChild(root)

for table in result:
    table = str(table).split(",")[0]
    table_name = table[2:len(table) - 1]
    tables = doc.createElement(table_name)
    root.appendChild(tables)

    curs.execute("select * from " + table_name + " limit 30;")
    table_content = curs.fetchall()
    table_content = list(table_content)
    curs.execute("select COLUMN_NAME from information_schema.COLUMNS where table_name = "\
                 +"'" +table_name+"' and table_schema ='proyectoBD';")
    columns = curs.fetchall()
    attributes = list(columns)
    row = 0



    while (row < len(table_content)):
        element = doc.createElement("Element")
        tables.appendChild(element)
        col = 0

        while (col < len(attributes)):

            attribute = str(attributes[col]).split("'")[1]
            att = doc.createElement(attribute)
            element.appendChild(att)
            text = table_content[row][col]
            att.appendChild(doc.createTextNode(str(text)))
            col = col + 1
        row += 1


f = open('/Users/yangyangli/Desktop/Ingenieria/bdBiologico/generaXML/bd_xml.xml','w')
doc.writexml(f, indent='\t', addindent='\t', newl='\n')
f.close()
connection.close()

