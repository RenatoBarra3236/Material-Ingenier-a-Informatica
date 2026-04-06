import streamlit as st
import pandas as pd
import numpy as np
import json
import plotly.express as px
import os

# -----------------------------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Dashboard Electoral · Votos 2025",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 Dashboard Electoral · Votos 2025")

# -----------------------------------------------------------------------------
# CONSTANTES Y DEFINICIONES POLÍTICAS
# -----------------------------------------------------------------------------
GRUPO_ROJO = [
    'JEANNETTE JARA', 'JEANNETTE JARA ROMAN',
    'EDUARDO ANTONIO ARTES BRICHETTI',
    'MARCO ANTONIO ENRIQUEZ-OMINAMI GUMUCIO'
]
GRUPO_AZUL = [
    'JOSE ANTONIO KAST RIST',
    'EVELYN MATTHEI FORNET',
    'JOHANNES KAISER BARENTS-VON HOHENHAGEN'
]
GRUPO_MORADO = [
    'FRANCO PARISI FERNANDEZ',
    'HAROLD MAYNE-NICHOLLS SECUL'
]

COLOR_MAP = {
    "izquierda": "#E63946",  # Rojo suave
    "derecha": "#1D3557",    # Azul oscuro
    "centro": "#8338EC",     # Morado
    "otros": "#A8DADC"       # Gris/Celeste claro
}

# -----------------------------------------------------------------------------
# FUNCIONES DE LIMPIEZA Y CARGA
# -----------------------------------------------------------------------------

def asignar_bloque(nombre):
    """Asigna un color/bloque político según el nombre del candidato."""
    if pd.isna(nombre):
        return "otros"
    n = str(nombre).strip().upper()
    
    if any(x in n for x in [g.upper() for g in GRUPO_ROJO]):
        return "izquierda"
    if any(x in n for x in [g.upper() for g in GRUPO_AZUL]):
        return "derecha"
    if any(x in n for x in [g.upper() for g in GRUPO_MORADO]):
        return "centro"
    return "otros"

def normalizar_nombre_region(nombre_csv):
    """Normaliza nombres de regiones para coincidir con el GeoJSON."""
    if pd.isna(nombre_csv): 
        return "Desconocida"
    
    n = str(nombre_csv).strip().upper()
    
    mapeo = {
        "DE ARICA Y PARINACOTA": "Arica y Parinacota",
        "DE TARAPACA": "Tarapacá",
        "DE ANTOFAGASTA": "Antofagasta",
        "DE ATACAMA": "Atacama",
        "DE COQUIMBO": "Coquimbo",
        "DE VALPARAISO": "Valparaíso",
        "METROPOLITANA DE SANTIAGO": "Metropolitana de Santiago",
        "DEL LIBERTADOR GENERAL BERNARDO O'HIGGINS": "Libertador General Bernardo O'Higgins",
        "DE MAULE": "Maule",
        "DE ÑUBLE": "Ñuble",
        "DEL BIOBIO": "Biobío",
        "DE LA ARAUCANIA": "La Araucanía",
        "DE LOS RIOS": "Los Ríos",
        "DE LOS LAGOS": "Los Lagos",
        "DE AYSEN DEL GENERAL CARLOS IBANEZ DEL CAMPO": "Aysén del General Carlos Ibáñez del Campo",
        "DE MAGALLANES Y DE LA ANTARTICA CHILENA": "Magallanes y de la Antártica Chilena"
    }
    
    if n in mapeo:
        return mapeo[n]
    
    return n.replace("DE ", "").title()

@st.cache_data
def load_data(file_input):
    """Carga y procesa el CSV desde un archivo subido o ruta local."""
    try:
        df = pd.read_csv(file_input)
    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")
        return None
    
    # Limpieza básica de columnas
    df.columns = [c.strip().lower() for c in df.columns]

    # --- CORRECCIÓN 1: Eliminar duplicados exactos ---
    # Esto previene que si el archivo tiene filas repetidas, se sumen doble.
    df.drop_duplicates(inplace=True)
    
    # Convertir numéricos
    cols_num = ["votos", "electores", "mesa"]
    for c in cols_num:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0).astype(int)
    
    # Normalizar País
    if "pais" not in df.columns:
        df["pais"] = "Chile"
    
    # Columna extranjero
    paises_chile = ["chile", "chilè", "chile "]
    df["es_extranjero"] = ~df["pais"].str.strip().str.lower().isin(paises_chile)
    
    # Asignar bloque
    col_cand = "nombre_candidato" if "nombre_candidato" in df.columns else "candidato"
    if col_cand in df.columns:
        df["bloque"] = df[col_cand].apply(asignar_bloque)
        df.rename(columns={col_cand: "nombre_candidato"}, inplace=True)
    else:
        df["nombre_candidato"] = "SIN NOMBRE"
        df["bloque"] = "otros"
        
    # Normalizar Región
    if "region" in df.columns:
        df["region_normalizada"] = df["region"].apply(normalizar_nombre_region)
    else:
        df["region_normalizada"] = "Desconocida"

    return df

