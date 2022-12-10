# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 13:28:48 2022

@author: James
"""
from datetime import datetime
import sys
sys.path.append('Project Part 1')
sys.path.append('Project Part 2')
import ScrapeWebsite # part 1 of project
import DataDisplay  # part 2 of project

now = datetime.now()
date_str = now.strftime('%Y-%m-%d')
file_name = f'CovidData.{date_str}.json'
# calls for part 1:
Country_list=['us','india','france','germany','brazil','japan','italy','russia','turkey','spain','taiwan','iran'] # The list of countries selected for dashbaord
ScrapeWebsite.json_frame_writer(Country_list,'worldometer',file_name) # writes a nested dict json with all the data for country list
# Call for generating Dashbaord:
DataDisplay.dataDisplay(file_name)# runs the Dashboard html creation with the current covid data written from above.



