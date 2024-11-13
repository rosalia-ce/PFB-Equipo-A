import streamlit as st
from PIL import Image
import numpy as np
import mysql.connector
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

@st.cache_data
def load_monthly_data():
    return pd.read_csv('C:/Users/andre/OneDrive/Desktop/MYPROJECT/monthly_historical.csv')

@st.cache_data
def load_weekly_data():
    return pd.read_csv('C:/Users/andre/OneDrive/Desktop/MYPROJECT/weekly_historical.csv')

st.set_page_config(page_title="Dashboard", page_icon="🌐", layout="wide")

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
    query = "SELECT ticker, date, open, close FROM historical_prices"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    df = pd.DataFrame(result, columns=["ticker", "date", "open", "close"])
    df["date"] = pd.to_datetime(df["date"])
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
        roi = ((df_ticker["close"].iloc[-1] - df_ticker["open"].iloc[0]) / df_ticker["open"].iloc[0]) * 100
        return roi
    else:
        return None

def calculate_drawdown(df, ticker):
    df_ticker = df[df['ticker'] == ticker].copy()
    df_ticker['max'] = df_ticker['close'].cummax()
    df_ticker['drawdown'] = (df_ticker['max'] - df_ticker['close']) / df_ticker['max'] * 100
    max_drawdown = df_ticker['drawdown'].max()
    return max_drawdown, df_ticker[['date', 'drawdown', 'close']]

# Código Volatilidad
def calculate_volatility(df, period='daily'):
    if 'close' not in df.columns:
        st.error('El DataFrame no contiene la columna "close".')
        return None
    if period == 'daily':
        return np.std(df['close'].astype("float").pct_change()) * float(np.sqrt(252))  # Volatilidad diaria anualizada
    elif period == 'weekly':
        return np.std(df['close'].astype("float").pct_change()) * float(np.sqrt(52))  # Volatilidad semanal anualizada
    elif period == 'monthly':
        return np.std(df['close'].astype("float").pct_change()) * float(np.sqrt(12))  # Volatilidad mensual anualizada
    else:
        return None

show_initial_graph = True

# Cargar datos
historical_data = get_historical_prices()
stocks_data = get_stocks()

df_stocks = pd.DataFrame(stocks_data, columns=["ticker", "name", "sector", "industry", "market_cap", "full_time_employees", "ipo_date", "extraction_timestamp"])
df_historical_prices = pd.DataFrame(historical_data, columns=["ticker", "date", "open", "close"])

st.sidebar.image("data/yfinance.png", caption="We provide access to real-time financial data, including stock quotes and price evolution for technology companies.")

# Menú de navegación

st.sidebar.markdown(
    """
    <style>
        .button {
            background-color: #4CAF50; /* Verde */
            border-style: solid;
            color: white;
            padding: 15px 32px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 12px;
        }
    </style>
    """, unsafe_allow_html=True)

st.sidebar.markdown("<h1 style='text-align: center; color: white;'>💼Menu</h1>", unsafe_allow_html=True)

if 'page' not in st.session_state:
    st.session_state.page = "Página 1"

# Botones de navegación en la barra lateral
if st.sidebar.button("💶Home", key="btn1", help="Go to Beginning Page"):
    st.session_state.page = "Página 1"

if st.sidebar.button("👨‍💼Overview", key="btn2", help="Go to Overview Page"):
    st.session_state.page = "Página 2"

if st.sidebar.button("📊Charts and Measures", key="btn3", help="Go to Charts Page"):
    st.session_state.page = "Página 3"

if st.sidebar.button("📈Client dashboard", key="btn4", help="Go to Client dashboard Page"):
    st.session_state.page = "Página 4"

if st.sidebar.button("👩‍🔧About", key="btn5", help="Go to About Page"):
    st.session_state.page = "Página 5"

if st.session_state.page == "Página 1":
    st.title("Página 1")
    # Agregar contenido para la Página 1 aquí

