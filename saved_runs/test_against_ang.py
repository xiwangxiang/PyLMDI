#%%
import os
if os.getcwd().endswith('saved_runs'):
    os.chdir('../')#go abck one folder so we can access all the functions
elif os.getcwd().endswith('Github'):
    os.chdir('./PyLMDI/')
else:
    print('You are in this folder: ', os.getcwd())

import pandas as pd
import numpy as np
import main_function
import plot_output
import data_creation_functions
import LMDI_functions
import re
AUTO_OPEN = True
#%%
original_ang = True
if original_ang:
    #load and test data from ang PAPER TO TEST WE GOT SAME RESULTS:
    #THIS IS FROM PG.378 OF THE PAPER:  X.Y. Xu, B.W. Ang / Energy Economics 44(2014) 375–382 
    results_ang = pd.read_csv('input_data/example_data_ang_2014.csv')
    activity_data = results_ang[['Year', 'Sector 1', 'Sector 2', 'Activity']]
    energy_data = results_ang[['Year', 'Sector 1', 'Sector 2', 'Energy']]
    #load in function options
    combination_dict = {'scenario':'Reference', 'transport_type':'passenger', 'medium':'road', 'activity_variable':'passenger_km', 'structure_variables_list':['Sector 1', 'Sector 2'], 'graph_title':'ang 2014', 'extra_identifier':'TEST', 'emissions_divisia':False, 'hierarchical':True}

    #rename activity with variable
    activity_data = activity_data.rename(columns={'Activity':combination_dict['activity_variable']})

    #set variables to input into the LMDI function
    activity_variable = combination_dict['activity_variable']
    structure_variables_list = combination_dict['structure_variables_list']
    graph_title = combination_dict['graph_title']
    extra_identifier = combination_dict['extra_identifier']
    data_title = 'test_ang_2014'
    energy_variable = 'Energy'
    time_variable = 'Year'
    font_size=25
    y_axis_min_percent_decrease=0.1
    residual_variable1='Energy intensity'
    emissions_divisia = combination_dict['emissions_divisia']
    hierarchical = combination_dict['hierarchical']

    
    #test out running the hierarchical function using debugging mode
    main_function.run_divisia(data_title, extra_identifier, activity_data, energy_data, structure_variables_list, activity_variable, emissions_variable = 'Emissions', energy_variable = energy_variable, emissions_divisia = emissions_divisia, emissions_data=[], time_variable=time_variable,hierarchical=hierarchical)

    # big_df, big_df_2 = LMDI_functions.hierarchical_LMDI(energy_data, activity_data, energy_variable, activity_variable, structure_variables_list, time_variable)
    
    results_ang = pd.read_csv('output_data/{}{}_hierarchical_multiplicative_output.csv'.format(data_title, extra_identifier))
    print(results_ang)
    #Looks like something is wrong with the second structural effect.
    
#%%
#test out using angs method but for 3 sectors:
# example_data_ang_2014_3SECTORS
results_ang = pd.read_csv('input_data/example_data_ang_2014_3SECTORS.csv')
activity_data = results_ang[['Year', 'Sector 1', 'Sector 2', 'Sector 3', 'Activity']]
energy_data = results_ang[['Year', 'Sector 1', 'Sector 2', 'Sector 3', 'Energy']]
#load in function options
#load in function options
combination_dict = {'scenario':'Reference', 'transport_type':'passenger', 'medium':'road', 'activity_variable':'passenger_km', 'structure_variables_list':['Sector 1', 'Sector 2', 'Sector 3'], 'graph_title':'ang 2014', 'extra_identifier':'TEST', 'emissions_divisia':False, 'hierarchical':True}

#rename activity with variable
activity_data = activity_data.rename(columns={'Activity':combination_dict['activity_variable']})

#set variables to input into the LMDI function
activity_variable = combination_dict['activity_variable']
structure_variables_list = combination_dict['structure_variables_list']
graph_title = combination_dict['graph_title']
extra_identifier = combination_dict['extra_identifier']
data_title = 'test_ang_2014'
energy_variable = 'Energy'
time_variable = 'Year'
font_size=25
y_axis_min_percent_decrease=0.1
residual_variable1='Energy intensity'
emissions_divisia = combination_dict['emissions_divisia']
hierarchical = combination_dict['hierarchical']

#%%
#test out running the hierarchical function using debugging mode
main_function.run_divisia(data_title, extra_identifier, activity_data, energy_data, structure_variables_list, activity_variable, emissions_variable = 'Emissions', energy_variable = energy_variable, emissions_divisia = emissions_divisia, emissions_data=[], time_variable=time_variable,hierarchical=hierarchical)

# big_df, big_df_2 = LMDI_functions.hierarchical_LMDI(energy_data, activity_data, energy_variable, activity_variable, structure_variables_list, time_variable)
#%%
results_ang = pd.read_csv('output_data/{}{}_hierarchical_multiplicative_output.csv'.format(data_title, extra_identifier))
print(results_ang)


#if tehre is a new_structure_variables_list, we will use that when plotting
if 'new_structure_variables_list' in combination_dict:
    structure_variables_list = combination_dict['new_structure_variables_list']
    
#plot LMDI
plot_output.plot_additive_waterfall(data_title, extra_identifier, structure_variables_list=structure_variables_list,activity_variable=activity_variable,energy_variable='Energy', emissions_variable='Emissions',emissions_divisia=emissions_divisia, time_variable='Year', graph_title=graph_title, residual_variable1=residual_variable1, residual_variable2='Emissions intensity', font_size=font_size, y_axis_min_percent_decrease=y_axis_min_percent_decrease,AUTO_OPEN=AUTO_OPEN, hierarchical=hierarchical)

plot_output.plot_multiplicative_timeseries(data_title, extra_identifier,structure_variables_list=structure_variables_list,activity_variable=activity_variable,energy_variable='Energy', emissions_variable='Emissions',emissions_divisia=emissions_divisia, time_variable='Year', graph_title=graph_title, residual_variable1=residual_variable1, residual_variable2='Emissions intensity', font_size=font_size,AUTO_OPEN=AUTO_OPEN, hierarchical=hierarchical)

#%%