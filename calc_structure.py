#take in total gdp per sector and calculate share of total inndustry gdp
#eg. chemcials xsector = 5 gdp, total industyr gdp = 10 gdp so chem share = 0.5
#%%

import pandas as pd
import numpy as np
import os

#import gdp data from excel
data = pd.read_excel('input_data/divisia-test-input-data.xlsx', sheet_name='ind_sectoral_gdp')
#here we could also take in industry_activity but this is needless as its easy to calc the total

# %%
#make data long
long_data = data.melt(id_vars=['Sector'], var_name='Year', value_name='GDP')

#group by year and sum up all sectors to ccreate total column from which we'll calc thne structure
long_data_total = long_data.groupby(['Year']).sum()

#merge long data total to long data on the years column so we havbe a industry total for each sector and year
long_data= pd.merge(long_data,long_data_total,on='Year', how='left')

long_data['Sectoral_share_of_gdp'] = long_data['GDP_x'] / long_data['GDP_y']#gdp_x is original, gdp_y is the total

# %%

#create a new dataframe with the structure by get5ting only the colzs we want
structure = long_data[['Year','Sector','Sectoral_share_of_gdp']]

#save
pd.DataFrame.to_csv(structure, 'intermediate_data/industry_structure.csv')

#%%