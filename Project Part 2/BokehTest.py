import json
import pandas as pd
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html
from bokeh.layouts import row, column
from bokeh.palettes import viridis
from bokeh.models import DatePicker, CustomJS
from datetime import date
"""
This is a test file for running bokeh and creating html files. I will be creating the official file later,
this is just a little file for all the important kewords/commands I need to remember.

Also: I'm assuming our profs open the html file, and I need to make the html file be able to use our json files

Currently trying to figure out a bar graph to compare two countries

@author: Brooke Boone
"""

#open file, get data
filef = open('CovidData.2022-12-09.full.json')
covidData = json.load(filef)
filef.close()

#Get all of the data out of the dictionaries, and into lists I can use
numCountries = len(list(covidData.keys()))
nameCountries = []
dailyDeaths = []
totalDeaths = []
dailyDper100 = []
totalDper100 = []
key1 = list(covidData.keys())[0]
dates = pd.to_datetime(list(covidData[key1]['Dates'].values()))
#all dates for all countries are the same
#this adds data in order of the countries
for i in covidData.keys():
    nameCountries.append(i)
    dailyDeaths.append(list(covidData[i]['Daily Deaths'].values()))
    totalDeaths.append(list(covidData[i]['Total Deaths'].values()))
    dailyDper100.append(list(covidData[i]['Daily Deaths per 100k'].values()))
    totalDper100.append(list(covidData[i]['Total Deaths per 100k'].values()))


plot = figure(y_range = nameCountries)
bardata = []
for i in range(0,len(nameCountries)):
    bardata.append(dailyDper100[i][-1])
plot.hbar(right=bardata,y=nameCountries)

callback = CustomJS(args=dict(x=nameCountries,DDper100=dailyDper100,barplot=plot,dates=dates), code = """
    console.log('date_picker: value=' + this.value, this.toString())
    const a = cd_obj.value;
    const y = [];  
    index = dates.indexOf(a)
    for (let i = 0; i < x.length(); i++) {
        y[i] = DDper100[i][a];
    } 
    barplot.hbar(right=y,y=x)
""")

date_picker = DatePicker(title='Select date', value=dates[-1].date(), min_date=dates[0].date(), max_date=dates[-1].date(),height=50,width=100)
date_picker.js_on_change("value", callback)

bokehHTML = column(date_picker,plot)
html = file_html(bokehHTML, CDN, "COVID Dashboard")

f = open('BokehTest.html', 'w')
f.write(html)
f.close()




# $.getJSON('mydata.json', function(data) {});
# Put in html, use to access data


