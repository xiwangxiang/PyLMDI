#take in gdp per sector and calculate total inndustry gdp
#%%

import pandas as pd
import numpy as np
import os

#import gdp data from excel
data = pd.read_excel('input_data/divisia-test-input-data.xlsx', sheet_name='ind_sectoral_gdp')


# %%
#make data long
long_data = data.melt(id_vars=['Sector'], var_name='Year', value_name='GDP')

#group by year and sum up all sectors to ccreate total column from which we'll calc thne structure
long_data_total = long_data.groupby(['Year']).sum()

#%%

#create a new dataframe with the structure by get5ting only the colzs we want
structure = long_data[['Year','GDP']]

#save
pd.DataFrame.to_csv(structure, 'intermediate_data/industry_activity.csv')

#%%