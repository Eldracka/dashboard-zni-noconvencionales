import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import locale

st.set_page_config(
    page_title="Zonas no interconectadas ZNI",    
    layout="wide"
    )

logo= "logo_talentotech.webp"
st.logo(logo, size="large")

st.sidebar.image(logo,use_container_width=True)
# Establecer configuración regional a español para usar punto como separador de miles
try:
    locale.setlocale(locale.LC_ALL, 'es_CO.UTF-8')  # Colombia
except:
    locale.setlocale(locale.LC_ALL, '')  # fallback si no está disponible

st.title("Zonas no interconectadas ZNI")

# importar dataset limpiado
zni_data = pd.read_csv("datos/zni_geodata.csv") #----REMPLAZAR POR EL LIMPIO

# procesar datos selecciona los departamentos y los guarda, al igual que los años del dataset
departamentos = sorted(zni_data["DEPARTAMENTO"].dropna().unique())
municipios = sorted(zni_data["MUNICIPIO"].dropna().unique())
years = sorted(zni_data["AÑO SERVICIO"].dropna().unique())


# Interfaz de usuario card columnas
col1, col2, col3 = st.columns(3, border=True)

with col1:
    st.subheader("📊 Energía Total por Departamento", divider="blue")
        
    colA, colB = st.columns(2)
    with colA:
        dep_seleccionado = st.selectbox("Selecciona un departamento", departamentos)
    with colB:
        year_seleccionado = st.selectbox("Selecciona un año de servicio", years, key="depar")
    
    #Filtrar y calcular total
    filtro = (zni_data["DEPARTAMENTO"] == dep_seleccionado) & (zni_data["AÑO SERVICIO"] == year_seleccionado)
    energia_total = zni_data.loc[filtro, "ENERGÍA ACTIVA"].sum()
    energia_total = locale.format_string("%.0f",energia_total, grouping=True)

    st.metric(label="ENERGÍA ACTIVA TOTAL", value=f"{energia_total} kWh")
    filtro2 = zni_data[filtro].shape[0]
    #st.markdown(f":red[meses contados] {filtro2}")
    
with col2:
    st.subheader("🔋 Energía Activa Total por Año (Zonas No Interconectadas)", divider="green")    
    year_seleccionado_total = st.selectbox("Selecciona un año de servicio", years, key="total")
    total_energia = zni_data[zni_data["AÑO SERVICIO"] == year_seleccionado_total]["ENERGÍA ACTIVA"].sum()
    total_energia = locale.format_string("%.0f",total_energia, grouping=True)
    st.metric("ENERGIA ACTIVA TOTAL POR AÑO", value=f"{total_energia:} kWh")
    

with col3:
    st.subheader("🏡 Detalle Energético por Municipio (ZNI)", divider="orange")
    colC, colD = st.columns(2)
    with colC:
        mun_seleccionado = st.selectbox("Selecciona un municipio", municipios)
    with colD:
        year_seleccionado = st.selectbox("Selecciona un año de servicio", years, key="munic")

    filtro = (zni_data["MUNICIPIO"] == mun_seleccionado) & (zni_data["AÑO SERVICIO"] == year_seleccionado)
    energia_total = zni_data.loc[filtro, "ENERGÍA ACTIVA"].sum()
    energia_total = locale.format_string("%.0f",energia_total, grouping=True)
    st.metric(label="ENERGÍA ACTIVA TOTAL", value=f"{energia_total} kWh")



#st.title("Energía Activa por Departamento (Filtrado por Año)")
st.divider()
st.markdown("## Energía Activa por Departamento (Filtrado por Año)")
año_seleccionado = st.selectbox("Selecciona un año", years, key="graficDep")


# Agrupar por departamento y sumar energía activa
# Filtrar por año seleccionado
df_filtrado = zni_data[zni_data["AÑO SERVICIO"] == año_seleccionado]

# Agrupar y ordenar
# Agrupar por departamento y excluir los totales en cero
energia_por_dep = (
    df_filtrado.groupby("DEPARTAMENTO")["ENERGÍA ACTIVA"]
    .sum()
    .loc[lambda x: x > 0]  # Filtrar donde el total sea mayor a 0
    .sort_values(ascending=True)
)


st.bar_chart(energia_por_dep, horizontal=True, y_label="Departamento", x_label="Energía Activa")
#st.write(energia_por_dep)

