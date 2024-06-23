import altair as alt
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import geopandas as gpd


df = pd.read_csv('dpt2020.csv', sep=';')

df.drop(df[df.preusuel == '_PRENOMS_RARES'].index, inplace=True)
df.drop(df[df.dpt == 'XX'].index, inplace=True)

df.columns = ['sex', 'name', 'year', 'dept', 'count']

df['year'] = pd.to_numeric(df['year'], errors='coerce').astype('Int64')
df = df[(df['year'] >= 1900) & (df['year'] <= 2000)]

df.sample(5)


dpt_df = gpd.read_file('departements-version-simplifiee.geojson')

dpt_df.sample(5)



name_df = df

name_df_pos = name_df.merge(dpt_df, left_on='dept', right_on='code', how='left')

name_df_pos.drop(columns='code', inplace=True)
name_df_pos.rename(columns={'nom': 'nom_dept'}, inplace=True)

#delete the rows with NaN values
name_df_pos.dropna(inplace=True)
name_df_pos.sample(5)

def create_map(year):
    filtered_data = name_df_pos[name_df_pos['year'] == year]
    grouped = filtered_data.groupby(['dept', 'name']).agg({'count': 'sum'}).reset_index()
    max_count = grouped.loc[grouped.groupby('dept')['count'].idxmax()]
    
    merged = dpt_df.merge(max_count, left_on='code', right_on='dept')
    
    chart = alt.Chart(merged).mark_geoshape(stroke='white').encode(
        color='count:Q',
        tooltip=['nom:N', 'dept:N', 'count:Q', 'name:N']
    ).properties(
        width=800,
        height=600
    ).project(
        type='mercator'
    )
    
    return chart

def create_top50_table(year):
    filtered_data = df[df['year'] == year]
    top50 = filtered_data.groupby('name').agg({'count': 'sum'}).reset_index().nlargest(50, 'count')
    
    return dbc.Table.from_dataframe(top50, striped=True, bordered=True, hover=True)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.H1("Carte des Prénoms en France par Département"),
    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': str(year), 'value': year} for year in range(1900, 2021)],
        value=1900,
        clearable=False
    ),
    html.Div(id='map-container'),
    html.H2("Top 50 des prénoms les plus nombreux"),
    html.Div(id='top50-table')
])

@app.callback(
    [Output('map-container', 'children'),
     Output('top50-table', 'children')],
    [Input('year-dropdown', 'value')]
)
def update_content(selected_year):
    chart = create_map(selected_year)
    table = create_top50_table(selected_year)
    return html.Iframe(
        srcDoc=chart.to_html(),
        style={'width': '100%', 'height': '600px', 'border': 'none'}
    ), table

if __name__ == '__main__':
    app.run_server(debug=True, port=8055)