#take in gdp per sector and calculate total inndustry gdp
#%%

import pandas as pd
import numpy as np
import os

def format_activity(activity_data,activity_variable, time_variable):
    """
    This function takes the activity data and returns the sum of the activity for each year
    This function is unaffected by whetehr there is one or more structural variables"""
    #group by year and sum up all sectors so we have the total activity for each year
    activity_data_total = activity_data.groupby(time_variable)[activity_variable].sum().reset_index()

    #rename the activity variable to total activity
    activity_data_total = activity_data_total.rename(columns={activity_variable:'Total_{}'.format(activity_variable)})

    #create a new dataframe with the structure by get5ting only the colzs we want
    activity = activity_data_total[[time_variable,'Total_{}'.format(activity_variable)]]

    return activity

def format_structure_multiple(activity_data,structure_variables_list,activity_variable, time_variable):

    #this is intended to be used for any number of structure variables, even just one. 
    #go through list of structural variables, calculating their share of the total activity for each year, but in a way that works for hierarchical structure.
    #let's assume we have the following structure variables: ['Economy','Vehicle Type', 'Drive']
    #so for example, for the first structure variable, Economy, we will calculate the share of the total activity for each year, for each instance of that structural variable.
    #then for the second structure variable, Vehicle Type, we will calculate the share of the total activity for each economy for each year, for each instance of that structural variable.
    #then for the third structure variable, Drive, we will calculate the share of the total activity for each economy and vehicle type for each year, for each instance of that structural variable.
    #this will be done with indexing, so that we can use the same function for any number of structure variables.

    activity_data_new = activity_data.copy().drop(columns=[activity_variable])

    structure_share_values_names = []#this will be reutnred at the end of the function

    for i in range(0, len(structure_variables_list)):
        structure_variable_i = structure_variables_list[i]
        previous_structure_variables = structure_variables_list[0:i]

        #sum the activity for previous_structure_variables plus the structure_variable_i for each year
        activity_data_i = activity_data.groupby(previous_structure_variables + [time_variable, structure_variable_i])[activity_variable].sum().reset_index()
        #calculate the share of the total activity for each previous_structure_variables for each year, for each instance of that structural variable.
        activity_data_i[structure_variable_i + '_share'] = activity_data_i.groupby(previous_structure_variables + [time_variable])[activity_variable].apply(lambda x: x / x.sum())
        #drop the activity variable, as we don't need it anymore
        activity_data_i = activity_data_i.drop(activity_variable, axis=1)

        #merge the data onto a copy of the original long data
        activity_data_new = activity_data_new.merge(activity_data_i, on=previous_structure_variables + [time_variable, structure_variable_i], how='left')

        #record structure variable values names
        structure_share_values_names.append(structure_variable_i + '_share')

    return activity_data_new, structure_share_values_names

def format_energy_intensity(activity_data, energy_data, structure_variables_list, activity_variable, energy_variable, time_variable):
    #Calculate energy intensity for every year, for every unique combination of structure variables

    #join activity and energy data together
    data = pd.merge(activity_data,energy_data,on=[time_variable]+structure_variables_list, how='left')
    
    #calcualte intensity as enegry / gdp
    data['{} intensity'.format(energy_variable)] = data[energy_variable] / data[activity_variable]

    #create a new dataframe with the structure by getting only the colzs we want
    energy_intensity = data[[time_variable,'{} intensity'.format(energy_variable)] + structure_variables_list]

    return energy_intensity

def format_emissions_intensity(emissions_data, energy_data, structure_variables_list, emissions_variable, energy_variable, time_variable):
    #Calculate emissions intensity for every year, for every unique combination of structure variables
    #join data together
    data = pd.merge(energy_data,emissions_data,on=[time_variable]+structure_variables_list, how='left')

    #calcualte intensity as emissions / enegry
    data['{} intensity'.format(emissions_variable)] = data[emissions_variable] / data[energy_variable]

    #create a new dataframe with the structure by getting only the colzs we want
    emissions_intensity = data[[time_variable,'{} intensity'.format(emissions_variable)] + structure_variables_list]

    return emissions_intensity
