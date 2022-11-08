#what the title says. plot specifics:
#%%
import os
if os.getcwd().endswith('saved_runs'):
    os.chdir('../')#go abck one folder so we can access all the functions
elif os.getcwd().endswith('Github'):
    os.chdir('./PyLMDI/')
else:
    print('You are in this folder: ', os.getcwd())

#%%
import pandas as pd
import numpy as np
import main_function
import plot_output
import data_creation_functions
import LMDI_functions
from enum import auto
import pandas as pd
import numpy as np

import plotly.express as px
pd.options.plotting.backend = "plotly"#set pandas backend to plotly plotting instead of matplotlib
import plotly.io as pio
pio.renderers.default = "browser"#allow plotting of graphs in the interactive notebook in vscode #or set to notebook
import plotly.graph_objects as go
import plotly
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





#%%

#for hiierarchical we jsut have to deal having an intensity effect for each structure variable rather than one with the name of the residual variable the user sets

#########################
#graph hierarchical here so we can be specific about the details
combination_dict = {'scenario':'Carbon Neutral', 'transport_type':'passenger', 'medium':'road', 'activity_variable':'passenger_km', 'structure_variables_list':['Vehicle Type', 'Drive'], 'graph_title':'Road passenger - Drivers of changes in energy use (CN) - Hierarchical', 'extra_identifier':'PASSENGER_CN_MODE_DRIVE_ROAD_HIERARCHICAL', 'emissions_divisia':False, 'hierarchical':True}
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
residual_variable1='Energy intensity'
emissions_divisia = combination_dict['emissions_divisia']
hierarchical = combination_dict['hierarchical']

#%%
########################################################################################################################################################################

#for hiierarchical we jsut have to deal having an intensity effect for each structure variable rather than one with the name of the residual variable the user sets

#get data
lmdi_output_multiplicative = pd.read_csv('output_data/{}{}_hierarchical_multiplicative_output.csv'.format(data_title, extra_identifier))

#rename the residual col
lmdi_output_multiplicative.rename(columns={'Drive intensity effect':'Residual efficiency'}, inplace=True)
#rename the Drive effect col to Engine type
lmdi_output_multiplicative.rename(columns={'Drive effect':'Engine type'}, inplace=True)
#rename passenger_km with activity variable
lmdi_output_multiplicative.rename(columns={'passenger_km effect':'Activity'}, inplace=True)
#rename Vehicle Type effect with 'Vehicle type'
lmdi_output_multiplicative.rename(columns={'Vehicle Type effect':'Vehicle type'}, inplace=True)

#create list of driver names in the order we want them to appear in the graph
driver_list = ['Activity', 'Vehicle type', 'Engine type', 'Residual efficiency']

#need to make the data in long format so we have a driver column instead fo a column for each driver:
mult_plot = pd.melt(lmdi_output_multiplicative, id_vars=[time_variable], var_name='Driver', value_name='Value')

#create category based on whether data is driver or change in energy use. because we dont want it to show in the graph we will just make driver a double space, and the change in enegry a singel space
mult_plot['Line type'] = mult_plot['Driver'].apply(lambda i: '' if i == 'Percent change in {}'.format(energy_variable) else ' ')

#set title
if graph_title == '':
    title = '{}{} - Multiplicative LMDI'.format(data_title, extra_identifier)
else:
    title = graph_title + ' - Multiplicative LMDI'

#plot
fig = px.line(mult_plot, x=time_variable, y="Value", color="Driver", line_dash = 'Line type',  category_orders={"Line type":['', ' '],"Driver":['Percent change in {}'.format(energy_variable)]+driver_list})#title=title,

fig.update_layout(
    font=dict(
        size=font_size
    ),legend_title_text='Line/Driver')
#set name of y axis to 'Proportional effect on energy use'
fig.update_yaxes(title_text='Proportional effect on energy use')

plotly.offline.plot(fig, filename='./plotting_output/' + data_title + extra_identifier + 'multiplicative_timeseries.html', auto_open=AUTO_OPEN)
fig.write_image("./plotting_output/static/" + data_title + extra_identifier + 'multiplicative_timeseries.png')

#%% 














#%%


