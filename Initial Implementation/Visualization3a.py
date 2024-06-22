import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from bokeh.layouts import column, row
from bokeh.models import Select, ColumnDataSource
from bokeh.plotting import figure, curdoc
import geopandas as gpd
from io import BytesIO
from PIL import Image
import base64

names = pd.read_csv("dpt2020.csv", sep=";")
names.drop(names[names.preusuel == '_PRENOMS_RARES'].index, inplace=True)
names.drop(names[names.dpt == 'XX'].index, inplace=True)
just_names = names
depts = gpd.read_file('departements-avec-outre-mer.geojson')
names_grouped_by_name = names.groupby(
    ['preusuel', 'annais', 'sexe']).nombre.sum().reset_index()
names = depts.merge(names, how='right', left_on='code', right_on='dpt')

years = sorted(names['annais'].unique().tolist(), reverse=True)
departments = sorted(names['nom'].dropna().unique().tolist())
departments.insert(0, 'Tous les départements')


def mpl_to_bokeh(fig):
    buf = BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    img = Image.open(buf)
    img = img.resize((1600, 800), Image.LANCZOS)
    buf = BytesIO()
    img.save(buf, format='png')
    img64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    return img64


def generate_wordcloud(department, year):
    fig, axes = plt.subplots(1, 2, figsize=(50, 25))
    if department == 'Tous les départements':
        df_filtered = names_grouped_by_name[names_grouped_by_name['annais'] == str(
            year)]
        code = '--'
    else:
        df_filtered = names[(names['nom'] == str(department))
                            & (names['annais'] == str(year))]
        dpts_data = names.loc[names['nom'] == department]
        code = dpts_data['code'].iloc[0]
        if code is None:
            code = 'code unfound'

    if df_filtered.empty:
        print(f"No data for year {year} and department {department}")
        axes[0].set_title('Pas de données', color='red', fontsize=20, pad=20)
        axes[0].imshow([], interpolation='bilinear')
        axes[0].axis('off')
        axes[1].set_title('Pas de données', color='red', fontsize=20, pad=20)
        axes[1].imshow([], interpolation='bilinear')
        axes[1].axis('off')
        fig.text(0.5, 0.5, f'Année : {year}',
                 fontsize=150, color='black', ha='center')
        fig.text(0.5, 0.45, f'{department} ({code})',
                 fontsize=75, color='grey', ha='center')
        return mpl_to_bokeh(fig)

    df_male = df_filtered[df_filtered['sexe'] == 1].groupby(
        'preusuel', as_index=False)['nombre'].sum()
    df_female = df_filtered[df_filtered['sexe'] == 2].groupby(
        'preusuel', as_index=False)['nombre'].sum()

    if df_male.empty and df_female.empty:
        print(
            f"No male or female names for year {year} and department {department}")
        axes[0].set_title(
            'Pas de données pour les prénoms masculins', color='red', fontsize=65, pad=20)
        axes[0].imshow([], interpolation='bilinear')
        axes[0].axis('off')
        axes[1].set_title('Pas de données pour les prénoms féminins',
                          color='red', fontsize=65, pad=20)
        axes[1].imshow([], interpolation='bilinear')
        axes[1].axis('off')
        fig.text(0.5, 0.5, f'Année : {year}',
                 fontsize=150, color='black', ha='center')
        fig.text(0.5, 0.45, f'{department} ({code})',
                 fontsize=75, color='grey', ha='center')
        return mpl_to_bokeh(fig)

    male_freq = dict(zip(df_male['preusuel'], df_male['nombre']))
    female_freq = dict(zip(df_female['preusuel'], df_female['nombre']))

    if not male_freq and not female_freq:
        print(
            f"No frequencies found for year {year} and department {department}")
        axes[0].set_title('Pas de données', color='red', fontsize=65, pad=20)
        axes[0].imshow([], interpolation='bilinear')
        axes[0].axis('off')
        axes[1].set_title('Pas de données', color='red', fontsize=65, pad=20)
        axes[1].imshow([], interpolation='bilinear')
        axes[1].axis('off')
        fig.text(0.5, 0.5, f'Année : {year}',
                 fontsize=150, color='black', ha='center')
        fig.text(0.5, 0.45, f'{department} ({code})',
                 fontsize=75, color='grey', ha='center')
        return mpl_to_bokeh(fig)

    wordcloud_male = WordCloud(
        width=1200, height=500, background_color='white').generate_from_frequencies(male_freq)
    wordcloud_female = WordCloud(
        width=1200, height=500, background_color='white').generate_from_frequencies(female_freq)

    axes[0].clear()
    if male_freq:
        axes[0].set_title('Prénoms masculins',
                          color='blue', fontsize=65, pad=20)
        axes[0].imshow(wordcloud_male, interpolation='bilinear')
    else:
        axes[0].set_title(
            'Pas de données pour les prénoms masculins', color='red', fontsize=65, pad=20)
    axes[0].axis('off')

    axes[1].clear()
    if female_freq:
        axes[1].set_title('Prénoms féminins',
                          color='#FF1493', fontsize=65, pad=20)
        axes[1].imshow(wordcloud_female, interpolation='bilinear')
    else:
        axes[1].set_title('Pas de données pour les prénoms féminins',
                          color='red', fontsize=65, pad=20)
    axes[1].axis('off')

    fig.texts.clear()
    fig.text(0.5, 0.90, f'Année : {year}',
             fontsize=150, color='black', ha='center')
    fig.text(0.5, 0.85, f'{department} ({code})',
             fontsize=75, color='grey', ha='center')
    plt.tight_layout(pad=3.0)
    return mpl_to_bokeh(fig)


def update_wordcloud(attr, old, new):
    department = department_selector.value
    year = year_selector.value
    img64 = generate_wordcloud(department, year)
    img_source.data = dict(url=[f'data:image/png;base64,{img64}'])


department_selector = Select(
    title="Département:", value=departments[0], options=departments)
year_selector = Select(title="Année:", value=years[0], options=years)

department_selector.on_change('value', update_wordcloud)
year_selector.on_change('value', update_wordcloud)

img_source = ColumnDataSource(data=dict(url=[]))
img = figure(x_range=(0, 1), y_range=(0, 1), width=1600,
             height=800, title="WordCloud", toolbar_location=None)
img.axis.visible = False
img.grid.visible = False
img.outline_line_color = None
img.image_url(url='url', x=0, y=1, w=1, h=1, source=img_source)

layout = column(row(department_selector, year_selector), img)
curdoc().add_root(layout)

update_wordcloud(None, None, None)

# !bokeh serve --show Visualization3a.py
