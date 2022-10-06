#main function as sued in general_run.py is saved here for ease of use

import os
import pandas as pd
import numpy as np
import data_creation_functions 
import LMDI_functions

#%%
def run_divisia(data_title, extra_identifier, activity_data, energy_data, structure_variable, activity_variable, emissions_variable = 'MtCO2', energy_variable = 'PJ', emissions_divisia = False, emissions_data=[], time_variable='Year'):
    """This is a central function that will run the LMDI model. It will take the input data and format/adjust it using the functions in data_creation_functions.py. 
    It will then run the LMDI model and save the output. It will also plot the output.
    If you want to run the method using emissions intensity then you jsut set emissions divisia to true and include data for emissions_data"""
    if not emissions_divisia:
        #we are just taking in energy, activity, sturcture, energy intensity. 
        #In the future, if emissions_divisia == True we will have the ability to calcualte emissions related LMDI outputs for that

        ###################################
        #run data creation functions using variables names set by the user
        activity = data_creation_functions.activity(activity_data,structure_variable, activity_variable, time_variable)
        energy_intensity = data_creation_functions.energy_intensity(activity_data, energy_data, structure_variable, activity_variable, energy_variable, time_variable)
        structure = data_creation_functions.structure(activity_data, structure_variable,activity_variable, time_variable)

        energy = data_creation_functions.energy(energy_data,structure_variable, energy_variable, time_variable)

        ###################################
        #format data

        #merge all except energy (this makes it so that all dataframes are the same length when we sep them)
        activity_structure = pd.merge(structure,activity,on=[time_variable], how='left')
        activity_structure_intensity = pd.merge(activity_structure, energy_intensity,on=[time_variable,structure_variable], how='left')

        #now we will separate each measure and make them wide format, ready to be passed to the divisia method
        activity_wide = activity_structure_intensity[[time_variable,structure_variable,'Total_{}'.format(activity_variable)]]
        activity_wide = activity_wide.pivot(index=structure_variable, columns=time_variable, values='Total_{}'.format(activity_variable))

        structure_wide = activity_structure_intensity[[time_variable,structure_variable,'{}_share_of_{}'.format(structure_variable,activity_variable)]]
        structure_wide = structure_wide.pivot(index=structure_variable, columns=time_variable, values='{}_share_of_{}'.format(structure_variable,activity_variable))

        energy_intensity_wide = activity_structure_intensity[[time_variable,structure_variable,'Energy_intensity']]
        energy_intensity_wide = energy_intensity_wide.pivot(index=structure_variable, columns=time_variable, values='Energy_intensity')

        energy_wide = energy.pivot(index=structure_variable, columns=time_variable, values=energy_variable)

        ###################################
        #run LMDI_functions for additivie and multpiplicatuve outputs from the LMDI_functions.py file. It is the meat and sausages of this process.
        #now calcualte the additive drivers usiung the input data
        activity_driver, energy_change = LMDI_functions.Add(activity_wide, energy_wide)

        structure_driver, energy_change = LMDI_functions.Add(structure_wide, energy_wide)
        
        energy_intensity_driver, energy_change = LMDI_functions.Add(energy_intensity_wide, energy_wide)

        #create column of energy data to include in outputs
        energy_col = energy[[time_variable, energy_variable]].groupby([time_variable]).sum()

        #concat all data together:
        lmdi_output_additive = pd.concat({'Activity': activity_driver, structure_variable: structure_driver, 'Energy intensity': energy_intensity_driver, 'Change in energy' : energy_change, 'Energy':energy_col[energy_variable]}, axis=1)

        #now calcualte the mult drivers usiung the input data.
        activity_driver_mult, energy_change_mult = LMDI_functions.Mult(activity_wide, energy_wide)

        structure_driver_mult, energy_change_mult = LMDI_functions.Mult(structure_wide, energy_wide)

        energy_intensity_driver_mult, energy_change_mult = LMDI_functions.Mult(energy_intensity_wide, energy_wide)

        #concat all data together:
        lmdi_output_multiplicative = pd.concat({'Activity': activity_driver_mult, structure_variable: structure_driver_mult, 'Energy intensity': energy_intensity_driver_mult, 'Change in energy' : energy_change_mult, 'Energy':energy_col[energy_variable]}, axis=1)
        
        ###################################

        #save data:
        lmdi_output_additive.to_csv('output_data/{}{}_lmdi_output_additive.csv'.format(data_title, extra_identifier))
        lmdi_output_multiplicative.to_csv('output_data/{}{}_lmdi_output_multiplicative.csv'.format(data_title, extra_identifier))

        print('Done {}'.format(data_title, extra_identifier))


    ######################################################################    
    else:
    ######################################################################

        print('Running LMDI for emissions, so incroporating the emissions intensity driver into the model')

        ###################################
        #run data creation functions using variables names set by the user
        activity = data_creation_functions.activity(activity_data,structure_variable, activity_variable, time_variable)
        energy_intensity = data_creation_functions.energy_intensity(activity_data, energy_data, structure_variable, activity_variable, energy_variable, time_variable)
        structure = data_creation_functions.structure(activity_data, structure_variable,activity_variable, time_variable)

        # energy = data_creation_functions.energy(energy_data,structure_variable, energy_variable)

        emissions_intensity = data_creation_functions.emissions_intensity(emissions_data, energy_data, structure_variable, emissions_variable, energy_variable, time_variable)

        emissions = data_creation_functions.emissions(emissions_data,structure_variable, emissions_variable, time_variable)
        ###################################
        #format data

        #merge all except emissions (this makes it so that all dataframes are the same length when we sep them)
        activity_structure = pd.merge(structure,activity,on=[time_variable], how='left')
        activity_structure_energyintensity = pd.merge(activity_structure, energy_intensity,on=[time_variable,structure_variable], how='left')
        activity_structure_energyintensity_emissionsintensity = pd.merge(activity_structure_energyintensity, emissions_intensity,on=[time_variable,structure_variable], how='left')

        #now we will separate each measure and make them wide format, ready to be passed to the divisia method
        activity_wide = activity_structure_energyintensity_emissionsintensity[[time_variable,structure_variable,'Total_{}'.format(activity_variable)]]
        activity_wide = activity_wide.pivot(index=structure_variable, columns=time_variable, values='Total_{}'.format(activity_variable))

        structure_wide = activity_structure_energyintensity_emissionsintensity[[time_variable,structure_variable,'{}_share_of_{}'.format(structure_variable,activity_variable)]]
        structure_wide = structure_wide.pivot(index=structure_variable, columns=time_variable, values='{}_share_of_{}'.format(structure_variable,activity_variable))

        energy_intensity_wide = activity_structure_energyintensity_emissionsintensity[[time_variable,structure_variable,'Energy_intensity']]
        energy_intensity_wide = energy_intensity_wide.pivot(index=structure_variable, columns=time_variable, values='Energy_intensity')

        emissions_intensity_wide = activity_structure_energyintensity_emissionsintensity[[time_variable,structure_variable,'Emissions_intensity']]
        emissions_intensity_wide = emissions_intensity_wide.pivot(index=structure_variable, columns=time_variable, values='Emissions_intensity')

        emissions_wide = emissions.pivot(index=structure_variable, columns=time_variable, values=emissions_variable)

        ###################################
        #run LMDI_functions for additivie and multpiplicatuve outputs from the LMDI_functions.py file. It is the meat and sausages of this process.
        #now calcualte the additive drivers usiung the input data
        activity_driver, emissions_change = LMDI_functions.Add(activity_wide, emissions_wide)

        structure_driver, emissions_change = LMDI_functions.Add(structure_wide, emissions_wide)
        
        energy_intensity_driver, emissions_change = LMDI_functions.Add(energy_intensity_wide, emissions_wide)

        emissions_intensity_driver, emissions_change = LMDI_functions.Add(emissions_intensity_wide, emissions_wide)

        emissions_col = emissions[[time_variable, emissions_variable]].groupby([time_variable]).sum()

        #concat all data together:
        lmdi_output_additive = pd.concat({'Activity': activity_driver, structure_variable: structure_driver, 'Energy intensity': energy_intensity_driver, 'Emissions intensity': emissions_intensity_driver, 'Change in emissions' : emissions_change,  'Emissions':emissions_col[emissions_variable]}, axis=1)
        #now calcualte the mult drivers usiung the input data.
        activity_driver_mult, emissions_change_mult = LMDI_functions.Mult(activity_wide, emissions_wide)

        structure_driver_mult, emissions_change_mult = LMDI_functions.Mult(structure_wide, emissions_wide)

        energy_intensity_driver_mult, emissions_change_mult = LMDI_functions.Mult(energy_intensity_wide, emissions_wide)

        emissions_intensity_driver_mult, emissions_change_mult = LMDI_functions.Mult(emissions_intensity_wide, emissions_wide)

        #concat all data together:
        lmdi_output_multiplicative = pd.concat({'Activity': activity_driver_mult, structure_variable: structure_driver_mult, 'Energy intensity': energy_intensity_driver_mult,'Emissions intensity': emissions_intensity_driver_mult, 'Change in emissions' : emissions_change_mult, 'Emissions':emissions_col[emissions_variable]}, axis=1)
        
        ###################################

        #save data:
        lmdi_output_additive.to_csv('output_data/{}{}_lmdi_output_additive.csv'.format(data_title, extra_identifier))
        lmdi_output_multiplicative.to_csv('output_data/{}{}_lmdi_output_multiplicative.csv'.format(data_title, extra_identifier))

        print('Done {}'.format(data_title, extra_identifier))
#%%