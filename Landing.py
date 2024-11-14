import streamlit as st
import pandas as pd
import numpy as np
import requests
from PIL import Image

# Cargar la imagen 
image_path = '/Users/DATA/Desktop/PFB-Equipo-A/yfinance.png'  
image = Image.open(image_path)

# Crear columnas para centrar la imagen
col1, col2, col3 = st.columns([1, 2, 1]) 

# Colocar la imagen en la columna del medio
with col2:
    st.image(image, width=300)  

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
st.markdown('<div class="section-title"> · Yahoo Finance</div>', unsafe_allow_html=True)
st.markdown('<div class="section-content";">Yahoo Finance is a toolkit that allows you to track the stocks you’re interested in, create watchlists, and set up multiple portfolios based on your actual potential, fantasy values, or linked brokerage account portfolios (as applicable)</div>', unsafe_allow_html=True)


##############2
st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)  

st.markdown('<div class="section-title"> · Introduction</div>', unsafe_allow_html=True)
st.markdown('<div class="section-content";">This project aims to build an interactive tool for the analysis of stocks in the technology market, using the Yahoo Finance API as the primary source for extracting financial data. By utilizing Python, Streamlit, Power BI, and various data analysis libraries, this project implements an application that allows users to access key information about companies in the technology sector, visualize market trends, and perform personalized analysis through an interactive and easy-to-navigate interface.</div>', unsafe_allow_html=True)



##############3
import streamlit as st

# Contenido con títulos en negro y el contenido en gris
st.markdown("""
1. **Integration with Yahoo Finance API**:  
   <p style="color:gray;">We use the Yahoo Finance API to extract updated financial data from key companies such as NVIDIA (NVDA), Dell (DELL), Microsoft (MSFT), Oracle (ORCL), and ABBGO. This integration provides access to historical and current data on stock prices, volatility, market capitalization, among other indicators.</p>

2. **Data Processing and Manipulation**:  
   <p style="color:gray;">Once the financial data is extracted, we process and clean it. We normalize time series, calculate custom metrics, and filter data based on relevant criteria. These tools allow us to prepare the data for exploratory analysis, statistical calculations, and dynamic visualizations, ensuring consistency and accuracy in the results presented.</p>

3. **Data Visualization**:  
   <p style="color:gray;">The visualization is developed using Streamlit to present financial data in a visual and intuitive way. We have integrated line graphs for historical price trends, scatter plots to analyze correlations between variables, and bar charts, among others, to compare key metrics between selected companies. Additionally, Power BI is used to offer advanced interactive dashboards that summarize the main findings of the analysis.</p>

4. **User and Client Interface**:  
   <p style="color:gray;">The interface is designed to allow users with varying levels of experience to navigate through different sections of the application, including:
   - Yahoo Finance Data Visualization
   - Technology Sector Analysis
   - Team Profile and Contact</p>
""", unsafe_allow_html=True)

########
st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True) 

st.subheader(" · Technologies we have used:")

st.write("""
- **Streamlit**
- **Python**
- **NumPy**
- **Pandas**
- **Power BI**
- **Yahoo Finance API**
- **SQL**
""")      

