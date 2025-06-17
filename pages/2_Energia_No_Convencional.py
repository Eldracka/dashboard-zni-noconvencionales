import streamlit as st
import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt

import locale

st.set_page_config(
    page_title="Energias no convencionales",
    page_icon=":material/edit:",
    layout="wide"
)

logo= "logo_talentotech.webp"
st.logo(logo, size="large")

st.sidebar.image(logo,use_container_width=True)

# Establecer configuración regional a español para usar punto como separador de miles
try:
    locale.setlocale(locale.LC_ALL, "es_CO.UTF-8")
except:
    locale.setlocale(locale.LC_ALL, "")  # Fallback si la localización exacta no está disponible

st.title("Energías No Convencionales")

no_convencionales = pd.read_csv("datos/Fuentes_No_Convencionales_de_Energ_a_Renovable.csv")



# Asegurar que la columna de energía sea numérica
no_convencionales["Energía [kWh/día]"] = pd.to_numeric(
    no_convencionales["Energía [kWh/día]"], errors="coerce"
)

# 🔎 Departamentos válidos (energía > 0 por tipo)
dep_solar_validos = (
    no_convencionales[no_convencionales["Tipo"].str.lower() == "solar"]
    .groupby("Departamento")["Energía [kWh/día]"]
    .sum()
    .loc[lambda x: x > 0]
    .index.tolist()
)

dep_total_validos = (
    no_convencionales.groupby("Departamento")["Energía [kWh/día]"]
    .sum()
    .loc[lambda x: x > 0]
    .index.tolist()
)

dep_eolico_validos = (
    no_convencionales[no_convencionales["Tipo"].str.lower() == "eólico"]
    .groupby("Departamento")["Energía [kWh/día]"]
    .sum()
    .loc[lambda x: x > 0]
    .index.tolist()
)

# 🧊 Visual elegante en 3 columnas
st.markdown("### ⚡ Energía por Departamento y Tipo (con proyectos)")
col1, col2, col3 = st.columns(3, border=True)

with col1:
    st.subheader("☀️ Solar", divider="orange")
    dep_solar = st.selectbox("Departamento", dep_solar_validos, key="solar")
    filtro_solar = (no_convencionales["Departamento"] == dep_solar) & (
        no_convencionales["Tipo"].str.lower() == "solar"
    )
    energia_solar = no_convencionales.loc[filtro_solar, "Energía [kWh/día]"].sum()
    proyectos_solar = no_convencionales.loc[filtro_solar, "Proyecto"].nunique()
    
    valor_formateado = locale.format_string("%.0f", energia_solar, grouping=True)
    st.metric(label="Energía Solar", value=f"{valor_formateado} kWh/día", delta=f"{proyectos_solar} proyectos")

with col2:
    st.subheader("🔁 Total", divider="blue")
    dep_total = st.selectbox("Departamento", dep_total_validos, key="total")
    filtro_total = no_convencionales["Departamento"] == dep_total
    energia_total = no_convencionales.loc[filtro_total, "Energía [kWh/día]"].sum()
    proyectos_total = no_convencionales.loc[filtro_total, "Proyecto"].nunique()
    st.metric(label="Energía Total", value=f"{energia_total:,.0f} kWh/día", delta=f"{proyectos_total} proyectos")

with col3:
    st.subheader("🌬️ Eólica", divider="gray")
    dep_eolico = st.selectbox("Departamento", dep_eolico_validos, key="eolico")
    filtro_eolico = (no_convencionales["Departamento"] == dep_eolico) & (
        no_convencionales["Tipo"].str.lower() == "eólico"
    )
    energia_eolica = no_convencionales.loc[filtro_eolico, "Energía [kWh/día]"].sum()
    proyectos_eolico = no_convencionales.loc[filtro_eolico, "Proyecto"].nunique()
    st.metric(label="Energía Eólica", value=f"{energia_eolica:,.0f} kWh/día", delta=f"{proyectos_eolico} proyectos")



st.write("------------------------------------------------------------------------------------")

# Asegurar que las columnas relevantes sean numéricas
no_convencionales["Capacidad"] = pd.to_numeric(no_convencionales["Capacidad"], errors="coerce")
no_convencionales["Energía [kWh/día]"] = pd.to_numeric(no_convencionales["Energía [kWh/día]"], errors="coerce")

# Eliminar filas con datos faltantes en las columnas clave
df_corr = no_convencionales[["Capacidad", "Energía [kWh/día]", "Tipo"]].dropna()

# Calcular la correlación numérica
correlacion = df_corr["Capacidad"].corr(df_corr["Energía [kWh/día]"])

# Título
#st.title("📈 Correlación entre Capacidad y Energía [kWh/día]")
st.markdown("### 📈 Correlación entre Capacidad y Energía [kWh/día]")
st.write(f"**Coeficiente de correlación de Pearson**: {correlacion:.3f}")

# Gráfico de dispersión con ajuste de tendencia
fig, ax = plt.subplots(figsize=(8, 6))
sns.scatterplot(data=df_corr, x="Capacidad", y="Energía [kWh/día]", hue="Tipo", palette="tab10", ax=ax)
sns.regplot(data=df_corr, x="Capacidad", y="Energía [kWh/día]", scatter=False, color="gray", ax=ax, line_kws={"label": "Tendencia global"})

ax.set_title("Relación: Capacidad vs Energía Diaria")
ax.legend()
st.pyplot(fig)
