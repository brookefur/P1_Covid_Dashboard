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
from bokeh.models import Div
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
    lineplot = figure(x_axis_type="datetime", title="Daily Deaths since 2020-02-15 (Rolling Average = 7 days)",height=600,width=600)
    colorNames = viridis(numCountries)
    for i in range(0,numCountries):
        Cname = nameCountries[i]
        rolling_mean = pd.Series(dailyDeaths[i]).rolling(7).mean()
        lineplot.line(dates,rolling_mean,legend_label = Cname,line_color = colorNames[i],line_width=1.5)
    lineplot.legend.click_policy="hide"
    lineplot.xaxis.axis_label = "Select a country in the legend to hide it."

    #this is for the bar graph, it takes the total deaths
    topDeaths = []
    for i in totalDeaths:
        topDeaths.append(i[-1])
    titletext = "Total Covid Deaths on " + dates[-1].strftime("%m/%d/%Y")
    barplot = figure(x_range=nameCountries, title=titletext,height = 600,width=600)
    barplot.vbar(x=nameCountries, top=topDeaths, width=0.9, color=colorNames)
    barplot.yaxis.formatter.use_scientific = False

    # only using 2 countries, displaying all of their data
    #Make title be htmal or something, it gets cut off
    c1=0 
    c2=3
    day=-1 # -1 input makes it current
    titletext="Data for " + nameCountries[c1].upper() + " and "+nameCountries[c2].upper() + " on " + dates[day].strftime("%m/%d/%Y")

    x1 = ["Daily Deaths"]
    x2 = [nameCountries[c1],nameCountries[c2]]
    xplot = [(x1s,x2s) for x1s in x1 for x2s in x2]
    yplot = (dailyDeaths[c1][day],dailyDeaths[1][day])
    smallplot1 = figure(x_range=FactorRange(*xplot), height=300,width=300,toolbar_location=None, tools="")
    smallplot1.vbar(x=xplot, top=yplot, width=0.2, color=[colorNames[c1],colorNames[c2]] )

    x1 = ["Total Deaths"]
    x2 = [nameCountries[c1],nameCountries[c2]]
    xplot = [(x1s,x2s) for x1s in x1 for x2s in x2]
    yplot = (totalDeaths[c1][day],totalDeaths[c2][day])
    smallplot2 = figure(x_range=FactorRange(*xplot), height=300,width=300,toolbar_location=None, tools="")
    smallplot2.vbar(x=xplot, top=yplot, width=0.2, color=[colorNames[c1],colorNames[c2]] )
    smallplot2.yaxis.formatter.use_scientific = False

    x1 = ["Daily Deaths per 100k"]
    x2 = [nameCountries[c1],nameCountries[c2]]
    xplot = [(x1s,x2s) for x1s in x1 for x2s in x2]
    yplot = (dailyDper100[c1][day],dailyDper100[c2][day])
    smallplot3 = figure(x_range=FactorRange(*xplot), height=300,width=300,toolbar_location=None, tools="")
    smallplot3.vbar(x=xplot, top=yplot, width=0.2,  color=[colorNames[c1],colorNames[c2]])
    smallplot3.yaxis.formatter.use_scientific = False

    x1 = ["Total Deaths per 100k"]
    x2 = [nameCountries[c1],nameCountries[c2]]
    xplot = [(x1s,x2s) for x1s in x1 for x2s in x2]
    yplot = (totalDper100[c1][day],totalDper100[c2][day])
    smallplot4 = figure(x_range=FactorRange(*xplot), height=300,width=300,toolbar_location=None, tools="")
    smallplot4.vbar(x=xplot, top=yplot, width=0.2, color=[colorNames[c1],colorNames[c2]])
    smallplot4.yaxis.formatter.use_scientific = False

    smallplots1 = row(smallplot1,smallplot2)
    smallplots2 = row(smallplot3,smallplot4)
    text = Div(text=titletext,align='center')
    smallplot = column(text, smallplots1,smallplots2)

    #interactive plot, uses tabs
    tabs = []
    for i in range(0,numCountries):
        plot = figure(x_axis_type="datetime",width=600, height=600,title="Total Deaths per 100k (Rolling Average = 7 days)")
        rolling_mean = pd.Series(totalDper100[i]).rolling(7).mean()
        plot.line(dates,rolling_mean, line_width=1.5, color=colorNames[i])
        plot.yaxis.formatter.use_scientific = False
        tab = TabPanel(child=plot,title=nameCountries[i])
        tabs.append(tab)
    tabplot=Tabs(tabs=tabs)

    htmlTitle = """
        <!DOCTYPE html>
        <html>
        <body>
        <center>
        <h1>Covid Dashboard 2022</h1>
        <p>By James Rosenberg and Brooke Boone</p>
        </body>
        </center>
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
    print("DashBoard Exported")
