import pandas as pd
import numpy as np
from covid19_utils import get_active_cases
from covid19_utils import clean_active_cases
from datetime import date

pd.options.mode.chained_assignment = None

today = date.today()

df_today = get_active_cases(today)
df_today = clean_active_cases(df_today, today)

# bring in csv of previous dates
# set index to lga column
df_all_dates = pd.read_csv('../data/all_dates.csv')
df_all_dates.set_index('lga', inplace = True)

# merge df_all_dates with df_today, but only if it hasn't already been added
if (df_all_dates.columns[-1] != today.isoformat()):
    df_all_dates = df_all_dates.merge(df_today, on = 'lga', how = 'outer')

# replace nans with 0s
# this shouldn't be an issue, but is included just in case the dhhs starts excluding lgas with
# 0 cases from the daily table
df_all_dates.replace(np.nan, 0, inplace = True)

# order by index so the data for a specific LGA is easier to find
# again, this should already be in order, but just in case
df_all_dates.sort_values(by='lga', axis=0, inplace=True)

df_all_dates.to_csv('../data/all_dates.csv')

