import streamlit as st
import pandas as pd
import plotly.graph_objs as go

# Función para calcular el Drawdown
def calculate_drawdown(df, ticker):
    # Filtrar los datos del ticker seleccionado
    df_ticker = df[df["ticker"] == ticker].sort_values(by="date").copy()
    
    # Asegurarse de que la columna "close" sea de tipo float
    df_ticker["close"] = df_ticker["close"].astype(float)
    
    # Calcular el precio máximo hasta cada fecha
    df_ticker['peak'] = df_ticker['close'].cummax()
    
    # Calcular el drawdown
    df_ticker['drawdown'] = (df_ticker['close'] - df_ticker['peak']) / df_ticker['peak']
    
    # Encontrar el drawdown máximo
    max_drawdown = df_ticker['drawdown'].min()  # El valor más bajo será el drawdown máximo
    
    return max_drawdown * 100, df_ticker

# Cargar datos
st.header("7 · Drawdown Calculation")
historical_data = get_historical_prices()

# Seleccionar ticker
tickers = historical_data["ticker"].unique()
selected_ticker_drawdown = st.selectbox("Select Ticker for Drawdown Calculation", tickers)

# Calcular Drawdown para el ticker seleccionado
drawdown_value, drawdown_df = calculate_drawdown(historical_data, selected_ticker_drawdown)

if drawdown_value is not None:
    st.write(f"Maximum Drawdown for {selected_ticker_drawdown}: {drawdown_value:.2f}%")
else:
    st.write("No data available for selected ticker")

# Gráfico del Drawdown
st.subheader("Drawdown Over Time")
drawdown_fig = go.Figure()

# Gráfico del Drawdown
drawdown_fig.add_trace(go.Scatter(
    x=drawdown_df['date'],
    y=drawdown_df['drawdown'],
    mode='lines',
    name='Drawdown',
    line=dict(color='red')
))

drawdown_fig.update_layout(
    title=f"Drawdown Over Time for {selected_ticker_drawdown}",
    xaxis_title='Date',
    yaxis_title='Drawdown',
    yaxis_tickformat='%'
)

st.plotly_chart(drawdown_fig)