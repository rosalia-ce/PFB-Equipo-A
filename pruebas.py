import streamlit as st
import pandas as pd
import numpy as np
import requests
from PIL import Image


st.header("1 · EVOLUCIÓN EN EL TIEMPO")
st.markdown(" - Dashboard Interactivo: Visualización de la evolución en el tiempo, métricas (rentabilidad, volatilidad y Sharpe ratio) ")
st.info("A - Descripción de la Industria Tecnológica. Grafica 5 años")
#image = Image.open("/Users/DATA/Desktop/PFB-Equipo-A/descarga (1).jpeg")
#st.image(image, caption="foto1", use_column_width=True)

#uploaded_file = st.file_uploader("/Users/DATA/Desktop/PFB-Equipo-A/CSV/stocks_20241024.csv", type=["csv"])

df=pd.read_csv("/Users/DATA/Desktop/PFB-Equipo-A/CSV/stocks_20241024.csv")
df
st.info("B - Descripción de la acción, añadir intervalo de fechas. 3 Graficas metricas, 1 año, mensual y diario ")
#image1 = Image.open("/Users/DATA/Desktop/PFB-Equipo-A/imagenes para streamlit /descarga (2).jpeg")
#image2 = Image.open("/Users/DATA/Desktop/PFB-Equipo-A/imagenes para streamlit /descarga (4).jpeg")
#image3 = Image.open("/Users/DATA/Desktop/PFB-Equipo-A/imagenes para streamlit /descarga (5).jpeg")

#st.image(
 #   [image1, image2, image3], 
#    caption=["descarga(2)",   "descarga(4)",   "descarga(5)"], 
 #   width=100
#)

st.header("2 · COMPARADOR DE ACTIVOS")
st.markdown(" - Comparador de Activos: Herramienta para comparar el rendimiento de diferentes acciones. ")
#with st.expander (label= "Dataframe", expanded=false):
# st.dataframe(pd.read_csv)
#activos=["Rosalía","Camilo", "Noe"]
#choice=st.selectbox(label="Select", options=select)
#st.write(f"Select:{choice}")
#rendimiento=["A","B","C"]
#choice=st.selectbox(label="Select", options=select)
#st.write(f"Select:{choice}")

st.write("Descripción y grafica 5 años, año y mensual")

st.header("3 · ANALISIS TÉCNICO")
st.markdown(" - Análisis Técnico: Gráficos interactivos con indicadores técnicos (velas japonesas, medias móviles, etc.) para identificar patrones y tendencias. ")
st.info("A - Descripción y grafica 5 años , año y mensual")
#image = Image.open("/Users/DATA/Desktop/PFB-Equipo-A/imagenes para streamlit ")
st.info("B - Descripción de la acción a mostrar en cuanto a un hecho histórico (pandemia) *cripto???**extra")
#image = Image.open("/Users/DATA/Desktop/PFB-Equipo-A/imagenes para streamlit ")
st.write("3 gráficas metricas (1 año, mensual y diario)")
st.write("Balance General / Estado de resultados, Medias móviles, Relative Strength Index (RSI), 2.5 del script analizar como se relacionan las variables entre ellas")

st.header("4 · GRÁFICA TEMPORAL")
st.markdown(" - Gráfica Temporal: Gráfica interactiva para mostrar la evolución en el tiempo de las acciones. ")
#image = Image.open("/Users/DATA/Desktop/PFB-Equipo-A/imagenes para streamlit ")
st.info("A - Precios Históricos (Time Series With Range Slider) visualizacion de plotly")
st.info("B - Accion en contexto")

st.header("5 · DATOS")
st.markdown(" - Tabla de datos: Presentación detallada de las acciones")
#st.table(df)
#st.dataframe(df.select_dtypes(include=np.number).style.highlight_max(axis=0))
st.info("A - Tabla resumen que se pueda filtrar pr año y mes")
#st.table(df)
st.info("B - KPI (rentabilidad)")

#st.dataframe(dir(st))

st.write("csv")
#st.dataframe(df)