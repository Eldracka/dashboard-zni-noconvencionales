import streamlit as st
import locale

st.set_page_config(
    page_title="Home",
    page_icon="👋",
    layout="wide"
)

logo= "logo_talentotech.webp"
st.logo(logo, size="large")

st.sidebar.image(logo,use_container_width=True)

try:
    locale.setlocale(locale.LC_ALL, 'es_CO.UTF-8')  # Colombia
except:
    locale.setlocale(locale.LC_ALL, '')  # fallback si no está disponible

st.write("## Visualización Geográfica de Energía en Colombia: Zonas No Interconectadas y Energías No Convencionales")

#st.sidebar.success("Selecciona una pagina en el menú")

st.markdown(
    """
    Este dashboard presenta una visualización interactiva sobre el comportamiento energético de las Zonas No Interconectadas (ZNI) en Colombia entre 2020 y 2025. Además, incluye información clave sobre proyectos de generación a partir de fuentes no convencionales, como la energía solar, eólica y biomasa, evidenciando su distribución geográfica y su aporte a la transición energética del país.
    
"""
)

st.image("portada.png", use_container_width=True)