import streamlit as st
from PIL import Image

# Título principal con margen inferior
st.header("· About us ·")
st.markdown("<div style='margin-bottom: 40px;'></div>", unsafe_allow_html=True)  # Espacio después del título

# Función para mostrar cada miembro del equipo con los botones
def mostrar_miembro_equipo(nombre, imagen_ruta, linkedin_url, github_url):
    st.image(imagen_ruta, use_column_width=True, caption=nombre)
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
        "/Users/DATA/Desktop/PFB-Equipo-A/Rosalia.jpg",
        "https://www.linkedin.com/in/rosaliacrespo/",
        "https://github.com/rosalia-ce"
    )

# Camilo
with col2:
    mostrar_miembro_equipo(
        "Camilo León",
        "/Users/DATA/Desktop/PFB-Equipo-A/Camilo.jpg",
        "https://www.linkedin.com/in/camilo-leon/",
        "https://github.com/andresvillafx"
    )

# Noemí
with col3:
    mostrar_miembro_equipo(
        "Noemí Hernando",
        "/Users/DATA/Desktop/PFB-Equipo-A/Noe.jpg",
        "https://www.linkedin.com/in/noemihernando/",
        "https://github.com/noehernando"
    )

# Añadir un espacio entre las secciones de fotos y tecnologías
st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)  # Espacio después de las fotos


st.subheader(" · CONCLUSION · ")
st.write("We have achieved the goal of creating a tool that allows us to use Yahoo Finance as a data source. We have focused on the technology stock market, and the Yahoo Finance API has enabled us to extract the necessary data to provide a concrete view of this market.")
st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)  # Espacio antes de la conclusión



st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)  # Espacio antes de la conclusión

