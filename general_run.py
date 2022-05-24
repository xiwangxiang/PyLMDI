#%%
# from PyLMDI import PyLMDI
import pandas as pd
import numpy as np
import data_creation_functions 
import LMDI_functions
#load data in

#import gdp data from excel
gdp_data = pd.read_excel('input_data/divisia-test-input-data.xlsx', sheet_name='ind_sectoral_gdp')
energy_data = pd.read_excel('input_data/divisia-test-input-data.xlsx', sheet_name='ind_sectoral_pj')

emissions_divisia = False

#%%
if emissions_divisia:
    print('to do')
    #we will take in six diff data sets to insert into the divisia method
    #energy, activity, sturcture, energy intensity,fuel mix, emissions factor


else:
    #we are just taking in energy, activity, sturcture, energy intensity

    activity = data_creation_functions.activity(gdp_data)
    energy_intensity = data_creation_functions.energy_intensity(gdp_data, energy_data)
    structure = data_creation_functions.structure(gdp_data)

    energy = data_creation_functions.energy(energy_data)

    #merge all except energy (this makes it so that all dataframes are the same length when we sep them)
    activity_structure = pd.merge(structure,activity,on=['Year'], how='left')
    activity_structure_intensity = pd.merge(activity_structure, energy_intensity,on=['Year','Sector'], how='left')

    #now we will separate each measure and make them wide format, ready to be passed to the divisia method
    activity_wide = activity_structure_intensity[['Year','Sector','Total_GDP']]
    activity_wide = activity_wide.pivot(index='Sector', columns='Year', values='Total_GDP')

    structure_wide = activity_structure_intensity[['Year','Sector','Sectoral_share_of_gdp']]
    structure_wide = structure_wide.pivot(index='Sector', columns='Year', values='Sectoral_share_of_gdp')

    Energy_intensity_wide = activity_structure_intensity[['Year','Sector','Energy_intensity']]
    Energy_intensity_wide = Energy_intensity_wide.pivot(index='Sector', columns='Year', values='Energy_intensity')

    energy_wide = energy.pivot(index='Sector', columns='Year', values='PJ')

    ###################################

    #now calcualte the additive drivers usiung the input data
    activity_driver, energy_change = LMDI_functions.Add(activity_wide, energy_wide)
    
    structure_driver, energy_change = LMDI_functions.Add(structure_wide, energy_wide)
    
    energy_intensity_driver, energy_change = LMDI_functions.Add(Energy_intensity_wide, energy_wide)

    #concat all data together:
    lmdi_output_additive = pd.concat({'Activity': activity_driver, 'Structure': structure_driver, 'Energy intensity': energy_intensity_driver, 'Change in energy' : energy_change}, axis=1)


    #now calcualte the mult drivers usiung the input data
    activity_driver_mult, energy_change_mult = LMDI_functions.Mult(activity_wide, energy_wide)
    
    structure_driver_mult, energy_change_mult = LMDI_functions.Mult(structure_wide, energy_wide)
    
    energy_intensity_driver_mult, energy_change_mult = LMDI_functions.Mult(Energy_intensity_wide, energy_wide)
    
    #concat all data together:
    lmdi_output_multiplicative = pd.concat({'Activity': activity_driver_mult, 'Structure': structure_driver_mult, 'Energy intensity': energy_intensity_driver_mult, 'Change in energy' : energy_change_mult}, axis=1)
    
    #

#%%

#plot data

import plotly.express as px
pd.options.plotting.backend = "plotly"#set pandas backend to plotly plotting instead of matplotlib
import plotly.io as pio
pio.renderers.default = "browser"#allow plotting of graphs in the interactive notebook in vscode #or set to notebook

#need to make the data in long format first:
mult_plot = pd.melt(lmdi_output_multiplicative.reset_index(), id_vars=['Year'], var_name='Driver', value_name='Value')

#set title
title = 'Drivers of changes in energy use'

#plot
fig2 = px.line(mult_plot, x="Year", y="Value", color="Driver", line_dash = 'Driver', title=title, category_orders={"Driver":['Change in energy', 'Activity', 'Structure', 'Energy intensity']})#,

import plotly
plotly.offline.plot(fig2, filename='./plotting_output/' + title + '.html')
fig2.write_image("./plotting_output/static/" + title + '.png')

#%%