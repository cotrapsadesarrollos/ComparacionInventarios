import pandas as pd
import numpy as np
import openpyxl
import os
from pathlib import Path
from openpyxl.utils.dataframe import dataframe_to_rows
import streamlit as st

#Diccionario de nombres de Bases para cambiar los nombres de los archivos a los nombres de los almacenes en el inventario de la plataforma
dictio_nombres_bases = {"BARCEL TOLUCA":"Barcel Lerma" , "BIMBO TOLUCA":"Bimbo Toluca" , "BARCEL ACAYUCAN":"Barcel Acayucan" , "BIMBO SAN LUIS POTOSI":"Bimbo San Luis Potosí"}

st.title("Comparacion de Inventarios", text_alignment="center")

st.divider()
st.header("Archvios necesarios para el procesamiento:")
inventario_plataforma = st.file_uploader("Seleccionar Inventario de la Plataforma:", type=["xlsx","xls"])
inventario_sae = st.file_uploader("Seleccionar Inventario de SAE:", type=["xlsx","xls"])
#bases = st.file_uploader("Seleccionar Carpeta con los Inventarios de las Bases:", type=["xlsx","xls"], accept_multiple_files="directory")

st.divider()
st.subheader("Archvios de Inventarios realizados en las Bases:")
numero_de_bases = st.number_input("Cuantas bases se encuentran activas?", min_value=1, max_value=10)
dictio_bases = {}
for i in range(numero_de_bases):
    base = st.file_uploader(f"Seleccionar Inventario de la Base {i+1}:", type=["xlsx","xls"], key=f"Base_{i}")
    if base is not None:
        dictio_bases[dictio_nombres_bases[base.name.split(".")[0]]] = pd.read_excel(base)
        st.write(f"Inventario de {base.name.split(".")[0]} subido correctamente")
        base = None

st.divider()
if inventario_plataforma is not None and inventario_sae is not None and len(dictio_bases.keys())==numero_de_bases:
    # Leer el archivo Excel del inventario de la plataforma e Inventario SAE
    df_inventario_plataforma = pd.read_excel(inventario_plataforma)
    df_inventario_sae = pd.read_excel(inventario_sae)

    st.write("### Inventario de la plataforma")
    st.dataframe(df_inventario_plataforma)

    st.write("### Inventario SAE")
    st.dataframe(df_inventario_sae)

    for i in dictio_bases.keys():
        st.write(f"### Inventario {i}")
        st.dataframe(dictio_bases[i])

    # Procesamiento para realizar la comparacion de Inventarios Reales vs Plataformna
    if st.button("Comparacion de inventarios"):
        #Quitamos los Numeros de parte de servicios
        df_inventario_plataforma = df_inventario_plataforma[~df_inventario_plataforma['NUMERO DE PARTE'].isin(['001','002','003','004','009','010','012','013','015','016','018'])].reset_index(drop=True).copy()
        
        #Creamos un diccionario con el inventario real de cada Base
        inventarios_plataforma={}
        for i in dictio_bases.keys():
            #inventarios_reales[i] = dict(zip(dictio_bases[i]['NO. DE PARTE '], dictio_bases[i]['INVENTARIO']))
            df_inventario_plataforma_filtrado = df_inventario_plataforma[df_inventario_plataforma['ALMACEN']==i].copy()
            inventarios_plataforma[i] = dict(zip([str(x) for x in df_inventario_plataforma_filtrado['NUMERO DE PARTE']], df_inventario_plataforma_filtrado["EXISTENCIA"]))
            inventarios_plataforma[i][None] = [None]
            dictio_bases[i]["INVENTARIO PLATAFORMA"] = [inventarios_plataforma[i][x] for x in dictio_bases[i]['NO. DE PARTE ']]

            st.write(f"### Inventario {i}")
            st.dataframe(dictio_bases[i])







