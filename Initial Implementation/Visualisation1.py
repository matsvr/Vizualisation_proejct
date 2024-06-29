import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from dash.dependencies import Input, Output

# Charger les données avec le bon séparateur
df = pd.read_csv('dpt2020.csv', sep=';')

# Convertir les colonnes en numérique, en gérant les erreurs
df['annais'] = pd.to_numeric(df['annais'], errors='coerce')
df['nombre'] = pd.to_numeric(df['nombre'], errors='coerce')

# Filtrer les données pour une période spécifique si nécessaire
df = df[(df['annais'] >= 1900) & (df['annais'] <= 2020)]

# Générer une palette de couleurs unique pour chaque prénom
colors = px.colors.qualitative.Set3  # Utiliser une palette de couleurs plus douce

def assign_colors(df):
    prénoms = df['preusuel'].unique()
    color_map = {prénom: colors[i % len(colors)] for i, prénom in enumerate(prénoms)}
    df['color'] = df['preusuel'].map(color_map)
    return df

df = assign_colors(df)

# Initialiser l'application Dash
app = dash.Dash(__name__)

# Définir la disposition de l'application
app.layout = html.Div(style={'backgroundColor': '#f8f9fa', 'height': '100vh'}, children=[
    html.Div(style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '5px', 'margin': '10px'}, children=[
        html.H1(children='Visualisation des prénoms en France'),

        html.Div(children='''
            Comment les prénoms ont évolué en popularité de 1900 à 2020 ?
        ''')
    ]),

    html.Div(style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '5px', 'margin': '10px'}, children=[
        html.Label('Sélectionnez le sexe:', style={'fontWeight': 'bold', 'fontSize': '16px'}),
        dcc.RadioItems(
            id='sex-filter',
            options=[
                {'label': 'Tous', 'value': 'Tous'},
                {'label': 'Garçons', 'value': 1},
                {'label': 'Filles', 'value': 2}
            ],
            value='Tous',
            labelStyle={'display': 'inline-block', 'marginRight': '10px'}
        ),
        html.Br(),
        html.Label('Sélectionnez le département:', style={'fontWeight': 'bold', 'fontSize': '16px'}),
        dcc.Dropdown(
            id='department-filter',
            options=[{'label': dpt, 'value': dpt} for dpt in df['dpt'].unique()],
            value=None,
            multi=True,
            style={'marginBottom': '20px'}
        ),
        html.Br(),
        html.Label('Sélectionnez le type:', style={'fontWeight': 'bold', 'fontSize': '16px'}),
        dcc.RadioItems(
            id='popularity-filter',
            options=[
                {'label': 'Les plus populaires', 'value': 'populaire'},
                {'label': 'Les moins populaires', 'value': 'impopulaire'}
            ],
            value='populaire',
            labelStyle={'display': 'inline-block', 'marginRight': '10px'}
        )
    ]),

    html.Div(style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '5px', 'margin': '10px', 'flex': '1'}, children=[
        dcc.Graph(
            id='bar-race-chart',
            style={'height': '70vh'}
        )
    ])
])

# Définir les callbacks pour mettre à jour le graphique en fonction des filtres
@app.callback(
    Output('bar-race-chart', 'figure'),
    [Input('sex-filter', 'value'),
     Input('department-filter', 'value'),
     Input('popularity-filter', 'value')]
)
def update_bar_race(selected_sex, selected_departments, popularity_type):
    filtered_df = df
    if selected_sex != 'Tous':
        filtered_df = filtered_df[filtered_df['sexe'] == selected_sex]
    if selected_departments:
        filtered_df = filtered_df[filtered_df['dpt'].isin(selected_departments)]

    # Grouper les données par année et prénom, puis calculer la somme des naissances pour chaque prénom chaque année
    grouped_df = filtered_df.groupby(['annais', 'preusuel', 'color'])['nombre'].sum().reset_index()

    # Filtrer pour obtenir le top 15 prénoms chaque année ou les 15 moins populaires
    def get_top_15(df, ascending=True):
        top_15 = df.sort_values(by='nombre', ascending=ascending).groupby('annais').head(15)
        return top_15

    top_15_df = get_top_15(grouped_df, ascending=(popularity_type == 'impopulaire'))

    # Créer la figure de la course de barres
    years = sorted(top_15_df['annais'].unique())
    frames = []
    for year in years:
        frame_data = top_15_df[top_15_df['annais'] == year]
        frame = go.Frame(
            data=[go.Bar(
                x=frame_data['nombre'],
                y=frame_data['preusuel'],
                text=frame_data.apply(lambda row: f"{row['preusuel']} ({row['nombre']})", axis=1),
                textposition='inside',
                orientation='h',
                marker=dict(color=frame_data['color'])
            )],
            name=str(year),
            layout=go.Layout(
                title=f'Prénoms {"les moins populaires" if popularity_type == "impopulaire" else "les plus populaires"} en {int(year)}',
            )
        )
        frames.append(frame)

    # Créer la figure initiale
    initial_data = top_15_df[top_15_df['annais'] == years[0]]
    fig = go.Figure(
        data=[go.Bar(
            x=initial_data['nombre'],
            y=initial_data['preusuel'],
            text=initial_data.apply(lambda row: f"{row['preusuel']} ({row['nombre']})", axis=1),
            textposition='inside',
            orientation='h',
            marker=dict(color=initial_data['color'])
        )],
        layout=go.Layout(
            title=f'Prénoms {"les moins populaires" if popularity_type == "impopulaire" else "les plus populaires"} en {int(years[0])}',
            xaxis=dict(title='Nombre de naissances', range=[0, top_15_df['nombre'].max() * 1.1]),  # Ajuster la plage de l'axe x dynamiquement
            yaxis=dict(title='Prénom', autorange='reversed'),
            margin=dict(l=100, r=40, t=40, b=40),  # Ajuster les marges
            transition=dict(duration=500),
            updatemenus=[dict(
                type='buttons',
                showactive=False,
                y=1,
                x=1.15,
                xanchor='right',
                yanchor='top',
                pad=dict(t=0, r=10),
                buttons=[
                    dict(
                        label='Play',
                        method='animate',
                        args=[None, dict(frame=dict(duration=500, redraw=True), 
                                         fromcurrent=True, mode='immediate')]
                    ),
                    dict(
                        label='Stop',
                        method='animate',
                        args=[[None], dict(frame=dict(duration=0, redraw=False), 
                                          mode='immediate', transition=dict(duration=0))]
                    )
                ]
            )]
        ),
        frames=frames
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
