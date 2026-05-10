#%%
#%%
# from PyLMDI import PyLMDI
import pandas as pd
import numpy as np
import data_creation_functions 
import LMDI_functions
#load data in

#%%
#import data from excel using a preset name for the data, which is also used for creating graph titles and genreally identifying outputs/inputs related to this dataset specifically
data_title = 'outlook-transport-divisia'

extra_identifier = 'CN'#use this if you need the program to insert an extra identifier in things like filenames and plot titles

gdp_data = pd.read_excel('input_data/{}.xlsx'.format(data_title), sheet_name='ref_p_km')
energy_data = pd.read_excel('input_data/{}.xlsx'.format(data_title), sheet_name='ref_pass_energy_pj')

structure_variable = 'Mode'#set to the name of the varaible that will be used to group the data by. noramlly, sector for industry data, mode for transport data

emissions_divisia = False

#%%
if emissions_divisia:
    print('to do')
    #we will take in six diff data sets to insert into the divisia method
    #energy, activity, sturcture, energy intensity,fuel mix, emissions factor


else:
    #we are just taking in energy, activity, sturcture, energy intensity

    activity = data_creation_functions.activity(gdp_data)
    energy_intensity = data_creation_functions.energy_intensity(gdp_data, energy_data)
    structure = data_creation_functions.structure(gdp_data)

    energy = data_creation_functions.energy(energy_data)

    #merge all except energy (this makes it so that all dataframes are the same length when we sep them)
    activity_structure = pd.merge(structure,activity,on=['Year'], how='left')
    activity_structure_intensity = pd.merge(activity_structure, energy_intensity,on=['Year',structure_variable], how='left')

    #now we will separate each measure and make them wide format, ready to be passed to the divisia method
    activity_wide = activity_structure_intensity[['Year',structure_variable,'Total_GDP']]
    activity_wide = activity_wide.pivot(index=structure_variable, columns='Year', values='Total_GDP')

    structure_wide = activity_structure_intensity[['Year',structure_variable,'Sectoral_share_of_gdp']]
    structure_wide = structure_wide.pivot(index=structure_variable, columns='Year', values='Sectoral_share_of_gdp')

    Energy_intensity_wide = activity_structure_intensity[['Year',structure_variable,'Energy_intensity']]
    Energy_intensity_wide = Energy_intensity_wide.pivot(index=structure_variable, columns='Year', values='Energy_intensity')

    energy_wide = energy.pivot(index=structure_variable, columns='Year', values='PJ')

    ###################################

    #now calcualte the additive drivers usiung the input data
    activity_driver, energy_change = LMDI_functions.Add(activity_wide, energy_wide)
    
    structure_driver, energy_change = LMDI_functions.Add(structure_wide, energy_wide)
    
    energy_intensity_driver, energy_change = LMDI_functions.Add(Energy_intensity_wide, energy_wide)

    #concat all data together:
    lmdi_output_additive = pd.concat({'Activity': activity_driver, 'Structure': structure_driver, 'Energy intensity': energy_intensity_driver, 'Change in energy' : energy_change}, axis=1)


    #now calcualte the mult drivers usiung the input data
    activity_driver_mult, energy_change_mult = LMDI_functions.Mult(activity_wide, energy_wide)
    
    structure_driver_mult, energy_change_mult = LMDI_functions.Mult(structure_wide, energy_wide)
    
    energy_intensity_driver_mult, energy_change_mult = LMDI_functions.Mult(Energy_intensity_wide, energy_wide)
    
    #concat all data together:
    lmdi_output_multiplicative = pd.concat({'Activity': activity_driver_mult, 'Structure': structure_driver_mult, 'Energy intensity': energy_intensity_driver_mult, 'Change in energy' : energy_change_mult}, axis=1)
        
    #save data:
    lmdi_output_additive.to_csv('output_data/{}{}_lmdi_output_additive.csv'.format(data_title, extra_identifier))
    lmdi_output_multiplicative.to_csv('output_data/{}{}_lmdi_output_multiplicative.csv'.format(data_title, extra_identifier))

#%%