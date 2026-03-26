import polars as pl

def unificar_votaciones(path_chile, path_extranjero):
    print("Leyendo archivos...")
    
    # 1. Cargar archivos (Polars intentará usar fastexcel/calamine automáticamente si está instalado para mayor velocidad)
    # schema_overrides ayuda si alguna columna numérica se lee como texto por error
    df_chile = pl.read_excel(path_chile)
    df_extranjero = pl.read_excel(path_extranjero)

    # 2. Estandarizar nombres de columnas clave
    # Renombrar si existe la columna, si no, ignora para evitar errores
    if "votos_preliminares" in df_chile.columns:
        df_chile = df_chile.rename({"votos_preliminares": "votos"})

    # 3. Definir columnas faltantes y metadatos
    # En Polars usamos expresiones (pl.lit) para crear columnas constantes de forma muy eficiente
    
    # Preparar DF Chile
    df_chile = df_chile.with_columns([
        pl.lit('NACIONAL').alias('origen'),
        pl.lit('CHILE').alias('pais'),
        pl.lit('AMERICA').alias('continente'),
        pl.lit('NO APLICA').alias('consulado'),
        pl.lit('NO APLICA').alias('circunscripcion')
    ])

    # Preparar DF Extranjero
    df_extranjero = df_extranjero.with_columns([
        pl.lit('EXTRANJERO').alias('origen'),
        pl.lit('NO APLICA').alias('distrito'),
        pl.lit('NO APLICA').alias('comuna'),
        pl.lit('NO APLICA').alias('sede_colegio_escrutador') # Ajustar según tus columnas reales
    ])

    # 4. Manejo de Tipos (Casting)
    # Polars es estricto. Si 'incidencia_mesa' es Int en uno y String en otro, fallará al unir.
    # Convertimos a String explícitamente las columnas conflictivas y rellenamos nulos.
    
    def limpiar_texto(df, col_name):
        if col_name in df.columns:
            return df.with_columns(
                pl.col(col_name).cast(pl.String).fill_null("")
            )
        return df

    df_chile = limpiar_texto(df_chile, 'incidencia_mesa')
    df_extranjero = limpiar_texto(df_extranjero, 'incidencia_mesa')
    
    # Normalizar columna 'electo_nominado' si existe solo en uno (rellenar con null o 0)
    if "electo_nominado" not in df_extranjero.columns and "electo_nominado" in df_chile.columns:
         df_extranjero = df_extranjero.with_columns(pl.lit(None).cast(df_chile["electo_nominado"].dtype).alias("electo_nominado"))

    # 5. Unir DataFrames (Diagonal concat maneja columnas que no coinciden orden o faltan rellenando con null)
    # Usamos diagonal=True para que sea tolerante si alguna columna auxiliar falta en uno de los dos
    print("Unificando datos...")
    df_consolidado = pl.concat([df_chile, df_extranjero], how="diagonal")
    
    columnas_a_eliminar = [
        'cod_local_votacion',
        'local_votacion',
        'cod_colegio_escrutador',
        'colegio_escrutador',
        'sede_colegio_escrutador',
        'incidencia_mesa',
        'vocales',
        'form_40',
        'electo_nominado',
        'origen'
    ]
    
    # Solo eliminar las que existen en el DataFrame
    columnas_existentes = [col for col in columnas_a_eliminar if col in df_consolidado.columns]
    df_consolidado = df_consolidado.drop(columnas_existentes)
    

    return df_consolidado

# --- Ejecución ---
try:
    df_final = unificar_votaciones('chile.xlsx', 'extranjero.xlsx')
    
    # Nota: Tu input original en el prompt anterior eran CSVs disfrazados de Excel o viceversa.
    # Si tus archivos reales SON .xlsx usa el código de arriba.
    # Si son .csv, usa pl.read_csv(path) en lugar de pl.read_excel(path).

    # 6. Guardar garantizando caracteres en español
    # Streamlit prefiere UTF-8 estándar. Excel en Windows prefiere UTF-8-BOM.
    # Polars escribe UTF-8 estándar. Esto es perfecto para Streamlit y Python.
    print("Guardando archivo...")
    df_final.write_csv('votos2025.csv', separator=',')
    
    print(f"¡Listo! Archivo generado con {df_final.height} filas.")
    print(df_final.head())

except Exception as e:
    print(f"Ocurrió un error: {e}")