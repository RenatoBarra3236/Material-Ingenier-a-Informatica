import dash
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import warnings
warnings.filterwarnings('ignore')
from dash import Dash, html, dcc, dash_table, Input, Output

# Leer datos
df = pd.read_csv('student-mat.csv')

# Crear variable de consumo promedio de alcohol
df['alcohol_avg'] = (df['Dalc'] + df['Walc']) / 2

# Categorizar consumo de alcohol para el gráfico de caja
df['alcohol_cat'] = pd.cut(
    df['alcohol_avg'],
    bins=[0, 1.5, 3, 5],
    labels=['Bajo', 'Medio', 'Alto']
)
avg_g3 = round(df['G3'].mean(), 2)
pass_rate = round((df['G3'] >= 10).mean() * 100, 1)  # % con G3 >= 10
avg_alcohol = round(df['alcohol_avg'].mean(), 2)
avg_studytime = round(df['studytime'].mean(), 2)

# Inicializar la app
app = dash.Dash(__name__)

# Layout principal
app.layout = html.Div(style={'font-family': 'Arial', 'padding': '20px'}, children=[
    html.H1('Dashboard de Bienestar Estudiantil', style={'textAlign': 'center'}),

    # Filtros
    html.Div(style={'display': 'flex', 'gap': '24px', 'width': '80%', 'margin': 'auto', 'justifyContent': 'space-between'}, children=[
        html.Div(children=[
            html.H4('Seleccione Colegio:'),
            dcc.Dropdown(
                id='filtro-school',
                options=[
                    {'label': 'Todos', 'value': 'All'},
                    {'label': 'GP', 'value': 'GP'},
                    {'label': 'MS', 'value': 'MS'}
                ],
                clearable=False,
                value='All'
            )
        ], style={'flex': '1'}),

        html.Div(children=[
            html.H4('Seleccione Género:'),
            dcc.Dropdown(
                id='filtro-gender',
                options=[
                    {'label': 'Todos', 'value': 'All'},
                    {'label': 'M', 'value': 'M'},
                    {'label': 'F', 'value': 'F'}
                ],
                clearable=False,
                value='All'
            )
        ], style={'flex': '1'}),

        html.Div(children=[
            html.H4('Seleccione Rango de Edad:'),
            dcc.RangeSlider(15, 22, 1, value=[15, 22], id='filtro-age',
                            marks={i: str(i) for i in range(15, 23)})
        ], style={'flex': '2'})
    ]),

    html.Br(),
    html.Div(
        style={
            'display': 'flex',
            'gap': '16px',
            'width': '80%',
            'margin': '12px auto',
            'justifyContent': 'space-between',
            'alignItems': 'center'
        },
        children=[
            html.Div([
                html.Div("Promedio G3", style={'fontSize': 12, 'color': 'black'}),
                html.H3(f"{avg_g3}", id='kpi-avg-g3', style={'margin': '6px 0'})
            ], style={'flex': '0 0 23%', 'padding': '12px', 'backgroundColor': "#5195C5", 'borderRadius': '6px', 'boxShadow': '0 1px 3px rgba(0,0,0,0.1)'}),

            html.Div([
                html.Div("Tasa Aprobación (%)", style={'fontSize': 12, 'color': 'black'}),
                html.H3(f"{pass_rate}%", id='kpi-pass-rate', style={'margin': '6px 0', 'color': '#111'})
            ], style={'flex': '0 0 23%', 'padding': '12px', 'backgroundColor': "#65B4C6", 'borderRadius': '6px', 'boxShadow': '0 1px 3px rgba(0,0,0,0.1)'}),

            html.Div([
                html.Div("Consumo Alcohol (avg)", style={'fontSize': 12, 'color': 'black'}),
                html.H3(f"{avg_alcohol}", id='kpi-alcohol', style={'margin': '6px 0', 'color': '#111'})
            ], style={'flex': '0 0 23%', 'padding': '12px', 'backgroundColor': '#BDE5B5', 'borderRadius': '6px', 'boxShadow': '0 1px 3px rgba(0,0,0,0.1)'}),

            html.Div([
                html.Div("Tiempo Estudio (avg)", style={'fontSize': 12, 'color': 'black'}),
                html.H3(f"{avg_studytime}", id='kpi-studytime', style={'margin': '6px 0', 'color': '#111'})
            ], style={'flex': '0 0 23%', 'padding': '12px', 'backgroundColor': "#96A6BB", 'borderRadius': '6px', 'boxShadow': '0 1px 3px rgba(0,0,0,0.1)'})
        ]
    ),
    # Gráficos
    html.Div(style={'display': 'flex', 'gap': '30px', 'justifyContent': 'center'}, children=[
        dcc.Graph(id="fig1", style={'width': '48%'}),
        dcc.Graph(id="fig2", style={'width': '48%'})
    ]),

    html.Div(style={'display': 'flex', 'gap': '30px', 'justifyContent': 'center'}, children=[
        dcc.Graph(id="fig3", style={'width': '32%'}),
        # dcc.Graph(id="fig4", style={'width': '32%'}),
        dcc.Graph(id="fig6", style={'width': '32%'}),
        dcc.Graph(id="fig5", style={'width': '32%'})
    ]),

    html.Div(style={'display': 'flex', 'gap': '30px', 'justifyContent': 'center'}, children=[
        #dcc.Graph(id="fig6", style={'width': '48%'}),
        dcc.Graph(id="fig4", style={'width': '48%'}),
        dcc.Graph(id="fig7", style={'width': '48%'})
    ]),

    # Tabla
    html.H3("Tabla de Datos Originales", style={'textAlign': 'center', 'marginTop': '30px'}),
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        page_size=10,
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left', 'padding': '10px', 'minWidth': '100px'},
        style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'}
    )
])

