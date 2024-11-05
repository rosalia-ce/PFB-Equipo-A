import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px

# Configuración de la conexión a la base de datos
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',  
            user='root',  
            password='Elisa17',  
            database='yfinance_stocks'  
        )
        return connection
    except mysql.connector.Error as err:
        st.error(f"Error de conexión: {err}")
        return None

# Obtener datos históricos de precios
def get_historical_prices():
    connection = create_connection()
    if connection is None:
        st.write("No se pudo establecer la conexión con la base de datos.")
        return pd.DataFrame()  # Devuelve un DataFrame vacío en caso de error de conexión
    
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
        first_open = df_ticker["open"].iloc[0]
        last_close = df_ticker["close"].iloc[-1]
        roi = ((last_close - first_open) / first_open) * 100
        st.write(f"Calculando ROI: Precio de apertura inicial {first_open}, Precio de cierre final {last_close}, ROI: {roi:.2f}%")
        return roi
    else:
        st.write("No hay datos disponibles para el cálculo del ROI.")
        return None

# Cargar datos históricos de precios
st.header("6 · ROI Calculation and Volatility")
historical_data = get_historical_prices()

# Verificar si los datos históricos están cargados
if historical_data.empty:
    st.write("No se encontraron datos en la tabla historical_prices.")
else:
    # Mostrar el DataFrame con los datos históricos para verificar su estructura
    st.write("Datos históricos cargados:", historical_data.head())

    # Seleccionar ticker
    tickers = historical_data["ticker"].unique()
    selected_ticker = st.selectbox("Select Ticker for ROI Calculation", tickers)

    # Calcular ROI para el ticker seleccionado
    roi_value = calculate_roi(historical_data, selected_ticker)
    if roi_value is not None:
        st.write(f"ROI for {selected_ticker}: {roi_value:.2f}%")
    else:
        st.write("No data available for selected ticker")

    # Gráfico del precio a lo largo del tiempo para el ticker seleccionado
    st.write(f"Price Evolution for {selected_ticker}")
    fig = px.line(historical_data[historical_data["ticker"] == selected_ticker], x="date", y="close",
                  title=f"Price Evolution - {selected_ticker}")
    st.plotly_chart(fig)
    