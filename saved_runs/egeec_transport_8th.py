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
from plot_output import plot_multiplicative
from egeec_transport_8th_plots import plot_additive_EGEEC_transport


###########################################################################
#%%
#BY MODE:
MODE = True
if MODE:
    structure_variable = 'Vehicle Type'#set to the name of the varaible that will be used to group the data by. noramlly, sector for industry data, mode for transport data
    energy_variable = 'PJ'#this will not often change

    residual_variable1 = 'Residual efficiency'
    emissions_divisia = False
    data_title = 'outlook-transport-divisia'
    font_size=45   

    ############################################################################

    #import data from excel using a preset name for the data, which is also used for creating graph titles and genreally identifying outputs/inputs related to this dataset specifically
    data_title = 'outlook-transport-divisia'
    extra_identifier = 'PASSENGER_REF_MODE'#use this if you need the program to insert an extra identifier in things like filenames and plot titles

    activity_data = pd.read_csv('input_data/tranport_8th/transport_8th_road_ref_passenger_activity_wide_mode.csv')
    energy_data = pd.read_csv('input_data/tranport_8th/transport_8th_road_ref_passenger_energy_wide_mode.csv')

    activity_variable = 'passenger_km'#set to the name of the varaible that will be used for the activity data eg. gdp or passenger km or freight tonne km

    graph_title = 'Road passenger - Drivers of changes in energy use (Ref)'

    run_divisia(data_title=data_title, extra_identifier=extra_identifier, activity_data=activity_data, energy_data=energy_data, structure_variable=structure_variable, activity_variable=activity_variable, emissions_variable = 'MtCO2', energy_variable = energy_variable, emissions_divisia = emissions_divisia, emissions_data=[], time_variable='Year')

    #plot_multiplicative(data_title, extra_identifier, emissions_divisia, time_variable='Year', structure_variable=structure_variable, graph_title = graph_title, residual_variable1 = residual_variable1)
    plot_additive_EGEEC_transport(data_title, extra_identifier, emissions_divisia, time_variable='Year', structure_variable=structure_variable, graph_title = graph_title, residual_variable1 = residual_variable1,font_size=font_size)

    ############################################################################
    data_title = 'outlook-transport-divisia'
    extra_identifier = 'PASSENGER_CN_MODE'#use this if you need the program to insert an extra identifier in things like filenames and plot titles

    activity_data = pd.read_csv('input_data/tranport_8th/transport_8th_road_cn_passenger_activity_wide_mode.csv')
    energy_data = pd.read_csv('input_data/tranport_8th/transport_8th_road_cn_passenger_energy_wide_mode.csv')

    activity_variable = 'passenger_km'#set to the name of the varaible that will be used for the activity data eg. gdp or passenger km or freight tonne km

    graph_title = 'Road passenger - Drivers of changes in energy use (CN)'

    run_divisia(data_title=data_title, extra_identifier=extra_identifier, activity_data=activity_data, energy_data=energy_data, structure_variable=structure_variable, activity_variable=activity_variable, emissions_variable = 'MtCO2', energy_variable = energy_variable, emissions_divisia = emissions_divisia, emissions_data=[], time_variable='Year')

    #plot_multiplicative(data_title, extra_identifier, emissions_divisia, time_variable='Year', structure_variable=structure_variable, graph_title = graph_title, residual_variable1 = residual_variable1)
    plot_additive_EGEEC_transport(data_title, extra_identifier, emissions_divisia, time_variable='Year', structure_variable=structure_variable, graph_title = graph_title, residual_variable1 = residual_variable1,font_size=font_size)
    
    ############################################################################
    data_title = 'outlook-transport-divisia'
    extra_identifier = 'FREIGHT_REF_MODE'#use this if you need the program to insert an extra identifier in things like filenames and plot titles

    activity_data = pd.read_csv('input_data/tranport_8th/transport_8th_road_ref_freight_activity_wide_mode.csv')
    energy_data = pd.read_csv('input_data/tranport_8th/transport_8th_road_ref_freight_energy_wide_mode.csv')

    activity_variable = 'freight_tonne_km'#set to the name of the varaible that will be used for the activity data eg. gdp or passenger km or freight tonne km

    graph_title = 'Road freight - Drivers of changes in energy use (CN)'

    run_divisia(data_title=data_title, extra_identifier=extra_identifier, activity_data=activity_data, energy_data=energy_data, structure_variable=structure_variable, activity_variable=activity_variable, emissions_variable = 'MtCO2', energy_variable = energy_variable, emissions_divisia = emissions_divisia, emissions_data=[], time_variable='Year')

    #plot_multiplicative(data_title, extra_identifier, emissions_divisia, time_variable='Year', structure_variable=structure_variable, graph_title = graph_title, residual_variable1 = residual_variable1)
    plot_additive_EGEEC_transport(data_title, extra_identifier, emissions_divisia, time_variable='Year', structure_variable=structure_variable, graph_title = graph_title, residual_variable1 = residual_variable1,font_size=font_size)
    
    ############################################################################
    data_title = 'outlook-transport-divisia'
    extra_identifier = 'FREIGHT_CN_MODE'#use this if you need the program to insert an extra identifier in things like filenames and plot titles

    activity_data = pd.read_csv('input_data/tranport_8th/transport_8th_road_cn_freight_activity_wide_mode.csv')
    energy_data = pd.read_csv('input_data/tranport_8th/transport_8th_road_cn_freight_energy_wide_mode.csv')

    activity_variable = 'freight_tonne_km'#set to the name of the varaible that will be used for the activity data eg. gdp or passenger km or freight tonne km

    graph_title = 'Road freight - Drivers of changes in energy use (CN)'

    run_divisia(data_title=data_title, extra_identifier=extra_identifier, activity_data=activity_data, energy_data=energy_data, structure_variable=structure_variable, activity_variable=activity_variable, emissions_variable = 'MtCO2', energy_variable = energy_variable, emissions_divisia = emissions_divisia, emissions_data=[], time_variable='Year')

    #plot_multiplicative(data_title, extra_identifier, emissions_divisia, time_variable='Year', structure_variable=structure_variable, graph_title = graph_title, residual_variable1 = residual_variable1)
    plot_additive_EGEEC_transport(data_title, extra_identifier, emissions_divisia, time_variable='Year', structure_variable=structure_variable, graph_title = graph_title, residual_variable1 = residual_variable1,font_size=font_size)
    



