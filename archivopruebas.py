
import streamlit as st
import pandas as pd
import numpy as np
import requests
from PIL import Image
import mysql.connector

st.set_page_config(page_title="Dashboard", page_icon="🌐", layout="wide")
st.subheader("💰 API Yfinance")
st.markdown("##")



st.header("1 · TIME EVOLUTION")
st.markdown(" - Dashboard Interactivo: Visualización de la evolución en el tiempo, métricas (rentabilidad, volatilidad y Sharpe ratio) ")
st.info("A - IT Sector. X Year")

st.title("Stocks table")
# Configuración de la conexión a la base de datos
def create_connection():
    connection = mysql.connector.connect(
        host='localhost',  
        user='root',  
        password='Elisa17',  
        database='yfinance_stocks'  
    )
    return connection

# Obtener datos de la tabla stocks
def get_stocks():
    connection = create_connection()
    cursor = connection.cursor()
    
    query = "SELECT * FROM stocks"
    cursor.execute(query)
    
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    
    return result

# Cargar los datos automáticamente al iniciar la aplicación
stocks_data = get_stocks()
if stocks_data:
    # Convertir datos a un formato mostrable (por ejemplo, un DataFrame)
    df = pd.DataFrame(stocks_data, columns=["ticker", "name", "sector", "industry", "market_cap", "full_time_employees", "ipo_date", "extraction_timestamp"])
    st.write(df)
else:
    st.write("No se encontraron datos en la tabla.")

# Agregar los filtros solo si df no es None
if stocks_data:
    # Sidebar
    st.sidebar.image("/Users/DATA/Desktop/PFB-Equipo-A/imagenes para streamlit /yahoo-logo.png", caption="Descripción general y resumida")
    
    # Filtros en el sidebar
    st.sidebar.header("Please filter")
    
    ticker = st.sidebar.multiselect(
        "SELECT ticker",
        options=df["ticker"].unique(),
        default=df["ticker"].unique(),
    )
    
    name = st.sidebar.multiselect(
        "SELECT name",
        options=df["name"].unique(),
        default=df["name"].unique(),
    )
    
    sector = st.sidebar.multiselect(
        "SELECT sector",
        options=df["sector"].unique(),
        default=df["sector"].unique(),
    )
    
    industry = st.sidebar.multiselect(
        "SELECT industry",
        options=df["industry"].unique(),
        default=df["industry"].unique(),
    )

    # Aplicar filtros al df
    filtered_df = df[
        (df['ticker'].isin(ticker)) &
        (df['name'].isin(name)) &
        (df['sector'].isin(sector)) &
        (df['industry'].isin(industry))
    ]

    # Mostrar el DataFrame filtrado
    st.write(filtered_df)



st.info("B - Description of the STOCK. 3 Graphs, 1 Year, monthly y daily ")


#st.image(
 #   [image1, image2, image3], 
#    caption=["descarga(2)",   "descarga(4)",   "descarga(5)"], 
 #   width=100
#)

st.header("2 · ASSET COMPARISON (Comparador de Activos: Herramienta para comparar el rendimiento de diferentes acciones)")
#with st.expander (label= "Dataframe", expanded=false):
# st.dataframe(pd.read_csv)
#activos=["Rosalía","Camilo", "Noe"]
#choice=st.selectbox(label="Select", options=select)
#st.write(f"Select:{choice}")
#rendimiento=["A","B","C"]
#choice=st.selectbox(label="Select", options=select)
#st.write(f"Select:{choice}")

st.write(" Graph 5 Years, Year, Monthly")

st.header("3 · TECHNICAL ANALYSIS")
st.markdown(" - Interactive Graphs, technical indicators (velas japonesas, medias móviles) para identificar Patterns&Trends. ")

st.info("A - Graph 5 Years, Year, Monthly")

st.info("B - Description of STOCK During the Pandemic *cripto???**extra")
st.write("3 Graphs, 1 Year, monthly y daily")


st.write("Balance / Results, Medias móviles, Relative Strength Index (RSI), 2.5 del script analizar como se relacionan las variables entre ellas")


st.header("4 · TIME SERIES GRAPH")
st.markdown(" - Gráfica Temporal: Gráfica interactiva para mostrar la evolución en el tiempo de las acciones. ")
#image = Image.open("/Users/DATA/Desktop/PFB-Equipo-A/imagenes para streamlit ")
st.info("A - Historical Prices (Time Series With Range Slider) Plotly visual")
st.info("B - Stock Enviorment")

st.header("5 · DATA")
st.markdown(" - Data Table: Detail of Stocks")
#st.table(df)
#st.dataframe(df.select_dtypes(include=np.number).style.highlight_max(axis=0))
st.info("A - Resume Table - filter by year and month")
#st.table(df)
st.info("B - KPI (rentabilidad)")

#st.dataframe(dir(st))

st.write("csv")
#st.dataframe(df)