import json
import pandas as pd
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html
from bokeh.layouts import row, column
from bokeh.palettes import viridis
from bokeh.models import FactorRange
from bokeh.transform import dodge
from bokeh.models import TabPanel, Tabs
"""
This file takes the json file from the datascraping, and uses Bokeh to make an interactive html site
- Making assumption that in the JSON, you already got the data for the countries you want (don't need input on what countries to select out of JSON)
- Making assumption that the focus is on numbers for the most recent date.
- assuming at least 2 countries are on the JSON file

@author: Brooke Boone
"""
def dataDisplay(jsonName):
    #assuming jsonName is correct
    #open file, get data
    filef = open(jsonName)
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


    #plotting historical data as a line graph
    lineplot = figure(x_axis_type="datetime", title="Daily Deaths since 2022-02-15",height=600,width=600)
    colorNames = viridis(numCountries)
    for i in range(0,numCountries):
        Cname = nameCountries[i]
        lineplot.line(dates,dailyDeaths[i],legend_label = Cname,line_color = colorNames[i])
    lineplot.legend.click_policy="hide"
    lineplot.xaxis.axis_label = "Select a country in the legend to hide it."


    #this is for the bar graph, it takes the total deaths
    topDeaths = []
    for i in totalDeaths:
        topDeaths.append(i[-1])
    titletext = "Total Covid Deaths on " + dates[-1].strftime("%m/%d/%Y")
    barplot = figure(x_range=nameCountries, title=titletext,height = 600,width=600)
    barplot.vbar(x=nameCountries, top=topDeaths, width=0.9)


    # only using 2 countries, displaying all of their data
    #Make title be htmal or something, it gets cut off
    titletext="Data for " + nameCountries[0].upper() + " and "+nameCountries[1].upper() + " on " + dates[-1].strftime("%m/%d/%Y")

    x1 = ["Daily Deaths"]
    x2 = [nameCountries[0],nameCountries[1]]
    xplot = [(x1s,x2s) for x1s in x1 for x2s in x2]
    yplot = (dailyDeaths[0][-1],dailyDeaths[1][-1])
    smallplot1 = figure(x_range=FactorRange(*xplot), height=300,width=300,toolbar_location=None, tools="")
    smallplot1.vbar(x=xplot, top=yplot, width=0.2, )

    x1 = ["Total Deaths"]
    x2 = [nameCountries[0],nameCountries[1]]
    xplot = [(x1s,x2s) for x1s in x1 for x2s in x2]
    yplot = (totalDeaths[0][-1],totalDeaths[1][-1])
    smallplot2 = figure(x_range=FactorRange(*xplot), height=300,width=300,toolbar_location=None, tools="", title=titletext)
    smallplot2.vbar(x=xplot, top=yplot, width=0.2 )

    x1 = ["Daily Deaths per 100k"]
    x2 = [nameCountries[0],nameCountries[1]]
    xplot = [(x1s,x2s) for x1s in x1 for x2s in x2]
    yplot = (dailyDper100[0][-1],dailyDper100[1][-1])
    smallplot3 = figure(x_range=FactorRange(*xplot), height=300,width=300,toolbar_location=None, tools="")
    smallplot3.vbar(x=xplot, top=yplot, width=0.2 )

    x1 = ["Total Deaths per 100k"]
    x2 = [nameCountries[0],nameCountries[1]]
    xplot = [(x1s,x2s) for x1s in x1 for x2s in x2]
    yplot = (totalDper100[0][-1],totalDper100[1][-1])
    smallplot4 = figure(x_range=FactorRange(*xplot), height=300,width=300,toolbar_location=None, tools="")
    smallplot4.vbar(x=xplot, top=yplot, width=0.2)

    smallplots1 = row(smallplot1,smallplot2)
    smallplots2 = row(smallplot3,smallplot4)
    smallplot = column(smallplots1,smallplots2)


    #interactive plot, uses tabs
    tabs = []
    for i in range(0,numCountries):
        plot = figure(x_axis_type="datetime",width=600, height=600,title="Daily Deaths per 100k")
        plot.line(dates,dailyDper100[i])
        tab = TabPanel(child=plot,title=nameCountries[i])
        tabs.append(tab)
    tabplot=Tabs(tabs=tabs)

    htmlTitle = """
        <!DOCTYPE html>
        <html>
        <body>
        <h1>Covid Dashboard 2022</h1>
        <p>By James Rosenberg and Brooke Boone</p>
        </body>
        </html> 
    """



    #put all the plots into rows and columns
    row1 = row( barplot,smallplot) #historical data, bar with all countries and 1 piece of data
    row2 = row(lineplot,tabplot) # data for first 2 countries, interactive plot
    dashboard = column(row1,row2)
    html = htmlTitle + file_html(dashboard, CDN, "COVID Dashboard")
    f = open('CovidDashboard.html', 'w')
    f.write(html)
    f.close()

