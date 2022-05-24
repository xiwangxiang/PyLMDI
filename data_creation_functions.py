#take in gdp per sector and calculate total inndustry gdp
#%%

import pandas as pd
import numpy as np
import os

def activity(gdp_data):

    #make data long
    long_data = gdp_data.melt(id_vars=['Sector'], var_name='Year', value_name='Total_GDP')

    #group by year and sum up all sectors to ccreate total column from which we'll calc thne structure
    long_data_total = long_data.groupby(['Year']).sum().reset_index()

    #create a new dataframe with the structure by get5ting only the colzs we want
    activity = long_data_total[['Year','Total_GDP']]

    #save
    # pd.DataFrame.to_csv(activity, 'intermediate_data/industry_activity.csv')

    return activity

def structure(gdp_data):
    #make data long
    long_data = gdp_data.melt(id_vars=['Sector'], var_name='Year', value_name='GDP')

    #group by year and sum up all sectors to ccreate total column from which we'll calc thne structure
    long_data_total = long_data.groupby(['Year']).sum()

    #merge long data total to long data on the years column so we havbe a industry total for each sector and year
    long_data= pd.merge(long_data,long_data_total,on='Year', how='left')

    long_data['Sectoral_share_of_gdp'] = long_data['GDP_x'] / long_data['GDP_y']#gdp_x is original, gdp_y is the total
    
    #create a new dataframe with the structure by get5ting only the colzs we want
    structure = long_data[['Year','Sector','Sectoral_share_of_gdp']]

    return structure


def energy_intensity(gdp_data, energy_data):
    #make data long
    long_data_pj = energy_data.melt(id_vars=['Sector'], var_name='Year', value_name='PJ')
    long_data_gdp = gdp_data.melt(id_vars=['Sector'], var_name='Year', value_name='GDP')

    #join data together
    long_data = pd.merge(long_data_pj,long_data_gdp,on=['Year','Sector'], how='left')

    #calcualte intensity as enegry / gdp
    long_data['Energy_intensity'] = long_data['PJ'] / long_data['GDP']#gdp_x is original, gdp_y is the total

    #create a new dataframe with the structure by getting only the colzs we want
    energy_intensity = long_data[['Year','Sector','Energy_intensity']]

    return energy_intensity

def energy(energy_data):
    energy = energy_data.melt(id_vars=['Sector'], var_name='Year', value_name='PJ')
    return energy

