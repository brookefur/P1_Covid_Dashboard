import json
import ScrapeWebsite
import codecs
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html

"""
This is a test file for running bokeh and creating html files. I will be creating the official file later,
this is just a little file for all the important kewords/commands I need to remember.

Also: I'm assuming our profs open the html file, and I need to make the html file be able to use our json files
"""
filef = open('CovidData.json')
covidData = json.load(filef)
filef.close()

print(covidData['us']['Daily Deaths'])

plot = figure()
#plot.line(covidData["us"]["Dates"], covidData["us"]["Daily Deaths"])

html = file_html(plot, CDN, "my plot")

f = open('test_html.html', 'w')
f.write(html)
f.close()

# $.getJSON('mydata.json', function(data) {});
# Put in html, use to access data