# -----------------------------------------------------------------------------
# SIDEBAR - CARGA DE ARCHIVO
# -----------------------------------------------------------------------------
st.sidebar.header("📂 Carga de Datos")
uploaded_file = st.sidebar.file_uploader("Sube tu archivo CSV (votos2025.csv)", type=["csv"])

# Lógica de carga: Prioridad Subido > Local > Error
df = None
DEFAULT_CSV = "votos2025.csv"
GEOJSON_FILE = "Regiones_Chile.geojson"

if uploaded_file is not None:
    df = load_data(uploaded_file)
    st.sidebar.success("Archivo subido cargado con éxito.")
elif os.path.exists(DEFAULT_CSV):
    st.sidebar.info(f"Usando archivo local: {DEFAULT_CSV}")
    df = load_data(DEFAULT_CSV)
else:
    st.warning("⚠️ Esperando archivo. Por favor sube un CSV en la barra lateral.")
    st.stop()

if df is None:
    st.stop()

# -----------------------------------------------------------------------------
# SIDEBAR - FILTROS
# -----------------------------------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.header("🔍 Filtros Globales")

lista_candidatos = ["Todos"] + sorted(df["nombre_candidato"].dropna().unique().tolist())
lista_regiones = ["Todas"] + sorted(df[~df["es_extranjero"]]["region_normalizada"].unique().tolist())
lista_paises = ["Todos"] + sorted(df[df["es_extranjero"]]["pais"].dropna().unique().tolist())

candidato_sel = st.sidebar.selectbox("Candidato", lista_candidatos)
region_sel = st.sidebar.selectbox("Región (Chile)", lista_regiones)
pais_sel = st.sidebar.selectbox("País (Extranjero)", lista_paises)
scope_sel = st.sidebar.radio("Alcance Geográfico", ["Ambos", "Solo Chile", "Solo Extranjero"], index=0)

# -----------------------------------------------------------------------------
# FILTRADO
# -----------------------------------------------------------------------------
df_filtrado = df.copy()

if candidato_sel != "Todos":
    df_filtrado = df_filtrado[df_filtrado["nombre_candidato"] == candidato_sel]

if region_sel != "Todas":
    df_filtrado = df_filtrado[df_filtrado["region_normalizada"] == region_sel]

if pais_sel != "Todos":
    df_filtrado = df_filtrado[df_filtrado["pais"] == pais_sel]

if scope_sel == "Solo Chile":
    df_filtrado = df_filtrado[~df_filtrado["es_extranjero"]]
elif scope_sel == "Solo Extranjero":
    df_filtrado = df_filtrado[df_filtrado["es_extranjero"]]

# -----------------------------------------------------------------------------
# METRICAS (KPIs)
# -----------------------------------------------------------------------------
total_votos = df_filtrado["votos"].sum()
votos_cl = df_filtrado[~df_filtrado["es_extranjero"]]["votos"].sum()
votos_ext = df_filtrado[df_filtrado["es_extranjero"]]["votos"].sum()

col1, col2, col3 = st.columns(3)
col1.metric("Total Votos (Filtrado)", f"{total_votos:,.0f}")
col2.metric("Votos Chile 🇨🇱", f"{votos_cl:,.0f}")
col3.metric("Votos Extranjero 🌍", f"{votos_ext:,.0f}")

st.markdown("---")

# -----------------------------------------------------------------------------
# PESTAÑAS PRINCIPALES
# -----------------------------------------------------------------------------
tab_chile, tab_mundo, tab_stats = st.tabs(["🇨🇱 Mapa Chile", "🌍 Mapa Mundial", "📈 Análisis & Gráficos"])

