import streamlit as st
import mysql.connector
import pandas as pd

st.set_page_config(page_title="Dashboard", page_icon="🌐", layout="wide")
st.subheader("💰 API Yfinance")
st.markdown("##")

st.title("Datos de la tabla Stocks")

# Configuración de la conexión a la base de datos
def create_connection():
    connection = mysql.connector.connect(
        host='localhost',  
        user='root',  
        password='Andres980612',  
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
    st.sidebar.image("data/yahoo-logo.png", caption="Online Analytics")
    
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

