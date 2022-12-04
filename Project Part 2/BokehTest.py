import json
import pandas as pd
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html

"""
This is a test file for running bokeh and creating html files. I will be creating the official file later,
this is just a little file for all the important kewords/commands I need to remember.

Also: I'm assuming our profs open the html file, and I need to make the html file be able to use our json files

@author: Brooke Boone
"""

filef = open('CovidData.json')
covidData = json.load(filef)
filef.close()

dates = pd.to_datetime(list(covidData['us']['Dates'].values()))
deaths = list(covidData['us']['Daily Deaths'].values())

#When setting plot for dates, make sure to adjust x-axis to start at 2020-02-15
#LINE GRAPH
plot = figure(x_axis_type="datetime")
plot.line(dates,deaths)




html = file_html(plot, CDN, "COVID Dashboard")

f = open('test_html.html', 'w')
f.write(html)
f.close()

# $.getJSON('mydata.json', function(data) {});
# Put in html, use to access data


