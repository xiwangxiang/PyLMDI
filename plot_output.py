#plot output
#aim to keep plots so they can handle any output from general_run but there will be somethings that need to be asdjusted easch time
#%%

import pandas as pd
import numpy as np

import plotly.express as px
pd.options.plotting.backend = "plotly"#set pandas backend to plotly plotting instead of matplotlib
import plotly.io as pio
pio.renderers.default = "browser"#allow plotting of graphs in the interactive notebook in vscode #or set to notebook


#%%
def plot_multiplicative(data_title, extra_identifier, emissions_divisia):
    """
    data used by this function:
        
        data_title = 'outlook-transport-divisia'
        extra_identifier = 'PASSENGER_REF'
        lmdi_output_multiplicative = pd.read_csv('output_data/{}{}_lmdi_output_multiplicative.csv'.format(data_title, extra_identifier))
        lmdi_output_additive = pd.read_csv('output_data/{}{}_lmdi_output_additive.csv'.format(data_title, extra_identifier))

        emissions_divisia = False
    """
    if not emissions_divisia:
        
        #get data
        lmdi_output_multiplicative = pd.read_csv('output_data/{}{}_lmdi_output_multiplicative.csv'.format(data_title, extra_identifier))
        lmdi_output_additive = pd.read_csv('output_data/{}{}_lmdi_output_additive.csv'.format(data_title, extra_identifier))

        #need to make the data in long format first:
        mult_plot = pd.melt(lmdi_output_multiplicative, id_vars=['Year'], var_name='Driver', value_name='Value')
        
        #create category based on whether dfata is driver or change in erggy use
        mult_plot['Line type'] = mult_plot['Driver'].apply(lambda i: i if i == 'Change in energy' else 'Driver')
        #set title
        title = '{}{} Drivers of changes in energy use'.format(data_title, extra_identifier)

        #plot
        fig2 = px.line(mult_plot, x="Year", y="Value", color="Driver", line_dash = 'Line type', title=title, category_orders={"Line type":['Change in energy', 'Driver'],"Driver":['Change in energy', 'Activity', 'Structure', 'Energy intensity']})#,

        import plotly
        plotly.offline.plot(fig2, filename='./plotting_output/' + title + 'multiplicative_timeseries.html')
        fig2.write_image("./plotting_output/static/" + title + 'multiplicative_timeseries.png')

    
#%%
def plot_additive(data_title, extra_identifier, emissions_divisia):
    """
    data used by this function:
        
        data_title = 'outlook-transport-divisia'
        extra_identifier = 'PASSENGER_REF'
        lmdi_output_multiplicative = pd.read_csv('output_data/{}{}_lmdi_output_multiplicative.csv'.format(data_title, extra_identifier))
        lmdi_output_additive = pd.read_csv('output_data/{}{}_lmdi_output_additive.csv'.format(data_title, extra_identifier))

        emissions_divisia = False
    """
    if not emissions_divisia:
        #try to find a way to plot the waterfall kind of  chart for the additive data
        #it will use the final years' data from the additive drivers data and the first and final years energy data divided by 1000 i think.
        #would be good to include options of choposing to plkot waterfalls between years making intervals betweeen first and last year. eg. 2020-2030-2040-2050
        print('to do. additive not done yet')

#%%