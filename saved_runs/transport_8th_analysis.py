#%%
#run this file on transport energy data as found in the input data to get the transport output
#its very likely that this could be useful for other analysis tasks within transport. so dont delte ti!
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

#%%
#load data in

###########################################################################

#we will create a script which will loop through the different combinations of data we have and run the LMDI model on them and plot them
all_data = pd.read_csv('input_data/tranport_8th/activity_efficiency_energy_road_stocks.csv')
transport_8th_emissions = pd.read_csv('input_data/tranport_8th/transport_8th_emissions.csv')
#filter out data after 2050
all_data = transport_8th_emissions[transport_8th_emissions['Year']<=2050]
#we will store our combvinations in a list of dictionaries and loop through them
combination_dict_list = []
AUTO_OPEN = False
#set out rules for the combinations from which we'll let github copilot create the code for us
#rules are:
#for each scenario
#for each transport type, setting activity variable to freight tonne km for freight and passenger km for passenger

#for medium == road or medium is everything

combination_dict_list.append({'scenario':'Reference', 'transport_type':'passenger', 'medium':'road', 'activity_variable':'passenger_km', 'structure_variables_list':['Vehicle Type', 'Drive'], 'graph_title':'Road passenger - Drivers of changes in energy use (Ref)', 'extra_identifier':'PASSENGER_REF_MODE_DRIVE_ROAD', 'emissions_divisia':False, 'hierarchical':False, 'residual_variable1':'Residual efficiency'})
combination_dict_list.append({'scenario':'Carbon Neutral', 'transport_type':'passenger', 'medium':'road', 'activity_variable':'passenger_km', 'structure_variables_list':['Vehicle Type', 'Drive'], 'graph_title':'Road passenger - Drivers of changes in energy use (CN)', 'extra_identifier':'PASSENGER_CN_MODE_DRIVE_ROAD', 'emissions_divisia':False, 'hierarchical':False, 'residual_variable1':'Residual efficiency'})
combination_dict_list.append({'scenario':'Reference', 'transport_type':'freight', 'medium':'road', 'activity_variable':'freight_tonne_km', 'structure_variables_list':['Vehicle Type', 'Drive'], 'graph_title':'Road freight - Drivers of changes in energy use (Ref)', 'extra_identifier':'FREIGHT_REF_MODE_DRIVE_ROAD', 'emissions_divisia':False, 'hierarchical':False, 'residual_variable1':'Residual efficiency'})
combination_dict_list.append({'scenario':'Carbon Neutral', 'transport_type':'freight', 'medium':'road', 'activity_variable':'freight_tonne_km', 'structure_variables_list':['Vehicle Type', 'Drive'], 'graph_title':'Road freight - Drivers of changes in energy use (CN)', 'extra_identifier':'FREIGHT_CN_MODE_DRIVE_ROAD', 'emissions_divisia':False, 'hierarchical':False, 'residual_variable1':'Residual efficiency'})
#for medium is everything
combination_dict_list.append({'scenario':'Reference', 'transport_type':'passenger', 'medium':'everything', 'activity_variable':'passenger_km', 'structure_variables_list':['Vehicle Type', 'Drive'], 'graph_title':'Road passenger - Drivers of changes in energy use (Ref)', 'extra_identifier':'PASSENGER_REF_MODE_DRIVE', 'emissions_divisia':False, 'hierarchical':False, 'residual_variable1':'Residual efficiency'})
combination_dict_list.append({'scenario':'Carbon Neutral', 'transport_type':'passenger', 'medium':'everything', 'activity_variable':'passenger_km', 'structure_variables_list':['Vehicle Type', 'Drive'], 'graph_title':'Road passenger - Drivers of changes in energy use (CN)', 'extra_identifier':'PASSENGER_CN_MODE_DRIVE', 'emissions_divisia':False, 'hierarchical':False, 'residual_variable1':'Residual efficiency'})
combination_dict_list.append({'scenario':'Reference', 'transport_type':'freight', 'medium':'everything', 'activity_variable':'freight_tonne_km', 'structure_variables_list':['Vehicle Type', 'Drive'], 'graph_title':'Road freight - Drivers of changes in energy use (Ref)', 'extra_identifier':'FREIGHT_REF_MODE_DRIVE', 'emissions_divisia':False, 'hierarchical':False, 'residual_variable1':'Residual efficiency'})
combination_dict_list.append({'scenario':'Carbon Neutral', 'transport_type':'freight', 'medium':'everything', 'activity_variable':'freight_tonne_km', 'structure_variables_list':['Vehicle Type', 'Drive'], 'graph_title':'Road freight - Drivers of changes in energy use (CN)', 'extra_identifier':'FREIGHT_CN_MODE_DRIVE', 'emissions_divisia':False, 'hierarchical':False, 'residual_variable1':'Residual efficiency'})