#########################
#graph hierarchical here so we can be specific about the details
combination_dict = {'scenario':'Reference', 'transport_type':'passenger', 'medium':'road', 'activity_variable':'passenger_km', 'structure_variables_list':['Vehicle Type', 'Drive'], 'graph_title':'Road passenger - Drivers of changes in energy use (REF) - Hierarchical', 'extra_identifier':'PASSENGER_REF_MODE_DRIVE_ROAD_HIERARCHICAL', 'emissions_divisia':False, 'hierarchical':True}
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
residual_variable1='Energy intensity'
emissions_divisia = combination_dict['emissions_divisia']
hierarchical = combination_dict['hierarchical']

#%%
########################################################################################################################################################################

#for hiierarchical we jsut have to deal having an intensity effect for each structure variable rather than one with the name of the residual variable the user sets

#get data
lmdi_output_multiplicative = pd.read_csv('output_data/{}{}_hierarchical_multiplicative_output.csv'.format(data_title, extra_identifier))

#rename the residual col
lmdi_output_multiplicative.rename(columns={'Drive intensity effect':'Residual efficiency'}, inplace=True)
#rename the Drive effect col to Engine type
lmdi_output_multiplicative.rename(columns={'Drive effect':'Engine type'}, inplace=True)
#rename passenger_km with activity variable
lmdi_output_multiplicative.rename(columns={'passenger_km effect':'Activity'}, inplace=True)
#rename Vehicle Type effect with 'Vehicle type'
lmdi_output_multiplicative.rename(columns={'Vehicle Type effect':'Vehicle type'}, inplace=True)

#create list of driver names in the order we want them to appear in the graph
driver_list = ['Activity', 'Vehicle type', 'Engine type', 'Residual efficiency']

#need to make the data in long format so we have a driver column instead fo a column for each driver:
mult_plot = pd.melt(lmdi_output_multiplicative, id_vars=[time_variable], var_name='Driver', value_name='Value')

#create category based on whether data is driver or change in energy use. because we dont want it to show in the graph we will just make driver a double space, and the change in enegry a singel space
mult_plot['Line type'] = mult_plot['Driver'].apply(lambda i: '' if i == 'Percent change in {}'.format(energy_variable) else ' ')

#set title
if graph_title == '':
    title = '{}{} - Multiplicative LMDI'.format(data_title, extra_identifier)
else:
    title = graph_title + ' - Multiplicative LMDI'

#plot
fig = px.line(mult_plot, x=time_variable, y="Value", color="Driver", line_dash = 'Line type',  category_orders={"Line type":['', ' '],"Driver":['Percent change in {}'.format(energy_variable)]+driver_list})#title=title,

fig.update_layout(
    font=dict(
        size=font_size
    ),legend_title_text='Line/Driver')
#set name of y axis to 'Proportional effect on energy use'
fig.update_yaxes(title_text='Proportional effect on energy use')

plotly.offline.plot(fig, filename='./plotting_output/' + data_title + extra_identifier + 'multiplicative_timeseries.html', auto_open=AUTO_OPEN)
fig.write_image("./plotting_output/static/" + data_title + extra_identifier + 'multiplicative_timeseries.png')
# %%









#%%


#########################
#graph hierarchical here so we can be specific about the details
combination_dict = {'scenario':'Reference', 'transport_type':'passenger', 'medium':'everything', 'activity_variable':'passenger_km', 'structure_variables_list':['Vehicle Type', 'Drive'], 'graph_title':'Passenger - Drivers of changes in energy use (REF) - Hierarchical', 'extra_identifier':'PASSENGER_REF_MODE_DRIVE_HIERARCHICAL', 'emissions_divisia':False, 'hierarchical':True}
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
residual_variable1='Energy intensity'
emissions_divisia = combination_dict['emissions_divisia']
hierarchical = combination_dict['hierarchical']

#%%
########################################################################################################################################################################

#for hiierarchical we jsut have to deal having an intensity effect for each structure variable rather than one with the name of the residual variable the user sets

#get data
lmdi_output_multiplicative = pd.read_csv('output_data/{}{}_hierarchical_multiplicative_output.csv'.format(data_title, extra_identifier))

#rename the residual col
lmdi_output_multiplicative.rename(columns={'Drive intensity effect':'Residual efficiency'}, inplace=True)
#rename the Drive effect col to Engine type
lmdi_output_multiplicative.rename(columns={'Drive effect':'Engine type'}, inplace=True)
#rename passenger_km with activity variable
lmdi_output_multiplicative.rename(columns={'passenger_km effect':'Activity'}, inplace=True)
#rename Vehicle Type effect with 'Vehicle type'
lmdi_output_multiplicative.rename(columns={'Mode effect':'Vehicle type'}, inplace=True)

