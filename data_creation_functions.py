#take in gdp per sector and calculate total inndustry gdp
#%%

import pandas as pd
import numpy as np
import os

def activity(gdp_data, structure_variable,activity_variable):

    #make data long
    long_data = gdp_data.melt(id_vars=[structure_variable], var_name='Year', value_name='Total_{}'.format(activity_variable))

    #group by year and sum up all sectors to ccreate total column from which we'll calc thne structure
    long_data_total = long_data.groupby(['Year']).sum().reset_index()

    #create a new dataframe with the structure by get5ting only the colzs we want
    activity = long_data_total[['Year','Total_{}'.format(activity_variable)]]

    #save
    # pd.DataFrame.to_csv(activity, 'intermediate_data/industry_activity.csv')

    return activity

def structure(gdp_data, structure_variable,activity_variable):
    #make data long
    long_data = gdp_data.melt(id_vars=[structure_variable], var_name='Year', value_name=activity_variable)

    #group by year and sum up all sectors to ccreate total column from which we'll calc thne structure
    long_data_total = long_data.groupby(['Year']).sum()

    #merge long data total to long data on the years column so we havbe a industry total for each sector and year
    long_data= pd.merge(long_data,long_data_total,on='Year', how='left')

    long_data['{}_share_of_{}'.format(structure_variable,activity_variable)] = long_data['{}_x'.format(activity_variable)] / long_data['{}_y'.format(activity_variable)]#gdp_x is original, gdp_y is the total
    
    #create a new dataframe with the structure by get5ting only the colzs we want
    structure = long_data[['Year', structure_variable, '{}_share_of_{}'.format(structure_variable,activity_variable)]]

    return structure


def energy_intensity(gdp_data, energy_data, structure_variable, activity_variable, energy_variable='PJ'):
    #make data long
    long_data_pj = energy_data.melt(id_vars=[structure_variable], var_name='Year', value_name=energy_variable)
    long_data_gdp = gdp_data.melt(id_vars=[structure_variable], var_name='Year', value_name=activity_variable)

    #join data together
    long_data = pd.merge(long_data_pj,long_data_gdp,on=['Year',structure_variable], how='left')

    #calcualte intensity as enegry / gdp
    long_data['Energy_intensity'] = long_data[energy_variable] / long_data[activity_variable]

    #create a new dataframe with the structure by getting only the colzs we want
    energy_intensity = long_data[['Year',structure_variable,'Energy_intensity']]

    return energy_intensity

def energy(energy_data,structure_variable, energy_variable='PJ'):
    #just get the energy data in the long format
    energy = energy_data.melt(id_vars=[structure_variable], var_name='Year', value_name=energy_variable)
    return energy

