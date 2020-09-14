
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: LAB 1 INVERSION PASIVA Y ACTIVA                                                          -- #
# -- script: data.py : python script for data collection                                                 -- #
# -- author: apaolavr                                                                      -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: https://github.com/apaolavr/myst_Lab1_APVR                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

import time
import numpy as np
import pandas as pd
import yfinance as yf
import math

from os import listdir, path
from os.path import isfile, join
from datetime import datetime
from datetime import timedelta


def f_archivo(abspath):
    archivos = [f[:-4] for f in listdir(abspath) if isfile(join(abspath, f))]
    archivos = sorted(archivos, key=lambda t: datetime.strptime(t[8:], '%d%m%y'))

    return archivos


# ----------------------------

# DICC de archivos (base que tenia en data antes )

def f_data_archivos_dicc(archivos):

    data_archivos = {}

    for i in archivos:
        # leer archivos despues de los primeros dos renglones
        data = pd.read_csv('files/NAFTRAC_holdings/' + i + '.csv', skiprows=2, header=None)
        # renombrar las columnas con lo que tiene el 1er renglon
        data.columns = list(data.iloc[0, :])
        # quitar columnas que no sean nan
        data = data.loc[:, pd.notnull(data.columns)]
        # resetear el indice
        data = data.iloc[1:-1].reset_index(drop=True, inplace=False)
        # quitar las comas en la columna de precios
        data['Precio'] = [i.replace(',', '') for i in data['Precio']]
        # quitar el asterisco de columna ticker
        data['Ticker'] = [i.replace('*', '') for i in data['Ticker']]
        # hacer conversiones de tipos de columnas a numerico
        convert_dict = {'Ticker': str, 'Nombre': str, 'Peso (%)': float, 'Precio': float}
        data = data.astype(convert_dict)
        # convertir a decimal la columna de peso (%)
        data['Peso (%)'] = data['Peso (%)'] / 100
        # guardar en diccionario
        data_archivos[i] = data

    return data_archivos