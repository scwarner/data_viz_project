import numpy as np
import pandas as pd

from bokeh.charts import Bar
from bokeh.io import output_file, show

output_file('population.html')

file = 'country-pops.csv'

countries = pd.read_csv(file, nrows=5)
countries_array = np.array(countries.head)

#print(countries_array)

bar_chart = Bar(countries, 'Country_English', values='Population', title='Population', legend=False)

show(bar_chart)