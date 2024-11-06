import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

st.set_page_config(page_title="Dashboard", page_icon="🌐", layout="wide")
st.subheader("💰 Stock Analysis")
st.markdown("##")

# Configuración de la conexión a la base de datos
def create_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Andres980612',  # Ajustar según tus credenciales
        database='yfinance_stocks'
    )
    return connection

def get_stocks():
    connection = create_connection()
    cursor = connection.cursor()
    
    query = "SELECT * FROM stocks"
    cursor.execute(query)
    
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    
    return result

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

def calculate_rsi(data, window=14):
    delta = data['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_roi(df, ticker):
    df_ticker = df[df["ticker"] == ticker].sort_values(by="date")
    
    if not df_ticker.empty:
        # ROI como porcentaje
        roi = ((df_ticker["close"].iloc[-1] - df_ticker["open"].iloc[0]) / df_ticker["open"].iloc[0]) * 100
        return roi
    else:
        return None

# Cargar datos
historical_data = get_historical_prices()
stocks_data = get_stocks()

df_stocks = pd.DataFrame(stocks_data, columns=["ticker", "name", "sector", "industry", "market_cap", "full_time_employees", "ipo_date", "extraction_timestamp"])
df_historical_prices = pd.DataFrame(historical_data, columns=["ticker", "date", "open", "close"])

# Crear una variable booleana para el control de visualización
show_initial_graph = True

if stocks_data:
    # Sidebar for user inputs and image
    st.sidebar.image("data/yfinance.png", caption="We provide access to real-time financial data, including stock quotes and price evolution for all companies")

    
    st.sidebar.header("Please filter")

    # Select tickers for filtering
    ticker = st.sidebar.multiselect(
        "SELECT Company",
        options=df_historical_prices["ticker"].unique(),
        default=[]
    )
    
    if ticker:
        df_filtered = df_historical_prices[df_historical_prices["ticker"].isin(ticker)]
        show_initial_graph = False  # No mostrar gráfico inicial si se aplican filtros

        period = st.sidebar.selectbox(
            "Select time period",
            options=["Daily", "Weekly", "Monthly"],
            key='time_period1'  
        )
        
        df_filtered['date'] = pd.to_datetime(df_filtered['date'])
        
        if period == "Daily":
            df_grouped = df_filtered
        elif period == "Weekly":
            df_grouped = df_filtered.resample('W-Mon', on='date').mean().reset_index()
        elif period == "Monthly":
            df_grouped = df_filtered.resample('M', on='date').mean().reset_index()

        # Boxplot of closing prices
        # Boxplot of closing prices
        if ticker:
    # Concatenar tickers seleccionados para mostrarlos en el título
         tickers_selected = ", ".join(ticker)
         fig = px.box(df_grouped, x='ticker', y='close', 
                 title=f'Boxplot of Closing Prices ({tickers_selected})',  # Modificar aquí
                 labels={'close': 'Closing Prices', 'ticker': 'Company'},
                 points="all")
         st.plotly_chart(fig)


        # Calculate statistics
        stats = df_grouped.groupby('ticker')['close'].agg(['mean', 'median', 'std', 'min', 'max']).reset_index()
        st.write(stats)

        # Line chart of closing prices
        st.header("Line Chart of Closing Prices")
        line_fig = px.line(df_grouped, x='date', y='close', color='ticker', 
                           title='Line Chart of Closing Prices', 
                           labels={'close': 'Closing Prices', 'date': 'Date', 'ticker': 'Ticker'})
        line_fig.add_vrect(x0="2020-03-01", x1="2020-12-01", fillcolor="red", opacity=0.25, annotation_text="Covid")
        st.plotly_chart(line_fig)

        # RSI filter
        st.sidebar.subheader("RSI Filter")
        rsi_ticker = st.sidebar.selectbox("Select ticker for RSI", options=ticker)
        if rsi_ticker:
            df_rsi_filtered = df_filtered[df_filtered['ticker'] == rsi_ticker]
            rsi_period = st.sidebar.selectbox("Select time period for RSI", options=["Daily", "Weekly", "Monthly"], key='rsi_time_period')
            
            df_rsi_filtered['date'] = pd.to_datetime(df_rsi_filtered['date'])
            
            if rsi_period == "Daily":
                df_rsi_grouped = df_rsi_filtered
            elif rsi_period == "Weekly":
                df_rsi_grouped = df_rsi_filtered.resample('W-Mon', on='date').mean().reset_index()
            elif rsi_period == "Monthly":
                df_rsi_grouped = df_rsi_filtered.resample('M', on='date').mean().reset_index()

            # Calculate RSI
            df_rsi_grouped['RSI'] = calculate_rsi(df_rsi_grouped)

            st.header("RSI Chart")
            rsi_fig = px.line(df_rsi_grouped, x='date', y='RSI', 
                               title='Relative Strength Index (RSI)', 
                               labels={'RSI': 'RSI', 'date': 'Date'})
            rsi_fig.add_hline(y=70, line_color="red", line_dash="dash", 
                              annotation_text="Overbought", 
                              annotation_position="top right")
            rsi_fig.add_hline(y=30, line_color="green", line_dash="dash", 
                              annotation_text="Oversold", 
                              annotation_position="bottom right")
            st.plotly_chart(rsi_fig)

        # Sección de cálculo de ROI
        st.header("6 · ROI Calculation")
        selected_ticker = st.sidebar.selectbox("Select Ticker for ROI Calculation", df_filtered['ticker'].unique())
        roi_value = calculate_roi(historical_data, selected_ticker)
        if roi_value is not None:
            st.write(f"ROI for {selected_ticker}: {roi_value:.2f}%")
        else:
            st.write("No data available for selected ticker")

        # Gráfico del precio a lo largo del tiempo para el ticker seleccionado
        st.write(f"Price Evolution for {selected_ticker}")
        price_fig = px.line(historical_data[historical_data["ticker"] == selected_ticker], x="date", y="close",
                             title=f"Price Evolution - {selected_ticker}")
        st.plotly_chart(price_fig)

        # Correlation analysis
        df_pivot = df_filtered.pivot(index='date', columns='ticker', values='close')
        correlation_matrix = df_pivot.corr()
        
        # Mostrar matriz de correlación
        st.header("Correlation Analysis")
        st.dataframe(correlation_matrix)

        # Heatmap for correlation
        fig_heatmap = ff.create_annotated_heatmap(correlation_matrix.values, 
                                                    x=list(correlation_matrix.columns), 
                                                    y=list(correlation_matrix.index),
                                                    colorscale='Viridis', 
                                                    showscale=True)
        st.plotly_chart(fig_heatmap)

# Mostrar gráfico de precios para todos los tickers solo si no hay filtros aplicados
if show_initial_graph and not df_historical_prices.empty:
    all_tickers_fig = px.line(df_historical_prices, x='date', y='close', color='ticker',
                               title='Price evolution for all Companies',
                               labels={'close': 'Closing Price', 'date': 'Date', 'ticker': 'Company'})
    st.plotly_chart(all_tickers_fig)




#thema
hide_st_style="""
 
<style>
#MainMenu{visibility:hidden;}
footer{visibility:hidden;}
header{visibility:hidden;}
</style>
"""

