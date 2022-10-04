#attempt to analyse the data from the 8th edition of the outlook. so the data can be energy use or emissions out to 2050, by sector, and the activity data will be gdp, by sector.

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
from plot_output import plot_multiplicative#, plot_additive
#load data in

#%%

#import data from excel using a preset name for the data, which is also used for creating graph titles and genreally identifying outputs/inputs related to this dataset specifically
data_title = 'energy-outlook-8th-divisia'
extra_identifier = 'ENERGY'#use this if you need the program to insert an extra identifier in things like filenames and plot titles

    activity_data = pd.read_excel('input_data/{}.xlsx'.format(data_title), sheet_name='ref_p_km')
    energy_data = pd.read_excel('input_data/{}.xlsx'.format(data_title), sheet_name='ref_pass_energy_pj')

structure_variable = 'Sector'#set to the name of the varaible that will be used to group the data by. noramlly, sector for industry data, mode for transport data
activity_variable = 'GDP'#set to the name of the varaible that will be used for the activity data eg. gdp or passenger km or freight tonne km
energy_variable = 'PJ'#this will not often change

emissions_divisia = False

run_divisia(data_title, extra_identifier, activity_data, energy_data, emissions_divisia,structure_variable,activity_variable, energy_variable)

plot_multiplicative(data_title, extra_identifier, emissions_divisia)
#plot_additive(data_title, extra_identifier, emissions_divisia)



#%%

#import data from excel using a preset name for the data, which is also used for creating graph titles and genreally identifying outputs/inputs related to this dataset specifically
data_title = 'emissions-outlook-8th-divisia'
extra_identifier = 'EMISSIONS'#use this if you need the program to insert an extra identifier in things like filenames and plot titles

    activity_data = pd.read_excel('input_data/{}.xlsx'.format(data_title), sheet_name='ref_p_km')
    energy_data = pd.read_excel('input_data/{}.xlsx'.format(data_title), sheet_name='ref_pass_energy_pj')
    emissions_data = pd.read_excel('input_data/{}.xlsx'.format(data_title), sheet_name='ref_pass_energy_pj')


structure_variable = 'Sector'#set to the name of the varaible that will be used to group the data by. noramlly, sector for industry data, mode for transport data
activity_variable = 'GDP'#set to the name of the varaible that will be used for the activity data eg. gdp or passenger km or freight tonne km

emissions_variable = 'MtCO2'#this will not often change
energy_variable = 'PJ'
emissions_divisia = True

run_divisia(data_title, extra_identifier, activity_data, energy_data, structure_variable, activity_variable, emissions_variable, energy_variable, emissions_divisia, emissions_data)

plot_multiplicative(data_title, extra_identifier, emissions_divisia)
#plot_additive(data_title, extra_identifier, emissions_divisia)