#and now with emissions divisia = True and the extra_identifier has _EMISSIONS on the end , and  Drivers of changes in emissions (Ref) and Drivers of changes in emissions (CN) as the graph title
combination_dict_list.append({'scenario':'Reference', 'transport_type':'passenger', 'medium':'road', 'activity_variable':'passenger_km', 'structure_variables_list':['Vehicle Type', 'Drive'], 'graph_title':'Road passenger - Drivers of changes in emissions (Ref)', 'extra_identifier':'PASSENGER_REF_MODE_DRIVE_ROAD_EMISSIONS', 'emissions_divisia':True, 'hierarchical':False, 'residual_variable1':'Residual efficiency'})
combination_dict_list.append({'scenario':'Carbon Neutral', 'transport_type':'passenger', 'medium':'road', 'activity_variable':'passenger_km', 'structure_variables_list':['Vehicle Type', 'Drive'], 'graph_title':'Road passenger - Drivers of changes in emissions (CN)', 'extra_identifier':'PASSENGER_CN_MODE_DRIVE_ROAD_EMISSIONS', 'emissions_divisia':True, 'hierarchical':False, 'residual_variable1':'Residual efficiency'})
combination_dict_list.append({'scenario':'Reference', 'transport_type':'freight', 'medium':'road', 'activity_variable':'freight_tonne_km', 'structure_variables_list':['Vehicle Type', 'Drive'], 'graph_title':'Road freight - Drivers of changes in emissions (Ref)', 'extra_identifier':'FREIGHT_REF_MODE_DRIVE_ROAD_EMISSIONS', 'emissions_divisia':True, 'hierarchical':False, 'residual_variable1':'Residual efficiency'})
combination_dict_list.append({'scenario':'Carbon Neutral', 'transport_type':'freight', 'medium':'road', 'activity_variable':'freight_tonne_km', 'structure_variables_list':['Vehicle Type', 'Drive'], 'graph_title':'Road freight - Drivers of changes in emissions (CN)', 'extra_identifier':'FREIGHT_CN_MODE_DRIVE_ROAD_EMISSIONS', 'emissions_divisia':True, 'hierarchical':False, 'residual_variable1':'Residual efficiency'})
#for medium is everything
combination_dict_list.append({'scenario':'Reference', 'transport_type':'passenger', 'medium':'everything', 'activity_variable':'passenger_km', 'structure_variables_list':['Vehicle Type', 'Drive'], 'graph_title':'Road passenger - Drivers of changes in emissions (Ref)', 'extra_identifier':'PASSENGER_REF_MODE_DRIVE_EMISSIONS', 'emissions_divisia':True, 'hierarchical':False, 'residual_variable1':'Residual efficiency'})
combination_dict_list.append({'scenario':'Carbon Neutral', 'transport_type':'passenger', 'medium':'everything', 'activity_variable':'passenger_km', 'structure_variables_list':['Vehicle Type', 'Drive'], 'graph_title':'Road passenger - Drivers of changes in emissions (CN)', 'extra_identifier':'PASSENGER_CN_MODE_DRIVE_EMISSIONS', 'emissions_divisia':True, 'hierarchical':False, 'residual_variable1':'Residual efficiency'})
combination_dict_list.append({'scenario':'Reference', 'transport_type':'freight', 'medium':'everything', 'activity_variable':'freight_tonne_km', 'structure_variables_list':['Vehicle Type', 'Drive'], 'graph_title':'Road freight - Drivers of changes in emissions (Ref)', 'extra_identifier':'FREIGHT_REF_MODE_DRIVE_EMISSIONS', 'emissions_divisia':True, 'hierarchical':False, 'residual_variable1':'Residual efficiency'})
combination_dict_list.append({'scenario':'Carbon Neutral', 'transport_type':'freight', 'medium':'everything', 'activity_variable':'freight_tonne_km', 'structure_variables_list':['Vehicle Type', 'Drive'], 'graph_title':'Road freight - Drivers of changes in emissions (CN)', 'extra_identifier':'FREIGHT_CN_MODE_DRIVE_EMISSIONS', 'emissions_divisia':True, 'hierarchical':False, 'residual_variable1':'Residual efficiency'})

