import mysql.connector
import streamlit as st 

#connection
def create_connection():
    connection = mysql.connector.connect(
        host='localhost',  
        user='root',  
        password='Andres980612',  
        database='yfinance_stocks'  
    )
    return connection

# Obtener datos de la tabla stocks
def get_stocks(connection):
    cursor = connection.cursor()
    
    query = "SELECT * FROM stocks"
    cursor.execute(query)
    
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    
    return result