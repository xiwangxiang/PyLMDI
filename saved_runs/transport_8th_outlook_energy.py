#%%
#run this file on transport energy data as found in the input data to get the transport output
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
import data_creation_functions 
import LMDI_functions
from main_function import run_divisia
from plot_output import plot_multiplicative, plot_additive
#load data in


#import data from excel using a preset name for the data, which is also used for creating graph titles and genreally identifying outputs/inputs related to this dataset specifically
data_title = 'outlook-transport-divisia'
extra_identifier = 'PASSENGER_REF'#use this if you need the program to insert an extra identifier in things like filenames and plot titles

activity_data = pd.read_excel('input_data/{}.xlsx'.format(data_title), sheet_name='ref_p_km')
energy_data = pd.read_excel('input_data/{}.xlsx'.format(data_title), sheet_name='ref_pass_energy_pj')

structure_variable = 'Mode'#set to the name of the varaible that will be used to group the data by. noramlly, sector for industry data, mode for transport data
activity_variable = 'passenger_km'#set to the name of the varaible that will be used for the activity data eg. gdp or passenger km or freight tonne km
energy_variable = 'PJ'#this will not often change

graph_title = 'Passenger transport drivers of changes in energy use (Reference)'

emissions_divisia = False

run_divisia(data_title=data_title, extra_identifier=extra_identifier, activity_data=activity_data, energy_data=energy_data, structure_variable=structure_variable, activity_variable=activity_variable, emissions_variable = 'MtCO2', energy_variable = energy_variable, emissions_divisia = False, emissions_data=[], time_variable='Year')

plot_multiplicative(data_title, extra_identifier, emissions_divisia, time_variable='Year', structure_variable=structure_variable, graph_title = graph_title)
plot_additive(data_title, extra_identifier, emissions_divisia, time_variable='Year', structure_variable=structure_variable, graph_title = graph_title)

#%%
data_title = 'outlook-transport-divisia'
extra_identifier = 'PASSENGER_CN'#use this if you need the program to insert an extra identifier in things like filenames and plot titles

activity_data = pd.read_excel('input_data/{}.xlsx'.format(data_title), sheet_name='cn_p_km')
energy_data = pd.read_excel('input_data/{}.xlsx'.format(data_title), sheet_name='cn_pass_energy_pj')

structure_variable = 'Mode'#set to the name of the varaible that will be used to group the data by. noramlly, sector for industry data, mode for transport data
activity_variable = 'passenger_km'#set to the name of the varaible that will be used for the activity data eg. gdp or passenger km or freight tonne km
energy_variable = 'PJ'#this will not often change

graph_title = 'Passenger transport drivers of changes in energy use (Carbon neutral scenario)'

emissions_divisia = False

run_divisia(data_title=data_title, extra_identifier=extra_identifier, activity_data=activity_data, energy_data=energy_data, structure_variable=structure_variable, activity_variable=activity_variable, emissions_variable = 'MtCO2', energy_variable = energy_variable, emissions_divisia = False, emissions_data=[], time_variable='Year')

plot_multiplicative(data_title, extra_identifier, emissions_divisia, time_variable='Year', structure_variable=structure_variable, graph_title = graph_title)
plot_additive(data_title, extra_identifier, emissions_divisia, time_variable='Year', structure_variable=structure_variable, graph_title = graph_title)
#%%
data_title = 'outlook-transport-divisia'

extra_identifier = 'FREIGHT_CN'#use this if you need the program to insert an extra identifier in things like filenames and plot titles

activity_data = pd.read_excel('input_data/{}.xlsx'.format(data_title), sheet_name='cn_freight_tonne_km')
energy_data = pd.read_excel('input_data/{}.xlsx'.format(data_title), sheet_name='cn_freight_energy_pj')

structure_variable = 'Mode'#set to the name of the varaible that will be used to group the data by. noramlly, sector for industry data, mode for transport data
activity_variable = 'freight_tonne_km'#set to the name of the varaible that will be used for the activity data eg. gdp or passenger km or freight tonne km
energy_variable = 'PJ'#this will not often change

graph_title = 'Freight transport drivers of changes in energy use (Carbon neutral scenario)'
emissions_divisia = False

run_divisia(data_title=data_title, extra_identifier=extra_identifier, activity_data=activity_data, energy_data=energy_data, structure_variable=structure_variable, activity_variable=activity_variable, emissions_variable = 'MtCO2', energy_variable = energy_variable, emissions_divisia = False, emissions_data=[], time_variable='Year')

plot_multiplicative(data_title, extra_identifier, emissions_divisia, time_variable='Year', structure_variable=structure_variable, graph_title = graph_title)
plot_additive(data_title, extra_identifier, emissions_divisia, time_variable='Year', structure_variable=structure_variable, graph_title = graph_title)
#%%
data_title = 'outlook-transport-divisia'

extra_identifier = 'FREIGHT_REF'#use this if you need the program to insert an extra identifier in things like filenames and plot titles

activity_data = pd.read_excel('input_data/{}.xlsx'.format(data_title), sheet_name='ref_freight_tonne_km')
energy_data = pd.read_excel('input_data/{}.xlsx'.format(data_title), sheet_name='ref_freight_energy_pj')

structure_variable = 'Mode'#set to the name of the varaible that will be used to group the data by. noramlly, sector for industry data, mode for transport data
activity_variable = 'freight_tonne_km'#set to the name of the varaible that will be used for the activity data eg. gdp or passenger km or freight tonne km
energy_variable = 'PJ'#this will not often change

graph_title = 'Freight transport drivers of changes in energy use (Reference)'
emissions_divisia = False

run_divisia(data_title=data_title, extra_identifier=extra_identifier, activity_data=activity_data, energy_data=energy_data, structure_variable=structure_variable, activity_variable=activity_variable, emissions_variable = 'MtCO2', energy_variable = energy_variable, emissions_divisia = False, emissions_data=[], time_variable='Year')

plot_multiplicative(data_title, extra_identifier, emissions_divisia, time_variable='Year', structure_variable=structure_variable, graph_title = graph_title)
plot_additive(data_title, extra_identifier, emissions_divisia, time_variable='Year', structure_variable=structure_variable, graph_title = graph_title)
#%%

################################################