#and now woith hierarchical = True and the extra_identifier has _HIERARCHICAL on the end , and  Drivers of changes in energy use (Ref) - Hierarchical and Drivers of changes in energy use (CN) - Hierarchical as the graph title, and if medium = 'everything' then swapo 'vehicle type' for 'Mode' in the structure_variables_list. Also change drive to Engine type
combination_dict_list.append({'scenario':'Carbon Neutral', 'transport_type':'freight', 'medium':'everything', 'activity_variable':'Activity', 'new_structure_variables_list':['Mode', 'Engine type'], 'structure_variables_list':['Vehicle Type', 'Drive'], 'graph_title':'Freight - Drivers of changes in energy use (CN) - Hierarchical', 'extra_identifier':'FREIGHT_CN_MODE_DRIVE_HIERARCHICAL', 'emissions_divisia':False, 'hierarchical':True, 'residual_variable1':'Residual efficiency'})
combination_dict_list.append({'scenario':'Reference', 'transport_type':'freight', 'medium':'everything', 'activity_variable':'Activity', 'new_structure_variables_list':['Mode', 'Engine type'], 'structure_variables_list':['Vehicle Type', 'Drive'], 'graph_title':'Freight - Drivers of changes in energy use (Ref) - Hierarchical', 'extra_identifier':'FREIGHT_REF_MODE_DRIVE_HIERARCHICAL', 'emissions_divisia':False, 'hierarchical':True, 'residual_variable1':'Residual efficiency'})
combination_dict_list.append({'scenario':'Carbon Neutral', 'transport_type':'passenger', 'medium':'everything', 'activity_variable':'Activity', 'new_structure_variables_list':['Mode', 'Engine type'], 'structure_variables_list':['Vehicle Type', 'Drive'], 'graph_title':'Passenger - Drivers of changes in energy use (CN) - Hierarchical', 'extra_identifier':'PASSENGER_CN_MODE_DRIVE_HIERARCHICAL', 'emissions_divisia':False, 'hierarchical':True, 'residual_variable1':'Residual efficiency'})
combination_dict_list.append({'scenario':'Reference', 'transport_type':'passenger', 'medium':'everything', 'activity_variable':'Activity', 'new_structure_variables_list':['Mode', 'Engine type'], 'structure_variables_list':['Vehicle Type', 'Drive'], 'graph_title':'Passenger - Drivers of changes in energy use (Ref) - Hierarchical', 'extra_identifier':'PASSENGER_REF_MODE_DRIVE_HIERARCHICAL', 'emissions_divisia':False, 'hierarchical':True, 'residual_variable1':'Residual efficiency'})

