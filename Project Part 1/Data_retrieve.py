# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 13:28:48 2022

@author: James
"""
import ScrapeWebsite
from datetime import datetime
now = datetime.now()
date_str = now.strftime('%Y-%m-%d')
file_name = f'CovidData.{date_str}.json'
Country_list=['us','france','greece','germany','spain']
ScrapeWebsite.json_frame_writer(Country_list,'worldometer',file_name)
