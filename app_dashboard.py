import streamlit as st
import pandas as pd
import requests

# Configuración de la página web
st.set_page_config(
    page_title="Dashboard de Estadísticas Públicas",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Panel Estadístico de Datos Públicos con Python")
st.markdown("Este dashboard interactivo procesa en tiempo real información demográfica y la presenta de forma visual.")

# Función para cargar y cachear los datos públicos
@st.cache_data
def cargar_datos():
    url = "https://jsonplaceholder.typicode.com/users" # O tu API de preferencia
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        registros = []
        for usuario in data:
            company = usuario.get("company", {})
            address = usuario.get("address", {})
            registros.append({
                "Nombre": usuario.get("name", "N/A"),
                "Ciudad": address.get("city", "N/A"),
                "Empresa": company.get("name", "N/A"),
                "Email": usuario.get("email", "N/A")
            })
        return pd.DataFrame(registros)
    return pd.DataFrame()

# Cargamos el DataFrame
df = cargar_datos()

if not df.empty:
    # 1. Métricas principales (KPIs en tarjetas visuales)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total de Registros", value=len(df))
    with col2:
        st.metric(label="Ciudades Únicas", value=df["Ciudad"].nunique())
    with col3:
        st.metric(label="Empresas Asociadas", value=df["Empresa"].nunique())

    st.markdown("---")

    # 2. Filtro interactivo en la barra lateral
    st.sidebar.header("Filtros de Búsqueda")
    ciudades = ["Todas"] + list(df["Ciudad"].unique())
    ciudad_seleccionada = st.sidebar.selectbox("Filtrar por Ciudad", ciudades)

    if ciudad_seleccionada != "Todas":
        df_filtrado = df[df["Ciudad"] == ciudad_seleccionada]
    else:
        df_filtrado = df

    # 3. Mostrar tabla interactiva en la web
    st.subheader(f"Listado de Registros ({len(df_filtrado)})")
    st.dataframe(df_filtrado, use_container_width=True)

    # 4. Gráfico estadístico básico integrado
    st.markdown("---")
    st.subheader("📈 Distribución por Ciudad")
    conteo_ciudades = df["Ciudad"].value_counts()
    st.bar_chart(conteo_ciudades)

else:
    st.error("No se pudieron cargar los datos desde la fuente pública.")