#now with medium = road
combination_dict_list.append({'scenario':'Carbon Neutral', 'transport_type':'freight', 'medium':'road', 'activity_variable':'Activity', 'new_structure_variables_list':['Mode', 'Engine type'], 'structure_variables_list':['Vehicle Type', 'Drive'], 'graph_title':'Road freight - Drivers of changes in energy use (CN) - Hierarchical', 'extra_identifier':'FREIGHT_CN_MODE_DRIVE_ROAD_HIERARCHICAL', 'emissions_divisia':False, 'hierarchical':True, 'residual_variable1':'Residual efficiency'})
combination_dict_list.append({'scenario':'Reference', 'transport_type':'freight', 'medium':'road', 'activity_variable':'Activity', 'new_structure_variables_list':['Mode', 'Engine type'], 'structure_variables_list':['Vehicle Type', 'Drive'], 'graph_title':'Road freight - Drivers of changes in energy use (Ref) - Hierarchical', 'extra_identifier':'FREIGHT_REF_MODE_DRIVE_ROAD_HIERARCHICAL', 'emissions_divisia':False, 'hierarchical':True, 'residual_variable1':'Residual efficiency'})
combination_dict_list.append({'scenario':'Carbon Neutral', 'transport_type':'passenger', 'medium':'road', 'activity_variable':'Activity', 'new_structure_variables_list':['Mode', 'Engine type'], 'structure_variables_list':['Vehicle Type', 'Drive'], 'graph_title':'Road passenger - Drivers of changes in energy use (CN) - Hierarchical', 'extra_identifier':'PASSENGER_CN_MODE_DRIVE_ROAD_HIERARCHICAL', 'emissions_divisia':False, 'hierarchical':True, 'residual_variable1':'Residual efficiency'})
combination_dict_list.append({'scenario':'Reference', 'transport_type':'passenger', 'medium':'road', 'activity_variable':'Activity', 'new_structure_variables_list':['Mode', 'Engine type'], 'structure_variables_list':['Vehicle Type', 'Drive'], 'graph_title':'Road passenger - Drivers of changes in energy use (Ref) - Hierarchical', 'extra_identifier':'PASSENGER_REF_MODE_DRIVE_ROAD_HIERARCHICAL', 'emissions_divisia':False, 'hierarchical':True, 'residual_variable1':'Residual efficiency'})

#for structure_variables_list = 'Drive' and medium ='road':
combination_dict_list.append({'scenario':'Reference', 'transport_type':'passenger', 'medium':'road', 'activity_variable':'passenger_km', 'structure_variables_list':['Drive'], 'graph_title':'Road passenger - Drivers of changes in energy use (Ref)', 'extra_identifier':'PASSENGER_REF_DRIVE_ROAD', 'emissions_divisia':False, 'hierarchical':False, 'residual_variable1':'Residual efficiency'})
combination_dict_list.append({'scenario':'Carbon Neutral', 'transport_type':'passenger', 'medium':'road', 'activity_variable':'passenger_km', 'structure_variables_list':['Drive'], 'graph_title':'Road passenger - Drivers of changes in energy use (CN)', 'extra_identifier':'PASSENGER_CN_DRIVE_ROAD', 'emissions_divisia':False, 'hierarchical':False, 'residual_variable1':'Residual efficiency'})
combination_dict_list.append({'scenario':'Reference', 'transport_type':'freight', 'medium':'road', 'activity_variable':'freight_tonne_km', 'structure_variables_list':['Drive'], 'graph_title':'Road freight - Drivers of changes in energy use (Ref)', 'extra_identifier':'FREIGHT_REF_DRIVE_ROAD', 'emissions_divisia':False, 'hierarchical':False, 'residual_variable1':'Residual efficiency'})
combination_dict_list.append({'scenario':'Carbon Neutral', 'transport_type':'freight', 'medium':'road', 'activity_variable':'freight_tonne_km', 'structure_variables_list':['Drive'], 'graph_title':'Road freight - Drivers of changes in energy use (CN)', 'extra_identifier':'FREIGHT_CN_DRIVE_ROAD', 'emissions_divisia':False, 'hierarchical':False, 'residual_variable1':'Residual efficiency'})


