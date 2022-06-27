#main function as sued in general_run.py is saved here for ease of use

import os
import pandas as pd
import numpy as np
import data_creation_functions 
import LMDI_functions

#%%
def run_divisia(data_title, extra_identifier, gdp_data, energy_data, emissions_divisia,structure_variable,activity_variable, energy_variable='PJ'):
    """This is a central function that will run the LMDI model. It will take the input data and format/adjust it using the functions in data_creation_functions.py. 
    It will then run the LMDI model and save the output. It will also plot the output."""
    if not emissions_divisia:
        #we are just taking in energy, activity, sturcture, energy intensity. 
        #In the future, if emissions_divisia == True we will have the ability to calcualte emissions related LMDI outputs for that

        ###################################
        #run data creation functions using variables names set by the user
        activity = data_creation_functions.activity(gdp_data,structure_variable, activity_variable)
        energy_intensity = data_creation_functions.energy_intensity(gdp_data, energy_data, structure_variable, activity_variable, energy_variable)
        structure = data_creation_functions.structure(gdp_data, structure_variable,activity_variable)

        energy = data_creation_functions.energy(energy_data,structure_variable, energy_variable)

        ###################################
        #format data

        #merge all except energy (this makes it so that all dataframes are the same length when we sep them)
        activity_structure = pd.merge(structure,activity,on=['Year'], how='left')
        activity_structure_intensity = pd.merge(activity_structure, energy_intensity,on=['Year',structure_variable], how='left')

        #now we will separate each measure and make them wide format, ready to be passed to the divisia method
        activity_wide = activity_structure_intensity[['Year',structure_variable,'Total_{}'.format(activity_variable)]]
        activity_wide = activity_wide.pivot(index=structure_variable, columns='Year', values='Total_{}'.format(activity_variable))

        structure_wide = activity_structure_intensity[['Year',structure_variable,'{}_share_of_{}'.format(structure_variable,activity_variable)]]
        structure_wide = structure_wide.pivot(index=structure_variable, columns='Year', values='{}_share_of_{}'.format(structure_variable,activity_variable))

        Energy_intensity_wide = activity_structure_intensity[['Year',structure_variable,'Energy_intensity']]
        Energy_intensity_wide = Energy_intensity_wide.pivot(index=structure_variable, columns='Year', values='Energy_intensity')

        energy_wide = energy.pivot(index=structure_variable, columns='Year', values=energy_variable)

        ###################################
        #run LMDI_functions for additivie and multpiplicatuve outputs from the LMDI_functions.py file. It is the meat and sausages of this process.
        #now calcualte the additive drivers usiung the input data
        activity_driver, energy_change = LMDI_functions.Add(activity_wide, energy_wide)

        structure_driver, energy_change = LMDI_functions.Add(structure_wide, energy_wide)
        
        energy_intensity_driver, energy_change = LMDI_functions.Add(Energy_intensity_wide, energy_wide)

        #concat all data together:
        lmdi_output_additive = pd.concat({'Activity': activity_driver, 'Structure': structure_driver, 'Energy intensity': energy_intensity_driver, 'Change in energy' : energy_change}, axis=1)

        #now calcualte the mult drivers usiung the input data.
        activity_driver_mult, energy_change_mult = LMDI_functions.Mult(activity_wide, energy_wide)

        structure_driver_mult, energy_change_mult = LMDI_functions.Mult(structure_wide, energy_wide)

        energy_intensity_driver_mult, energy_change_mult = LMDI_functions.Mult(Energy_intensity_wide, energy_wide)

        #concat all data together:
        lmdi_output_multiplicative = pd.concat({'Activity': activity_driver_mult, 'Structure': structure_driver_mult, 'Energy intensity': energy_intensity_driver_mult, 'Change in energy' : energy_change_mult}, axis=1)
        
        ###################################

        #save data:
        lmdi_output_additive.to_csv('output_data/{}{}_lmdi_output_additive.csv'.format(data_title, extra_identifier))
        lmdi_output_multiplicative.to_csv('output_data/{}{}_lmdi_output_multiplicative.csv'.format(data_title, extra_identifier))

        print('Done {}'.format(data_title, extra_identifier))
    else:
        print('Cannot do emissions LMDI yet')
         #simply add to (energy, activity, sturcture, energy intensity), the outputs 'emissions intensity and 'emissions change', i think.  
#%%