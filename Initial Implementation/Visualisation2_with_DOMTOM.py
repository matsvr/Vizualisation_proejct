import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import geopandas as gpd
from dash import dcc, html


df = pd.read_csv('Initial Implementation/dpt2020.csv', sep=';')

df.drop(df[df.preusuel == '_PRENOMS_RARES'].index, inplace=True)
df.drop(df[df.dpt == 'XX'].index, inplace=True)

df.columns = ['sex', 'name', 'year', 'dept', 'count']

df['year'] = pd.to_numeric(df['year'], errors='coerce').astype('Int64')
df = df[(df['year'] >= 1900) & (df['year'] <= 2000)]

dpt_df = gpd.read_file('Initial Implementation/departements-avec-outre-mer.geojson')

name_df = df

name_df_pos = name_df.merge(dpt_df, left_on='dept', right_on='code', how='left')

name_df_pos.drop(columns='code', inplace=True)
name_df_pos.rename(columns={'nom': 'nom_dept'}, inplace=True)

name_df_pos.dropna(inplace=True)

def create_map(year):
    filtered_data = df[df['year'] == year]
    grouped = filtered_data.groupby(['dept', 'name']).agg({'count': 'sum'}).reset_index()
    max_count = grouped.loc[grouped.groupby('dept')['count'].idxmax()]
    
    fig = px.choropleth(
        max_count,
        geojson=dpt_df,
        locations='dept',
        featureidkey="properties.code",
        color='count',
        hover_name='name',
        hover_data={'dept': False},
        title=f'Carte des prénoms en {year}',
        projection='mercator'
    )
    
    # Mise à jour de l'apparence de la carte
    fig.update_geos(
        visible=False,
        resolution=50,
        showcountries=True,
        countrycolor="Black"
    )
    
    fig.update_layout(
        width=800,
        height=600,
        margin={"r":0,"t":0,"l":0,"b":0}
    )
    
    return fig

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.H1("Carte des Prénoms en France par Département (y compris DOM-TOM)"),
    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': str(year), 'value': year} for year in range(1900, 2021)],
        value=1900,
        clearable=False
    ),
    dcc.Graph(id='map-container')
])

@app.callback(
    Output('map-container', 'figure'),
    Input('year-dropdown', 'value')
)
def update_map(selected_year):
    fig = create_map(selected_year)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, port=8056)