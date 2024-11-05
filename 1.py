import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px
import numpy as np

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



# Función para calcular la volatilidad de los rendimientos diarios
def calculate_volatility(df, ticker):
    df_ticker = df[df["ticker"] == ticker].sort_values(by="date").reset_index(drop=True)
    if not df_ticker.empty:
        # Calcular los rendimientos diarios
        df_ticker['daily_return'] = df_ticker['close'].pct_change()
        
        # Calcular la volatilidad diaria
        daily_volatility = df_ticker['daily_return'].std() * 100
        
        # Calcular la volatilidad anualizada
        annualized_volatility = daily_volatility * np.sqrt(252)
        return daily_volatility, annualized_volatility, df_ticker
    else:
        return None, None, df_ticker

# Cargar datos
st.header("6 · ROI and Volatility Calculation")
historical_data = get_historical_prices()

# Seleccionar ticker
tickers = historical_data["ticker"].unique()
selected_ticker = st.selectbox("Select Ticker for ROI and Volatility Calculation", tickers)

# Calcular ROI para el ticker seleccionado
roi_value = calculate_roi(historical_data, selected_ticker)
if roi_value is not None:
    st.write(f"ROI for {selected_ticker}: {roi_value:.2f}%")
else:
    st.write("No data available for selected ticker")

# Calcular volatilidad para el ticker seleccionado
daily_volatility, annualized_volatility, ticker_data = calculate_volatility(historical_data, selected_ticker)
if daily_volatility is not None:
    st.write(f"Daily Volatility for {selected_ticker}: {daily_volatility:.2f}%")
    st.write(f"Annualized Volatility for {selected_ticker}: {annualized_volatility:.2f}%")
else:
    st.write("No data available for selected ticker")

# Gráfico del precio a lo largo del tiempo para el ticker seleccionado
st.write(f"Price Evolution for {selected_ticker}")
fig = px.line(ticker_data, x="date", y="close", title=f"Price Evolution - {selected_ticker}")
st.plotly_chart(fig)

# Gráfico de los rendimientos diarios para el ticker seleccionado
st.write(f"Daily Returns for {selected_ticker}")
fig_returns = px.line(ticker_data, x="date", y="daily_return", title=f"Daily Returns - {selected_ticker}")
st.plotly_chart(fig_returns)