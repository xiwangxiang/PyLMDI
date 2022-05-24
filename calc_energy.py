#take in total gdp per sector and total energy per sector
#  calculate: Energy /  gdp , for each sector for each year

#%%

import pandas as pd
import numpy as np
import os

if 'Github\\PyLMDI\\grooming_code' in os.getcwd():
    os.chdir('../')  
elif 'Github\\PyLMDI\\analysis_code' in os.getcwd():
    os.chdir('../')  

#import pj data from excel
data_pj = pd.read_excel('input_data/divisia-test-input-data.xlsx', sheet_name='ind_sectoral_pj')

# %%
#make data long
long_data_pj = data_pj.melt(id_vars=['Sector'], var_name='Year', value_name='PJ')

# %%

#save
pd.DataFrame.to_csv(long_data_pj, 'intermediate_data/industry_energy.csv')

#%%