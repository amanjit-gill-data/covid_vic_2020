import pandas as pd
import numpy as np
import calendar
from datetime import date
from datetime import timedelta
import json

# date formats on the dhhs website:

# 05-june-2020
# 9-june-2020
# 21-june
# sunday-12-july
# thursday-16-july-2020

def get_active_cases(date):
        
    prefix = 'https://www.dhhs.vic.gov.au/coronavirus-update-victoria-'
        
    y = date.year
    m = calendar.month_name[date.month].lower()
    d = date.day
    wd = calendar.day_name[date.weekday()].lower()
    
    suffixes = []
    
    if (d < 10):
        suffixes.append('0{}-{}-{}'.format(d, m, y))
        suffixes.append('0{}-{}'.format(d, m))
        suffixes.append('{}-0{}-{}'.format(wd, d, m))
        suffixes.append('{}-0{}-{}-{}'.format(wd, d, m, y))

    suffixes.append('{}-{}-{}'.format(d, m, y))
    suffixes.append('{}-{}'.format(d, m))
    suffixes.append('{}-{}-{}'.format(wd, d, m))
    suffixes.append('{}-{}-{}-{}'.format(wd, d, m, y))
        
    df_list = None
    suffix_index = 0
        
    while (df_list == None and suffix_index < len(suffixes)):   
        url = prefix + suffixes[suffix_index]
        try:
            df_list = pd.read_html(url)
        except Exception:
            suffix_index += 1
        
    return df_list[0]

def clean_active_cases(df_cases, date):
    df_cases.columns = ['lga', 'total', date]
    df_cases.drop('total', axis = 1, inplace = True)
    df_cases.set_index('lga', inplace = True)

    # replace all the NaNs and dashes with 0, as some of the earlier daily tables 
    # used blanks and dashes rather than 0s
    df_cases.replace(np.nan, 0, inplace = True)
    df_cases.replace('-', 0, inplace = True)

    # remove any row whose index doesn't match an LGA name
    lgas = get_lgas()
    df_cases = df_cases[df_cases.index.isin(lgas)]

    # some values are ints, some are floats. change all to ints, as you can't have 
    # a fraction of a person.
    df_cases = df_cases.astype('int')

    return df_cases

def get_lgas():
    # create list of LGA names
    # use the list to eliminate all rows where the LGA is not in that list 

    with open('../data/VIC_LOCALITY_POLYGON_shp.geojson') as json_data:
        vic_data = json.load(json_data)
   
    lgas = []

    for i in range(len(vic_data['features'])):
        lgas.append(vic_data['features'][i]['properties']['VIC_LGA__3'])

    return lgas