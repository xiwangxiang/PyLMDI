#take in total gdp per sector and total energy per sector
#  calculate: Energy /  gdp , for each sector for each year

#%%

import pandas as pd
import numpy as np
import os

#import pj data from excel
data_pj = pd.read_excel('input_data/divisia-test-input-data.xlsx', sheet_name='ind_sectoral_pj')
#import gdp data from excel
data_gdp = pd.read_excel('input_data/divisia-test-input-data.xlsx', sheet_name='ind_sectoral_gdp')

# %%
#make data long
long_data_pj = data_pj.melt(id_vars=['Sector'], var_name='Year', value_name='PJ')
long_data_gdp = data_gdp.melt(id_vars=['Sector'], var_name='Year', value_name='GDP')

#join data together
long_data = pd.merge(long_data_pj,long_data_gdp,on=['Year','Sector'], how='left')

#calcualte intensity as enegry / gdp
long_data['Energy_intensity'] = long_data['PJ'] / long_data['GDP']#gdp_x is original, gdp_y is the total

# %%

#create a new dataframe with the structure by getting only the colzs we want
long_data = long_data[['Year','Sector','Energy_intensity']]

#save
pd.DataFrame.to_csv(long_data, 'intermediate_data/industry_energy_intensity.csv')

#%%