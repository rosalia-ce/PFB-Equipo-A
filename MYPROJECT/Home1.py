import streamlit as st
import mysql.connector
import pandas as pd
import plotly.graph_objs as go
from sqlalchemy import create_engine

st.set_page_config(page_title="Dashboard", page_icon="🌐", layout="wide")
st.title("Dashboard Financiero 🎉")

# Configuración de la conexión a la base de datos
def create_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Andres980612',
        database='yfinance'
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

# Obtener datos de la tabla historical_prices
def get_historical_prices():
    connection = create_connection()
    cursor = connection.cursor()
    
    query = "SELECT * FROM historical_prices"
    cursor.execute(query)
    
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    
    return result

# Cargar los datos
stocks_data = get_stocks()
historical_prices_data = get_historical_prices()

# Convertir datos a DataFrames
df_stocks = pd.DataFrame(stocks_data, columns=["ticker", "name", "sector", "industry", "market_cap", "full_time_employees", "ipo_date", "extraction_timestamp"])
df_historical_prices = pd.DataFrame(historical_prices_data, columns=["ticker", "date", "open", "high", "low", "close", "volume","adj_close","extraction_timestamp"])

# Sección para visualizar los datos de stocks
st.subheader("Datos de Stocks")
st.write(df_stocks)

# Filtros en el sidebar
st.sidebar.header("Filtros de Stocks")
sector = st.sidebar.multiselect(
    "Selecciona Sector",
    options=df_stocks["sector"].unique(),
    default=[]
)

# Filtrar DataFrame basado en el sector seleccionado
if sector:
    df_stocks = df_stocks[df_stocks["sector"].isin(sector)]

st.write(df_stocks)

# Sección para gráficos de precios históricos
st.subheader("Gráficos de Precios Históricos")

# Selector de ticker
selected_ticker = st.selectbox("Selecciona un Ticker", df_historical_prices["ticker"].unique())
df_selected = df_historical_prices[df_historical_prices["ticker"] == selected_ticker]

# Gráfico de precios históricos
fig = go.Figure()
fig.add_trace(go.Scatter(x=df_selected["date"], y=df_selected["close"], mode='lines', name='Precio de Cierre'))
fig.update_layout(title=f'Precio de Cierre de {selected_ticker}', xaxis_title='Fecha', yaxis_title='Precio')
st.plotly_chart(fig)

# Gráfico de media móvil
window_size = st.slider("Tamaño de la Ventana para Media Móvil", 1, 50, 20)
df_selected['MA'] = df_selected['close'].rolling(window=window_size).mean()

fig_ma = go.Figure()
fig_ma.add_trace(go.Scatter(x=df_selected["date"], y=df_selected["close"], mode='lines', name='Precio de Cierre'))
fig_ma.add_trace(go.Scatter(x=df_selected["date"], y=df_selected['MA'], mode='lines', name=f'Media Móvil {window_size} días'))
fig_ma.update_layout(title=f'Media Móvil de {selected_ticker}', xaxis_title='Fecha', yaxis_title='Precio')
st.plotly_chart(fig_ma)

# Sección para estadísticas de precios
st.subheader(f"Estadísticas para {selected_ticker}")
mean_price = df_selected["close"].mean()
median_price = df_selected["close"].median()
st.write(f"**Media de precios**: {mean_price:.2f}")
st.write(f"**Mediana de precios**: {median_price:.2f}")

