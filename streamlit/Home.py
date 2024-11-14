import streamlit as st
from PIL import Image
import numpy as np
import mysql
import mysql.connector
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import plotly.figure_factory as ff
import requests


@st.cache_data
def load_monthly_data():
    return pd.read_csv('C:/Users/rce_5/OneDrive/Escritorio/proyecto/PFB-Equipo-A/streamlit/data/monthly_historical.csv')

@st.cache_data
def load_weekly_data():
    return pd.read_csv('C:/Users/rce_5/OneDrive/Escritorio/proyecto/PFB-Equipo-A/streamlit/data/weekly_historical.csv')

st.set_page_config(page_title="Yahoo Finance", page_icon="📈", layout="wide")

def create_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Hackaboss_2024',
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

st.sidebar.markdown("""
    <style>
        section[data-testid="stSidebar"] button {
            color: black !important;
            background-color: white !important;
            border: 1px solid #ccc !important;
            border-radius: 8px !important;
            padding: 8px 20px !important;
            margin-bottom: 10px !important;
        }
    </style>
    """, unsafe_allow_html=True)

st.sidebar.markdown("<h1 style='text-align: center; color: white;'>🚀Menu</h1>", unsafe_allow_html=True)


# Estilo para los títulos
title_style = """
    <style>
        .custom-title {
            font-size: 24px; /* Ajusta el tamaño aquí */
            font-weight: bold;
            color: #333;
        }
    </style>
"""
st.markdown(title_style, unsafe_allow_html=True)

if 'page' not in st.session_state:
    st.session_state.page = "Página 1"

# Botones de navegación en la barra lateral
if st.sidebar.button("🌐Overview", key="btn1", help="Go to Home"):
    st.session_state.page = "Página 1"

if st.sidebar.button("📊Charts and Measures", key="btn3", help="Go to Charts and Measures"):
    st.session_state.page = "Página 3"

if st.sidebar.button("🧑‍💻Client Dashboard", key="btn4", help="Go to Client Dashboard"):
    st.session_state.page = "Página 4"

if st.sidebar.button("👩‍🔧About", key="btn5", help="Go to About"):
    st.session_state.page = "Página 5"

if st.session_state.page == "Página 1":
    st.title("Overview")
    # Agregar contenido para la Página 1 aquí

    # Cargar la imagen 
    image_path = 'C:/Users/rce_5/OneDrive/Escritorio/proyecto/PFB-Equipo-A/streamlit/data/Banner.png'  
    image = Image.open(image_path)

    # Crear columnas para centrar la imagen
    col1, col2, col3 = st.columns([1, 2, 1]) 

    # Colocar la imagen en la columna del medio
    with col2:
        st.image(image, width=700)  

        ###########Separar las partes
        st.markdown("""
            <style>
            .section-title {
                margin-top: 40px;
                margin-bottom: 20px;
                font-size: 24px;
                font-weight: bold;
            }
            .section-content {
                margin-bottom: 40px;
                font-size: 16px;
            }
            </style>
        """, unsafe_allow_html=True)

        ##############1
        st.markdown('<div class="section-title">Yahoo Finance</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-content";">Yahoo Finance is a toolkit that allows you to track the stocks you’re interested in, create watchlists, and set up multiple portfolios based on your actual potential, fantasy values, or linked brokerage account portfolios (as applicable).</div>', unsafe_allow_html=True)


        if show_initial_graph and not df_historical_prices.empty:
                    all_tickers_fig = px.line(df_historical_prices, x='date', y='close', color='ticker',
                                            title='Stock price evolution',
                                            labels={'close': 'Closing Price($)', 'date': 'Year', 'ticker': 'Company'})
                    all_tickers_fig.update_layout(
                        template='plotly_dark',
                        title_font=dict(size=24),
                        xaxis_title_font=dict(size=18),
                        yaxis_title_font=dict(size=18))

                    st.plotly_chart(all_tickers_fig)

        ##############2
        #st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)  
        st.markdown('<div class="section-title">The Yahoo Finance Project</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-content";">This project aims to build an interactive tool for the analysis of stocks in the technology market, using the Yahoo Finance API as the primary source for extracting financial data. By utilizing Python, Streamlit, Power BI, and various data analysis libraries, this project implements an application that allows users to access key information about companies in the technology sector, visualize market trends, and perform personalized analysis through an interactive and easy-to-navigate interface.</div>', unsafe_allow_html=True)

        ##############3
        # Contenido con títulos en negro y el contenido en gris
        st.markdown("""
        **1. Integration with Yahoo Finance API**  
        <p>We use the Yahoo Finance API to extract updated financial data from top companies such as NVIDIA (NVDA) or Microsoft (MSFT). This integration provides access to historical and current data on stock prices, volatility, market capitalization, among other indicators.</p>

        **2. Data Processing and Manipulation**
        <p>Once the financial data is extracted, we process and clean it. We normalize time series, calculate custom metrics, and filter data based on relevant criteria. These tools allow us to prepare the data for exploratory analysis, statistical calculations, and dynamic visualizations, ensuring consistency and accuracy in the results presented.</p>

        **3. Data Visualization**
        <p>The visualization is developed using Streamlit to present financial data in a visual and intuitive way. We have integrated line graphs for historical price trends, scatter plots to analyze correlations between variables, and bar charts, among others, to compare key metrics between selected companies. Additionally, Power BI is used to offer advanced interactive dashboards that summarize the main findings of the analysis.</p>

        **4. User and Client Interface**
        <p>The interface is designed to allow users with varying levels of experience to navigate through different sections of the application, including:
        - Yahoo Finance Data Visualization
        - Technology Sector Analysis
        - Team Profile and Contact</p>
        """, unsafe_allow_html=True)

        ########
        st.markdown('<div class="section-title">Technologies used</div>', unsafe_allow_html=True)

        st.write("""
        - **Yahoo Finance API**
        - **Streamlit**
        - **Python**
        - **NumPy**
        - **Pandas**
        - **Plotly**
        - **Power BI**
        - **SQL**
        """)   

