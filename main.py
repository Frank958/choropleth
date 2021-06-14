import json
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.io as pio

pio.renderers.default = 'browser'

f = open("diaphantinh.geojson", encoding="utf8")
vietnam = json.load(f)
df = pd.read_csv("V02.02.csv")

# Check provinces name error
geo_provinces = set(f['properties']['ten_tinh'] for f in vietnam['features'])
density = df['Địa phương'].to_dict()
density_provinces = set(density.values())
a = density_provinces - geo_provinces
corrections = {
    'Bà Rịa -Vũng Tàu': 'Bà Rịa - Vũng Tàu',
    'Cần Thơn': 'Cần Thơ',
    'Hòa Bình': 'Hoà Bình',
    'Khánh Hòa': 'Khánh Hoà',
    'Kien Giang': 'Kiên Giang',
    'Quản Bình': 'Quảng Bình',
    'TP. Hồ Chí Minh': 'TP.Hồ Chí Minh',
    'Thanh Hóa': 'Thanh Hoá',
    'Đăk Lăk': 'Đắk Lắk',
    'Đăk Nông': 'Đắk Nông'
}
for feature in vietnam['features']:
    name = feature['properties']['ten_tinh']
    if name in corrections:
        # correct province's name if needed
        feature['properties']['ten_tinh'] = corrections[name]
        name = corrections[name]

# Save after correcting json file
with open('vn-density.json', 'w') as f:
    json.dump(vietnam, f)

state_id_map = {}
for feature in vietnam['features']:
    feature['id'] = feature['properties']['gid']
    state_id_map[feature['properties']['ten_tinh']] = feature['id']
df['ID'] = df['Địa phương'].apply(lambda x: state_id_map[x])

df['DensityScale'] = np.log10(df['Mật độ dân số (Người/km2)'])

# Create fig with Choropleth
fig = px.choropleth(
    df, locations='ID',
    geojson=vietnam,
    color='DensityScale',
    scope='asia',
    hover_name='Địa phương',
    hover_data=['Mật độ dân số (Người/km2)']
)
fig.update_geos(fitbounds='locations', visible=False)

# Create fig with Mapbox
fig = px.choropleth_mapbox(
    df, locations='ID',
    geojson=vietnam,
    color='DensityScale',
    hover_name='Địa phương',
    hover_data=['Mật độ dân số (Người/km2)'],
    mapbox_style='carto-positron',
    center={'lat': 16.18, 'lon': 106.660172},
    opacity=0.65, zoom=4.75
    # color_continuous_scale=px.colors.diverging.BrBG,
    # color_continuous_midpoint=0
)
fig.update_geos(fitbounds='locations', visible=False)
fig.show()