# --- TAB 1: MAPA CHILE ---
with tab_chile:
    st.subheader("Distribución Regional en Chile")
    df_chile_map = df_filtrado[~df_filtrado["es_extranjero"]].groupby("region_normalizada", as_index=False)["votos"].sum()
    
    if os.path.exists(GEOJSON_FILE):
        with open(GEOJSON_FILE, "r", encoding="utf-8") as f:
            geojson_data = json.load(f)
        
        feature_key = "properties.REGION"
        if geojson_data['features']:
            props = geojson_data['features'][0]['properties']
            if 'REGION' not in props and 'name' in props: feature_key = "properties.name"
            elif 'REGION' not in props and 'Name' in props: feature_key = "properties.Name"

        if not df_chile_map.empty:
            fig_map_cl = px.choropleth_mapbox(
                df_chile_map,
                geojson=geojson_data,
                locations="region_normalizada",
                featureidkey=feature_key,
                color="votos",
                color_continuous_scale="Reds",
                range_color=(0, df_chile_map["votos"].max()),
                mapbox_style="carto-positron",
                zoom=3,
                center={"lat": -35.6751, "lon": -71.543},
                opacity=0.6
            )
            fig_map_cl.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig_map_cl, use_container_width=True)
        else:
            st.warning("No hay datos para mostrar en el mapa de Chile.")
    else:
        st.error(f"No se encontró el archivo `{GEOJSON_FILE}`.")
        st.dataframe(df_chile_map)

# --- TAB 2: MAPA MUNDIAL ---
with tab_mundo:
    st.subheader("Votos en el Extranjero")
    df_world_map = df_filtrado[df_filtrado["es_extranjero"]].groupby("pais", as_index=False)["votos"].sum()
    
    if not df_world_map.empty:
        fig_world = px.choropleth(
            df_world_map,
            locations="pais",
            locationmode="country names",
            color="votos",
            hover_name="pais",
            color_continuous_scale="Blues",
            projection="natural earth"
        )
        fig_world.update_layout(margin={"r":0,"t":40,"l":0,"b":0}, geo=dict(showframe=False, showcoastlines=True))
        st.plotly_chart(fig_world, use_container_width=True)
    else:
        st.info("No hay votos en el extranjero con los filtros seleccionados.")