elif st.session_state.page == "Página 3":
    st.title("Charts and Measures")
    
    # Filtro para seleccionar compañías
    ticker = st.multiselect(
        "Select company",
        options=df_historical_prices["ticker"].unique(),
        default=[])

    df_filtered = None
    drawdown_fig = None
    if ticker:
        df_filtered = df_historical_prices[df_historical_prices["ticker"].isin(ticker)]
        show_initial_graph = False

        period = st.sidebar.selectbox(
            "Select time period",
            options=["Daily", "Weekly", "Monthly"],
            key='time_period1')

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
            col1, col2 = st.columns([1, 2])

            with col1:
                st.markdown(f'<div class="custom-title">Violin Chart of Closing Prices</div>', unsafe_allow_html=True)
                st.markdown("""                                     
                - **Minimum**: The lowest value.
                - **First quartile (Q1)**: Bottom 25% of the data.
                - **Median (Q2)**: Divides the data into two halves.
                - **Third quartile (Q3)**: Top 25% of data.
                - **Maximum**: The highest value.

                The **outliers** are outside the expected range.
                            """)

            with col2:
                fig = px.violin(df_grouped, x='ticker', y='close', box=True, points="all",
                            labels={'close': 'Closing Prices', 'ticker': 'Company'})

                st.plotly_chart(fig)

            stats = df_grouped.groupby('ticker')['close'].agg(['mean', 'median', 'std', 'min', 'max']).reset_index()

            st.markdown(f'<div class="custom-title">Dispersion Measurements</div>', unsafe_allow_html=True)

            for index, row in stats.iterrows():
                 st.write(f"**- Company**: {row['ticker']}")
                 st.write(f" **Mean**: {row['mean']:.2f}")
                 st.write(f" **Median**: {row['median']:.2f}")
                 st.write(f" **Standard Deviation**: {row['std']:.2f}")
                 st.write(f" **Minimun**: {row['min']:.2f}")
                 st.write(f" **Maximun**: {row['max']:.2f}")
                 st.write("")

            line_fig = px.line(df_grouped, x='date', y='close', color='ticker',
                   labels={'close': 'Closing Prices', 'date': 'Year', 'ticker': 'Company'},
                   title=f'Closing Prices for {tickers_selected} during Covid-19')  # Añadido el título con los tickers seleccionados

            line_fig.add_vrect(x0="2020-03-01", x1="2020-08-01", fillcolor="red", opacity=0.45, annotation_text="Covid-19    ")
            
            st.plotly_chart(line_fig)
            st.write("---")

            # RSI filter
            st.markdown(f'<div class="custom-title">Relative Strength Index (RSI)</div>', unsafe_allow_html=True)
            st.markdown("""The RSI (Relative Strength Index) is a technical indicator used in financial analysis to measure 
                            the speed and change of price movements, assessing whether an asset is overbought
                             or oversold. Its value ranges from 0 to 100, and levels above 70 are considered to indicate 
                            overbought, while levels below 30 suggest oversold. """)

            if ticker:  
                rsi_figs = [] 
                for selected_ticker in ticker:
                    df_rsi_filtered = df_filtered[df_filtered['ticker'] == selected_ticker]
                    df_rsi_filtered['RSI'] = calculate_rsi(df_rsi_filtered)

                    rsi_fig = px.line(df_rsi_filtered, x='date', y='RSI', 
                                      labels={'RSI': 'RSI', 'date': 'Date'},
                                      title=f'RSI for {selected_ticker}')  # Añadido el título con el ticker

                    rsi_fig.add_hline(y=70, line_color="red", line_dash="dash",
                                      annotation_text="Overbought",
                                      annotation_position="top right")
                    rsi_fig.add_hline(y=30, line_color="green", line_dash="dash",
                                      annotation_text="Oversold",
                                      annotation_position="bottom right")

                    rsi_figs.append(rsi_fig)

                for fig in rsi_figs:
                    st.plotly_chart(fig)

                st.write("---")


            df_pivot = df_filtered.pivot(index='date', columns='ticker', values='close')
            correlation_matrix = df_pivot.corr()

        # Display correlation matrix
            st.header("Correlation Analysis")
            st.markdown("""This metric measures the relationship between two variables to understand how they move together. """)

            # Redondear los valores a dos decimales
            text_values = np.round(correlation_matrix.values * 100, 2).astype(str)  # Multiplicado por 100 si deseas porcentaje

                #text_values = np.char.add(text_values, '%')


                    # Heatmap for correlation
            fig_heatmap = ff.create_annotated_heatmap(correlation_matrix.values, 
                                                                x=list(correlation_matrix.columns), 
                                                                y=list(correlation_matrix.index),
                                                                colorscale='Blues', 
                                                                showscale=True,
                                                                text= text_values,
                                                                hoverinfo='text'
                )

            fig_heatmap.update_layout(
                title='Correlation Heatmap',
                xaxis_title='Companies',
                yaxis_title='Companies')


            st.plotly_chart(fig_heatmap)

            st.write("---")


            st.title("Detailed Calculations")    

            
            if df_filtered is not None and not df_filtered.empty:
                st.markdown('<div class="custom-title">ROI Calculation</div>', unsafe_allow_html=True)
                st.markdown("""Return on Investment is a financial indicator that measures the profitability of an investment in relation to its cost.""")
                
                selected_ticker = st.sidebar.selectbox("Select Company for Detailed Calculations", df_filtered['ticker'].unique())
                roi_value = calculate_roi(historical_data, selected_ticker)
                if roi_value is not None:
                    st.write(f"**ROI for {selected_ticker}**: {roi_value:.2f}%")
                else:
                    st.write("No data available for selected ticker")

                st.write("---")

                
                # Calcular drawdown
                drawdown_value, drawdown_df = calculate_drawdown(historical_data, selected_ticker)

                drawdown_fig = go.Figure()
                drawdown_fig.add_trace(go.Scatter(
                    x=drawdown_df['date'],
                    y=drawdown_df['drawdown'],
                    mode='lines',
                    name='Drawdown',
                    line=dict(color='CornflowerBlue')
                ))

                st.markdown(f'<div class="custom-title">Drawdown Over Time</div>', unsafe_allow_html=True)

                drawdown_fig.update_layout(
                    xaxis_title='Date',
                    yaxis_title='Drawdown (%)',
                    yaxis_tickformat=',.2f',
                    title=f'Drawdown Over Time for {selected_ticker}'  # Añadido el título con el ticker
                )
                st.markdown("""It is a financial term that refers to the reduction in the value of an asset from its peak
                             to its subsequent low, indicating the maximum loss that an investor could experience in that period.""")

                if drawdown_value is not None:
                    st.write(f"**Maximum Drawdown for {selected_ticker}**: {drawdown_value:.2f}%")
                else:
                    st.write("No data available for selected ticker")

                st.plotly_chart(drawdown_fig)
                st.write("---")

                if df_filtered is not None and not df_filtered.empty:
                    st.markdown(f'<div class="custom-title">Volatility</div>', unsafe_allow_html=True)

                    st.markdown("""It is a statistical measure that reflects the variability or risk of the prices
                                   of a financial asset over a given period. An increase in volatility indicates greater
                                   fluctuations in price, which can mean higher investment risk.""")

                    # Calcular y mostrar la volatilidad
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        daily_volatility = calculate_volatility(drawdown_df, period='daily')
                        if daily_volatility is not None:
                            st.write(f"**{selected_ticker} Daily Volatility**: {daily_volatility:.2f}")

                    with col2:
                        weekly_volatility = calculate_volatility(drawdown_df, period='weekly')
                        if weekly_volatility is not None:
                            st.write(f"**{selected_ticker} Weekly Volatility**: {weekly_volatility:.2f}")

                    with col3:
                        monthly_volatility = calculate_volatility(drawdown_df, period='monthly')
                        if monthly_volatility is not None:
                            st.write(f"**{selected_ticker} Monthly Volatility**: {monthly_volatility:.2f}")
                st.write("---")


  



