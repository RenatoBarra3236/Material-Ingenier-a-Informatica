# prueba3.py (versión corregida - pestaña Mapas arriba, geojson real de Chile)
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.express as px
import plotly.graph_objects as go
import geopandas as gpd
import json
import os
import requests

st.set_page_config(page_title="Dashboard Electoral 2025", layout="wide")

# -------------------------
# Cabecera
# -------------------------
st.markdown(
    """
    <div style="background-color:#FF6D7D;padding:18px;border-radius:10px;margin-bottom:18px;">
        <h1 style="color:white;margin:0;">📊 Dashboard Electoral</h1>
        <h3 style="color:white;margin:0;">Elecciones Presidenciales Primarias Chile 2025</h3>
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------------
# Rutas GeoJSON (local / fallback download)
# -------------------------
CHILE_GEOJSON = "chile_regiones.geojson"   # ya lo subiste
WORLD_GEOJSON = "countries.geojson"
WORLD_GEOJSON_URL = "https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson"

def ensure_file(path: str, url: str = None, timeout: int = 8) -> bool:
    """Asegura que exista el archivo local; si no, opcionalmente lo descarga desde url."""
    if os.path.exists(path):
        return True
    if url is None:
        return False
    try:
        r = requests.get(url, timeout=timeout)
        if r.status_code == 200:
            with open(path, "w", encoding="utf-8") as f:
                f.write(r.text)
            return True
        return False
    except Exception:
        return False

# intentar asegurar world geojson (silencioso)
_ = ensure_file(WORLD_GEOJSON, WORLD_GEOJSON_URL)

# -------------------------
# Subir CSV de votos
# -------------------------
uploaded_file = st.file_uploader("Subir archivo de votaciones (CSV)", type=["csv"])
if uploaded_file is None:
    st.info("Sube un CSV con los resultados (columnas esperadas: region, comuna, nombre_candidato, votos, pais, electores, ...).")
    st.stop()

# -------------------------
# Cargar y normalizar datos
# -------------------------
df = pd.read_csv(uploaded_file)
df.columns = [c.strip() for c in df.columns]
df.columns = [c.lower() for c in df.columns]

# Asegurar columnas mínimas
for col in ["region", "nombre_candidato", "votos", "pais"]:
    if col not in df.columns:
        if col == "votos":
            df[col] = 0
        else:
            df[col] = ""

# Tipos
df["region"] = df["region"].astype(str)
df["nombre_candidato"] = df["nombre_candidato"].astype(str)
df["pais"] = df["pais"].astype(str)
df["votos"] = pd.to_numeric(df["votos"], errors="coerce").fillna(0).astype(int)

# listas de exclusión y grupos
EXCLUIR = ["VOTOS NULOS", "VOTOS EN BLANCO", "TOTAL SUFRAGIOS VALIDAMENTE EMITIDOS", "TOTAL SUMA CALCULADA"]

grupo_morado = ['FRANCO PARISI FERNANDEZ', 'HAROLD MAYNE-NICHOLLS SECUL']
grupo_rojo = ['JEANNETTE JARA ROMAN', 'EDUARDO ANTONIO ARTES BRICHETTI', 'MARCO ANTONIO ENRIQUEZ-OMINAMI GUMUCIO']
grupo_azul = ['JOHANNES KAISER BARENTS-VON HOHENHAGEN', 'JOSE ANTONIO KAST RIST', 'EVELYN MATTHEI FORNET']

def asignar_grupo(nombre):
    n = str(nombre).upper().strip()
    if n in [g.upper() for g in grupo_rojo]:
        return "rojo"
    if n in [g.upper() for g in grupo_azul]:
        return "azul"
    if n in [g.upper() for g in grupo_morado]:
        return "morado"
    return "no aplica"

df["grupo"] = df["nombre_candidato"].apply(asignar_grupo)
color_scale = {'rojo': '#E02424', 'azul': '#1F77B4', 'morado': '#9467BD', 'no aplica': 'gray'}

# dividir nacional / extranjero
# asumo que las filas nacionales pueden tener pais == 'CHILE' o pais vacío
mask_chile = df["pais"].astype(str).str.upper().str.contains("CHILE") | (df["pais"].astype(str).str.strip() == "")
df_chile = df[mask_chile].copy()
df_chile = df_chile[~df_chile["nombre_candidato"].str.upper().isin(EXCLUIR)]

df_world = df[~df.index.isin(df_chile.index)].copy()

# agrupados
df_region_votos = (
    df_chile.assign(region_norm=df_chile["region"].astype(str).str.upper())
            .groupby("region_norm", as_index=False)["votos"]
            .sum()
            .rename(columns={"region_norm": "region"})
)

df_world_votos = df_world.groupby("pais", as_index=False)["votos"].sum()


# -------------------------
# Tabs superiores (Mapas arriba)
# -------------------------
tab_nac, tab_ext, tab_maps = st.tabs([
    "🇨🇱 Resultados Nacionales",
    "🌎 Resultados en el Extranjero",
    "🗺️ Mapas"
])

# -------------------------
# TAB NACIONALES
# -------------------------
with tab_nac:
    st.subheader("Filtros Nacionales")
    col_f1, col_f2 = st.columns(2)
    regiones = ["Todas"] + sorted(df_chile["region"].dropna().unique().tolist())
    candidatos = ["Todos"] + sorted(df["nombre_candidato"].dropna().unique().tolist())
    region_sel = col_f1.selectbox("Seleccionar región", regiones, key="region_nac")
    cand_sel = col_f2.selectbox("Seleccionar candidato", candidatos, key="cand_nac")

    df_nac = df_chile.copy()
    if region_sel != "Todas":
        df_nac = df_nac[df_nac["region"] == region_sel]
    if cand_sel != "Todos":
        df_nac = df_nac[df_nac["nombre_candidato"] == cand_sel]

    # KPIs
    st.markdown("### 📌 Métricas Nacionales")
    k1, k2 = st.columns(2)
    try:
        top_cand = df_nac.groupby("nombre_candidato")["votos"].sum().idxmax()
    except Exception:
        top_cand = "No disponible"
    blancos = df_nac[df_nac["nombre_candidato"].str.contains("BLANCO", case=False, na=False)]["votos"].sum()
    k1.metric("🗳️ Candidato más votado", top_cand)
    k2.metric("⬜ Votos Blancos", int(blancos))

    st.markdown("---")
    # tabla + barras
    cand_nac = df_nac.groupby(["nombre_candidato","grupo"], as_index=False)["votos"].sum().sort_values("votos", ascending=False)
    st.subheader("Resultados por Candidato")
    st.dataframe(cand_nac[["nombre_candidato","votos"]].reset_index(drop=True), width="stretch")

    bar = alt.Chart(cand_nac).mark_bar().encode(
        x=alt.X("nombre_candidato:N", sort='-y', title="Candidato"),
        y=alt.Y("votos:Q", title="Votos"),
        color=alt.Color("grupo:N", scale=alt.Scale(domain=list(color_scale.keys()), range=list(color_scale.values())), legend=None),
        tooltip=["nombre_candidato","votos"]
    ).properties(height=380)
    st.altair_chart(bar, width="stretch", key="bar_nac")

    # Scatter optimizado (opción D)
    st.markdown("---")
    st.subheader("Dispersión: electores vs votos normalizados (muestra optimizada)")
    df_scatter = df_nac.copy()
    df_scatter["electores"] = pd.to_numeric(df_scatter.get("electores", pd.Series(dtype=float)), errors="coerce")
    df_scatter["votos"] = pd.to_numeric(df_scatter["votos"], errors="coerce")
    df_scatter["votos_normalizados"] = df_scatter.apply(
        lambda r: (r["votos"]/r["electores"]) if (pd.notnull(r.get("votos")) and pd.notnull(r.get("electores")) and r["electores"]>0) else np.nan,
        axis=1
    )
    df_scatter = df_scatter.dropna(subset=["electores","votos_normalizados"])
    SAMPLE_LIMIT = 5000
    if len(df_scatter) > SAMPLE_LIMIT:
        df_sample = df_scatter.sample(SAMPLE_LIMIT, random_state=42)
        st.caption(f"Mostrando aleatoriamente {SAMPLE_LIMIT} puntos de {len(df_scatter)}")
    else:
        df_sample = df_scatter.copy()

    scatter = alt.Chart(df_sample).mark_circle(opacity=0.7, size=60).encode(
        x=alt.X("electores:Q", title="Electores"),
        y=alt.Y("votos_normalizados:Q", title="Votos / Electores"),
        color=alt.Color("grupo:N", scale=alt.Scale(domain=list(color_scale.keys()), range=list(color_scale.values())), legend=None),
        tooltip=["region","comuna","nombre_candidato","votos","electores"]
    ).interactive().properties(height=420)
    st.altair_chart(scatter, width="stretch", key="scatter_nac")

    # Heatmap agregado
    st.markdown("---")
    st.subheader("Heatmap: Región vs Candidato (agregado)")
    df_heat = df_nac.groupby([df_nac["region"].astype(str).str.upper(), "nombre_candidato"], as_index=False)["votos"].sum().rename(columns={"region":"region_norm"})
    heat = alt.Chart(df_heat).mark_rect().encode(
        x=alt.X("region_norm:N", title="Región"),
        y=alt.Y("nombre_candidato:N", title="Candidato"),
        color=alt.Color("votos:Q", title="Votos"),
        tooltip=["region_norm","nombre_candidato","votos"]
    ).properties(height=420)
    st.altair_chart(heat, width="stretch", key="heat_nac")

    # Boxplot
    st.subheader("Boxplot de votos por candidato")
    box = alt.Chart(df_nac).mark_boxplot(extent="min-max").encode(
        y="nombre_candidato:N",
        x="votos:Q",
        color=alt.Color("grupo:N", scale=alt.Scale(domain=list(color_scale.keys()), range=list(color_scale.values())), legend=None)
    ).properties(height=420)
    st.altair_chart(box, width="stretch", key="box_nac")

    # Tabla dinámica
    st.markdown("---")
    st.subheader("Tabla Dinámica: Región x Candidato")
    try:
        tabla_din = pd.pivot_table(df_nac, values="votos", index="region", columns="nombre_candidato", aggfunc="sum", fill_value=0)
        st.dataframe(tabla_din, width="stretch")
        st.download_button("Descargar tabla dinámica (CSV)", tabla_din.to_csv().encode("utf-8"), "tabla_nacional.csv", "text/csv")
    except Exception as e:
        st.info("No se pudo generar la tabla dinámica: " + str(e))

# -------------------------
# TAB EXTRANJERO
# -------------------------
with tab_ext:
    st.subheader("Filtros en el Extranjero")
    col_f1, col_f2 = st.columns(2)
    paises = ["Todos"] + sorted(df_world["pais"].dropna().unique().tolist())
    candidatos_ext = ["Todos"] + sorted(df["nombre_candidato"].dropna().unique().tolist())
    pais_sel = col_f1.selectbox("Seleccionar país", paises, key="pais_ext")
    cand_sel_e = col_f2.selectbox("Seleccionar candidato", candidatos_ext, key="cand_ext")

    df_ext = df_world.copy()
    if pais_sel != "Todos":
        df_ext = df_ext[df_ext["pais"] == pais_sel]
    if cand_sel_e != "Todos":
        df_ext = df_ext[df_ext["nombre_candidato"] == cand_sel_e]

    # KPIs extranjero
    st.markdown("### 📌 Métricas en el Extranjero")
    c1, c2 = st.columns(2)
    try:
        top_cand_ext = df_ext.groupby("nombre_candidato")["votos"].sum().idxmax()
    except Exception:
        top_cand_ext = "No disponible"
    blancos_e = df_ext[df_ext["nombre_candidato"].str.contains("BLANCO", case=False, na=False)]["votos"].sum()
    c1.metric("🗳️ Candidato más votado", top_cand_ext)
    c2.metric("⬜ Votos Blancos", int(blancos_e))

    st.markdown("---")
    votos_ext = df_ext.groupby(["nombre_candidato","grupo"], as_index=False)["votos"].sum().sort_values("votos", ascending=False)
    st.subheader("Resultados por Candidato (Extranjero)")
    st.dataframe(votos_ext[["nombre_candidato","votos"]], width="stretch")

    # Barras extranjeros
    bar_e = alt.Chart(votos_ext).mark_bar().encode(
        x=alt.X("nombre_candidato:N", sort='-y'),
        y=alt.Y("votos:Q"),
        color=alt.Color("grupo:N", scale=alt.Scale(domain=list(color_scale.keys()), range=list(color_scale.values())), legend=None),
        tooltip=["nombre_candidato","votos"]
    ).properties(height=380)
    st.altair_chart(bar_e, width="stretch", key="bar_ext")

    # Scatter / Heatmap / Boxplot / Tabla (mismos gráficos que en nacional)
    st.markdown("---")
    st.subheader("Dispersión: electores vs votos normalizados (Extranjero)")
    df_scatter_ext = df_ext.copy()
    df_scatter_ext["electores"] = pd.to_numeric(df_scatter_ext.get("electores", pd.Series(dtype=float)), errors="coerce")
    df_scatter_ext["votos"] = pd.to_numeric(df_scatter_ext["votos"], errors="coerce")
    df_scatter_ext["votos_normalizados"] = df_scatter_ext.apply(
        lambda r: (r["votos"]/r["electores"]) if (pd.notnull(r.get("votos")) and pd.notnull(r.get("electores")) and r["electores"]>0) else np.nan,
        axis=1
    )
    df_scatter_ext = df_scatter_ext.dropna(subset=["electores","votos_normalizados"])
    if len(df_scatter_ext) > SAMPLE_LIMIT:
        df_sample_ext = df_scatter_ext.sample(SAMPLE_LIMIT, random_state=42)
        st.caption(f"Mostrando aleatoriamente {SAMPLE_LIMIT} puntos de {len(df_scatter_ext)}")
    else:
        df_sample_ext = df_scatter_ext.copy()
    scatter_ext = alt.Chart(df_sample_ext).mark_circle(opacity=0.7, size=60).encode(
        x="electores:Q",
        y="votos_normalizados:Q",
        color=alt.Color("grupo:N", scale=alt.Scale(domain=list(color_scale.keys()), range=list(color_scale.values())), legend=None),
        tooltip=["pais","nombre_candidato","votos","electores"]
    ).interactive().properties(height=420)
    st.altair_chart(scatter_ext, width="stretch", key="scatter_ext")

    st.markdown("---")
    st.subheader("Heatmap: País vs Candidato (Extranjero)")
    df_heat_ext = df_ext.groupby([df_ext["pais"].astype(str).str.upper(), "nombre_candidato"], as_index=False)["votos"].sum().rename(columns={"pais":"pais_norm"})
    heat_ext = alt.Chart(df_heat_ext).mark_rect().encode(
        x=alt.X("pais_norm:N", title="País"),
        y=alt.Y("nombre_candidato:N", title="Candidato"),
        color=alt.Color("votos:Q", title="Votos"),
        tooltip=["pais_norm","nombre_candidato","votos"]
    ).properties(height=420)
    st.altair_chart(heat_ext, width="stretch", key="heat_ext")

    st.subheader("Boxplot de votos por candidato (Extranjero)")
    box_ext = alt.Chart(df_ext).mark_boxplot(extent="min-max").encode(
        y="nombre_candidato:N",
        x="votos:Q",
        color=alt.Color("grupo:N", scale=alt.Scale(domain=list(color_scale.keys()), range=list(color_scale.values())), legend=None)
    ).properties(height=420)
    st.altair_chart(box_ext, width="stretch", key="box_ext")

    st.markdown("---")
    st.subheader("Tabla Dinámica Extranjero")
    try:
        tabla_ext = pd.pivot_table(df_ext, values="votos", index="pais", columns="nombre_candidato", aggfunc="sum", fill_value=0)
        st.dataframe(tabla_ext, width="stretch")
        st.download_button("Descargar tabla dinámica (CSV) - Extranjero", tabla_ext.to_csv().encode("utf-8"), "tabla_extranjero.csv", "text/csv")
    except Exception as e:
        st.info("No se pudo generar la tabla dinámica (extranjero): " + str(e))

# -------------------------
# TAB: MAPAS
# -------------------------
with tab_maps:
    st.header("Mapas")

    mapa_nac_tab, mapa_world_tab = st.tabs(["Mapa Nacional", "Mapa Mundial"])

    # -------------------------
    # Mapa Nacional (usa tu geojson)
    # -------------------------
    with mapa_nac_tab:
        st.subheader("Choropleth Nacional (Regiones de Chile)")

        if not os.path.exists(CHILE_GEOJSON):
            st.warning("No se encontró 'chile_regiones.geojson' en el directorio. Sube el archivo para mostrar el choropleth nacional.")
        else:
            try:
                # leer geojson como dict y como GeoDataFrame
                with open(CHILE_GEOJSON, "r", encoding="utf-8") as f:
                    chile_geojson = json.load(f)

                chile_gdf = gpd.read_file(CHILE_GEOJSON)
                # buscar columna de nombre de región dentro de properties o columnas
                region_col = None
                for cand in ["region", "Region", "REGION", "nombre", "name", "NOMBRE"]:
                    if cand in chile_gdf.columns:
                        region_col = cand
                        break
                # si no hay columna, intentar sacar desde properties
                if region_col is None:
                    # geopandas may flatten properties -> try first feature
                    props0 = chile_geojson["features"][0].get("properties", {})
                    for k in props0.keys():
                        # elegir la que se parezca a region
                        if "reg" in k.lower() or "nom" in k.lower():
                            region_col = k
                            break
                if region_col is None:
                    st.warning("No se pudo identificar la columna de nombre de región en el geojson.")
                else:
                    # normalizar y usar featureidkey method: usamos px.choropleth con featureidkey
                    # preparar df con regiones en mismo formato que geojson properties
                    # extraer nombre que corresponde en geojson (prop key)
                    # construiremos un mapping region->votos
                    # Normalizar ambas a upper no acentos para robustez:
                    def norm_txt(s):
                        return str(s).upper().strip()

                    # preparar mapping desde geojson properties
                    geo_regions = []
                    for feat in chile_geojson.get("features", []):
                        prop = feat.get("properties", {})
                        val = prop.get(region_col, None)
                        if val is None:
                            # si region_col no coincide con properties keys (por ejemplo geopandas creó otra columna)
                            # intentar buscar key that contains 'REG' or 'NOM'
                            for k, v in prop.items():
                                if 'reg' in k.lower() or 'nom' in k.lower():
                                    val = v
                                    break
                        geo_regions.append(norm_txt(val))

                    # construir df_region_simple con region names que vienen del CSV
                    df_region_simple = df_chile.groupby(df_chile["region"].astype(str).apply(lambda x: norm_txt(x)), as_index=False)["votos"].sum().rename(columns={"region":"region_norm"})
                    # usar px.choropleth con featureidkey: property path "properties.<region_col>"
                    featureid = f"properties.{region_col}"

                    fig_chile = px.choropleth(
                        df_region_simple,
                        geojson=chile_geojson,
                        locations="region_norm",
                        color="votos",
                        featureidkey=featureid,
                        hover_data={"region_norm":True, "votos":True},
                        labels={"region_norm":"Región"},
                        projection="mercator"
                    )
                    fig_chile.update_geos(fitbounds="locations", visible=False)
                    fig_chile.update_layout(margin={"l":0,"r":0,"t":0,"b":0}, height=600)
                    st.plotly_chart(fig_chile, width="stretch", key="choropleth_chile")
            except Exception as e:
                st.error(f"Error mostrando choropleth nacional: {e}")

        st.markdown("---")
        st.subheader("Bubble Map Nacional (centroides)")

        try:
            # si existe el geojson, emplear centroides
            if os.path.exists(CHILE_GEOJSON):
                chile_gdf = gpd.read_file(CHILE_GEOJSON)
                # intentar localizar la columna con nombre de region
                region_col = None
                for cand in ["region","Region","REGION","nombre","name","NOMBRE"]:
                    if cand in chile_gdf.columns:
                        region_col = cand
                        break
                if region_col is None:
                    # fallback: usar properties if present
                    # create region column from properties if necessary
                    try:
                        chile_gdf["region"] = chile_gdf["properties"].apply(lambda p: p.get("region","") if isinstance(p, dict) else "")
                        region_col = "region"
                    except Exception:
                        region_col = None

                # centroides
                chile_gdf["lon"] = chile_gdf.geometry.centroid.x
                chile_gdf["lat"] = chile_gdf.geometry.centroid.y
                # preparar df_bubble con nombres normalizados
                df_bubble = df_chile.groupby(df_chile["region"].astype(str).apply(lambda x: str(x).upper().strip()), as_index=False)["votos"].sum().rename(columns={"region":"region_norm"})
                # mapear centroides: normalizar region column of geo
                geo_map = chile_gdf.copy()
                geo_map["region_norm"] = geo_map[region_col].astype(str).apply(lambda x: str(x).upper().strip())
                df_bubble = df_bubble.merge(geo_map[["region_norm","lat","lon"]].drop_duplicates(), on="region_norm", how="left")
                df_bubble = df_bubble.dropna(subset=["lat","lon"])
                fig_bubble = px.scatter_mapbox(
                    df_bubble,
                    lat="lat",
                    lon="lon",
                    size="votos",
                    hover_name="region_norm",
                    color_discrete_sequence=["#FF5733"],
                    zoom=3.7,
                    height=520
                )
                fig_bubble.update_layout(mapbox_style="open-street-map", margin={"l":0,"r":0,"t":0,"b":0})
                st.plotly_chart(fig_bubble, width="stretch", key="bubble_chile")
            else:
                st.info("No hay geojson local para centroides; sube 'chile_regiones.geojson' para bubble map con centroides reales.")
        except Exception as e:
            st.info(f"No se pudo generar bubble map: {e}")

    # -------------------------
    # MAPA MUNDIAL
    # -------------------------
    with mapa_world_tab:
        st.subheader("Mapa Mundial — Choropleth")

        if not os.path.exists(WORLD_GEOJSON):
            ok = ensure_file(WORLD_GEOJSON, WORLD_GEOJSON_URL)
            if not ok:
                st.warning("No se pudo descargar el geojson mundial; mostraremos fallback con scatter_geo (si hay datos).")

        try:
            if os.path.exists(WORLD_GEOJSON):
                world_gdf = gpd.read_file(WORLD_GEOJSON)
                # identificar nombre de país en geojson
                name_col = None
                for cand in ["ADMIN","NAME","name","Country","COUNTRY"]:
                    if cand in world_gdf.columns:
                        name_col = cand
                        break
                if name_col is None:
                    name_col = world_gdf.columns[0]

                world_gdf["pais_norm"] = world_gdf[name_col].astype(str).str.upper().str.strip()
                df_world_local = df_world_votos.copy()
                df_world_local["pais_norm"] = df_world_local["pais"].astype(str).str.upper().str.strip()
                world_gdf = world_gdf.merge(df_world_local, on="pais_norm", how="left")

                # usar px.choropleth con featureidkey no es necesario si merge fue exitoso; usaremos locations=index
                fig_world = px.choropleth(
                    world_gdf,
                    geojson=world_gdf.__geo_interface__,
                    locations=world_gdf.index,
                    color="votos",
                    hover_name=name_col,
                    projection="natural earth"
                )
                fig_world.update_geos(fitbounds="locations", visible=False)
                fig_world.update_layout(margin={"l":0,"r":0,"t":0,"b":0}, height=620)
                st.plotly_chart(fig_world, width="stretch", key="choropleth_world")
            else:
                # fallback scatter_geo si no hay geojson
                if df_world_votos.shape[0] > 0:
                    fig_w = px.scatter_geo(df_world_votos, locations="pais", locationmode="country names", size="votos", hover_name="pais", projection="natural earth")
                    fig_w.update_layout(margin={"l":0,"r":0,"t":0,"b":0}, height=620)
                    st.plotly_chart(fig_w, width="stretch", key="scatter_world_fb")
                else:
                    st.info("No hay datos para el mapa mundial.")
        except Exception as e:
            st.error(f"Error mostrando mapa mundial: {e}")

st.success("Dashboard cargado (mapas arriba). Si algún mapa no carga correctamente revisa el archivo geojson local o pega el traceback aquí.")
