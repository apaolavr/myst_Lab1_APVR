
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: LAB 1 INVERSION PASIVA Y ACTIVA                                                          -- #
# -- script: data.py : python script for data collection                                                 -- #
# -- author: apaolavr                                                                      -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: https://github.com/apaolavr/myst_Lab1_APVR                                                                   -- #
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

#pos_datos['timestamp'] = ic_fechas[0]


def data_pasiva(inv_pasiva):

    df_pasiva = pd.DataFrame()
    df_pasiva['Capital'] = inv_pasiva['Capital']
    df_pasiva['timestamp'] = inv_pasiva['timestamp']
    df_pasiva['rend'] = 0
    df_pasiva['rend_acum'] = 0

    # Calculo de rendimientos
    # rend log = ( i - (i-1))/(i-1))
    for i in range(1, len(df_pasiva)):
        df_pasiva.loc[i, 'rend'] = (df_pasiva.loc[i, 'Capital'] - df_pasiva.loc[i - 1, 'Capital']) / df_pasiva.loc[i - 1, 'Capital']
        df_pasiva.loc[i, 'rend_acum'] = df_pasiva.loc[i, 'rend'] + df_pasiva.loc[i - 1, 'rend_acum']

    return df_pasiva




