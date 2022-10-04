#take in gdp per sector and calculate total inndustry gdp
#%%

import pandas as pd
import numpy as np
import os

def activity(activity_data, structure_variable,activity_variable, time_variable='Year'):

    #make data long
    long_data = activity_data.melt(id_vars=[structure_variable], var_name=time_variable, value_name='Total_{}'.format(activity_variable))

    #group by year and sum up all sectors to ccreate total column from which we'll calc thne structure
    long_data_total = long_data.groupby([time_variable]).sum().reset_index()

    #create a new dataframe with the structure by get5ting only the colzs we want
    activity = long_data_total[[time_variable,'Total_{}'.format(activity_variable)]]

    #save
    # pd.DataFrame.to_csv(activity, 'intermediate_data/industry_activity.csv')

    return activity

def structure(activity_data, structure_variable,activity_variable, time_variable='Year'):
    #make data long
    long_data = activity_data.melt(id_vars=[structure_variable], var_name=time_variable, value_name=activity_variable)

    #group by year and sum up all sectors to ccreate total column from which we'll calc thne structure
    long_data_total = long_data.groupby([time_variable]).sum()

    #merge long data total to long data on the years column so we havbe a industry total for each sector and year
    long_data= pd.merge(long_data,long_data_total,on=time_variable, how='left')

    long_data['{}_share_of_{}'.format(structure_variable,activity_variable)] = long_data['{}_x'.format(activity_variable)] / long_data['{}_y'.format(activity_variable)]#gdp_x is original, gdp_y is the total
    
    #create a new dataframe with the structure by get5ting only the colzs we want
    structure = long_data[[time_variable, structure_variable, '{}_share_of_{}'.format(structure_variable,activity_variable)]]

    return structure


def energy_intensity(activity_data, energy_data, structure_variable, activity_variable, energy_variable='PJ', time_variable='Year'):
    #make data long
    long_data_pj = energy_data.melt(id_vars=[structure_variable], var_name=time_variable, value_name=energy_variable)
    long_data_gdp = activity_data.melt(id_vars=[structure_variable], var_name=time_variable, value_name=activity_variable)

    #join data together
    long_data = pd.merge(long_data_pj,long_data_gdp,on=[time_variable,structure_variable], how='left')

    #calcualte intensity as enegry / gdp
    long_data['Energy_intensity'] = long_data[energy_variable] / long_data[activity_variable]

    #create a new dataframe with the structure by getting only the colzs we want
    energy_intensity = long_data[[time_variable,structure_variable,'Energy_intensity']]

    return energy_intensity

def energy(energy_data,structure_variable, energy_variable='PJ', time_variable='Year'):
    #just get the energy data in the long format
    energy = energy_data.melt(id_vars=[structure_variable], var_name=time_variable, value_name=energy_variable)
    return energy

def emissions_intensity(emissions_data, energy_data, structure_variable, emissions_variable='MtCO2', energy_variable='PJ', time_variable='Year'):
    #make data long
    long_data_pj = energy_data.melt(id_vars=[structure_variable], var_name=time_variable, value_name=energy_variable)
    long_data_emissions = emissions_data.melt(id_vars=[structure_variable], var_name=time_variable, value_name=emissions_variable)

    #join data together
    long_data = pd.merge(long_data_pj,long_data_emissions,on=[time_variable,structure_variable], how='left')

    #calcualte intensity as emissions / enegry
    long_data['Emissions_intensity'] = long_data[emissions_variable] / long_data[energy_variable]

    #create a new dataframe with the structure by getting only the colzs we want
    emissions_intensity = long_data[[time_variable,structure_variable,'Emissions_intensity']]

    return emissions_intensity

def emissions(emissions_data,structure_variable, emissions_variable='MtCO2', time_variable='Year'):
    #just get the emissions data in the long format
    emissions = emissions_data.melt(id_vars=[structure_variable], var_name=time_variable, value_name=emissions_variable)
    return emissions