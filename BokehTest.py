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

plot = figure()
plot.circle([1,2], [3,4])

html = file_html(plot, CDN, "my plot")

f = open('test_html.html', 'w')
f.write(html)
f.close()

# $.getJSON('mydata.json', function(data) {});
# Put in html, use to access data

