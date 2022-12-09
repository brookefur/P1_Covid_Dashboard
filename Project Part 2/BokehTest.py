import json
import pandas as pd
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html
from bokeh.layouts import row, column
from bokeh.palettes import viridis
from bokeh.models import FactorRange, ColumnDataSource
from bokeh.transform import dodge
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






# only using 2 countries, displaying all of their data
#Make title be htmal or something, it gets cut off
titletext="Data for " + nameCountries[0].upper() + " and "+nameCountries[1].upper() + " on " + dates[-1].strftime("%m/%d/%Y")

x1 = ["Daily Deaths"]
x2 = [nameCountries[0],nameCountries[1]]
xplot = [(x1s,x2s) for x1s in x1 for x2s in x2]
yplot = (dailyDeaths[0][-1],dailyDeaths[1][-1])
smallplot1 = figure(x_range=FactorRange(*xplot), height=200, title=titletext,width=200,toolbar_location=None, tools="")
smallplot1.vbar(x=xplot, top=yplot, width=0.2, )

x1 = ["Total Deaths"]
x2 = [nameCountries[0],nameCountries[1]]
xplot = [(x1s,x2s) for x1s in x1 for x2s in x2]
yplot = (totalDeaths[0][-1],totalDeaths[1][-1])
smallplot2 = figure(x_range=FactorRange(*xplot), height=200,width=200,toolbar_location=None, tools="")
smallplot2.vbar(x=xplot, top=yplot, width=0.2 )

x1 = ["Daily Deaths per 100k"]
x2 = [nameCountries[0],nameCountries[1]]
xplot = [(x1s,x2s) for x1s in x1 for x2s in x2]
yplot = (dailyDper100[0][-1],dailyDper100[1][-1])
smallplot3 = figure(x_range=FactorRange(*xplot), height=200,width=200,toolbar_location=None, tools="")
smallplot3.vbar(x=xplot, top=yplot, width=0.2 )

x1 = ["Total Deaths per 100k"]
x2 = [nameCountries[0],nameCountries[1]]
xplot = [(x1s,x2s) for x1s in x1 for x2s in x2]
yplot = (totalDper100[0][-1],totalDper100[1][-1])
smallplot4 = figure(x_range=FactorRange(*xplot), height=200,width=200,toolbar_location=None, tools="")
smallplot4.vbar(x=xplot, top=yplot, width=0.2 )

plot1 = row(smallplot1,smallplot2)
plot2 = row(smallplot3,smallplot4)
plots = column(plot1,plot2)
html = file_html(plots, CDN, "COVID Dashboard")
f = open('BokehTest.html', 'w')
f.write(html)
f.close()




# $.getJSON('mydata.json', function(data) {});
# Put in html, use to access data


