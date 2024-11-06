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
def calculate_volatility(df, ticker, frequency='