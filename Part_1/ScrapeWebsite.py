import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import re
import numpy as np
import json
import time ### testing purpose on code speed
## main function, calls subfunction for specific websites and returns the data in pandas df or dict
def scrape_country(country,website,ReturnType = 'pandas'): # takes in no caps country and website
   # imports country list and checks if its on the list
    # make a dict file assocated with the websites used:
    # CASE SENS FOR COUNTRY????
    
    weblist={'worldometer':'https://www.worldometers.info/coronavirus/country/'}    # lib of websites to use
    country_dict=scrape_pop() # generates a dict of country names and populations
    if country in country_dict:
        if website=='worldometer':
          return WorldometerScrape_country(country,website,ReturnType,weblist,country_dict)
        else:
            raise ValueError("Bad Site")
            return 0
    else:
        print(country_dict(country) +'~~~~'+ country)
        raise ValueError("Invalid Country")
        return 0    


def WorldometerScrape_country(country,website,ReturnType,weblist,country_dict):
    start_time = time.time()#### start time check
    url=(weblist[website]+country+'/') # combines url 
    requests.get(url)
    import_page=requests.get(url)
    htmlcontent = import_page.content
    soup = str(bs(htmlcontent, "html.parser"))
### finds Dates            
    n = soup.find("Deaths per Day<br>") 
    n_cat = soup[n:].find("categories:")
    n_start = soup[n_cat+n:].find('[')
    n_lengh = soup[n+n_cat+n_start:].find(']')
    start1=int(n+n_cat+n_start)+1
    stop1=int(start1+n_lengh)-1
    #print(soup[start1:stop1])
    p=soup[start1:stop1]
    split_dates = re.split(r',(?=")', p) #splits with comma delimiter while ignoring values inside quotes
                                            ############# maybe convert this format if i cant plot
### finds daily deaths
    n_cat = soup[n:].find("data:") 
    n_start = soup[n_cat+n:].find('[')
    n_lengh = soup[n+n_cat+n_start:].find(']')
    start2=int(n+n_cat+n_start)+1
    stop2=int(start2+n_lengh)-1
    dataY=soup[start2:stop2]
    daily_deaths = np.array(dataY.replace('null','0').split(','),dtype='int') #splits + replace null>>0
### finds total deaths
    n = soup.find("'Total Coronavirus Deaths'") 
    n_cat = soup[n:].find("data:")
    n_start = soup[n_cat+n:].find('[')
    n_lengh = soup[n+n_cat+n_start:].find(']')
    start3=int(n+n_cat+n_start)+1
    stop3=int(start3+n_lengh)-1
    dataY=soup[start3:stop3]
    cum_deaths = np.array(dataY.replace('null','0').split(','),dtype='int') # unrapped from pd.array( ) to fix dividing
    ###### data formatting
    df = pd.DataFrame(columns=['Dates']) # builds blank dataframe with headers        
    months = {'jan': '01','feb': '02','mar': '03','apr':'04','may':'05',
              'jun':'06','jul':'07','aug':'08','sep':'09',
              'oct':'10','nov':'11','dec':'12'} # dict to convert 'xxx' month to '#'
    format_dates=[]
    for d in split_dates: # converts Jan 02, 2020 to format 2020-01-02
        mm=months[d[1:4].casefold()]
        dd=d[5:7]
        yyyy=d[9:13]
        format_dates.append(yyyy+'-'+mm+'-'+dd)
    df['Index']=range(0,len(format_dates))  ################## not really needed just for plotting testing ########################
    df['Dates']=format_dates
    df['Daily Deaths']=daily_deaths
    df['Total Deaths']=cum_deaths  
    df['Daily Deaths per 100k']=np.divide(daily_deaths,int(country_dict[country][0]))
    df['Total Deaths per 100k']=np.divide(cum_deaths,int(country_dict[country][0]))
    print(country+"--- %s seconds ---" % (time.time() - start_time))##### cycle time check
### sets the output type
    if ReturnType=='pandas': 
        return df
    elif ReturnType=='dict':
        return df.to_dict()

def OurWorldData_json():
    url = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
    r = requests.get(url, allow_redirects=True)
    rd=r.content.decode("utf-8")
    data=pd.read_csv(rd)
    return data
    #open('OurWorldData_Covid.json', 'w').write(r2)


## this doesnt work so far. maybe create static country and pop list for countries we want to use

def scrape_C_names(): 
    url='https://www.worldometers.info/coronavirus/#countries'
    import_page=requests.get(url)
    htmlcontent = import_page.content
    soup = str(bs(htmlcontent, "html.parser"))
# finds Dates            
    n = soup.find('''table id="main_table_countries_today''') 
    print(n)
    n_cat = soup[n:].find("categories:")
    n_start = soup[n_cat+n:].find('[')
    n_lengh = soup[n+n_cat+n_start:].find(']')
    #start1=int(n+n_cat+n_start)+1
    #stop1=int(start1+n_lengh)-1
    start1=n+1
    stop1=start1+10
    #print(soup[start1:stop1])
    p=soup[start1:stop1]
    return p



def scrape_pop():
    url='https://www.worldometers.info/world-population/population-by-country/'
    requests.get(url)
    import_page=requests.get(url)
    htmlcontent = import_page.content
    soup = bs(htmlcontent, "html.parser")
    table_data = soup.find('table', class_ = 'table table-striped table-bordered')
    headers = []
    for th in table_data.find_all('th'):
        title = th.text
        headers.append(title)
    pop_table = pd.DataFrame(columns = headers)
    
    for j in table_data.find_all('tr')[1:]:
            row_data = j.find_all('td')
            row = [tr.text for tr in row_data]
            length = len(pop_table)
            pop_table.loc[length] = row

    df_cut= pop_table.loc[:,['Country (or dependency)','Population (2020)']]
    df_cut['Country (or dependency)']=df_cut['Country (or dependency)'].str.lower()
    
    df_cut['Population (2020)']=df_cut['Population (2020)'].str.replace(',','')
    
    Country_list=df_cut.set_index('Country (or dependency)').T.to_dict('list') # converts to library
    Country_list['us'] = Country_list.pop('united states') # fixes name for united states to us
    Country_list['viet-nam'] = Country_list.pop('vietnam') # fixes name 
    Country_list['congo'] = Country_list.pop('dr congo')
    Country_list['saint-vincent-and-the-grenadines'] = Country_list.pop('st. vincent & grenadines')
    
    
    return Country_list
    
def json_frame_writer(countries,site,filename='CovidData.json'):
    out={}
    for i in countries:
        temp=scrape_country(i,site).to_dict()
        out[i]=temp
    out = json.dumps(out)
    with open(filename, 'w') as outfile:
        outfile.write(out) 