# --- TAB 3: ESTADÍSTICAS AVANZADAS ---
with tab_stats:
    st.subheader("Tablero de Análisis Avanzado")
    
    # Sub-pestañas para organizar los tipos de gráficos solicitados
    subtab_rank, subtab_disp, subtab_dist, subtab_line, subtab_data = st.tabs([
        "📊 Ranking (Barras)", 
        "📉 Dispersión (Participación)", 
        "📦 Distribución (Box/Heat)", 
        "📅 Evolución", 
        "📋 Tabla Dinámica"
    ])

    # 1. RANKING (BARRAS TOP/BOTTOM)
    with subtab_rank:
        c1, c2 = st.columns(2)
        votos_cand = df_filtrado.groupby(["nombre_candidato", "bloque"], as_index=False)["votos"].sum().sort_values("votos", ascending=False)
        
        with c1:
            st.write("#### 🔝 Top 10 Candidatos")
            if not votos_cand.empty:
                fig_top = px.bar(votos_cand.head(10), x="nombre_candidato", y="votos", color="bloque", color_discrete_map=COLOR_MAP, text_auto='.2s')
                st.plotly_chart(fig_top, use_container_width=True)
            else:
                st.info("Sin datos.")
        
        with c2:
            st.write("#### 🔽 Bottom 10 Candidatos")
            if not votos_cand.empty:
                fig_bot = px.bar(votos_cand.tail(10).sort_values("votos", ascending=True), x="nombre_candidato", y="votos", color="bloque", color_discrete_map=COLOR_MAP, text_auto='.2s')
                st.plotly_chart(fig_bot, use_container_width=True)
            else:
                st.info("Sin datos.")

    # 2. DISPERSIÓN (PARTICIPACIÓN VS VOTOS)
    with subtab_disp:
        st.write("#### 📉 Relación Participación vs Votos (Por Comuna)")
        
        # --- CORRECCIÓN 2: Cálculo correcto de Electores ---
        if "electores" in df_filtrado.columns and "comuna" in df_filtrado.columns:
            # Paso A: Calcular votos por comuna y bloque
            votos_comuna = df_filtrado.groupby(["region_normalizada", "comuna", "bloque"], as_index=False)["votos"].sum()
            
            # Paso B: Calcular electores reales por comuna (sin duplicar por candidato)
            # Usamos drop_duplicates en 'cod_mesa' para contar los electores de la mesa solo una vez
            if "cod_mesa" in df_filtrado.columns:
                electores_comuna = df_filtrado[["comuna", "cod_mesa", "electores"]].drop_duplicates().groupby("comuna", as_index=False)["electores"].sum()
            else:
                # Si no hay cod_mesa, usamos una aproximación (menos precisa pero evita multiplicar x10)
                # Omitimos cálculo de electores si no podemos desagregar
                electores_comuna = pd.DataFrame(columns=["comuna", "electores"])

            # Paso C: Unir
            if not electores_comuna.empty:
                df_scatter = pd.merge(votos_comuna, electores_comuna, on="comuna", how="inner")
                
                # Calcular participación
                df_scatter["participacion_pct"] = np.where(df_scatter["electores"] > 0, (df_scatter["votos"] / df_scatter["electores"]) * 100, 0)
                
                if not df_scatter.empty:
                    fig_sc = px.scatter(
                        df_scatter, 
                        x="participacion_pct", 
                        y="votos", 
                        size="votos", 
                        color="bloque",
                        color_discrete_map=COLOR_MAP,
                        hover_name="comuna",
                        hover_data=["region_normalizada", "electores"],
                        labels={"participacion_pct": "% Participación (Votos/Electores)", "votos": "Cantidad Votos"},
                        title="Dispersión: Participación vs Votos Totales por Comuna"
                    )
                    st.plotly_chart(fig_sc, use_container_width=True)
                else:
                    st.warning("No hay datos suficientes tras el cruce de comunas.")
            else:
                 st.warning("No se pudo calcular electores únicos (falta columna 'cod_mesa').")
        else:
            st.error("Faltan columnas 'electores' o 'comuna' en el dataset para calcular la participación.")

    # 3. DISTRIBUCIÓN (HEATMAP / BOXPLOT)
    with subtab_dist:
        col_box, col_heat = st.columns(2)
        
        with col_box:
            st.write("#### 📦 Boxplot: Votos por Región")
            if not df_filtrado.empty:
                # Boxplot muestra la variabilidad de votos por mesa (o comuna) dentro de cada región
                # Agrupamos por comuna para reducir ruido de mesas individuales
                df_box = df_filtrado.groupby(["region_normalizada", "comuna"], as_index=False)["votos"].sum()
                fig_box = px.box(df_box, x="region_normalizada", y="votos", points="outliers", title="Distribución de Votos (por Comuna)")
                fig_box.update_layout(xaxis={'tickangle': 45})
                st.plotly_chart(fig_box, use_container_width=True)
            else:
                st.info("Sin datos.")

        with col_heat:
            st.write("#### 🔥 Heatmap de Correlaciones")
            # Seleccionar solo numéricas
            df_num = df_filtrado.select_dtypes(include=[np.number])
            if df_num.shape[1] > 1:
                corr = df_num.corr()
                fig_heat = px.imshow(corr, text_auto=True, aspect="auto", color_continuous_scale="RdBu_r", title="Matriz de Correlación")
                st.plotly_chart(fig_heat, use_container_width=True)
            else:
                st.info("No hay suficientes variables numéricas para correlación.")

    # 4. EVOLUCIÓN HISTÓRICA (LÍNEAS)
    with subtab_line:
        st.write("#### 📅 Evolución Histórica")
        # Chequear si existe alguna columna de tiempo (año, fecha, elección)
        possible_time_cols = ['año', 'anio', 'year', 'fecha', 'date', 'eleccion']
        time_col = next((c for c in possible_time_cols if c in df_filtrado.columns), None)
        
        if time_col:
            df_time = df_filtrado.groupby([time_col, "nombre_candidato"], as_index=False)["votos"].sum()
            fig_line = px.line(df_time, x=time_col, y="votos", color="nombre_candidato", markers=True, title=f"Evolución de Votos por {time_col}")
            st.plotly_chart(fig_line, use_container_width=True)
        else:
            st.warning("⚠️ No se detectó una columna de tiempo (ej: 'año', 'fecha') en el archivo CSV actual.")
            st.info("ℹ️ Si agregas datos de elecciones pasadas al CSV, asegúrate de incluir una columna 'año' para ver este gráfico.")

    # 5. TABLA DINÁMICA
    with subtab_data:
        st.write("#### 📋 Tabla Dinámica Exportable")
        
        # Opciones para la pivot table
        pivot_idx = st.multiselect("Filas (Index)", ["nombre_candidato", "region_normalizada", "comuna", "bloque"], default=["nombre_candidato"])
        pivot_col = st.multiselect("Columnas", ["region_normalizada", "bloque", "pais"], default=["region_normalizada"])
        
        if pivot_idx:
            try:
                pivot_table = df_filtrado.pivot_table(
                    index=pivot_idx, 
                    columns=pivot_col if pivot_col else None, 
                    values="votos", 
                    aggfunc="sum", 
                    fill_value=0
                )
                st.dataframe(pivot_table, use_container_width=True)
                
                # Botón descarga
                csv_pivot = pivot_table.to_csv().encode('utf-8')
                st.download_button("📥 Descargar Tabla Dinámica (CSV)", data=csv_pivot, file_name="tabla_dinamica_votos.csv", mime="text/csv")
            except Exception as e:
                st.error(f"Error creando tabla dinámica: {e}. Intenta simplificar la selección.")
        else:
            st.info("Selecciona al menos una variable para las filas.")