elif st.session_state.page == "Página 2":
    st.title("Overview")

    if show_initial_graph and not df_historical_prices.empty:
        all_tickers_fig = px.line(df_historical_prices, x='date', y='close', color='ticker',
                                   title='Price evolution for all Companies',
                                   labels={'close': 'Closing Price($)', 'date': 'Year', 'ticker': 'Company'})
        all_tickers_fig.update_layout(
            template='plotly_dark',
            title_font=dict(size=24),
            xaxis_title_font=dict(size=18),
            yaxis_title_font=dict(size=18)
        )

        st.plotly_chart(all_tickers_fig)

elif st.session_state.page == "Página 3":
    st.title("Charts and Measures")
    
    # Filtro para seleccionar compañías
    ticker = st.multiselect(
        "Seleccionar Compañía",
        options=df_historical_prices["ticker"].unique(),
        default=[]
    )

    df_filtered = None
    drawdown_fig = None
    if ticker:
        df_filtered = df_historical_prices[df_historical_prices["ticker"].isin(ticker)]
        show_initial_graph = False

        period = st.sidebar.selectbox(
            "Select time period",
            options=["Daily", "Weekly", "Monthly"],
            key='time_period1'
        )

        if period == "Daily":
            df_grouped = df_filtered
        elif period == "Weekly":
            weekly_data = load_weekly_data()
            df_grouped = weekly_data[weekly_data["ticker"].isin(ticker)]
            df_grouped['date'] = pd.to_datetime(df_grouped['date'])
        elif period == "Monthly":
            monthly_data = load_monthly_data()
            df_grouped = monthly_data[monthly_data["ticker"].isin(ticker)]
            df_grouped['monthly'] = pd.to_datetime(df_grouped['monthly'])

        # Boxplot of closing prices
        if ticker:
            tickers_selected = ", ".join(ticker)
            col1, col2 = st.columns([1, 3])

            st.markdown(f"### Dispersion measurements for {tickers_selected}")

            with col1:
                st.markdown("""
    - **Minimum**: The lowest value.
    - **First quartile (Q1)**: bottom 25% of the data.
    - **Median (Q2)**: Divides the data into two halves.
    - **Third quartile (Q3)**: Top 25% of data.
    - **Maximum**: The highest value.

    The **outliers** are outside the expected range.
                """)

            with col2:
                fig = px.violin(df_grouped, x='ticker', y='close', box=True, points="all",
                                 title=f'Violin Chart of Closing Prices by Company ({tickers_selected})',
                                 labels={'close': 'Closing Prices', 'ticker': 'Company'})

                st.plotly_chart(fig)

            stats = df_grouped.groupby('ticker')['close'].agg(['mean', 'median', 'std', 'min', 'max']).reset_index()

            for index, row in stats.iterrows():
                 st.write(f"**Company:** {row['ticker']}")
                 st.write(f"Mean: {row['mean']:.2f}")
                 st.write(f"Median: {row['median']:.2f}")
                 st.write(f"Standard Deviation: {row['std']:.2f}")
                 st.write(f"Minimun: {row['min']:.2f}")
                 st.write(f"Maximun: {row['max']:.2f}")
                 st.write("---")  # Línea separadora

            line_fig = px.line(df_grouped, x='date', y='close', color='ticker',
                               title=f'Closing Prices {tickers_selected}',
                               labels={'close': 'Closing Prices', 'date': 'Year', 'ticker': 'Company'})
            line_fig.add_vrect(x0="2020-03-01", x1="2020-08-01", fillcolor="red", opacity=0.45, annotation_text="Covid-19    ")
            st.plotly_chart(line_fig)
            st.write("---")

            # RSI filter
            if ticker:  
                rsi_figs = [] 
                for selected_ticker in ticker:
                    df_rsi_filtered = df_filtered[df_filtered['ticker'] == selected_ticker]
                    df_rsi_filtered['RSI'] = calculate_rsi(df_rsi_filtered)

                    rsi_fig = px.line(df_rsi_filtered, x='date', y='RSI',
                                       title=f'Relative Strength Index (RSI) - {selected_ticker}',
                                       labels={'RSI': 'RSI', 'date': 'Date'})

                    rsi_fig.add_hline(y=70, line_color="red", line_dash="dash",
                                      annotation_text="Overbought",
                                      annotation_position="top right")
                    rsi_fig.add_hline(y=30, line_color="green", line_dash="dash",
                                      annotation_text="Oversold",
                                      annotation_position="bottom right")
                    
                    st.markdown("""The RSI (Relative Strength Index) is a technical indicator used in financial analysis to measure 
                            the speed and change of price movements, assessing whether an asset is overbought
                             or oversold. Its value ranges from 0 to 100, and levels above 70 are considered to indicate 
                            overbought, while levels below 30 suggest oversold. """)

                    rsi_figs.append(rsi_fig)

                for fig in rsi_figs:
                    st.plotly_chart(fig)

            if df_filtered is not None and not df_filtered.empty:
                st.header("ROI Calculation")
                selected_ticker = st.sidebar.selectbox("Select Company for ROI Calculation", df_filtered['ticker'].unique())
                roi_value = calculate_roi(historical_data, selected_ticker)
                if roi_value is not None:
                    st.write(f"ROI for {selected_ticker}: {roi_value:.2f}%")
                else:
                    st.write("No data available for selected ticker")

                price_fig = px.line(historical_data[historical_data["ticker"] == selected_ticker], x="date", y="close",
                                     title=f"Price Evolution - {selected_ticker}")
                
                st.markdown("""Return on Investment is a financial indicator that measures the profitability of an investment in relation to its cost.""")
                st.plotly_chart(price_fig)
                st.write("---")

                # Calcular drawdown
                drawdown_value, drawdown_df = calculate_drawdown(historical_data, selected_ticker)


                if drawdown_value is not None:
                    st.write(f"Maximum Drawdown for {selected_ticker}: {drawdown_value:.2f}%")
                else:
                    st.write("No data available for selected ticker")

                drawdown_fig = go.Figure()
                drawdown_fig.add_trace(go.Scatter(
                    x=drawdown_df['date'],
                    y=drawdown_df['drawdown'],
                    mode='lines',
                    name='Drawdown',
                    line=dict(color='blue')
                ))

                drawdown_fig.update_layout(
                    title=f"Drawdown Over Time for {selected_ticker}",
                    xaxis_title='Date',
                    yaxis_title='Drawdown (%)',
                    yaxis_tickformat=',.2f'
                )
                st.markdown("""It is a financial term that refers to the reduction in the value of an asset from its peak
                             to its subsequent low, indicating the maximum loss that an investor could experience in that period.""")

                st.plotly_chart(drawdown_fig)
                st.write("---")

                

                if df_filtered is not None and not df_filtered.empty:
                    st.header(f"Volatility for {tickers_selected}")

                    # Calcular y mostrar la volatilidad
                    col1, col2, col3 = st.columns(3)  # Se han utilizado 3 columnas para mostrar diferentes volatilidades

                    with col1:
                        daily_volatility = calculate_volatility(drawdown_df, period='daily')
                        if daily_volatility is not None:
                            st.write(f"Daily: {daily_volatility:.2f}")

                    with col2:
                        weekly_volatility = calculate_volatility(drawdown_df, period='weekly')
                        if weekly_volatility is not None:
                            st.write(f"Weekly: {weekly_volatility:.2f}")

                    with col3:
                        monthly_volatility = calculate_volatility(drawdown_df, period='monthly')
                        if monthly_volatility is not None:
                            st.write(f"Monthly: {monthly_volatility:.2f}")

                    st.markdown("""Is a statistical measure that reflects the variability or risk of the prices
                                   of a financial asset over a given period. An increase in volatility indicates greater
                                   fluctuations in price, which can mean higher investment risk.""")

elif st.session_state.page == "Página 4":
    st.title("📈Client dashboard")
    # Agregar contenido para la Página 4 aquí
    powerbi_string = '''
    <iframe title="yahoo finance" width="1140" height="541.25" 
    src="https://app.powerbi.com/reportEmbed?reportId=b1c0590e-12d2-48fb-8ed2-8563c607bcb9&autoAuth=true&ctid=5e73de35-e825-4ed5-be22-88563527091e" 
    frameborder="0" allowFullScreen="true"></iframe>
    '''
    st.markdown(powerbi_string, unsafe_allow_html=True)

elif st.session_state.page == "Página 5":
    st.title("About")
    # Agregar contenido para la Página 5 aquí
