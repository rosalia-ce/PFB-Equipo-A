import streamlit as st
import mysql.connector
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from sqlalchemy import create_engine

st.set_page_config(page_title="Dashboard", page_icon="🌐", layout="wide")
st.subheader("💰 API")
st.markdown("##")

st.title("Datos de la tabla Stocks")

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
    st.sidebar.image("data/OIP.jpeg", caption="Proporcionamos acceso a datos financieros en tiempo real, incluyendo cotizaciones de acciones, información sobre fondos, índices, divisas y criptomonedas")

    # Filtros en el sidebar
    st.sidebar.header("Please filter")
    
    ticker = st.sidebar.multiselect(
        "SELECT ticker",
        options=df["ticker"].unique(),
        default=[],
    )
    
    name = st.sidebar.multiselect(
        "SELECT name",
        options=df["name"].unique(),
        default=[],
    )
    
    sector = st.sidebar.multiselect(
        "SELECT sector",
        options=df["sector"].unique(),
        default=[],
    )
    
    industry = st.sidebar.multiselect(
        "SELECT industry",
        options=df["industry"].unique(),
        default=[],
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


def get_historical_prices():
    connection = create_connection()
    cursor = connection.cursor()
    
    query = "SELECT * FROM historical_prices"
    cursor.execute(query)
    
    result = cursor.fetchall()
    cursor.close()
    connection.close()

    return result
historical_prices_data = get_historical_prices()
df_historical_prices = pd.DataFrame(historical_prices_data, columns=["ticker", "date", "open", "high", "low", "close", "volume"])
df= df_historical_prices

# Cálculo de la Media Móvil Simple (SMA)
def calculate_moving_averages(df, window=30):
    df["MA_" + str(window)] = df["close"].rolling(window=window).mean()

# Cálculo del RSI
def calculate_rsi(df, window=14):
    delta = df["close"].diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    df["RSI"] = 100 - (100 / (1 + rs))

calculate_moving_averages(df, window=20)
calculate_rsi(df)

# Aplicación Dash
app = dash.Dash(__name__)

# Layout del dashboard
app.layout = html.Div([
    html.H1("Dashboard de Precios Históricos"),

    # Dropdown selección ticker
    dcc.Dropdown(
        id="ticker-dropdown",
        options=[{"label": ticker, "value": ticker} for ticker in df["ticker"].unique()],
        value=df["ticker"].unique()[0],
        multi=False
    ),

    # Gráfica precios históricos con slider
    dcc.Graph(id="historical-prices-graph"),

    # Gráfica de RSI
    dcc.Graph(id="rsi-graph"),

    # Slider fechas
    dcc.RangeSlider(
        id="date-range-slider",
        min=0,
        max=len(df["date"]) - 1,
        value=[0, len(df["date"]) - 1],
        marks={i: str(date)[:10] for i, date in enumerate(df["date"].dt.date.unique())},
        step=1
    ),

    # Selector para el periodo
    dcc.Dropdown(
        id="period-dropdown",
        options=[
            {"label": "Diario", "value": "D"},
            {"label": "Semanal", "value": "W"},
            {"label": "Mensual", "value": "M"}
        ],
        value="D",
        multi=False
    ),

    # Gráfica de estadísticas
    dcc.Graph(id="stats-graph")
])

# Callback para actualizar los gráficos
@app.callback(
    [Output("historical-prices-graph", "figure"),
     Output("rsi-graph", "figure"),
     Output("stats-graph", "figure")],
    [Input("ticker-dropdown", "value"),
     Input("date-range-slider", "value"),
     Input("period-dropdown", "value")]
)
def update_graphs(selected_ticker, date_range, selected_period):
    # Filtro ticker seleccionado
    df_filtered = df[df["ticker"] == selected_ticker]

    # Filtro de fechas
    df_filtered = df_filtered.iloc[date_range[0]:date_range[1]]

    # Gráfica de precios históricos
    fig_prices = go.Figure()
    fig_prices.add_trace(go.Scatter(
        x=df_filtered["date"],
        y=df_filtered["close"],
        mode="lines",
        name="Precio de Cierre"
    ))
    fig_prices.add_trace(go.Scatter(
        x=df_filtered["date"],
        y=df_filtered["MA_20"],
        mode="lines",
        name="Media Móvil 20 días",
        line=dict(dash="dash")
    ))
    fig_prices.update_layout(
        title=f'Precios Históricos para {selected_ticker}',
        xaxis_title="Fecha",
        yaxis_title="Precio de Cierre",
        xaxis_rangeslider_visible=True
    )

    # Gráfica de RSI
    fig_rsi = go.Figure()
    fig_rsi.add_trace(go.Scatter(
        x=df_filtered["date"],
        y=df_filtered["RSI"],
        mode="lines",
        name="RSI"
    ))
    fig_rsi.update_layout(
        title=f"RSI para {selected_ticker}",
        xaxis_title="Fecha",
        yaxis_title="RSI",
        yaxis_range=[0, 100]
    )

    # Agrupación por período seleccionado y cálculo de estadísticas
    df_filtered.set_index("date", inplace=True)
    df_resampled = df_filtered["close"].resample(selected_period).agg(['mean', 'median', 'std', 'min', 'max']).reset_index()

    # Gráfica de estadísticas
    fig_stats = go.Figure()
    fig_stats.add_trace(go.Box(
        y=df_resampled['mean'],
        name='Media',
        boxmean='sd'  # Muestra la media y desviación estándar
    ))
    fig_stats.add_trace(go.Box(
        y=df_resampled['median'],
        name='Mediana'
    ))
    fig_stats.add_trace(go.Box(
        y=df_resampled['std'],
        name='Desviación Estándar'
    ))
    fig_stats.update_layout(title=f"Estadísticas de Precios de Cierre para {selected_ticker} (Periodo: {selected_period})",
                             yaxis_title="Precio de Cierre",
                             xaxis_title="Estadísticas")

    return fig_prices, fig_rsi, fig_stats

# Aplicación
if __name__ == "__main__":
    app.run_server(debug=True)

