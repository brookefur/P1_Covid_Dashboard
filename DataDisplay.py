import json
import pandas as pd
import matplotlib.colors as mcolors
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html

"""
This file takes the json file from the datascraping, and uses Bokeh to make an interactive html site

@author: Brooke Boone
"""

#open file, get data
filef = open('CovidData.json')
covidData = json.load(filef)
filef.close()

numCountries = len(list(covidData.keys()))
nameCountries = []
dailyDeaths = []
key1 = list(covidData.keys())[0]
dates = pd.to_datetime(list(covidData[key1]['Dates'].values()))
#for now, assuming all dates for all countries are the same

#this takes all data in the dictionary into lists. We need lists for plotting
for i in covidData.keys():
    nameCountries.append(i)
    dailyDeaths.append(list(covidData[i]['Daily Deaths'].values()))


plot = figure(x_axis_type="datetime")
colorNames = list(mcolors.CSS4_COLORS.keys())
for i in range(0,len(nameCountries)):
    Cname = nameCountries[i]
    plot.line(dates,dailyDeaths[i],legend_label = Cname,line_color = colorNames[i])

#plot.line(dates,dailyDeaths[0], legend_label = "country1")
#plot.line(dates,dailyDeaths[1], legend_label = "country2")

html = file_html(plot, CDN, "COVID Dashboard")
f = open('CovidDashboard.html', 'w')
f.write(html)
f.close()
