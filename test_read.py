# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 21:49:38 2022

@author: James
"""
import ScrapeWebsite
import pandas as pd
import json
import seaborn as sns





out=ScrapeWebsite.scrape_country('france','worldometer')
print(out)  
  

sns.lineplot(data=out,x='Index',y='Daily Deaths')

#data2=ScrapeWebsite.OurWorldData_json() # this works and downloads a json of all current covid data





## testing json list writing

'''
short_list=['us','france','greece','germany']
ScrapeWebsite.json_frame_writer(short_list,'worldometer')


with open('CovidData.json') as infile:
    data = json.load(infile) 
    for name in data.keys():
        US_data=pd.DataFrame(data[name])
        print("Total Deaths in "+ name +': ' + str(US_data['Total Deaths'][-1]) + ' at the current date of: '+ str(US_data['Dates'][-1]))
 '''   