#create list of driver names in the order we want them to appear in the graph
driver_list = ['Activity', 'Mode type', 'Engine type', 'Residual efficiency']

#need to make the data in long format so we have a driver column instead fo a column for each driver:
mult_plot = pd.melt(lmdi_output_multiplicative, id_vars=[time_variable], var_name='Driver', value_name='Value')

#create category based on whether data is driver or change in energy use. because we dont want it to show in the graph we will just make driver a double space, and the change in enegry a singel space
mult_plot['Line type'] = mult_plot['Driver'].apply(lambda i: '' if i == 'Percent change in {}'.format(energy_variable) else ' ')

#set title
if graph_title == '':
    title = '{}{} - Multiplicative LMDI'.format(data_title, extra_identifier)
else:
    title = graph_title + ' - Multiplicative LMDI'

#plot
fig = px.line(mult_plot, x=time_variable, y="Value", color="Driver", line_dash = 'Line type',  category_orders={"Line type":['', ' '],"Driver":['Percent change in {}'.format(energy_variable)]+driver_list})#title=title,

fig.update_layout(
    font=dict(
        size=font_size
    ),legend_title_text='Line/Driver')
#set name of y axis to 'Proportional effect on energy use'
fig.update_yaxes(title_text='Proportional effect on energy use')

plotly.offline.plot(fig, filename='./plotting_output/' + data_title + extra_identifier + 'multiplicative_timeseries.html', auto_open=AUTO_OPEN)
fig.write_image("./plotting_output/static/" + data_title + extra_identifier + 'multiplicative_timeseries.png')
# %%


#%%


#########################
#graph hierarchical here so we can be specific about the details
combination_dict = {'scenario':'Carbon Neutral', 'transport_type':'passenger', 'medium':'everything', 'activity_variable':'passenger_km', 'structure_variables_list':['Vehicle Type', 'Drive'], 'graph_title':'Passenger - Drivers of changes in energy use (CN) - Hierarchical', 'extra_identifier':'PASSENGER_CN_MODE_DRIVE_HIERARCHICAL', 'emissions_divisia':False, 'hierarchical':True}
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
residual_variable1='Energy intensity'
emissions_divisia = combination_dict['emissions_divisia']
hierarchical = combination_dict['hierarchical']





#%%
########################################################################################################################################################################

#for hiierarchical we jsut have to deal having an intensity effect for each structure variable rather than one with the name of the residual variable the user sets

#get data
lmdi_output_multiplicative = pd.read_csv('output_data/{}{}_hierarchical_multiplicative_output.csv'.format(data_title, extra_identifier))

#rename the residual col
lmdi_output_multiplicative.rename(columns={'Drive intensity effect':'Residual efficiency'}, inplace=True)
#rename the Drive effect col to Engine type
lmdi_output_multiplicative.rename(columns={'Drive effect':'Engine type'}, inplace=True)
#rename passenger_km with activity variable
lmdi_output_multiplicative.rename(columns={'passenger_km effect':'Activity'}, inplace=True)
#rename Vehicle Type effect with 'Vehicle type'
lmdi_output_multiplicative.rename(columns={'Mode effect':'Vehicle type'}, inplace=True)

#create list of driver names in the order we want them to appear in the graph
driver_list = ['Activity', 'Mode type', 'Engine type', 'Residual efficiency']

#need to make the data in long format so we have a driver column instead fo a column for each driver:
mult_plot = pd.melt(lmdi_output_multiplicative, id_vars=[time_variable], var_name='Driver', value_name='Value')

#create category based on whether data is driver or change in energy use. because we dont want it to show in the graph we will just make driver a double space, and the change in enegry a singel space
mult_plot['Line type'] = mult_plot['Driver'].apply(lambda i: '' if i == 'Percent change in {}'.format(energy_variable) else ' ')

#set title
if graph_title == '':
    title = '{}{} - Multiplicative LMDI'.format(data_title, extra_identifier)
else:
    title = graph_title + ' - Multiplicative LMDI'

#plot
fig = px.line(mult_plot, x=time_variable, y="Value", color="Driver", line_dash = 'Line type',  category_orders={"Line type":['', ' '],"Driver":['Percent change in {}'.format(energy_variable)]+driver_list})#title=title,

fig.update_layout(
    font=dict(
        size=font_size
    ),legend_title_text='Line/Driver')
