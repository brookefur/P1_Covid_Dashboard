from bokeh.layouts import column
from bokeh.models import ColumnDataSource, CustomJS, DatePicker
from bokeh.plotting import figure, show
from bokeh.embed import file_html
from bokeh.resources import CDN
import json
import pandas as pd

#open file, get data
filef = open('CovidData.2022-12-09.full.json')
covidData = json.load(filef)
filef.close()

#Get all of the data out of the dictionaries, and into lists I can use
numCountries = len(list(covidData.keys()))
nameCountries = []
dailyDper100 = []
key1 = list(covidData.keys())[0]
dates = pd.to_datetime(list(covidData[key1]['Dates'].values()))
#all dates for all countries are the same
#this adds data in order of the countries
for i in covidData.keys():
    nameCountries.append(i)
    dailyDper100.append(list(covidData[i]['Daily Deaths per 100k'].values()))



y = nameCountries
right = [dailyDper100[i][-1] for i in range (0,numCountries)]
index = 
source = ColumnDataSource(data=dict(y=y, right=right))

plot = figure(y_range = nameCountries,width=400, height=400)
plot.hbar(right='right', y='y',source=source, line_width=3, line_alpha=0.6)

callback = CustomJS(args=dict(source=source,DD100=dailyDper100), code="""
    const f = cb_obj.value
    const y = source.data.y
    const right = Array.from(y,(y) => );
    
    source.data = {  y,right }
""")

date_picker = DatePicker(title='Select date', value=dates[-1].date(), min_date=dates[0].date(), max_date=dates[-1].date(),height=50,width=100)
date_picker.js_on_change("value", callback)

layout = column(date_picker, plot)

html = file_html(layout, CDN, "COVID Dashboard")

f = open('testTest.html', 'w')
f.write(html)
f.close()