# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: LAB 1 INVERSION PASIVA Y ACTIVA                                                          -- #
# -- script: data.py : python script for data collection                                                 -- #
# -- author: apaolavr                                                                      -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: https://github.com/apaolavr/myst_Lab1_APVR
# -- --------------------------------------------------------------------------------------------------- -- #

import time
import numpy as np
import pandas as pd
import yfinance as yf
import math

from os import listdir, path
from os.path import isfile, join
from datetime import datetime
from datetime import timedelta

# ---------------------------
# Vector de fechas
#funciones para jalar las fechas de i_fechas y las ic_fechas

def f_fechas(archivos):
    i_fechas = [j.strftime('%Y-%m-%d') for j in sorted([pd.to_datetime(i[8:]).date() for i in archivos])]

    return i_fechas

def f_icfechas(data_close,i_fechas):

    # Fechas de interes
    ic_fechas = sorted(list(set(data_close.index.astype(str).tolist()) & set(i_fechas)))

    return ic_fechas

# ----------------------------
# Vector de tickers
#el vector normal de tickers que tenia con .mx

def f_tickers(archivos,data_archivos):

    tickers = []
    for i in archivos:
        l_tickers = list(data_archivos[i]['Ticker'])
        [tickers.append(i + '.MX') for i in l_tickers]
    global_tickers = np.unique(tickers).tolist()

    return global_tickers

# ---------------------------

def f_new_tickers(global_tickers):

    # Adj de nombre de tickers
    global_tickers = [i.replace('GFREGIOO.MX', 'RA.MX') for i in global_tickers]
    global_tickers = [i.replace('MEXCHEM.MX', 'ORBIA.MX') for i in global_tickers]
    global_tickers = [i.replace('LIVEPOLC.1.MX', 'LIVEPOLC-1.MX') for i in global_tickers]

    # Eliminar: MXN, USD,KOFL, BSMXB
    [global_tickers.remove(i) for i in ['MXN.MX', 'USD.MX', 'KOFL.MX', 'KOFUBL.MX', 'BSMXB.MX']]

    return global_tickers

# ---------------------------

def f_data(global_tickers):

    # Tiempo que se tarda en cargar
    inicio = time.time()
    # Descarga yfinance
    data = yf.download(global_tickers, start="2017-08-21", end="2020-09-21", actions=False,
                       group_by="close", interval='1d', auto_adjust=False, prepost=False, threads=True)
    # Tiempo que se tarda, solamenre muestra en terminal
    print('se tardo', round(time.time() - inicio, 2), 'segundos')

    return data

# ---------------------------

#need another fun para la data_close

def f_data_close(data,global_tickers):

    # Columna de fechas
    data_close = pd.DataFrame({i: data[i]['Close'] for i in global_tickers})

    return data_close

# ---------------------------


def f_precios(data_close , ic_fechas):

    # Localizar todos los precios
    precios = data_close.iloc[[int(np.where(data_close.index.astype(str) == i)[0]) for i in ic_fechas]]
    # Ordenar precios Lexicograficamente
    precios = precios.reindex(sorted(precios.columns), axis=1)

    return precios


# ------------------------------------------------------------------------------

def f_p_i(remv_activos,data_archivos,archivos,precios,k,c):
    pos_datos = data_archivos[archivos[0]].copy().sort_values('Ticker')[['Ticker', 'Nombre', 'Peso (%)']]

    # Extraer los activos a eliminar
    i_activos = list(pos_datos[pos_datos['Ticker'].isin(remv_activos)].index)

    # Eliminar los activos del Data
    pos_datos.drop(i_activos, inplace=True)

    # resetear index
    pos_datos.reset_index(inplace=True, drop=True)

    # Agregar .MX para empatar precios
    pos_datos['Ticker'] = pos_datos['Ticker'] + '.MX'

    # Corregir  ticker  en datos
    pos_datos['Ticker'] = pos_datos['Ticker'].replace('LIVEPOLC.1.MX', 'LIVEPOLC-1.MX')
    pos_datos['Ticker'] = pos_datos['Ticker'].replace('MEXCHEM.MX', 'ORBIA.MX')
    pos_datos['Ticker'] = pos_datos['Ticker'].replace('GFREGIOO.MX', 'RA.MX')

    # ----------------------------
    # P.I
    # precio, capital, titulos, postura, comision
    # need cash

    pos_datos['Precio'] = (np.array([precios.iloc[0, precios.columns.to_list().index(i)] for i in pos_datos['Ticker']]))
    # Capital por accion
    pos_datos['Capital'] = np.round(pos_datos['Peso (%)'] * k - pos_datos['Peso (%)'] * k * c, 2)
    # Titulos por accion
    pos_datos['Titulos'] = pos_datos['Capital'] / pos_datos['Precio']
    pos_datos['Titulos'] = [math.floor(i) for i in pos_datos['Titulos']]
    # Cash
    pos_datos['Postura'] = np.round(pos_datos['Precio'] * pos_datos['Titulos'], 2)
    # Comision en dinero
    pos_datos['Comision'] = np.round(pos_datos['Precio'] * pos_datos['Titulos'], 2) * c

    return pos_datos


# ----------------------------

def f_pasiva(ic_fechas,pos_datos,precios,cash,inv_pasiva):
#for nromal para iterar despues de tener mi p.i de ahi lleno el data con for
# inv_pasiva['timestamp'].append(dates[0])
    #inv_pasiva['timestamp'].append(ic_fechas[0])
    #inv_pasiva['Capital'].append(k - pos_datos['Comision'].sum())
    for i in range(len(ic_fechas)):
    #for i in range(1, len(dates)):
        pos_datos['Precios'] = (
            np.array([precios.iloc[i, precios.columns.to_list().index(j)] for j in pos_datos['Ticker']]))
        pos_datos['Comision'] = 0
        pos_datos['Postura'] = np.round(pos_datos['Precios'] * pos_datos['Titulos'], 2)
        inv_pasiva['Capital'].append(np.round(sum(pos_datos['Postura']) + cash, 2))
        #inv_pasiva['timestamp'].append(dates[i])
        inv_pasiva['timestamp'].append(ic_fechas[i])

    return inv_pasiva




