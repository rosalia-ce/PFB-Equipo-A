import streamlit as st
import pandas as pd
import numpy as np
import mysql.connector
import plotly.express as px

# Configuración de la conexión a la base de datos
def create_connection():
    connection = mysql.connector.connect(
        host='localhost',  
        user='root',  
        password='Elisa17',  
        database='yfinance_stocks'  
    )
    return connection

# Obtener datos históricos de precios
def get_historical_prices():
    connection = create_connection()
    cursor = connection.cursor()
    query = "SELECT ticker, date, open, close FROM historical_prices"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    
    # Convertir a DataFrame
    df = pd.DataFrame(result, columns=["ticker", "date", "open", "close"])
    df["date"] = pd.to_datetime(df["date"])  # Convertir columna de fecha
    return df

# Función para calcular el ROI
def calculate_roi(df, ticker):
    df_ticker = df[df["ticker"] == ticker].sort_values(by="date")
    
    if not df_ticker.empty:
        # ROI como porcentaje
        roi = ((df_ticker["close"].iloc[-1] - df_ticker["open"].iloc[0]) / df_ticker["open"].iloc[0]) * 100
        return roi
    else:
        return None

# Función para calcular la volatilidad de los rendimientos
def calculate_volatility(df, ticker, frequency='daily'):
    df_ticker = df[df["ticker"] == ticker].sort_values(by="date")
    df_ticker["returns"] = df_ticker["close"].pct_change()  # Rendimientos diarios
    
    if frequency == 'daily':
        # Volatilidad diaria (desviación estándar de los rendimientos diarios)
        volatility = df_ticker["returns"].std() * np.sqrt(252)  # Anualizada
    elif frequency == 'monthly':
        # Volatilidad mensual: Resamplear a fin de mes y calcular desviación estándar
        df_ticker.set_index("date", inplace=True)
        monthly_returns = df_ticker["close"].resample("M").ffill().pct_change()
        volatility = monthly_returns.std() * np.sqrt(12)  # Anualizada
    
    return volatility * 100  # Expresado en porcentaje

# Cargar datos
st.header("Financial Metrics Dashboard")
historical_data = get_historical_prices()

# Verificar si hay datos disponibles
if historical_data.empty:
    st.write("No se encontraron datos en la tabla historical_prices.")
else:
    tickers = historical_data["ticker"].unique()
    
    # ---- SECCIÓN ROI ----
    st.header("1. ROI Calculation")
    selected_ticker_roi = st.selectbox("Select Ticker for ROI Calculation", tickers, key="roi")

    # Calcular y mostrar el ROI para el ticker seleccionado
    roi_value = calculate_roi(historical_data, selected_ticker_roi)
    if roi_value is not None:
        st.write(f"ROI for {selected_ticker_roi}: {roi_value:.2f}%")
    else:
        st.write("No data available for selected ticker")


st.header("2. Volatility Calculation")
selected_ticker_volatility = st.selectbox("Select Ticker for Volatility Calculation", tickers, key="volatility")
frequency = st.radio("Select Frequency", ["daily", "monthly"], key="frequency")

    # Calcular y mostrar la volatilidad para el ticker seleccionado
volatility_value = calculate_volatility(historical_data, selected_ticker_volatility, frequency=frequency)
if volatility_value is not None:
        st.write(f"{frequency.capitalize()} Volatility for {selected_ticker_volatility}: {volatility_value:.2f}%")
else:
        st.write("No data available for selected ticker")

    # ---- GRÁFICO PRECIO A LO LARGO DEL TIEMPO ----
st.header("3. Price Evolution")
selected_ticker_graph = st.selectbox("Select Ticker for Price Evolution Graph", tickers, key="price_graph")
    
    # Gráfico del precio a lo largo del tiempo para el ticker seleccionado
st.write(f"Price Evolution for {selected_ticker_graph}")
fig = px.line(historical_data[historical_data["ticker"] == selected_ticker_graph], x="date", y="close",
                  title=f"Price Evolution - {selected_ticker_graph}")
st.plotly_chart(fig)