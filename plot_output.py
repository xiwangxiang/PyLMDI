#plot output
#aim to keep plots so they can handle any output from general_run but there will be somethings that need to be asdjusted easch time so we have many variables you can input
#if things get out of hand then suggest making a new function in a new file
#%%

import pandas as pd
import numpy as np

import plotly.express as px
pd.options.plotting.backend = "plotly"#set pandas backend to plotly plotting instead of matplotlib
import plotly.io as pio
pio.renderers.default = "browser"#allow plotting of graphs in the interactive notebook in vscode #or set to notebook
import plotly.graph_objects as go
import plotly
#%%
def plot_multiplicative(data_title, extra_identifier, emissions_divisia, time_variable='Year', structure_variable='Sector', graph_title='', residual_variable1='Energy intensity', residual_variable2='Emissions intensity', font_size=18):
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

        #remove the energy total from the data
        lmdi_output_multiplicative.drop('Energy', axis=1, inplace=True)
        #rename the energy intensity column to residual_variable1
        lmdi_output_multiplicative.rename(columns={'Energy intensity':residual_variable1}, inplace=True)
        #need to make the data in long format first:
        mult_plot = pd.melt(lmdi_output_multiplicative, id_vars=[time_variable], var_name='Driver', value_name='Value')
        
        #create category based on whether dfata is driver or change in erggy use
        mult_plot['Line type'] = mult_plot['Driver'].apply(lambda i: i if i == 'Change in energy' else 'Driver')
        #set title

        if graph_title == '':
            title = '{}{} - Multiplicative LMDI decomposition of energy use'.format(data_title, extra_identifier)
        else:
            title = graph_title + ' - Multiplicative LMDI decomposition of energy use'

        #plot
        fig = px.line(mult_plot, x=time_variable, y="Value", color="Driver", line_dash = 'Line type', title=title, category_orders={"Line type":['Change in energy', 'Driver'],"Driver":['Change in energy', 'Activity', structure_variable, 'Energy intensity']})#,

        fig.update_layout(
            font=dict(
                size=font_size
            )
        )

        plotly.offline.plot(fig, filename='./plotting_output/' + data_title + extra_identifier + 'multiplicative_timeseries.html')
        fig.write_image("./plotting_output/static/" + data_title + extra_identifier + 'multiplicative_timeseries.png')

    else:
        
        #get data
        lmdi_output_multiplicative = pd.read_csv('output_data/{}{}_lmdi_output_multiplicative.csv'.format(data_title, extra_identifier))

        #remove the Emissions total from the data
        lmdi_output_multiplicative.drop('Emissions', axis=1, inplace=True)
        #rename the energy intensity column to residual_variable1
        lmdi_output_multiplicative.rename(columns={'Energy intensity':residual_variable1}, inplace=True)
        #rename the emissions intensity column to residual_variable2
        lmdi_output_multiplicative.rename(columns={'Emissions intensity':residual_variable2}, inplace=True)

        #need to make the data in long format first:
        mult_plot = pd.melt(lmdi_output_multiplicative, id_vars=[time_variable], var_name='Driver', value_name='Value')
        
        #create category based on whether dfata is driver or change in erggy use
        mult_plot['Line type'] = mult_plot['Driver'].apply(lambda i: i if i == 'Change in emissions' else 'Driver')

        #set title
        if graph_title == '':
            title = '{}{} - Multiplicative LMDI decomposition of emissions'.format(data_title, extra_identifier)
        else:
            title = graph_title + '- Multiplicative LMDI decomposition of emissions'

        #plot
        fig = px.line(mult_plot, x=time_variable, y="Value", color="Driver", line_dash = 'Line type', title=title, category_orders={"Line type":['Change in emissions', 'Driver'],"Driver":['Change in emissions', 'Activity', structure_variable, 'Energy intensity', 'Emissions intensity']})#,
        fig.update_layout(
            font=dict(
                size=font_size
            )
        )
        plotly.offline.plot(fig, filename='./plotting_output/' + data_title + extra_identifier + 'multiplicative_timeseries.html')
        fig.write_image("./plotting_output/static/" + data_title + extra_identifier + 'multiplicative_timeseries.png')
    
#%%

