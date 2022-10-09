#plot output
#aim to keep plots so they can handle any output from general_run but there will be somethings that need to be asdjusted easch time so we have many variables you can input
#if things get out of hand then suggest making a new function in a new file
#%%

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
def plot_multiplicative_timeseries(data_title, extra_identifier, structure_variables_list,activity_variable,energy_variable='Energy', emissions_variable='Emissions',emissions_divisia=False, time_variable='Year', graph_title='', residual_variable1='Energy intensity', residual_variable2='Emissions intensity', font_size=25,AUTO_OPEN=False):
    """
    data used by this function:
        
        data_title eg. 'outlook-transport-divisia'
        extra_identifier eg. 'PASSENGER_REF'
        lmdi_output_multiplicative eg. pd.read_csv('output_data/{}{}_lmdi_output_multiplicative.csv'.format(data_title, extra_identifier))
        lmdi_output_additive = pd.read_csv('output_data/{}{}_lmdi_output_additive.csv'.format(data_title, extra_identifier))
        emissions_divisia eg. False
        structure_variables_list eg. ['Economy','Vehicle Type', 'Drive']
        graph_title eg. 'Road passenger - Drivers of changes in energy use (Ref)'
        residual_variable1 eg. 'Energy intensity' - this can be used to make the residual variable a bit more explanatory
        residual_variable2 eg. 'Emissions intensity' - this can be used to make the residual variable a bit more explanatory
    """
    if not emissions_divisia:
        
        #get data
        lmdi_output_multiplicative = pd.read_csv('output_data/{}{}_lmdi_output_multiplicative.csv'.format(data_title, extra_identifier))

        #remove activity and total energy data from the dataset
        lmdi_output_multiplicative.drop('Total_{}'.format(activity_variable), axis=1, inplace=True)
        lmdi_output_multiplicative.drop('Total {}'.format(energy_variable), axis=1, inplace=True)

        #rename the energy intensity column to residual_variable1
        lmdi_output_multiplicative.rename(columns={'{} intensity'.format(energy_variable):residual_variable1}, inplace=True)
        
        #need to make the data in long format so we have a driver column instead fo a column for each driver:
        mult_plot = pd.melt(lmdi_output_multiplicative, id_vars=[time_variable], var_name='Driver', value_name='Value')

        #create category based on whether data is driver or change in energy use
        mult_plot['Line type'] = mult_plot['Driver'].apply(lambda i: i if i == 'Percent change in {}'.format(energy_variable) else 'Driver')
        #set title

        if graph_title == '':
            title = '{}{} - Multiplicative LMDI decomposition of energy use'.format(data_title, extra_identifier)
        else:
            title = graph_title + ' - Multiplicative LMDI decomposition of energy use'

        #plot
        fig = px.line(mult_plot, x=time_variable, y="Value", color="Driver", line_dash = 'Line type', title=title, category_orders={"Line type":['Percent change in {}'.format(energy_variable), 'Driver'],"Driver":['Percent change in {}'.format(energy_variable), 'Activity']+structure_variables_list+[residual_variable1]})#,

        fig.update_layout(
            font=dict(
                size=font_size
            )
        )

        plotly.offline.plot(fig, filename='./plotting_output/' + data_title + extra_identifier + 'multiplicative_timeseries.html', auto_open=AUTO_OPEN)
        fig.write_image("./plotting_output/static/" + data_title + extra_identifier + 'multiplicative_timeseries.png')

    else:
        
        #get data
        lmdi_output_multiplicative = pd.read_csv('output_data/{}{}_lmdi_output_multiplicative.csv'.format(data_title, extra_identifier))

        #remove ' effect' where it is at the end of all column names using regex ($ marks the end of the string)
        lmdi_output_multiplicative.columns = lmdi_output_multiplicative.columns.str.replace(' effect$', '')

        #remove activity and total energy/emissions data from the dataset
        lmdi_output_multiplicative.drop('Total_{}'.format(activity_variable), axis=1, inplace=True)
        lmdi_output_multiplicative.drop('Total {}'.format(energy_variable), axis=1, inplace=True)
        lmdi_output_multiplicative.drop('Total {}'.format(emissions_variable), axis=1, inplace=True)

        #rename the energy intensity column to residual_variable1
        lmdi_output_multiplicative.rename(columns={'{} intensity'.format(energy_variable):residual_variable1}, inplace=True)
        #rename the emissions intensity column to residual_variable2
        lmdi_output_multiplicative.rename(columns={'{} intensity'.format(emissions_variable):residual_variable2}, inplace=True)

        #need to make the data in long format first:
        mult_plot = pd.melt(lmdi_output_multiplicative, id_vars=[time_variable], var_name='Driver', value_name='Value')
        
        #create category based on whether dfata is driver or change in erggy use
        mult_plot['Line type'] = mult_plot['Driver'].apply(lambda i: i if i == 'Percent change in {}'.format(emissions_variable) else 'Driver')

        #set title
        if graph_title == '':
            title = '{}{} - Multiplicative LMDI decomposition of emissions'.format(data_title, extra_identifier)
        else:
            title = graph_title + '- Multiplicative LMDI decomposition of emissions'

        #plot
        fig = px.line(mult_plot, x=time_variable, y="Value", color="Driver", line_dash = 'Line type', title=title, category_orders={"Line type":['Change in {}'.format(emissions_variable), 'Driver'],"Driver":['Percent change in {}'.format(emissions_variable), 'Activity']+structure_variables_list+[residual_variable1, residual_variable2]})

        fig.update_layout(
            font=dict(
                size=font_size
            )
        )
        plotly.offline.plot(fig, filename='./plotting_output/' + data_title + extra_identifier + 'multiplicative_timeseries.html',auto_open=AUTO_OPEN)
        fig.write_image("./plotting_output/static/" + data_title + extra_identifier + 'multiplicative_timeseries.png')
    