#set name of y axis to 'Proportional effect on energy use'
fig.update_yaxes(title_text='Proportional effect on energy use')

plotly.offline.plot(fig, filename='./plotting_output/' + data_title + extra_identifier + 'multiplicative_timeseries.html', auto_open=AUTO_OPEN)
fig.write_image("./plotting_output/static/" + data_title + extra_identifier + 'multiplicative_timeseries.png')
# %%












#%%


#########################
#graph hierarchical here so we can be specific about the details
combination_dict = {'scenario':'Reference', 'transport_type':'freight', 'medium':'everything', 'activity_variable':'freight_tonne_km', 'structure_variables_list':['Vehicle Type', 'Drive'], 'graph_title':'Freight - Drivers of changes in energy use (REF) - Hierarchical', 'extra_identifier':'FREIGHT_REF_MODE_DRIVE_HIERARCHICAL', 'emissions_divisia':False, 'hierarchical':True}
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
residual_variable1='Energy intensity'
emissions_divisia = combination_dict['emissions_divisia']
hierarchical = combination_dict['hierarchical']

#%%
########################################################################################################################################################################

#for hiierarchical we jsut have to deal having an intensity effect for each structure variable rather than one with the name of the residual variable the user sets

#get data
lmdi_output_multiplicative = pd.read_csv('output_data/{}{}_hierarchical_multiplicative_output.csv'.format(data_title, extra_identifier))

#rename the residual col
lmdi_output_multiplicative.rename(columns={'Drive intensity effect':'Residual efficiency'}, inplace=True)
#rename the Drive effect col to Engine type
lmdi_output_multiplicative.rename(columns={'Drive effect':'Engine type'}, inplace=True)
#rename passenger_km with activity variable
lmdi_output_multiplicative.rename(columns={'passenger_km effect':'Activity'}, inplace=True)
#rename Vehicle Type effect with 'Vehicle type'
lmdi_output_multiplicative.rename(columns={'Mode effect':'Vehicle type'}, inplace=True)

#create list of driver names in the order we want them to appear in the graph
driver_list = ['Activity', 'Mode type', 'Engine type', 'Residual efficiency']

#need to make the data in long format so we have a driver column instead fo a column for each driver:
mult_plot = pd.melt(lmdi_output_multiplicative, id_vars=[time_variable], var_name='Driver', value_name='Value')

#create category based on whether data is driver or change in energy use. because we dont want it to show in the graph we will just make driver a double space, and the change in enegry a singel space
mult_plot['Line type'] = mult_plot['Driver'].apply(lambda i: '' if i == 'Percent change in {}'.format(energy_variable) else ' ')

#set title
if graph_title == '':
    title = '{}{} - Multiplicative LMDI'.format(data_title, extra_identifier)
else:
    title = graph_title + ' - Multiplicative LMDI'

#plot
fig = px.line(mult_plot, x=time_variable, y="Value", color="Driver", line_dash = 'Line type',  category_orders={"Line type":['', ' '],"Driver":['Percent change in {}'.format(energy_variable)]+driver_list})#title=title,

fig.update_layout(
    font=dict(
        size=font_size
    ),legend_title_text='Line/Driver')
#set name of y axis to 'Proportional effect on energy use'
fig.update_yaxes(title_text='Proportional effect on energy use')

plotly.offline.plot(fig, filename='./plotting_output/' + data_title + extra_identifier + 'multiplicative_timeseries.html', auto_open=AUTO_OPEN)
fig.write_image("./plotting_output/static/" + data_title + extra_identifier + 'multiplicative_timeseries.png')
# %%


#%%


#########################
#graph hierarchical here so we can be specific about the details
#graph hierarchical here so we can be specific about the details
combination_dict = {'scenario':'Carbon Neutral', 'transport_type':'freight', 'medium':'everything', 'activity_variable':'Activity', 'structure_variables_list':['Mode', 'Engine type'], 'graph_title':'Freight - Drivers of changes in energy use (CN) - Hierarchical', 'extra_identifier':'FREIGHT_CN_MODE_DRIVE_HIERARCHICAL', 'emissions_divisia':False, 'hierarchical':True, 'residual_variable1':'Residual efficiency'}
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





#%%
########################################################################################################################################################################

#for hiierarchical we jsut have to deal having an intensity effect for each structure variable rather than one with the name of the residual variable the user sets

# %%

