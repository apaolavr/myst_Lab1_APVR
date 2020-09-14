
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: LAB 1 INVERSION PASIVA Y ACTIVA                                                          -- #
# -- script: data.py : python script for data collection                                                 -- #
# -- author: apaolavr                                                                      -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: https://github.com/apaolavr/myst_Lab1_APVR
# -- --------------------------------------------------------------------------------------------------- -- #
"""
#Procesos

import numpy as np
import data as dt
import functions as fn
import visualizations as vs
import pandas as pd
from os import listdir, path
from os.path import isfile, join

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.expand_frame_repr', False)

# ----------------------------

#Archivos a leer
#Se tiene el path desde archivos para jalar los datos

abspath = path.abspath('files/NAFTRAC_holdings')

archivos = dt.f_archivo(abspath)

data_archivos = dt.f_data_archivos_dicc(archivos)
# me traigo las fechas

i_fechas= fn.f_fechas(archivos)

global_tickers = fn.f_tickers(archivos,data_archivos)

global_tickers = fn.f_new_tickers(global_tickers)

data = fn.f_data(global_tickers)

data_close = fn.f_data_close(data,global_tickers)

ic_fechas = fn.f_icfechas(data_close,i_fechas)

precios = fn.f_precios(data_close,ic_fechas)


#_________________
#inversion pasiva

# capital inicial
k = 1000000
# comisiones por transaccion
c = 0.00125

remv_activos = ['KOFL','KOFUBL', 'BSMXB', 'MXN', 'USD']

inv_pasiva = {'timestamp': ['2018-01-30'], 'Capital': [k]}

# ----------------------------

pos_datos = fn.f_p_i(remv_activos,data_archivos,archivos,precios,k,c)

# ----------------------------

#Inversion total o cash
cash=k-pos_datos['Postura'].sum()-pos_datos['Comision'].sum()
cash=np.round(cash)

# ----------------------------

inv_pasiva = {'timestamp': ['2018-01-30'], 'Capital': [k]}

inv_pasiva =fn.f_pasiva(ic_fechas,pos_datos,precios,cash,inv_pasiva)
# ----------------------------

df_pasiva=vs.f_pasiva(inv_pasiva)
# ----------------------------

