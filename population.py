import pandas as pd

#from bokeh.charts import Bar
from bokeh.io import output_file, show
from bokeh.plotting import ColumnDataSource, figure
from bokeh.models import CategoricalColorMapper, HoverTool
from bokeh.layouts import column, row

output_file('pop-life.html')

file = 'country-pops.csv'

countries = pd.read_csv(file)

country_data = ColumnDataSource(countries)

color_mapper = CategoricalColorMapper(factors=['Asia', 'Africa', 'Antarctica', 
                                                'Australia', 'Central America', 
                                                'Europe', 'North America', 
                                                'Oceania', 'South America'],
                                    palette=['#00FF00', '#FFD343', 
                                            'darkgray', 'brown', 'cyan', 
                                            'crimson', 'red', '#0000FF', 
                                            'purple'])

TOOLTIPS = 'pan, wheel_zoom, box_zoom, reset, hover, save'
                                            

plot = figure(x_axis_label="Population", y_axis_label="Life Expectancy", tools=TOOLTIPS, title="Population vs. Life Expectancy")

plot_birthrate = figure(x_axis_label="Population", y_axis_label="Birthrate", title="Population vs. Birthrate", tools=TOOLTIPS)

plot_deathrate = figure(x_axis_label="Population", y_axis_label="Deathrate", title="Population vs. Deathrate", tools=TOOLTIPS)

plot.diamond(x='Population', y="Life_expectancy", source=country_data, size=10, color=dict(field="Continent", transform=color_mapper), legend='Continent')

plot_birthrate.circle(x="Population", y='Birthrate', source=country_data, size=10, color=dict(field="Continent", transform=color_mapper), legend='Continent')

plot_deathrate.triangle(x="Population", y='Deathrate', source=country_data, size=10, color=dict(field="Continent", transform=color_mapper), legend='Continent')

hover = plot.select_one(HoverTool)

hover.tooltips = [('Country Name English', '@Country_English'),
                ('Population', '@Population'),
                ('Life Expectancy (years)', '@Life_expectancy')]

plot.legend.location = 'bottom_right'
plot.legend.background_fill_color = 'lightgrey'

plot_birthrate.x_range = plot.x_range
plot_deathrate.x_range = plot.x_range

show(row(column(plot, plot_birthrate), column(plot_deathrate)))

#bar_chart = Bar(countries, 'Country_English', values='Population', title='Population', legend=False)

#show(bar_chart)