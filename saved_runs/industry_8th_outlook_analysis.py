#%%
#run this file on energy data from the outlook for the purposes of the egeec meeting
#%%

import os
if os.getcwd().endswith('saved_runs'):
    os.chdir('../')#go abck one folder so we can access all the functions
elif os.getcwd().endswith('Github'):
    os.chdir('./PyLMDI/')
else:
    print('Somehow you are in this folder: ', os.getcwd())

import pandas as pd
import numpy as np
import data_creation_functions 
import LMDI_functions
from main_function import run_divisia
from plot_output import plot_multiplicative, plot_additive
#load data in

#%%
#import data from excel using a preset name for the data, which is also used for creating graph titles and genreally identifying outputs/inputs related to this dataset specifically

#load both datasets in one csv and separate them into two dataframes


activity_energy = pd.read_csv('input_data/industry_activity_energy_remapped.csv')

#sum up economys. and create a new df for each scenario
activity_energy = activity_energy.groupby(['GDP_category', 'scenario', 'year']).sum().reset_index()
#scenario split
activity_energy_ref = activity_energy[activity_energy['scenario'] == 'Reference']
activity_energy_cn = activity_energy[activity_energy['scenario'] == 'Carbon Neutral']

#create activity and enegry dataframes for each scenario
activity_ref = activity_energy_ref[['GDP_category', 'year', 'activity']]

energy_ref = activity_energy_ref[['GDP_category', 'year', 'energy']]

activity_cn = activity_energy_cn[['GDP_category', 'year', 'activity']]

energy_cn = activity_energy_cn[['GDP_category', 'year', 'energy']]

#make data wide so we ahve a column for each yeuar
activity_ref = activity_ref.pivot(index='GDP_category', columns='year', values='activity').reset_index()
energy_ref = energy_ref.pivot(index='GDP_category', columns='year', values='energy').reset_index()
activity_cn = activity_cn.pivot(index='GDP_category', columns='year', values='activity').reset_index()
energy_cn = energy_cn.pivot(index='GDP_category', columns='year', values='energy').reset_index()

#%%
data_title = 'outlook-industry-divisia'
extra_identifier = 'MIXED_UNITS_CN'#use this if you need the program to insert an extra identifier in things like filenames and plot titles

structure_variable = 'GDP_category'#set to the name of the varaible that will be used to group the data by. noramlly, sector for industry data, mode for transport data
activity_variable = 'Activity'#set to the name of the varaible that will be used for the activity data eg. gdp or passenger km or freight tonne km
energy_variable = 'PJ'#this will not often change

emissions_divisia = False

run_divisia(data_title=data_title, extra_identifier=extra_identifier, activity_data=activity_cn, energy_data=energy_cn, structure_variable=structure_variable, activity_variable=activity_variable, emissions_variable = 'MtCO2', energy_variable = energy_variable, emissions_divisia = False, emissions_data=[], time_variable='Year')

plot_multiplicative(data_title, extra_identifier, emissions_divisia, time_variable='Year', structure_variable=structure_variable)
plot_additive(data_title, extra_identifier, emissions_divisia, time_variable='Year', structure_variable=structure_variable)

#%%
data_title = 'outlook-industry-divisia'
extra_identifier = 'MIXED_UNITS_REF'#use this if you need the program to insert an extra identifier in things like filenames and plot titles

structure_variable = 'GDP_category'#set to the name of the varaible that will be used to group the data by. noramlly, sector for industry data, mode for transport data
activity_variable = 'Activity'#set to the name of the varaible that will be used for the activity data eg. gdp or passenger km or freight tonne km
energy_variable = 'PJ'#this will not often change

emissions_divisia = False

run_divisia(data_title=data_title, extra_identifier=extra_identifier, activity_data=activity_ref, energy_data=energy_ref, structure_variable=structure_variable, activity_variable=activity_variable, emissions_variable = 'MtCO2', energy_variable = energy_variable, emissions_divisia = False, emissions_data=[], time_variable='Year')

plot_multiplicative(data_title, extra_identifier, emissions_divisia, time_variable='Year', structure_variable=structure_variable)
plot_additive(data_title, extra_identifier, emissions_divisia, time_variable='Year', structure_variable=structure_variable)

#%%








