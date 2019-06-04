#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 25/05/2019 21:13
# @Author: Yangyang Li
# @File  : toXML.py

# -*- coding: utf-8 -*- trabajo_xml
import pandas as pd
import xml.dom.minidom
import pymysql
import numpy as np
import os

# connect to database
connection = pymysql.connect(
    host='localhost',
    user='root',
    passwd="yangyang9099",
    db='proyectoBD',
    port=3306)

curs = connection.cursor()
curs.execute("select * from paciente limit 30;")
result = curs.fetchall()
pacientes = list(result)

curs.execute(
    "select COLUMN_NAME from information_schema.COLUMNS where table_name = 'paciente' and table_schema ='proyectoBD';")
columns = curs.fetchall()
attributes = list(columns)

doc = xml.dom.minidom.Document()
root = doc.createElement('pacientes')
doc.appendChild(root)
row = 0

while (row < len(pacientes)):
    paciente = doc.createElement("paciente")
    root.appendChild(paciente)
    col = 0
    enf_index = 0
    curs.execute("select Enfermedades_Raras_IdENFERM from paciente_has_enfermedades_raras where PACIENTE_DNI = '" +
                 pacientes[row][0] + "' limit 1;")
    enfer_id = curs.fetchall()
    curs.execute("select * from enfermedades_raras where IdENFERM = '" + str(enfer_id[col]).split("'")[1] + "';")
    enfer_info = curs.fetchall()

    curs.execute("SELECT * FROM enfermedades_raras_has_tratamiento where Enfermedades_Raras_IdENFERM = '"+ \
                 str(enfer_id[col]).split("'")[1] +"' limit 1;")
    tratm_info = curs.fetchall()

    # add pacients' attributes
    while (col < len(attributes)):
        attribute = str(attributes[col]).split("'")[1]
        att = doc.createElement(attribute)
        paciente.appendChild(att)
        text = pacientes[row][col]
        att.appendChild(doc.createTextNode(str(text)))
        col = col + 1

    # add enfermedad info
    while (enf_index < len(enfer_info)):
        enf = doc.createElement("enfermedad")
        paciente.appendChild(enf)
        text = enfer_info[enf_index]
        IdENFERM = doc.createElement("IdENFERM")
        IdENFERM.appendChild(doc.createTextNode(text[0]))
        DESCRIPCION = doc.createElement("DESCRIPCION")
        DESCRIPCION.appendChild(doc.createTextNode(text[1]))
        NOMBRE = doc.createElement("NOMBRE")
        NOMBRE.appendChild(doc.createTextNode(text[2]))
    #add pacient info
        enf.appendChild(IdENFERM)
        enf.appendChild(DESCRIPCION)
        enf.appendChild(NOMBRE)

    #add gen info
        curs.execute("select * from gen where idGEN = '"+str(text[3])+"';")
        gen_info = curs.fetchall()
        idGEN = doc.createElement("idGEN")
        idGEN.appendChild(doc.createTextNode(str(gen_info[0][0])))
        gen_NOMBRE = doc.createElement("NOMBRE")
        gen_NOMBRE.appendChild(doc.createTextNode(str(gen_info[0][1])))
        location = doc.createElement("LOCALIZAICION")
        location.appendChild(doc.createTextNode(str(gen_info[0][2])))
        gen = doc.createElement("GEN")
        gen.appendChild(idGEN)
        gen.appendChild(gen_NOMBRE)
        gen.appendChild(location)
        enf.appendChild(gen)
    #add protein info
        curs.execute("select * from proteina where GEN_idGEN = '"+str(text[3])+"';")
        protein_info = curs.fetchall()
        for p in protein_info:
            if(p[3] == text[3]):
                protein = doc.createElement("proteina")
                protein_id = doc.createElement("idPROTEINA")
                protein_id.appendChild(doc.createTextNode(str(p[0])))
                protein.appendChild(protein_id)
                protein_name = doc.createElement("NOMBRE")
                protein_name.appendChild(doc.createTextNode(str(p[1])))
                protein.appendChild(protein_name)
                protein_struc = doc.createElement("ESTRUCTURA")
                protein_struc.appendChild(doc.createTextNode(str(p[2])))
                protein.appendChild(protein_struc)
                gen.appendChild(protein)

    # add tratamiento info
        tratamiento = doc.createElement("tratamiento")
        for t in tratm_info:

            if(t[0] == text[0]):
                curs.execute("select * from tratamiento where idTRATAMIENTO = '"
                             +str(t[2]) + "';")
                tratm_name_descp = curs.fetchall()
                tratam_id = doc.createElement("idTRATAMIENTO")
                tratam_id.appendChild(doc.createTextNode(str(tratm_name_descp[0][0])))
                tratam_name = doc.createElement("NOMBRE")
                tratam_name.appendChild(doc.createTextNode(tratm_name_descp[0][1]))
                tratam_descp = doc.createElement("DESCRIPCION")
                tratam_descp.appendChild(doc.createTextNode(tratm_name_descp[0][2]))
                tratamiento.appendChild(tratam_id)
                tratamiento.appendChild(tratam_name)
                tratamiento.appendChild(tratam_descp)
                enf.appendChild(tratamiento)


        enf_index = enf_index + 1

    row += 1

f = open('/Users/yangyangli/Desktop/Ingenieria/bdBiologico/generaXML/bd_xml.xml', 'w')
doc.writexml(f, indent='\t', addindent='\t', newl='\n')
f.close()
connection.close()
