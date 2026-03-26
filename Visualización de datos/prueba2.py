import streamlit as st
import pandas as pd
import altair as alt
# -------------------------
# CONFIGURACIÓN
# -------------------------
st.set_page_config(
    page_title="Dashboard Electoral",
    layout="wide"
)

# -------------------------
# BARRA SUPERIOR
# -------------------------
st.markdown(
    """
    <div style="background-color:#FF6D7D;padding:25px;border-radius:10px;margin-bottom:20px;">
        <h1 style="color:white;margin:0;">📊 Dashboard Electoral</h1>
        <h3 style="color:white;margin:0;">Elecciones Presidenciales Primarias Chile 2025</h3>
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------------
# SUBIR ARCHIVO
# -------------------------
uploaded_file = st.file_uploader("Subir archivo de votaciones (CSV)", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # -------------------------
    # ASIGNACIÓN GRUPOS
    # -------------------------
    grupo_morado = [
        'FRANCO PARISI FERNANDEZ',
        'HAROLD MAYNE-NICHOLLS SECUL'
    ]
    grupo_rojo = [
        'JEANNETTE JARA ROMAN',
        'EDUARDO ANTONIO ARTES BRICHETTI',
        'MARCO ANTONIO ENRIQUEZ-OMINAMI GUMUCIO'
    ]
    grupo_azul = [
        'JOHANNES KAISER BARENTS-VON HOHENHAGEN',
        'JOSE ANTONIO KAST RIST',
        'EVELYN MATTHEI FORNET'
    ]

    def asignar_grupo(nombre):
        if nombre in grupo_rojo:
            return "rojo"
        if nombre in grupo_azul:
            return "azul"
        if nombre in grupo_morado:
            return "morado"
        return "no aplica"

    df["grupo"] = df["nombre_candidato"].apply(asignar_grupo)

    # -------------------------
    # TABS
    # -------------------------
    tab_nac, tab_ext = st.tabs(["🇨🇱 Resultados Nacionales", "🌎 Resultados en el Extranjero"])

    # -------------------------------------------------------------
    # TAB 1: NACIONALES
    # -------------------------------------------------------------
    with tab_nac:

        st.subheader("Filtros Nacionales")

        col_f1, col_f2 = st.columns(2)

        regiones = ["Todas"] + sorted(df[df["pais"] == "CHILE"]["region"].unique().tolist())
        candidatos = ["Todos"] + sorted(df["nombre_candidato"].unique().tolist())

        region_sel = col_f1.selectbox("Seleccionar región", regiones, key="region_nac")
        cand_sel = col_f2.selectbox("Seleccionar candidato", candidatos, key="cand_nac")


        df_nac = df[df["pais"] == "CHILE"].copy()

        if region_sel != "Todas":
            df_nac = df_nac[df_nac["region"] == region_sel]

        if cand_sel != "Todos":
            df_nac = df_nac[df_nac["nombre_candidato"] == cand_sel]

        # ---- KPIS ----
        st.markdown("### 📌 Métricas Nacionales")

        col1, col2 = st.columns(2)

        nulos = df_nac[df_nac["nombre_candidato"].str.contains("NULO", case=False)]["votos"].sum()
        blancos = df_nac[df_nac["nombre_candidato"].str.contains("BLANCO", case=False)]["votos"].sum()

        col1.metric("🗳️ Votos Nulos", int(nulos))
        col2.metric("⬜ Votos Blancos", int(blancos))

        st.markdown("---")

        # ---- Tabla ----
        cand_nac = (
            df_nac.groupby(["nombre_candidato"])["votos"]
            .sum()
            .reset_index()
            .sort_values(by="nombre_candidato", ascending=True)
        )
        
        st.subheader("Resultados por Candidato")
        st.dataframe(cand_nac, use_container_width=True,hide_index=True)

        # ---- Gráfico ----
        
        excluir = [
        "VOTOS NULOS",
        "VOTOS EN BLANCO",
        "TOTAL SUFRAGIOS VALIDAMENTE EMITIDOS", 
        "TOTAL SUMA CALCULADA"
    ]
        # Filtrar solo candidatos válidos
        df_validos = df_nac[~df_nac["nombre_candidato"].str.upper().isin(excluir)]
        

        # Agrupar (mismo código que tenías)
        cand_nac = (
            df_validos.groupby(["nombre_candidato","grupo"])["votos"]
            .sum()
            .reset_index()
            .sort_values(by="nombre_candidato")
        )

        st.subheader("Gráfico de Votos por Candidato")

        grafico = alt.Chart(cand_nac).mark_bar().encode(
            x=alt.X(
                'nombre_candidato', 
                title="Candidato",
                axis=alt.Axis(labelAngle=-45, labelLimit=0, labelOverlap=False) 
            ),
            y=alt.Y('votos', title="Total de Votos"),
            
            color=alt.Color(
                'grupo', # Usamos la columna grupo
                legend=None, # Opcional: ocultar la leyenda de colores si es obvio
                scale=alt.Scale(
                    # Definimos qué valor corresponde a qué color
                    domain=['rojo', 'azul', 'morado', 'no aplica'],
                    range=['#E02424', '#1F77B4', '#9467BD', 'gray'] 
                    # Puedes usar nombres: ['red', 'blue', 'purple', 'gray']
                    # O Hex codes como puse arriba para tonos más bonitos
                )
            ),
            tooltip=['nombre_candidato', 'votos'] 
        ).properties(
            height=500
        )
        col3, col4 = st.columns(2)
        with col3:
            st.altair_chart(grafico, use_container_width=True)
        
        

    # -------------------------------------------------------------
    # TAB 2: EXTRANJERO
    # -------------------------------------------------------------
    with tab_ext:

        st.subheader("Filtros en el Extranjero")

        col_f1, col_f2 = st.columns(2)

        paises = ["Todos"] + sorted(df[df["pais"] != "CHILE"]["pais"].unique().tolist())
        candidatos_ext = ["Todos"] + sorted(df["nombre_candidato"].unique().tolist())

        pais_sel = col_f1.selectbox("Seleccionar país", paises, key="pais_ext")
        cand_sel_e = col_f2.selectbox("Seleccionar candidato", candidatos_ext, key="cand_ext")

        df_ext = df[df["pais"] != "CHILE"].copy()

        if pais_sel != "Todos":
            df_ext = df_ext[df_ext["pais"] == pais_sel]

        if cand_sel_e != "Todos":
            df_ext = df_ext[df_ext["nombre_candidato"] == cand_sel_e]

        # ---- KPIS ----
        st.markdown("### 📌 Métricas en el Extranjero")

        col1, col2 = st.columns(2)

        nulos_e = df_ext[df_ext["nombre_candidato"].str.contains("NULO", case=False)]["votos"].sum()
        blancos_e = df_ext[df_ext["nombre_candidato"].str.contains("BLANCO", case=False)]["votos"].sum()

        col1.metric("🗳️ Votos Nulos", int(nulos_e))
        col2.metric("⬜ Votos Blancos", int(blancos_e))

        st.markdown("---")

        # ---- Tabla ----
        votos_ext = (
            df_ext.groupby(["nombre_candidato"])["votos"]
            .sum()
            .reset_index()
            .sort_values(by="nombre_candidato", ascending=True)
        )

        st.subheader("Resultados por Candidato")
        st.dataframe(votos_ext, use_container_width=True,hide_index=True)

        # ---- Gráfico ----
        df_validos2 = df_ext[~df_ext["nombre_candidato"].str.upper().isin(excluir)]
        
        cand_ext = (
            df_validos.groupby(["nombre_candidato","grupo"])["votos"]
            .sum()
            .reset_index()
            .sort_values(by="nombre_candidato")
        )
        
        st.subheader("Gráfico de Votos por Candidato")
        grafico = alt.Chart(cand_ext).mark_bar().encode(
            x=alt.X(
                'nombre_candidato', 
                title="Candidato",
                # labelAngle: Rota el texto -45 grados para que se lea mejor
                # labelLimit: 0 significa "sin límite", muestra el nombre completo
                axis=alt.Axis(labelAngle=-45, labelLimit=0, labelOverlap=False) 
            ),
            y=alt.Y('votos', title="Total de Votos"),
            
            color=alt.Color(
                'grupo', # Usamos la columna grupo
                legend=None, # Opcional: ocultar la leyenda de colores si es obvio
                scale=alt.Scale(
                    # Definimos qué valor corresponde a qué color
                    domain=['rojo', 'azul', 'morado', 'no aplica'],
                    range=['#E02424', '#1F77B4', '#9467BD', 'gray'] 
                    # Puedes usar nombres: ['red', 'blue', 'purple', 'gray']
                    # O Hex codes como puse arriba para tonos más bonitos
                )
            ),
            
            # Tooltip para ver el dato exacto al pasar el mouse
            tooltip=['nombre_candidato', 'votos'] 
        ).properties(
            height=500 # Aumentamos altura para dar espacio a las etiquetas
        )

        st.altair_chart(grafico, use_container_width=True)