#%%
######################################################
######################################################


def plot_additive_waterfall(data_title, extra_identifier, structure_variables_list, activity_variable,energy_variable='Energy', emissions_variable='Emissions',emissions_divisia=False, time_variable='Year', graph_title='', residual_variable1='Energy intensity', residual_variable2='Emissions intensity', font_size=25,y_axis_min_percent_decrease=0.9,AUTO_OPEN=False):
    """
    data used by this function:
        
        data_title eg. 'outlook-transport-divisia'
        extra_identifier eg. 'PASSENGER_REF'
        lmdi_output_multiplicative eg. pd.read_csv('output_data/{}{}_lmdi_output_multiplicative.csv'.format(data_title, extra_identifier))
        lmdi_output_additive = pd.read_csv('output_data/{}{}_lmdi_output_additive.csv'.format(data_title, extra_identifier))
        emissions_divisia eg. False
        structure_variables_list eg. ['Economy','Vehicle Type', 'Drive']
        graph_title eg. 'Road passenger - Drivers of changes in energy use (Ref)'
        residual_variable1 eg. 'Energy intensity' - this can be used to make the residual variable a bit more explanatory
        residual_variable2 eg. 'Emissions intensity' - this can be used to make the residual variable a bit more explanatory
    """
    if not emissions_divisia:
        
        lmdi_output_additive = pd.read_csv('output_data/{}{}_lmdi_output_additive.csv'.format(data_title, extra_identifier))

        #remove activity data from the dataset
        lmdi_output_additive.drop('Total_{}'.format(activity_variable), axis=1, inplace=True)

        #remove ' effect' where it is at the end of all column names using regex ($ marks the end of the string)
        lmdi_output_additive.columns = lmdi_output_additive.columns.str.replace(' effect$', '')
        
        #format data for waterfall plot
        #use the latest year, and the energy value for the first year
        beginning_year = lmdi_output_additive.Year.min()
        final_year = lmdi_output_additive.Year.max()
        add_plot_first_year_energy = lmdi_output_additive[lmdi_output_additive[time_variable] == beginning_year]['Total {}'.format(energy_variable)].values[0]
        add_plot = lmdi_output_additive[lmdi_output_additive[time_variable] == final_year]

        #set where the base for the y axis of the graph will begin 
        base_amount =  add_plot_first_year_energy * y_axis_min_percent_decrease
        #create a 'relative' vlaue  in the list for each driver in the dataset. to count the number of drivers, we can use the number of structure variables + 2 (activity and 2xresidual)
        measure_list = ['absolute'] + ['relative'] * (len(structure_variables_list) + 2) + ['total']

        if graph_title == '':
            title = '{}{} - Additive LMDI'.format(data_title, extra_identifier)
        else:
            title = graph_title + ' - Additive LMDI'

        y = [add_plot_first_year_energy-base_amount, 
        add_plot[activity_variable].iloc[0]] + add_plot[structure_variables_list].iloc[0].tolist() + [add_plot[residual_variable1].iloc[0],
        add_plot["Total {}".format(energy_variable)].iloc[0]]
        x = [str(beginning_year) + ' {}'.format(energy_variable),
        activity_variable] + structure_variables_list + [residual_variable1,
        str(final_year)+' {}'.format(energy_variable)]

        fig = go.Figure(go.Waterfall(
            orientation = "v",
            measure = measure_list,
            base = base_amount,

            x = [str(beginning_year) + ' {}'.format(energy_variable),
            activity_variable] + structure_variables_list + [residual_variable1,
            str(final_year)+' {}'.format(energy_variable)],

            textposition = "outside",

            #can add text to the waterfall plot here to show the values of the drivers
            # text = [int(add_plot_first_year_energy), 
            # str(int(add_plot["Activity"].round(0).iloc[0])), 
            # str(int(add_plot[structure_variable].round(0).iloc[0])),
            # str(int(add_plot["Energy intensity"].round(0).iloc[0])), 
            # str(int(add_plot["Energy"].round(0).iloc[0]))],

            y = [add_plot_first_year_energy-base_amount, 
            add_plot[activity_variable].iloc[0]] + add_plot[structure_variables_list].iloc[0].tolist() + [add_plot[residual_variable1].iloc[0],
            add_plot["Total {}".format(energy_variable)].iloc[0]],

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

        plotly.offline.plot(fig, filename='./plotting_output/' + data_title + extra_identifier + 'additive_waterfall.html',auto_open=AUTO_OPEN)
        fig.write_image("./plotting_output/static/" + data_title + extra_identifier + 'additive_waterfall.png')

    else:
        #this is for emissions plot:
        lmdi_output_additive = pd.read_csv('output_data/{}{}_lmdi_output_additive.csv'.format(data_title, extra_identifier))

        #remove activity data from the dataset
        lmdi_output_additive.drop('Total_{}'.format(activity_variable), axis=1, inplace=True)
        #remove total energy data from the dataset
        lmdi_output_additive.drop('Total {}'.format(energy_variable), axis=1, inplace=True)

        #remove ' effect' where it is at the end of all column names using regex ($ marks the end of the string)
        lmdi_output_additive.columns = lmdi_output_additive.columns.str.replace(' effect$', '')

        #format data for waterfall plot
        #use the latest year, and the energy value for the first year
        beginning_year = lmdi_output_additive.Year.min()
        final_year = lmdi_output_additive.Year.max()
        add_plot_first_year_emissions = lmdi_output_additive[lmdi_output_additive[time_variable] == beginning_year]['Total {}'.format(emissions_variable)].values[0]
        add_plot = lmdi_output_additive[lmdi_output_additive[time_variable] == final_year]

        #set where the base for the y axis of the graph will begin 
        base_amount =  add_plot_first_year_emissions * y_axis_min_percent_decrease
        #create a 'relative' vlaue  in the list for each driver in the dataset. to count the number of drivers, we can use the number of structure variables + 2 (activity and 2xresidual)
        measure_list = ['absolute'] + ['relative'] * (len(structure_variables_list) + 3) + ['total']

        if graph_title == '':
            title = '{}{} - Additive LMDI'.format(data_title, extra_identifier)
        else:
            title = graph_title + ' - Additive LMDI'

        fig = go.Figure(go.Waterfall(
            orientation = "v",
            measure = measure_list,
            base = base_amount,

            x = [str(beginning_year) + ' {}'.format(emissions_variable),
            activity_variable] + structure_variables_list + [residual_variable1,residual_variable2,
            str(final_year)+' {}'.format(emissions_variable)],

            textposition = "outside",

            #can add text to the waterfall plot here to show the values of the drivers
            # text = [int(add_plot_first_year_energy), 
            # str(int(add_plot["Activity"].round(0).iloc[0])), 
            # str(int(add_plot[structure_variable].round(0).iloc[0])),
            # str(int(add_plot["Energy intensity"].round(0).iloc[0])), 
            # str(int(add_plot["Energy"].round(0).iloc[0]))],

            y = [add_plot_first_year_emissions-base_amount, 
            add_plot[activity_variable].iloc[0]] + add_plot[structure_variables_list].iloc[0].tolist() + [add_plot[residual_variable1].iloc[0], 
            add_plot[residual_variable2].iloc[0],
            add_plot["Total {}".format(emissions_variable)].iloc[0]-base_amount],

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

        plotly.offline.plot(fig, filename='./plotting_output/' + data_title + extra_identifier + 'additive_waterfall.html',auto_open=AUTO_OPEN)
        fig.write_image("./plotting_output/static/" + data_title + extra_identifier + 'additive_waterfall.png')


##%%

