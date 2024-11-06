import streamlit as st
import mysql.connector
import pandas as pd  # O usa import pymysql si decides usar pymysql

# Configuración de la conexión a la base de datos
def create_connection():
    connection = mysql.connector.connect(
        host='localhost',  # Por ejemplo, 'localhost' o la dirección IP del servidor
        user='root',  # Tu usuario de MySQL
        password='Andres980612',  # Tu contraseña de MySQL
        database='yfinance_stocks'  # El nombre de tu base de datos
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



# Obtener datos y mostrarlos en Streamlit
result = get_stocks()  # Llama a la función get_stocks()
df = pd.DataFrame(result, columns=["ticker", "name", "sector", "industry", "market_cap", "full_time_employees", "ipo_date", "extraction_timestamp"])
st.dataframe(df)  # Mostrar el DataFrame en Streamlit