#%%
#create loop to run through the combinations
for combination_dict in combination_dict_list:
    if combination_dict['hierarchical'] == False:
        #next
        continue
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
    plot_output.plot_additive_waterfall(data_title, extra_identifier, structure_variables_list=structure_variables_list,activity_variable=activity_variable,energy_variable='Energy', emissions_variable='Emissions',emissions_divisia=emissions_divisia, time_variable='Year', graph_title=graph_title, residual_variable1='Energy intensity', residual_variable2='Emissions intensity', font_size=font_size, y_axis_min_percent_decrease=y_axis_min_percent_decrease,AUTO_OPEN=AUTO_OPEN, hierarchical=hierarchical)

    plot_output.plot_multiplicative_timeseries(data_title, extra_identifier,structure_variables_list=structure_variables_list,activity_variable=activity_variable,energy_variable='Energy', emissions_variable='Emissions',emissions_divisia=emissions_divisia, time_variable='Year', graph_title=graph_title, residual_variable1='Energy intensity', residual_variable2='Emissions intensity', font_size=font_size,AUTO_OPEN=AUTO_OPEN, hierarchical=hierarchical)

        
        





#%%
#ANALYSIS OF THE INPUT DATA
# # compare total energy in each of the data frames 
# all_data = pd.read_csv('input_data/tranport_8th/activity_efficiency_energy_road_stocks.csv')
# transport_8th_emissions = pd.read_csv('input_data/tranport_8th/transport_8th_emissions.csv')
# #when comparing the total energy in the two data frames, the total energy in the transport_8th_emissions is 1.2% higher than the total energy in the activity_efficiency_energy_road_stocks
# # # # the cateogires where there are missing values in transport 8th emissions Economy  Medium  Drive
# # 15_RP    road    bev      648
# #                  g        648
# # 17_SIN   road    g        648
# #                  bev      648
# # 15_RP    road    d        540
# #                  fcev     540
# # 17_SIN   road    fcev     540
# #                  d        540
# # 15_RP    road    lpg      432
# # 17_SIN   road    cng      324
# # 15_RP    air     air      216
# #          ship    ship     216
# #          rail    rail     216
# # 17_SIN   ship    ship     216
# #          rail    rail     108
# # 15_RP    road    phevg    108
# # 17_SIN   road    phevg    108

# #since its too hard to tell why this is occuring i will just use the transport_8th_emissions data frame for the emissions data
# X = all_data['Energy'].sum()
# Y = transport_8th_emissions['Energy'].sum()

# print(X)
# print(Y)

# #see what the difference is
# #first rrem,ove any cols that arent in both
# all_data = all_data[all_data.columns.intersection(transport_8th_emissions.columns)]
# transport_8th_emissions = transport_8th_emissions[transport_8th_emissions.columns.intersection(all_data.columns)]

# #join the two on their categorical columns and see where the NAs are
# joined = all_data.merge(transport_8th_emissions, on=['Year','Economy', 'Vehicle Type', 'Drive', 'Medium', 'Transport Type', 'Scenario'], how='outer', indicator=True)
# joined_na = joined[joined['_merge']=='left_only']
# joined_na = joined_na[joined_na['Energy_x'].notna()]

# #analysis of categorical cols that are different suing statistics
# joined_na['Economy'].value_counts()
# joined_na[['Economy','Medium', 'Drive']].value_counts()


# # #create df where only the categorical columns are kept
# # all_data_cat = all_data[['Year','Scenario', 'Transport Type', 'Medium', 'Vehicle Type', 'Drive']]
# # transport_8th_emissions_cat = transport_8th_emissions[['Year','Scenario', 'Transport Type', 'Medium', 'Vehicle Type', 'Drive']]
# # #see if
# # %%
