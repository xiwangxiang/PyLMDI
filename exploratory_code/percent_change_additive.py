#testing to see what the diff between percent change in additive vs multiplkicative results are and whether significiant:
#%%
import os
if os.getcwd().endswith('exploratory_code'):
    os.chdir('../')#go abck one folder so we can access all the functions
elif os.getcwd().endswith('Github'):
    os.chdir('./PyLMDI/')
else:
    print('Somehow you are in this folder: ', os.getcwd())


import pandas as pd
import numpy as np
import data_creation_functions

import plotly.express as px
pd.options.plotting.backend = "plotly"#set pandas backend to plotly plotting instead of matplotlib
import plotly.io as pio
pio.renderers.default = "browser"#allow plotting of graphs in the interactive notebook in vscode #or set to notebook

#load data in

#%%

data_title = 'outlook-transport-divisia'
extra_identifier = 'FREIGHT_REF'
lmdi_output_multiplicative = pd.read_csv('output_data/{}{}_lmdi_output_multiplicative.csv'.format(data_title, extra_identifier))
lmdi_output_additive = pd.read_csv('output_data/{}{}_lmdi_output_additive.csv'.format(data_title, extra_identifier))
energy_data = pd.read_excel('input_data/{}.xlsx'.format(data_title), sheet_name='ref_pass_energy_pj')
 
structure_variable = 'Mode'#set to the name of the varaible that will be used to group the data by. noramlly, sector for industry data, mode for transport data
activity_variable = 'freight_tonne_km'#set to the name of the varaible that will be used for the activity data eg. gdp or passenger km or freight tonne km
energy_variable = 'PJ'#this will not often change


#%%
# we will find it by doiung total enegry consumption in 2005 + additive in current year, divided by total energy consumption in 2005
lmdi_output_additive_percent_change = lmdi_output_additive.copy().set_index('Year')

#get energy datra in easy format
energy = data_creation_functions.energy(energy_data, structure_variable)
#sum up sectors for each year
energy_sum = energy.groupby(['Year'])[energy_variable].sum()
#get first year's energy value
energy_first_year = energy_sum.iloc[0]


#%%
#now we can calculate the percent change in energy use. 
#essentially just add and divide all vlaues by the first year's energy value
lmdi_output_additive_percent_change = lmdi_output_additive_percent_change.applymap(lambda x: (x+energy_first_year)/energy_first_year)

#%%
#now plot data against the data for multiplcative
#so first we before we join the datasets, we will format them ready for plotting, and so that the datasets can be differentiated:
lmdi_output_additive_percent_change_plot = pd.melt(lmdi_output_additive_percent_change.reset_index(), id_vars=['Year'], var_name='Driver', value_name='Value')
lmdi_output_additive_percent_change_plot['Dataset'] = 'Additive_percent_change'

mult_plot = pd.melt(lmdi_output_multiplicative, id_vars=['Year'], var_name='Driver', value_name='Value')
mult_plot['Dataset'] = 'Multiplicative'

plotting_df = pd.concat([lmdi_output_additive_percent_change_plot, mult_plot])


#%%

#set title
title = '{}{} Comparison of pertcent change and multiplicative lmdi output'.format(data_title,extra_identifier)

#plot
fig2 = px.line(plotting_df, x="Year", y="Value", color="Driver", line_dash = 'Dataset', title=title, category_orders={"Driver":['Change in energy', 'Activity', 'Structure', 'Energy intensity']})#,

import plotly
plotly.offline.plot(fig2, filename='./plotting_output/' + title + 'timeseries.html')
fig2.write_image("./plotting_output/static/" + title + 'timeseries.png')

#%%