###########################################################################
###########################################################################
#%%
#BY DRIVE:
DRIVE = True
if DRIVE:
    structure_variable = 'Engine type'#set to the name of the varaible that will be used to group the data by. noramlly, sector for industry data, mode for transport data
    energy_variable = 'PJ'#this will not often change

    residual_variable1 = 'Residual efficiency'
    emissions_divisia = False
    data_title = 'outlook-transport-divisia'
    font_size=45  

    ###########################################################################
    #import data from excel using a preset name for the data, which is also used for creating graph titles and genreally identifying outputs/inputs related to this dataset specifically
    extra_identifier = 'FREIGHT_CN'#use this if you need the program to insert an extra identifier in things like filenames and plot titles

    activity_data = pd.read_csv('input_data/tranport_8th/transport_8th_road_cn_freight_activity_wide.csv')
    energy_data = pd.read_csv('input_data/tranport_8th/transport_8th_road_cn_freight_energy_wide.csv')
    
    #change name of structure variable to structure_variable
    activity_data = activity_data.rename(columns={'Drive': structure_variable})
    energy_data = energy_data.rename(columns={'Drive': structure_variable})

    activity_variable = 'freight_tonne_km'#set to the name of the varaible that will be used for the activity data eg. gdp or passenger km or freight tonne km    
    
    graph_title = 'Road freight - Drivers of changes in energy use (CN)'

    run_divisia(data_title=data_title, extra_identifier=extra_identifier, activity_data=activity_data, energy_data=energy_data, structure_variable=structure_variable, activity_variable=activity_variable, emissions_variable = 'MtCO2', energy_variable = energy_variable, emissions_divisia = emissions_divisia, emissions_data=[], time_variable='Year')

    ##plot_multiplicative(data_title, extra_identifier, emissions_divisia, time_variable='Year', structure_variable=structure_variable, graph_title = graph_title, residual_variable1 = residual_variable1)
    plot_additive_EGEEC_transport(data_title, extra_identifier, emissions_divisia, time_variable='Year', structure_variable=structure_variable, graph_title = graph_title, residual_variable1 = residual_variable1,font_size=font_size)

    ###########################################################################

    #import data from excel using a preset name for the data, which is also used for creating graph titles and genreally identifying outputs/inputs related to this dataset specifically
    
    extra_identifier = 'FREIGHT_REF'#use this if you need the program to insert an extra identifier in things like filenames and plot titles

    activity_data = pd.read_csv('input_data/tranport_8th/transport_8th_road_ref_freight_activity_wide.csv')
    energy_data = pd.read_csv('input_data/tranport_8th/transport_8th_road_ref_freight_energy_wide.csv')

    #change name of structure variable to structure_variable
    activity_data = activity_data.rename(columns={'Drive': structure_variable})
    energy_data = energy_data.rename(columns={'Drive': structure_variable})

    activity_variable = 'freight_tonne_km'#set to the name of the varaible that will be used for the activity data eg. gdp or passenger km or freight tonne km
    
    graph_title = 'Road freight - Drivers of changes in energy use (Ref)'

    run_divisia(data_title=data_title, extra_identifier=extra_identifier, activity_data=activity_data, energy_data=energy_data, structure_variable=structure_variable, activity_variable=activity_variable, emissions_variable = 'MtCO2', energy_variable = energy_variable, emissions_divisia = emissions_divisia, emissions_data=[], time_variable='Year')

    ##plot_multiplicative(data_title, extra_identifier, emissions_divisia, time_variable='Year', structure_variable=structure_variable, graph_title = graph_title, residual_variable1 = residual_variable1)
    plot_additive_EGEEC_transport(data_title, extra_identifier, emissions_divisia, time_variable='Year', structure_variable=structure_variable, graph_title = graph_title, residual_variable1 = residual_variable1,font_size=font_size)

    ###########################################################################

    #import data from excel using a preset name for the data, which is also used for creating graph titles and genreally identifying outputs/inputs related to this dataset specifically
    extra_identifier = 'PASSENGER_REF'#use this if you need the program to insert an extra identifier in things like filenames and plot titles

    activity_data = pd.read_csv('input_data/tranport_8th/transport_8th_road_ref_passenger_activity_wide.csv')
    energy_data = pd.read_csv('input_data/tranport_8th/transport_8th_road_ref_passenger_energy_wide.csv')

    #change name of structure variable to structure_variable
    activity_data = activity_data.rename(columns={'Drive': structure_variable})
    energy_data = energy_data.rename(columns={'Drive': structure_variable})

    activity_variable = 'passenger_km'#set to the name of the varaible that will be used for the activity data eg. gdp or passenger km or freight tonne km

    graph_title = 'Road passenger - Drivers of changes in energy use (Ref)'

    run_divisia(data_title=data_title, extra_identifier=extra_identifier, activity_data=activity_data, energy_data=energy_data, structure_variable=structure_variable, activity_variable=activity_variable, emissions_variable = 'MtCO2', energy_variable = energy_variable, emissions_divisia = emissions_divisia, emissions_data=[], time_variable='Year')

    ##plot_multiplicative(data_title, extra_identifier, emissions_divisia, time_variable='Year', structure_variable=structure_variable, graph_title = graph_title, residual_variable1 = residual_variable1)
    plot_additive_EGEEC_transport(data_title, extra_identifier, emissions_divisia, time_variable='Year', structure_variable=structure_variable, graph_title = graph_title, residual_variable1 = residual_variable1,font_size=font_size)

    ###########################################################################

    #import data from excel using a preset name for the data, which is also used for creating graph titles and genreally identifying outputs/inputs related to this dataset specifically
    
    extra_identifier = 'PASSENGER_CN'#use this if you need the program to insert an extra identifier in things like filenames and plot titles

    activity_data = pd.read_csv('input_data/tranport_8th/transport_8th_road_cn_passenger_activity_wide.csv')
    energy_data = pd.read_csv('input_data/tranport_8th/transport_8th_road_cn_passenger_energy_wide.csv')

    #change name of structure variable to structure_variable
    activity_data = activity_data.rename(columns={'Drive': structure_variable})
    energy_data = energy_data.rename(columns={'Drive': structure_variable})

    activity_variable = 'passenger_km'#set to the name of the varaible that will be used for the activity data eg. gdp or passenger km or freight tonne km

    graph_title = 'Road passenger - Drivers of changes in energy use (CN)'

    run_divisia(data_title=data_title, extra_identifier=extra_identifier, activity_data=activity_data, energy_data=energy_data, structure_variable=structure_variable, activity_variable=activity_variable, emissions_variable = 'MtCO2', energy_variable = energy_variable, emissions_divisia = emissions_divisia, emissions_data=[], time_variable='Year')

    ##plot_multiplicative(data_title, extra_identifier, emissions_divisia, time_variable='Year', structure_variable=structure_variable, graph_title = graph_title, residual_variable1 = residual_variable1)
    plot_additive_EGEEC_transport(data_title, extra_identifier, emissions_divisia, time_variable='Year', structure_variable=structure_variable, graph_title = graph_title, residual_variable1 = residual_variable1, font_size=font_size)

#%%