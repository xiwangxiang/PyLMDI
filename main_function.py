#main function as sued in general_run.py is saved here for ease of use

import os
import pandas as pd
import numpy as np
import data_creation_functions 
import LMDI_functions
import re
#%%
def run_divisia(data_title, extra_identifier, activity_data, energy_data, structure_variables_list, activity_variable = 'Activity', emissions_variable = 'Emissions', energy_variable = 'Energy', emissions_divisia = False, emissions_data=[], time_variable='Year', hierarchical=False,output_data_folder='output_data'):
    """This is a central function that will run the LMDI model. It will take the input data and format/adjust it using the functions in data_creation_functions.py. 
    It will then run the LMDI model and save the output. It will also plot the output.
    If you want to run the method using emissions intensity then you jsut set emissions divisia to true and include data for emissions_data"""
    #first, if there are any 0's in the data replace them with a very small number. This means we dont have to deal with any issues with dividing by 0, and given the context of the data, it is unlikely that the 0's are actually 0, or even the result of replacing 0's with small numbers will have a noticeable impact on the results.
    activity_data.loc[:, activity_variable] = activity_data.loc[:, activity_variable].replace(0, 0.00000001)
    energy_data.loc[:, energy_variable] = energy_data.loc[:, energy_variable].replace(0, 0.00000001)
    if emissions_divisia==True:
        emissions_data.loc[:, emissions_variable] = emissions_data.loc[:, emissions_variable].replace(0, 0.00000001)
        
    #Now start the process of running the LMDI model
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
        
        lmdi_output_additive = LMDI_functions.Add(driver_input_data, energy_data, drivers_list, structure_variables_list,energy_variable,time_variable,extra_identifier)

        lmdi_output_multiplicative = LMDI_functions.Mult(driver_input_data, energy_data, drivers_list, structure_variables_list,energy_variable,time_variable,extra_identifier)

        ###################################
        #add energy and activity (summed per year) as a column since this is very useful for analysis
        total_energy = energy_data.groupby(time_variable).sum().reset_index()
        total_energy = total_energy.rename(columns={energy_variable:'Total {}'.format(energy_variable)})
        total_activity = activity_data.groupby(time_variable).sum().reset_index()
        total_activity = total_activity.rename(columns={activity_variable:'Total_{}'.format(activity_variable)})
        lmdi_output_additive = pd.merge(lmdi_output_additive,total_energy,on=[time_variable], how='left')
        lmdi_output_additive = pd.merge(lmdi_output_additive,total_activity,on=[time_variable], how='left')
        lmdi_output_multiplicative = pd.merge(lmdi_output_multiplicative,total_energy,on=[time_variable], how='left')
        lmdi_output_multiplicative = pd.merge(lmdi_output_multiplicative,total_activity,on=[time_variable], how='left')
        
        ###################################
        #save data:
        lmdi_output_additive.to_csv('{}/{}{}_lmdi_output_additive.csv'.format(output_data_folder,data_title, extra_identifier), index=False)
        lmdi_output_multiplicative.to_csv('{}/{}{}_lmdi_output_multiplicative.csv'.format(output_data_folder,data_title, extra_identifier), index=False)

        # print('Done {}'.format(data_title, extra_identifier))


    ######################################################################    
    elif hierarchical == False and emissions_divisia == True:
    ######################################################################

        # print('Running LMDI for emissions, so incroporating the emissions intensity driver into the model')

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
        
        lmdi_output_additive = LMDI_functions.Add(driver_input_data, emissions_data, drivers_list, structure_variables_list,emissions_variable,time_variable,extra_identifier)

        lmdi_output_multiplicative = LMDI_functions.Mult(driver_input_data, emissions_data, drivers_list, structure_variables_list,emissions_variable,time_variable,extra_identifier)

        ###################################
        #replace energy in 'change in energy' col names with emissions
        lmdi_output_additive.rename(columns={'Change in {}'.format(energy_variable):'Change in {}'.format(emissions_variable)}, inplace=True)
        lmdi_output_multiplicative.rename(columns={'Percent change in {}'.format(energy_variable):'Percent change in {}'.format(emissions_variable)}, inplace=True)

        ###################################
        #add emissions and activity (summed per year) as a column since this is very useful for analysis
        total_emissions = emissions_data.groupby(time_variable)[emissions_variable].sum().reset_index()
        total_emissions = total_emissions.rename(columns={emissions_variable:'Total {}'.format(emissions_variable)})
        total_activity = activity_data.groupby(time_variable)[activity_variable].sum().reset_index()
        total_activity = total_activity.rename(columns={activity_variable:'Total_{}'.format(activity_variable)})
        lmdi_output_additive = pd.merge(lmdi_output_additive,total_emissions,on=[time_variable], how='left')
        lmdi_output_additive = pd.merge(lmdi_output_additive,total_activity,on=[time_variable], how='left')
        lmdi_output_multiplicative = pd.merge(lmdi_output_multiplicative,total_emissions,on=[time_variable], how='left')
        lmdi_output_multiplicative = pd.merge(lmdi_output_multiplicative,total_activity,on=[time_variable], how='left')
        
        ##################################

        #save data:
        lmdi_output_additive.to_csv('{}/{}{}_lmdi_output_additive.csv'.format(output_data_folder,data_title, extra_identifier), index=False)
        lmdi_output_multiplicative.to_csv('{}/{}{}_lmdi_output_multiplicative.csv'.format(output_data_folder,data_title, extra_identifier), index=False)

        # print('Done {}'.format(data_title, extra_identifier))

    elif emissions_divisia==False and hierarchical==True:
        #run hierarchical fully from a separate script in LMDI_functions.py
        # print('Running hierarchical LMDI for energy.')
        #check that structure_variables_list length is > 1, if it is not, tell the user to use other method
        if len(structure_variables_list) < 2:
            print('You need to have more than one structure variable to run hierarchical LMDI. Please use the other method.')
            return None

        hierarchical_multiplicative_output = LMDI_functions.hierarchical_LMDI(energy_data, activity_data, energy_variable, activity_variable, structure_variables_list, time_variable,extra_identifier)

        hierarchical_multiplicative_output.to_csv('{}/{}{}_hierarchical_multiplicative_output.csv'.format(output_data_folder,data_title, extra_identifier), index=False)
    
    elif emissions_divisia==True and hierarchical==True:
        #run hierarchical fully from a separate script in LMDI_functions.py
        print('Please note that hierarchical LMDI for emissions is not yet available. Please use the other method.')
#%%