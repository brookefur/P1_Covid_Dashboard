import json
import pandas as pd
import matplotlib.colors as mcolors
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html
from bokeh.layouts import row

"""
This file takes the json file from the datascraping, and uses Bokeh to make an interactive html site

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
#all dates for all countries are the same

#this takes all data in the dictionary into lists. We need lists for plotting
for i in covidData.keys():
    nameCountries.append(i)
    dailyDeaths.append(list(covidData[i]['Daily Deaths'].values()))
    totalDeaths.append(list(covidData[i]['Total Deaths'].values()))


lineplot = figure(x_axis_type="datetime")
colorNames = list(mcolors.CSS4_COLORS.keys())
for i in range(0,len(nameCountries)):
    Cname = nameCountries[i]
    lineplot.line(dates,dailyDeaths[i],legend_label = Cname,line_color = colorNames[i+20])
lineplot.legend.click_policy="hide"


#this is for the bar graph, it takes the total deaths
topDeaths = []
for i in totalDeaths:
    topDeaths.append(i[-1])

barplot = figure(x_range=nameCountries)
barplot.vbar(x=nameCountries, top=topDeaths, width=0.9)

p = row(lineplot, barplot)
html = file_html(p, CDN, "COVID Dashboard")
f = open('CovidDashboard.html', 'w')
f.write(html)
f.close()
