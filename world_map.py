import numpy as np
import pandas as pd
import requests

from bokeh.io import output_file, show
from bokeh.models import HoverTool
from bokeh.plotting import ColumnDataSource, figure

output_file('world-map.html', title="World Map")

url = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"

TOOLS = 'pan, wheel_zoom, box_zoom, reset, hover, save'

r = requests.get(url)
json_data = r.json()

def get_coordinates(features):
   depth = lambda L: isinstance(L, list) and max(map(depth, L))+1
   country_id = []
   longitudes = []
   latitudes = []

   for feature in json_data['features']:
       coordinates = feature['geometry']['coordinates']
       number_dimensions = depth(coordinates)
       # one border
       if number_dimensions == 3:
           country_id.append(feature['id'])
           points = np.array(coordinates[0], 'f')
           longitudes.append(points[:, 0])
           latitudes.append(points[:, 1])
       # several borders
       else:
           for shape in coordinates:
                country_id.append(feature['id'])
                points = np.array(shape[0], 'f')
                longitudes.append(points[:, 0])
                latitudes.append(points[:, 1])
   return country_id, longitudes, latitudes

country_id, lats, longs = get_coordinates(json_data['features'])

country_coords = []

for index, country in enumerate(country_id):
    land_mass = {'country_code': country, 'latitudes': lats[index], 'longitudes': longs[index]}
    country_coords.append(land_mass)

country_maps = pd.DataFrame(country_coords)

input_file = 'country-pops.csv'
country_populations = pd.read_csv(input_file)

world_map_with_data = country_populations.merge(country_maps, left_on="ISO_3166-1_alpha3", right_on="country_code", how="outer")

map_data = ColumnDataSource(world_map_with_data)

world_map_plot = figure(plot_width=900, plot_height=600, title="World Map", tools=TOOLS, x_range =(-180, 180), y_range=(-90, 90))

world_map_plot.patches(xs='latitudes', ys='longitudes', source=map_data, fill_color="#F1EEF6", fill_alpha=0.7, line_width=2)

hover = world_map_plot.select_one(HoverTool)

hover.tooltips = [('Country Name English', '@Country_English'),
                ('Population', '@Population'),
                ('Life Expectancy (years)', '@Life_expectancy')]

show(world_map_plot)