elif st.session_state.page == "Página 4":
    st.title("🧑‍💻Client Dashboard")
    # Agregar contenido para la Página 4 aquí
    powerbi_string = '''
    <iframe title="yahoo finance" width="1280" height="720" 
    src="https://app.powerbi.com/view?r=eyJrIjoiMmE2YzMwODQtYWY0ZS00ODE2LWFlZjItZjFmNTBkMTgzNzc5IiwidCI6IjVlNzNkZTM1LWU4MjUtNGVkNS1iZTIyLTg4NTYzNTI3MDkxZSIsImMiOjl9&pageName=63d0211de84c967664b9" 
    frameborder="0" allowFullScreen="true"></iframe>
    '''
    st.markdown(powerbi_string, unsafe_allow_html=True)

elif st.session_state.page == "Página 5":
    st.title("About")
    # Agregar contenido para la Página 5 aquí
    st.header(" · Conclusion · ")
    st.write("We have achieved the goal of creating a tool that allows us to use Yahoo Finance as a data source. We have focused on the technology stock market, and the Yahoo Finance API has enabled us to extract the necessary data to provide a concrete view of this market.")

    # Título principal con margen inferior
    st.header("· Our Team ·")
    st.markdown("<div style='margin-bottom: 40px;'></div>", unsafe_allow_html=True)  # Espacio después del título

    # Función para mostrar cada miembro del equipo con los botones
    def mostrar_miembro_equipo(nombre, imagen_ruta, linkedin_url, github_url, image_width=300):
        st.image(imagen_ruta, use_column_width=False, width=image_width, caption=nombre)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f'<a href="{linkedin_url}" target="_blank" style="display: inline-block; text-align: center; padding: 8px 16px; border: none; border-radius: 5px; background-color: #0A66C2; color: white; text-decoration: none;">LinkedIn</a>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<a href="{github_url}" target="_blank" style="display: inline-block; text-align: center; padding: 8px 16px; border: none; border-radius: 5px; background-color: #333; color: white; text-decoration: none;">GitHub</a>', unsafe_allow_html=True)

    # Organizar las fotos en columnas
    col1, col2, col3 = st.columns(3)

    # Rosalía
    with col1:
        mostrar_miembro_equipo(
            "Rosalía Crespo",
            "C:/Users/rce_5/OneDrive/Escritorio/proyecto/PFB-Equipo-A/streamlit/data/Rosalia.jpg",
            "https://www.linkedin.com/in/rosaliacrespo/",
            "https://github.com/rosalia-ce"
        )

    # Camilo
    with col2:
        mostrar_miembro_equipo(
            "Camilo León",
            "C:/Users/rce_5/OneDrive/Escritorio/proyecto/PFB-Equipo-A/streamlit/data/Camilo.jpg",
            "https://www.linkedin.com/in/camilo-leon/",
            "https://github.com/andresvillafx"
        )

    # Noemí
    with col3:
        mostrar_miembro_equipo(
            "Noemí Hernando",
            "C:/Users/rce_5/OneDrive/Escritorio/proyecto/PFB-Equipo-A/streamlit/data/Noe.jpg",
            "https://www.linkedin.com/in/noemihernando/",
            "https://github.com/noehernando"
        )

    # Añadir un espacio entre las secciones de fotos y tecnologías
    st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)  # Espacio después de las fotos

   
    st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)  # Espacio antes de la conclusión