def plot_additive(data_title, extra_identifier, emissions_divisia, time_variable='Year', structure_variable='Sector', graph_title='', residual_variable1='Energy intensity', residual_variable2='Emissions intensity', font_size=18):
    """
    data used by this function:
        
        data_title = 'outlook-transport-divisia'
        extra_identifier = 'PASSENGER_REF'
        lmdi_output_multiplicative = pd.read_csv('output_data/{}{}_lmdi_output_multiplicative.csv'.format(data_title, extra_identifier))
        lmdi_output_additive = pd.read_csv('output_data/{}{}_lmdi_output_additive.csv'.format(data_title, extra_identifier))

        emissions_divisia = False
    """
    if not emissions_divisia:
        
        lmdi_output_additive = pd.read_csv('output_data/{}{}_lmdi_output_additive.csv'.format(data_title, extra_identifier))

        #format data for additive plot
        #use the latest year, and the energy value for the first year
        beginning_year = lmdi_output_additive.Year.min()
        final_year = lmdi_output_additive.Year.max()
        add_plot_first_year_energy = lmdi_output_additive[lmdi_output_additive[time_variable] == beginning_year]['Energy'].values[0]
        add_plot = lmdi_output_additive[lmdi_output_additive[time_variable] == final_year]

        base_amount = add_plot_first_year_energy/4

        if graph_title == '':
            title = '{}{} - Additive LMDI decomposition'.format(data_title, extra_identifier)
        else:
            title = graph_title + ' - Additive LMDI decomposition'

        fig = go.Figure(go.Waterfall(
            orientation = "v",
            measure = ["absolute", "relative", "relative", "relative", "total"],
            base = base_amount,

            x = [str(beginning_year) + ' total energy use',
            "Activity", structure_variable,residual_variable1,
            str(final_year)+' total energy use'],

            textposition = "outside",

            text = [int(add_plot_first_year_energy), 
            str(int(add_plot["Activity"].round(0).iloc[0])), 
            str(int(add_plot[structure_variable].round(0).iloc[0])),
            str(int(add_plot["Energy intensity"].round(0).iloc[0])), 
            str(int(add_plot["Energy"].round(0).iloc[0]))],

            y = [add_plot_first_year_energy-base_amount, 
            add_plot["Activity"].iloc[0],
            add_plot[structure_variable].iloc[0],
            add_plot["Energy intensity"].iloc[0],
            add_plot["Energy"].iloc[0]],

            decreasing = {"marker":{"color":"#93C0AC"}},
            increasing = {"marker":{"color":"#EB9C98"}},
            totals = {"marker":{"color":"#11374A"}}
        ))

        fig.update_layout(
                title = title,
                font=dict(
                size=font_size
            ), waterfallgap = 0.01
        )

        plotly.offline.plot(fig, filename='./plotting_output/' + data_title + extra_identifier + 'additive_waterfall.html')
        fig.write_image("./plotting_output/static/" + data_title + extra_identifier + 'additive_waterfall.png')

    else:

        lmdi_output_additive = pd.read_csv('output_data/{}{}_lmdi_output_additive.csv'.format(data_title, extra_identifier))

        #format data for additive plot
        #use the latest year, and the energy value for the first year
        beginning_year = lmdi_output_additive.Year.min()
        final_year = lmdi_output_additive.Year.max()
        add_plot_first_year_emissions = lmdi_output_additive[lmdi_output_additive[time_variable] == beginning_year]['Emissions'].values[0]
        add_plot = lmdi_output_additive[lmdi_output_additive[time_variable] == final_year]
        
        base_amount = add_plot_first_year_energy/4

        if graph_title == '':
            title = '{}{} - Additive LMDI decomposition of emissions'.format(data_title, extra_identifier)
        else:
            title = graph_title + ' - Additive LMDI decomposition of emissions'


        fig = go.Figure(go.Waterfall(
            orientation = "v",
            measure = ["absolute", "relative", "relative", "relative", "relative", "total"],
            base = base_amount,

            x = [str(beginning_year) + ' total emissions', "Activity", structure_variable,"Energy intensity", "Emissions intensity",str(final_year)+' total emissions'],

            textposition = "outside",

            text = [int(add_plot_first_year_emissions), 
            str(int(add_plot["Activity"].round(0).iloc[0])), 
            str(int(add_plot[structure_variable].round(0).iloc[0])),
            str(int(add_plot["Energy intensity"].round(0).iloc[0])), 
            str(int(add_plot["Emissions intensity"].round(0).iloc[0])), 
            str(int(add_plot["Emissions"].round(0).iloc[0]))],

            y = [add_plot_first_year_emissions-base_amount, 
            add_plot["Activity"].iloc[0],
            add_plot[structure_variable].iloc[0],
            add_plot["Emissions intensity"].iloc[0],
            add_plot["Emissions"].iloc[0]],

            decreasing = {"marker":{"color":"#93C0AC"}},
            increasing = {"marker":{"color":"#EB9C98"}},
            totals = {"marker":{"color":"#11374A"}}
        ))

        fig.update_layout(
                title = title,
                font=dict(
                size=font_size
            ), waterfallgap = 0.01
        )

        plotly.offline.plot(fig, filename='./plotting_output/' + data_title + extra_identifier + 'additive_waterfall.html')
        fig.write_image("./plotting_output/static/" + data_title + extra_identifier + 'additive_waterfall.png')

#%%

