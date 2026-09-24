import pandas as pd
import numpy as np
import openpyxl
import os
from pathlib import Path
from openpyxl.utils.dataframe import dataframe_to_rows
import streamlit as st

st.title("Comparacion de Inventarios", text_alignment="center")

st.divider()
st.header("Archvios necesarios para el procesamiento:")
inventario_plataforma = st.file_uploader("Seleccionar Inventario de la Plataforma:", type=["xlsx","xls"])
inventario_sae = st.file_uploader("Seleccionar Inventario de SAE:", type=["xlsx","xls"])
#bases = st.file_uploader("Seleccionar Carpeta con los Inventarios de las Bases:", type=["xlsx","xls"], accept_multiple_files="directory")

st.divider()
st.header("Archvios de Inventarios realizados en las Bases:")
numero_de_bases = st.number_input("Cuantas bases se encuentran activas?", min_value=1, max_value=10)
dictio_bases = {}
for i in range(numero_de_bases):
    base = st.file_uploader(f"Seleccionar Inventario de la Base {i+1}:", type=["xlsx","xls"], key=f"Base_{i}")
    if base is not None:
        dictio_bases[base.name.split(".")[0]] = pd.read_excel(base)
        st.write(f"Inventario de {base.name.split(".")[0]} subido correctamente")
        base = None

st.divider()
if inventario_plataforma is not None and inventario_sae is not None and len(dictio_bases.keys)==numero_de_bases:
    # Leer el archivo Excel del inventario de la plataforma e Inventario SAE
    df_inventario_plataforma = pd.read_excel(inventario_plataforma)
    df_inventario_sae = pd.read_excel(inventario_sae)

    st.write("### Inventario de la plataforma")
    st.dataframe(df_inventario_plataforma)

    st.write("### Inventario SAE")
    st.dataframe(df_inventario_sae)