# Callback
@app.callback(
    Output('kpi-avg-g3', 'children'),
    Output('kpi-pass-rate', 'children'),
    Output('kpi-alcohol', 'children'),
    Output('kpi-studytime', 'children'),
    Output("fig1", "figure"),
    Output("fig2", "figure"),
    Output("fig3", "figure"),
    Output("fig4", "figure"),
    Output("fig5", "figure"),
    Output("fig6", "figure"),
    Output("fig7", "figure"),
    Input("filtro-school", "value"),
    Input("filtro-gender", "value"),
    Input("filtro-age", "value")
)
def actualizar_graficos(school, gender, age_range):
    dff = df.copy()

    if school != "All":
        dff = dff[dff["school"] == school]
    if gender != "All":
        dff = dff[dff["sex"] == gender]
    if age_range:
        dff = dff[(dff["age"] >= age_range[0]) & (dff["age"] <= age_range[1])]

    # KPIs (manejo de sin datos)
    if dff.empty:
        kpi_avg_g3 = "N/A"
        kpi_pass_rate = "N/A"
        kpi_alcohol = "N/A"
        kpi_studytime = "N/A"
    else:
        kpi_avg_g3 = round(dff['G3'].mean(), 2)
        kpi_pass_rate = f"{round((dff['G3'] >= 10).mean() * 100, 1)}%"
        kpi_alcohol = round(dff['alcohol_avg'].mean(), 2)
        kpi_studytime = round(dff['studytime'].mean(), 2)

    if dff.empty:
        figs = [go.Figure().add_annotation(text="Sin datos disponibles", showarrow=False)] * 7
        return kpi_avg_g3, kpi_pass_rate, kpi_alcohol, kpi_studytime,figs

    fig1 = px.scatter(dff, x="studytime", y="G3", color="alcohol_avg",
                      color_continuous_scale="YlGnBu",
                      title="Relación Tiempo de Estudio vs Nota Final (G3)",
                      labels={'alcohol_avg': 'Consumo Promedio de Alcohol'})
    fig1.update_traces(marker=dict(
    size=7,
    line=dict(
        width=0.5,
        color='black'
    )), selector=dict(mode='markers'))

    fig2 = px.scatter(dff, x="goout", y="G3", color="alcohol_avg",
                      color_continuous_scale="Blues",
                      title="Relación Salidas con Amigos vs Nota Final (G3)",
                      labels={'alcohol_avg': 'Consumo Promedio de Alcohol'})
    fig2.update_traces(marker=dict(
    size=7,
    line=dict(
        width=0.5,
        color='black'
    )), selector=dict(mode='markers'))
    
    edu_avg = dff.groupby(["Medu", "Fedu"], as_index=False)["G3"].mean()
    # fig3 = px.bar(edu_avg, x="Medu", y="Fedu", color="G3",
    #               title="Comparación de Nota Final por Nivel Educ.<br>de ambos padres",
    #               labels={'Medu': 'Educación Madre', 'Fedu': 'Educación Padre', 'G3': 'Nota Final Promedio'})
    pivot = edu_avg.pivot(index='Medu', columns='Fedu', values='G3').sort_index(ascending=False).fillna(0).round(2)

    fig3 = px.imshow(
        pivot,
        labels={'x': 'Educación Padre (Fedu)', 'y': 'Educación Madre (Medu)', 'color': 'Nota G3'},
        x=pivot.columns.astype(str),
        y=pivot.index.astype(str),
        color_continuous_scale='Blues',
        text_auto=True,
        title="Comparación de Nota Final por Nivel Educ.<br>de ambos padres (heatmap)"
    )
    fig3.update_layout(margin={'t': 70})

    fig4 = px.box(
        dff, x="famrel", y="G3", color="alcohol_cat",
        title="Distribución de Notas Finales según Calidad Rel. Familiar",
        labels={'famrel': 'Relación Familiar', 'G3': 'Nota Final', 'alcohol_cat': 'Consumo Alcohol'},
        color_discrete_sequence=["#98CA93", "#41B6C4", "#225EA8"]  # 98CA93 Paleta igual a los otros gráficos
    )
    fig4.update_traces(marker=dict(line=dict(width=0.5, color='black')))
    fig4.update_layout(legend_title_text="Consumo de Alcohol")

    prom = dff[["G1", "G2", "G3"]].mean().reset_index()
    prom.columns = ["Evaluación", "Promedio"]
    fig5 = px.line(
        prom, x="Evaluación", y="Promedio", markers=True,
        title="Evolución de Notas (G1, G2, G3)"
    )
    fig5.update_traces(line=dict(color="#1C75BD",width=3))

    corr = dff.corr(numeric_only=True)
    fig6 = px.imshow(corr, title="Matriz de Correlación de Variables",
                     color_continuous_scale=["#FBFDCF", "#41B6C3", "#091D5B"]) if not corr.empty else go.Figure().add_annotation(text="Sin datos suficientes", showarrow=False)
    fig6.update_xaxes(tickangle=45)

    alcohol_avg = dff.groupby(["Dalc", "Walc"], as_index=False)["G3"].mean()
    fig7 = px.bar(
        alcohol_avg, x="Dalc", y="G3", color="Walc",
        title="Nota Final (G3) promedio según Consumo de Alcohol",
        labels={'Dalc': 'Consumo Diario', 'Walc': 'Consumo Fines de Semana', 'G3': 'Nota Promedio'},
        color_continuous_scale="YlGnBu"
    )

    return kpi_avg_g3, kpi_pass_rate, kpi_alcohol, kpi_studytime, fig1, fig2, fig3, fig4, fig5, fig6, fig7

# Ejecutar servidor
if __name__ == '__main__':
    app.run(debug=True)


