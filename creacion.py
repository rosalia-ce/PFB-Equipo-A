import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

st.set_page_config(page_title="Dashboard", page_icon="🌐", layout="wide")
st.subheader("💰 API")
st.markdown("##")

def create_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Andres980612',
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
    
    query = "SELECT * FROM historical_prices"
    cursor.execute(query)
    
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    
    return result

def calculate_rsi(data, window=14):
    delta = data['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi

stocks_data = get_stocks()
historical_prices_data = get_historical_prices()

df_stocks = pd.DataFrame(stocks_data, columns=["ticker", "name", "sector", "industry", "market_cap", "full_time_employees", "ipo_date", "extraction_timestamp"])
df_historical_prices = pd.DataFrame(historical_prices_data, columns=["date", "open", "high", "low", "close", "adj_close", "volume", "ticker", "extraction_timestamp"])

if stocks_data:
    # Sidebar for user inputs and image
    st.sidebar.image("data/OIP.jpeg", caption="Proporcionamos acceso a datos financieros en tiempo real, incluyendo cotizaciones de acciones, información sobre fondos, índices, divisas y criptomonedas")

    st.sidebar.header("Please filter")
    
    # Select tickers for filtering
    ticker = st.sidebar.multiselect(
        "SELECT ticker",
        options=df_historical_prices["ticker"].unique(),
        default=[]
    )
    
    if ticker:
        df_filtered = df_historical_prices[df_historical_prices["ticker"].isin(ticker)]
        
        period = st.sidebar.selectbox(
            "Select time period",
            options=["Daily", "Weekly", "Monthly"],
            key='time_period1'  # Unique key for this selectbox
        )
        
        df_filtered['date'] = pd.to_datetime(df_filtered['date'])
        
        if period == "Daily":
            df_grouped = df_filtered
        elif period == "Weekly":
            df_grouped = df_filtered.resample('W-Mon', on='date').mean().reset_index()
        elif period == "Monthly":
            df_grouped = df_filtered.resample('M', on='date').mean().reset_index()

        # Boxplot of closing prices
        fig = px.box(df_grouped, x='ticker', y='close', title='Boxplot of Closing Prices', 
                     labels={'close': 'Closing Prices', 'ticker': 'Ticker'},
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
        st.plotly_chart(line_fig)

        # Correlation analysis
        df_pivot = df_filtered.pivot(index='date', columns='ticker', values='close')
        correlation_matrix = df_pivot.corr()

        # Display correlation matrix
        st.header("Correlation Analysis")
        st.dataframe(correlation_matrix)

        # Heatmap for correlation
        fig_heatmap = ff.create_annotated_heatmap(correlation_matrix.values, 
                                                    x=list(correlation_matrix.columns), 
                                                    y=list(correlation_matrix.index),
                                                    colorscale='Viridis', 
                                                    showscale=True)
        st.plotly_chart(fig_heatmap)

        # RSI filter
        st.sidebar.subheader("RSI Filter")
        rsi_ticker = st.sidebar.selectbox("Select ticker for RSI", options=ticker)
        if rsi_ticker:
            # Data for RSI
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

st.write(df_historical_prices)

