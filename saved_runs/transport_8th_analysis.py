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
# all_data = pd.read_csv('input_data/tranport_8th/activity_efficiency_energy_road_stocks.csv')
transport_8th_emissions = pd.read_csv('input_data/tranport_8th/transport_8th_emissions.csv')
#filter out data after 2050
all_data = transport_8th_emissions[transport_8th_emissions['Year']<=2050]
#we will store our combvinations in a list of dictionaries and loop through them

AUTO_OPEN = False

better_names_dict = {'Drive': 'Engine type'}
#before going through the data lets rename some structural variables to be more readable
all_data = all_data.rename(columns=better_names_dict)

#%%
combination_dict_list = []
#instead of specifiying them manually which is quite repetivitve i am going to create the combinations for wehich we want to run the lmdi method and its graphing functions in a loop by creating a set of different values for each of the variables in the dictionary and then looping through all the combinations of these values to create a permutation of each of the combinations. In some cases there will need to be some extra logic because some values can only go with each other. 
scenario_list = ['Reference', 'Carbon Neutral']
transport_type_list = ['passenger', 'freight']
medium_list = ['everything', 'road']
structure_variables_list = [['Economy','Vehicle Type', 'Engine type'],['Vehicle Type', 'Engine type'], ['Engine type']]
emissions_divisia_list = [False, True]
hierarchical_list = [False, True]

for scenario in scenario_list:
    if scenario == 'Reference':
        scenario_text = 'REF'
    elif scenario == 'Carbon Neutral':
        scenario_text = 'CN'

    for transport_type in transport_type_list:
        if transport_type == 'passenger':
            activity_variable = 'passenger_km'
        elif transport_type == 'freight':
            activity_variable = 'freight_tonne_km'

        for medium in medium_list:
            if medium == 'everything':
                medium = ''
            for structure_variables in structure_variables_list:
                residual_variable1 = '{} efficiency'.format(structure_variables[-1])
                for emissions_divisia in emissions_divisia_list:
                    emissions_string = 'Energy use'
                    if emissions_divisia == True:
                        emissions_string = 'Emissions'
                        
                    for hierarchical in hierarchical_list:
                        hierarchical_string = '' 
                        if hierarchical == True:
                            hierarchical_string = 'Hierarchical'                          
                            if len(structure_variables) == 1:
                                continue#hierarchical only for more than one structure variable
                        else:
                            if len(structure_variables) > 1:
                                continue
                                # print('hierarchical shoudl almost always be used where there is more than one structure variable, so the graphing tools are not built to handle this case since each residual efficiency value wont have the correct labels')

                        extra_identifier = '{}_{}_{}_{}_{}_{}'.format(scenario, transport_type, medium, len(structure_variables),emissions_string, hierarchical_string)
                        graph_title = '{} {} - Drivers of changes in {} ({}) - {} LMDI'.format(medium, transport_type,emissions_string, scenario, hierarchical_string)

                        combination_dict_list.append({'scenario':scenario, 'transport_type':transport_type, 'medium':medium, 'activity_variable':activity_variable, 'structure_variables_list':structure_variables, 'graph_title':graph_title, 'extra_identifier':extra_identifier, 'emissions_divisia':emissions_divisia, 'hierarchical':hierarchical, 'residual_variable1':residual_variable1})

#%%


#%%
#create loop to run through the combinations
i=0
for combination_dict in combination_dict_list:
    # if combination_dict['hierarchical'] == False:
    #     #next
    #     continue
    i+=1
    print('\n\nRunning lmdi method for {}th iteration for '.format(i,combination_dict['extra_identifier']))

    #create a dataframe for each combination
    data = all_data.copy()
    #filter data by scenario
    data = data[data['Scenario']==combination_dict['scenario']]
    #filter data by transport type
    data = data[data['Transport Type']==combination_dict['transport_type']]
    #filter data by medium
    if combination_dict['medium'] == 'road':
        data = data[data['Medium']==combination_dict['medium']]
    else:
        pass

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

    #plot LMDI
    plot_output.plot_additive_waterfall(data_title, extra_identifier, structure_variables_list=structure_variables_list,activity_variable=activity_variable,energy_variable='Energy', emissions_variable='Emissions',emissions_divisia=emissions_divisia, time_variable='Year', graph_title=graph_title, residual_variable1=residual_variable1, residual_variable2='Emissions intensity', font_size=font_size, y_axis_min_percent_decrease=y_axis_min_percent_decrease,AUTO_OPEN=AUTO_OPEN, hierarchical=hierarchical)

    plot_output.plot_multiplicative_timeseries(data_title, extra_identifier,structure_variables_list=structure_variables_list,activity_variable=activity_variable,energy_variable='Energy', emissions_variable='Emissions',emissions_divisia=emissions_divisia, time_variable='Year', graph_title=graph_title, residual_variable1=residual_variable1, residual_variable2='Emissions intensity', font_size=font_size,AUTO_OPEN=AUTO_OPEN, hierarchical=hierarchical)

        
        


