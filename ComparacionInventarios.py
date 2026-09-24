import pandas as pd
import numpy as np
import openpyxl
import os
from pathlib import Path
from openpyxl.utils.dataframe import dataframe_to_rows
import streamlit as st

st.title("Comparacion de Inventarios", text_alignment="center")

st.header("Archvios necesarios para el procesamiento:")
inventario_plataforma = st.file_uploader("Seleccionar Inventario de la Plataforma:", type=["xlsx","xls"])
inventario_sae = st.file_uploader("Seleccionar Inventario de SAE:", type=["xlsx","xls"])
#bases = st.file_uploader("Seleccionar Carpeta con los Inventarios de las Bases:", type=["xlsx","xls"], accept_multiple_files="directory")

numero_de_bases = st.number_input("Cuantas bases se encuentran activas?", min_value=1, max_value=10)
dictio_bases = {}
for i in range(numero_de_bases):
    base = st.file_uploader(f"Seleccionar Inventario de la Base {i+1}:", type=["xlsx","xls"], key=f"Base_{i}")
    dictio_bases[base.name.split(".")[0]] = base
    while base not None:
        st.header(base.name.split(".")[0])
