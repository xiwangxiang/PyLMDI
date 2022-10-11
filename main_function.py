#main function as sued in general_run.py is saved here for ease of use

import os
import pandas as pd
import numpy as np
import data_creation_functions 
import LMDI_functions
import re
#%%
def run_divisia(data_title, extra_identifier, activity_data, energy_data, structure_variables_list, activity_variable = 'Activity', emissions_variable = 'Emissions', energy_variable = 'Energy', emissions_divisia = False, emissions_data=[], time_variable='Year', hierarchical=False):
    """This is a central function that will run the LMDI model. It will take the input data and format/adjust it using the functions in data_creation_functions.py. 
    It will then run the LMDI model and save the output. It will also plot the output.
    If you want to run the method using emissions intensity then you jsut set emissions divisia to true and include data for emissions_data"""
    if emissions_divisia == False and hierarchical == False:
        #we are just taking in energy, activity, sturcture, energy intensity. 
        #In the future, if emissions_divisia == True we will have the ability to calcualte emissions related LMDI outputs for that

        ###################################
        #run data creation functions using variables names set by the user
        activity = data_creation_functions.format_activity(activity_data, activity_variable, time_variable)

        energy_intensity = data_creation_functions.format_energy_intensity(activity_data, energy_data, structure_variables_list, activity_variable, energy_variable, time_variable)

        structure,structure_share_values_names = data_creation_functions.format_structure_multiple(activity_data, structure_variables_list,activity_variable, time_variable)

        ###################################
        #format data
        drivers_list = ['{} intensity'.format(energy_variable), 'Total_{}'.format(activity_variable)] + structure_share_values_names

        #merge all except energy (this makes it so that all dataframes are the same length when we sep them)
        activity_structure = pd.merge(structure,activity,on=[time_variable], how='left')
        activity_structure_intensity = pd.merge(activity_structure, energy_intensity,on=[time_variable]+structure_variables_list, how='left')

        driver_input_data = activity_structure_intensity.copy()

        ###################################
        #run LMDI_functions for additivie and multpiplicatuve outputs from the LMDI_functions.py file. It is the meat and sausages of this process.
        
        lmdi_output_additive = LMDI_functions.Add(driver_input_data, energy_data, drivers_list, structure_variables_list,energy_variable,time_variable,activity_variable)

        lmdi_output_multiplicative = LMDI_functions.Mult(driver_input_data, energy_data, drivers_list, structure_variables_list,energy_variable,time_variable,activity_variable)

        ###################################
        #add energy and activity (summed per year) as a column since this is very useful for analysis
        lmdi_output_additive['Total {}'.format(energy_variable)] = energy_data.groupby(time_variable).sum().reset_index()[energy_variable]
        lmdi_output_multiplicative['Total {}'.format(energy_variable)] = energy_data.groupby(time_variable).sum().reset_index()[energy_variable]
        lmdi_output_additive = lmdi_output_additive.merge(activity, on=time_variable, how='left')
        lmdi_output_multiplicative = lmdi_output_multiplicative.merge(activity, on=time_variable, how='left')
        ###################################
        #save data:
        lmdi_output_additive.to_csv('output_data/{}{}_lmdi_output_additive.csv'.format(data_title, extra_identifier), index=False)
        lmdi_output_multiplicative.to_csv('output_data/{}{}_lmdi_output_multiplicative.csv'.format(data_title, extra_identifier), index=False)

        print('Done {}'.format(data_title, extra_identifier))


    ######################################################################    
    elif hierarchical == False:
    ######################################################################

        print('Running LMDI for emissions, so incroporating the emissions intensity driver into the model')

        ###################################
        #run data creation functions using variables names set by the user
        activity = data_creation_functions.format_activity(activity_data, activity_variable, time_variable)

        energy_intensity = data_creation_functions.format_energy_intensity(activity_data, energy_data, structure_variables_list, activity_variable, energy_variable, time_variable)

        structure,structure_share_values_names = data_creation_functions.format_structure_multiple(activity_data, structure_variables_list,activity_variable, time_variable)

        emissions_intensity = data_creation_functions.format_emissions_intensity(emissions_data, energy_data, structure_variables_list, emissions_variable, energy_variable, time_variable)
        ###################################
        #format data
        drivers_list = ['{} intensity'.format(energy_variable), '{} intensity'.format(emissions_variable), 'Total_{}'.format(activity_variable)] + structure_share_values_names

        #merge all except energy (this makes it so that all dataframes are the same length when we sep them)
        activity_structure = pd.merge(structure,activity,on=[time_variable], how='left')
        activity_structure_energy_intensity = pd.merge(activity_structure, energy_intensity,on=[time_variable]+structure_variables_list, how='left')
        activity_structure_energy_intensity_emissions_intensity = pd.merge(activity_structure_energy_intensity, emissions_intensity,on=[time_variable]+structure_variables_list, how='left')

        driver_input_data = activity_structure_energy_intensity_emissions_intensity.copy()

        ###################################
        #run LMDI_functions for additivie and multpiplicatuve outputs from the LMDI_functions.py file. It is the meat and sausages of this process.
        
        lmdi_output_additive = LMDI_functions.Add(driver_input_data, emissions_data, drivers_list, structure_variables_list,emissions_variable,time_variable,activity_variable)

        lmdi_output_multiplicative = LMDI_functions.Mult(driver_input_data, emissions_data, drivers_list, structure_variables_list,emissions_variable,time_variable,activity_variable)

        ###################################
        #replace energy in 'change in energy' col names with emissions
        lmdi_output_additive.rename(columns={'Change in {}'.format(energy_variable):'Change in {}'.format(emissions_variable)}, inplace=True)
        lmdi_output_multiplicative.rename(columns={'Percent change in {}'.format(energy_variable):'Percent change in {}'.format(emissions_variable)}, inplace=True)

        ###################################
        #add emissions and activity (summed per year) as a column since this is very useful for analysis
        lmdi_output_additive['Total {}'.format(emissions_variable)] = emissions_data.groupby(time_variable).sum().reset_index()[emissions_variable]
        lmdi_output_multiplicative['Total {}'.format(emissions_variable)] = emissions_data.groupby(time_variable).sum().reset_index()[emissions_variable]
        lmdi_output_additive['Total {}'.format(energy_variable)] = energy_data.groupby(time_variable).sum().reset_index()[energy_variable]
        lmdi_output_multiplicative['Total {}'.format(energy_variable)] = energy_data.groupby(time_variable).sum().reset_index()[energy_variable]
        lmdi_output_additive = lmdi_output_additive.merge(activity, on=time_variable, how='left')
        lmdi_output_multiplicative = lmdi_output_multiplicative.merge(activity, on=time_variable, how='left')
        ##################################

        #save data:
        lmdi_output_additive.to_csv('output_data/{}{}_lmdi_output_additive.csv'.format(data_title, extra_identifier), index=False)
        lmdi_output_multiplicative.to_csv('output_data/{}{}_lmdi_output_multiplicative.csv'.format(data_title, extra_identifier), index=False)

        print('Done {}'.format(data_title, extra_identifier))

    elif emissions_divisia==False and hierarchical==True:
        #run hierarchical fully from a separate script in LMDI_functions.py
        print('Running hierarchical LMDI for energy. Please note that i am not 100% on whether this works as expected for more than 2 structural variables. Please check the output carefully. The product of all drivers in a given year t should equal energy_total_t/energy_total_base_year.')
        hierarchical_multiplicative_output = LMDI_functions.hierarchical_LMDI(energy_data, activity_data, energy_variable, activity_variable, structure_variables_list, time_variable)

        hierarchical_multiplicative_output.to_csv('output_data/{}{}_hierarchical_multiplicative_output.csv'.format(data_title, extra_identifier), index=False)

#%%