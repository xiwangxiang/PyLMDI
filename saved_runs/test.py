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
#TEST SIMPLE FUNCTIONALITY

###########################################################################
#load in the data
activity_data  = pd.read_csv('input_data/test_data_activity_PASSENGER_REF_MODE_DRIVE_ROAD.csv')
energy_data = pd.read_csv('input_data/test_data_energy_PASSENGER_REF_MODE_DRIVE_ROAD.csv')

#load in function options
combination_dict = {'scenario':'Reference', 'transport_type':'passenger', 'medium':'road', 'activity_variable':'passenger_km', 'structure_variables_list':['Vehicle Type', 'Drive'], 'graph_title':'Road passenger - Drivers of changes in energy use (Ref)', 'extra_identifier':'PASSENGER_REF_MODE_DRIVE_ROAD', 'emissions_divisia':False, 'hierarchical':True}

#rename activity with variable
activity_data = activity_data.rename(columns={'Activity':combination_dict['activity_variable']})

#set variables to input into the LMDI function
activity_variable = combination_dict['activity_variable']
structure_variables_list = combination_dict['structure_variables_list']
graph_title = combination_dict['graph_title']
extra_identifier = combination_dict['extra_identifier']
data_title = 'Transport_8th'
energy_variable = 'Energy'
time_variable = 'Year'
font_size=25
y_axis_min_percent_decrease=0.1
residual_variable1='Energy intensity'
emissions_divisia = combination_dict['emissions_divisia']
hierarchical = combination_dict['hierarchical']

#%%
#test out running the hierarchical function using debugging mode
results = main_function.run_divisia(data_title, extra_identifier, activity_data, energy_data, structure_variables_list, activity_variable, emissions_variable = 'Emissions', energy_variable = energy_variable, emissions_divisia = emissions_divisia, emissions_data=[], time_variable=time_variable,hierarchical=hierarchical)

#%%
#TEST SIMPLE FUNCTIONALITY USING FREIGHT DATA
energy_data = pd.read_csv('input_data/test_data_energy_FREIGHT_CN_MODE_DRIVE_ROAD.csv')
activity_data = pd.read_csv('input_data/test_data_activity_FREIGHT_CN_MODE_DRIVE_ROAD.csv')

#load in function options
combination_dict = {'scenario':'Carbon Neutral', 'transport_type':'freight', 'medium':'road', 'activity_variable':'freight_tonne_km', 'structure_variables_list':['Vehicle Type', 'Drive'], 'graph_title':'Road freight - Drivers of changes in energy use (CN)', 'extra_identifier':'FREIGHT_CN_MODE_DRIVE_ROAD', 'emissions_divisia':False, 'hierarchical':True}

#rename activity with variable
activity_data = activity_data.rename(columns={'Activity':combination_dict['activity_variable']})

#set variables to input into the LMDI function
activity_variable = combination_dict['activity_variable']
structure_variables_list = combination_dict['structure_variables_list']
graph_title = combination_dict['graph_title']
extra_identifier = combination_dict['extra_identifier']
data_title = 'Transport_8th'
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

###########################################################################


#%%
#TEST FOR 3+ HIERARCHICAL LEVELS

# all_data = pd.read_csv('input_data/tranport_8th/activity_efficiency_energy_road_stocks.csv')
transport_8th_emissions = pd.read_csv('input_data/tranport_8th/transport_8th_emissions.csv')
all_data = transport_8th_emissions[transport_8th_emissions['Year']<=2050]
combination_dict_list=[]
combination_dict_list.append({'scenario':'Carbon Neutral', 'transport_type':'freight', 'medium':'road', 'activity_variable':'freight_tonne_km', 'structure_variables_list':['Economy', 'Vehicle Type', 'Drive'], 'graph_title':'Road freight - Drivers of changes in energy use (CN)', 'extra_identifier':'FREIGHT_CN_ECONOMY_VTYPE_DRIVE_ROAD', 'emissions_divisia':False, 'hierarchical':True, 'residual_variable1':'Residual efficiency'})


#%%
#create loop to run through the combinations
for combination_dict in combination_dict_list:

    print('\n\nRunning ', combination_dict['extra_identifier'])
    #create a dataframe for each combination
    data = all_data.copy()
    #filter data by scenario
    data = data[data['Scenario']==combination_dict['scenario']]
    #filter data by transport type
    data = data[data['Transport Type']==combination_dict['transport_type']]
    #filter data by medium
    if combination_dict['medium'] == 'everything':
        pass
    else:
        data = data[data['Medium']==combination_dict['medium']]

    structure_variables_list = combination_dict['structure_variables_list']
    #sum the data
    data = data.groupby(['Year']+structure_variables_list).sum().reset_index()
    #Separate energy and activity data
    energy_data = data[['Year','Energy']+structure_variables_list]
    activity_data = data[['Year', 'Activity']+structure_variables_list]
    emissions_data = data[['Year',  'Emissions']+structure_variables_list]
    #rename activity with variable
    activity_data = activity_data.rename(columns={'Activity':combination_dict['activity_variable']})

    #set variables to input into the LMDI function
    activity_variable = combination_dict['activity_variable']
    structure_variables_list = combination_dict['structure_variables_list']
    graph_title = combination_dict['graph_title']
    extra_identifier = combination_dict['extra_identifier']
    data_title = 'Transport_8th'
    energy_variable = 'Energy'
    time_variable = 'Year'
    font_size=25
    y_axis_min_percent_decrease=0.1
    residual_variable1=combination_dict['residual_variable1']
    emissions_divisia = combination_dict['emissions_divisia']
    hierarchical = combination_dict['hierarchical']

    #run LMDI
    results = main_function.run_divisia(data_title, extra_identifier, activity_data, energy_data, structure_variables_list, activity_variable, emissions_variable = 'Emissions', energy_variable = energy_variable, emissions_divisia = emissions_divisia, emissions_data=emissions_data, time_variable=time_variable,hierarchical=hierarchical)

    #if tehre is a new_structure_variables_list, we will use that when plotting
    if 'new_structure_variables_list' in combination_dict:
        structure_variables_list = combination_dict['new_structure_variables_list']
        
    #plot LMDI
    plot_output.plot_additive_waterfall(data_title, extra_identifier, structure_variables_list=structure_variables_list,activity_variable=activity_variable,energy_variable='Energy', emissions_variable='Emissions',emissions_divisia=emissions_divisia, time_variable='Year', graph_title=graph_title, residual_variable1=residual_variable1, residual_variable2='Emissions intensity', font_size=font_size, y_axis_min_percent_decrease=y_axis_min_percent_decrease,AUTO_OPEN=AUTO_OPEN, hierarchical=hierarchical)

    plot_output.plot_multiplicative_timeseries(data_title, extra_identifier,structure_variables_list=structure_variables_list,activity_variable=activity_variable,energy_variable='Energy', emissions_variable='Emissions',emissions_divisia=emissions_divisia, time_variable='Year', graph_title=graph_title, residual_variable1=residual_variable1, residual_variable2='Emissions intensity', font_size=font_size,AUTO_OPEN=AUTO_OPEN, hierarchical=hierarchical)

        
        

# %%
