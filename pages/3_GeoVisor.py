import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from branca.colormap import LinearColormap

st.set_page_config(
    page_title="Zonas no interconectadas",    
    layout="wide"
    )

logo= "logo_talentotech.webp"
st.logo(logo, size="large")

st.sidebar.image(logo,use_container_width=True)

zni_data = pd.read_csv("datos/zni_geodata.csv") 

no_convencionales = pd.read_csv("datos/no_convencionales_geo.csv")

# Conversión segura
zni_data["LATITUD"] = pd.to_numeric(zni_data["LATITUD"], errors="coerce")
zni_data["LONGITUD"] = pd.to_numeric(zni_data["LONGITUD"], errors="coerce")
zni_data["ENERGÍA ACTIVA"] = pd.to_numeric(zni_data["ENERGÍA ACTIVA"], errors="coerce")
zni_data["POTENCIA MÁXIMA"] = pd.to_numeric(zni_data["POTENCIA MÁXIMA"], errors="coerce")

# UI general
st.title("Comparativo Geográfico: ZNI vs Energías No Convencionales")
col1, col2 = st.columns(2)

# --- Columna izquierda: Mapa ZNI ---
with col1:
    st.subheader("🔌 Mapa ZNI: Energía Activa y Potencia Máxima")

    # Año dentro del bloque
    año = st.selectbox("Selecciona un año", sorted(zni_data["AÑO SERVICIO"].dropna().unique()), key="año_zni")
    
    st.info(
        "Este mapa muestra las zonas no interconectadas (ZNI) con círculos proporcionales al consumo de energía activa "
        "y un color que representa la potencia máxima instalada. Ideal para visualizar intensidad y cobertura por ubicación."
    )

    # Filtrado
    df_zni = zni_data[
        (zni_data["AÑO SERVICIO"] == año) &
        zni_data["LATITUD"].notna() &
        zni_data["LONGITUD"].notna() &
        zni_data["ENERGÍA ACTIVA"].notna() &
        zni_data["POTENCIA MÁXIMA"].notna()
    ].copy()

    # Escalado de tamaño por energía activa
    min_r, max_r = 5, 15
    energia_norm = (df_zni["ENERGÍA ACTIVA"] - df_zni["ENERGÍA ACTIVA"].min()) / (
        df_zni["ENERGÍA ACTIVA"].max() - df_zni["ENERGÍA ACTIVA"].min()
    )
    df_zni["RADIO"] = energia_norm * (max_r - min_r) + min_r

    # Escala de color viridis para potencia máxima
    colormap = LinearColormap(
        colors=["#440154", "#3b528b", "#21918c", "#5ec962", "#fde725"],
        vmin=df_zni["POTENCIA MÁXIMA"].min(),
        vmax=df_zni["POTENCIA MÁXIMA"].max(),
        caption="Potencia Máxima (kW)"
    )

    # Crear mapa
    mapa_zni = folium.Map(location=[df_zni["LATITUD"].mean(), df_zni["LONGITUD"].mean()], zoom_start=6)

    for _, row in df_zni.iterrows():
        popup = f"""
        <b>Departamento:</b> {row['DEPARTAMENTO']}<br>
        <b>Municipio:</b> {row.get('MUNICIPIO', 'N/D')}<br>
        <b>Energía Activa:</b> {row['ENERGÍA ACTIVA']:,.0f} kWh<br>
        <b>Potencia Máxima:</b> {row['POTENCIA MÁXIMA']:,.0f} kW
        """
        folium.CircleMarker(
            location=[row["LATITUD"], row["LONGITUD"]],
            radius=row["RADIO"],
            color=colormap(row["POTENCIA MÁXIMA"]),
            fill=True,
            fill_opacity=0.85,
            popup=folium.Popup(popup, max_width=300)
        ).add_to(mapa_zni)

    colormap.add_to(mapa_zni)
    folium_static(mapa_zni, width=750, height=650)

# --- Columna derecha: Energías No Convencionales ---
with col2:
    st.subheader("⚡ Mapa de Energías No Convencionales por Tipo")
    st.info("Este mapa muestra los proyectos no convencionales con íconos específicos según el tipo de energía: ☀️ solar, 🌬️ eólica, 🔋 híbrida o 🔎 otros.")

    # Filtrar proyectos válidos con coordenadas
    df_nc = no_convencionales[
        no_convencionales["LATITUD"].notna() &
        no_convencionales["LONGITUD"].notna() &
        no_convencionales["Tipo"].notna()
    ].copy()

    # Diccionario de íconos por tipo
    iconos = {
    "solar": "star",
    "eólico": "leaf",
    "híbrido": "flash",
    "biomasa": "fire",
    "otro": "info-sign"
    }


    # Normalizar nombres
    df_nc["Tipo"] = df_nc["Tipo"].str.lower().str.strip()

    # Asignar ícono
    df_nc["icono"] = df_nc["Tipo"].map(iconos).fillna("info-sign")

    # Crear mapa
    mapa_nc = folium.Map(location=[df_nc["LATITUD"].mean(), df_nc["LONGITUD"].mean()], zoom_start=6)

    for _, row in df_nc.iterrows():
        popup = f"""
        <b>Proyecto:</b> {row['Proyecto']}<br>
        <b>Tipo:</b> {row['Tipo'].capitalize()}<br>
        <b>Departamento:</b> {row.get('Departamento', 'N/D')}<br>
        <b>Capacidad:</b> {row.get('Capacidad', 0):,.0f} kW<br>
        <b>Energía:</b> {row.get('Energía [kWh/día]', 0):,.0f} kWh/día
        """
        folium.Marker(
            location=[row["LATITUD"], row["LONGITUD"]],
            popup=popup,
            icon=folium.Icon(color="green", icon=row["icono"], prefix="glyphicon")
        ).add_to(mapa_nc)

    folium_static(mapa_nc, width=750, height=650)




