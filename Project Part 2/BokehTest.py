import json
import pandas as pd
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html
from bokeh.models import MultiChoice, CustomJS
from bokeh.palettes import viridis
from bokeh.layouts import column
"""
This is a test file for running bokeh and creating html files. I will be creating the official file later,
this is just a little file for all the important kewords/commands I need to remember.

Also: I'm assuming our profs open the html file, and I need to make the html file be able to use our json files

@author: Brooke Boone
"""

#open file, get data
filef = open('CovidData.2022-12-03.json')
covidData = json.load(filef)
filef.close()

numCountries = len(list(covidData.keys()))
nameCountries = []
dailyDeaths = []
totalDeaths = []
key1 = list(covidData.keys())[0]
dates = pd.to_datetime(list(covidData[key1]['Dates'].values()))
#for now, assuming all dates for all countries are the same

#this takes all data in the dictionary into lists. We need lists for plotting
for i in covidData.keys():
    nameCountries.append(i)
    dailyDeaths.append(list(covidData[i]['Daily Deaths'].values()))
    totalDeaths.append(list(covidData[i]['Total Deaths'].values()))

lineplot = figure(x_axis_type="datetime")
colorNames = viridis(len(nameCountries))
for i in range(0,len(nameCountries)):
    Cname = nameCountries[i]
    lineplot.line(dates,dailyDeaths[i],legend_label = Cname,line_color = colorNames[i])
lineplot.legend.click_policy="hide"


p = column(lineplot)
html = file_html(p, CDN, "COVID Dashboard")
f = open('TEST.html', 'w')
f.write(html)
f.close()





# $.getJSON('mydata.json', function(data) {});
# Put in html, use to access data


