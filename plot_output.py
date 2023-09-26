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
def plot_multiplicative_timeseries(data_title, extra_identifier, structure_variables_list,activity_variable,energy_variable='Energy', emissions_variable='Emissions',emissions_divisia=False, time_variable='Year', graph_title='', residual_variable1='Energy intensity', residual_variable2='Emissions intensity', font_size=25,AUTO_OPEN=False, hierarchical=False,output_data_folder='output_data',plotting_output_folder='./plotting_output/'):
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
    if emissions_divisia == False and hierarchical == False:
        
        #get data
        lmdi_output_multiplicative = pd.read_csv('{}/{}{}_lmdi_output_multiplicative.csv'.format(output_data_folder,data_title, extra_identifier))

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
            title = '{}{} - Multiplicative LMDI'.format(data_title, extra_identifier)
        else:
            title = graph_title + ' - Multiplicative LMDI'

        #plot
        fig = px.line(mult_plot, x=time_variable, y="Value", color="Driver", line_dash = 'Line type', title=title, category_orders={"Line type":['Percent change in {}'.format(energy_variable), 'Driver'],"Driver":['Percent change in {}'.format(energy_variable), 'Activity']+structure_variables_list+[residual_variable1]})#,

        fig.update_layout(
            font=dict(
                size=font_size
            )
        )

        plotly.offline.plot(fig, filename=plotting_output_folder + data_title + extra_identifier + 'multiplicative_timeseries.html', auto_open=AUTO_OPEN)
        #fig.write_image("./plotting_output/static/" + data_title + extra_identifier + 'multiplicative_timeseries.png')

    elif emissions_divisia == True and hierarchical == False:
        
        #get data
        lmdi_output_multiplicative = pd.read_csv('output_data/{}{}_lmdi_output_multiplicative.csv'.format(data_title, extra_identifier))

        #remove ' effect' where it is at the end of all column names using regex ($ marks the end of the string)
        lmdi_output_multiplicative.columns = lmdi_output_multiplicative.columns.str.replace(' effect$', '', regex=True)

        #remove activity and total energy/emissions data from the dataset
        lmdi_output_multiplicative.drop('Total_{}'.format(activity_variable), axis=1, inplace=True)
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
        plotly.offline.plot(fig, filename=plotting_output_folder + data_title + extra_identifier + 'multiplicative_timeseries.html',auto_open=AUTO_OPEN)
        #fig.write_image("./plotting_output/static/" + data_title + extra_identifier + 'multiplicative_timeseries.png')
    
    elif emissions_divisia == False and hierarchical == True:
                
        #get data
        lmdi_output_multiplicative = pd.read_csv('{}/{}{}_hierarchical_multiplicative_output.csv'.format(output_data_folder,data_title, extra_identifier))

        #Regardless of the column names, rename data in order of, 'Year', activity_variable, structure_variables_list, residual_variable1, 'Percent change in {}'.format(energy_variable)
        lmdi_output_multiplicative.columns = [time_variable, activity_variable] + structure_variables_list + [residual_variable1, 'Percent change in {}'.format(energy_variable)]

        #create list of driver names in the order we want them to appear in the graph
        driver_list = [activity_variable] + structure_variables_list + [residual_variable1]

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
        fig = px.line(mult_plot, x=time_variable, y="Value", color="Driver", line_dash = 'Line type',  category_orders={"Line type":['', ' '],"Driver":['Percent change in {}'.format(energy_variable)]+driver_list},title=title)#,

        fig.update_layout(
            font=dict(
                size=font_size
            ),legend_title_text='Line/Driver')
        #set name of y axis to 'Proportional effect on energy use'
        fig.update_yaxes(title_text='Proportional effect on energy use')

        plotly.offline.plot(fig, filename=plotting_output_folder + data_title + extra_identifier + 'multiplicative_timeseries.html', auto_open=AUTO_OPEN)
        #fig.write_image("./plotting_output/static/" + data_title + extra_identifier + 'multiplicative_timeseries.png')


    
#%%
######################################################
######################################################


def plot_additive_waterfall(data_title, extra_identifier, structure_variables_list, activity_variable,energy_variable='Energy', emissions_variable='Emissions',emissions_divisia=False, time_variable='Year', graph_title='', residual_variable1='Energy intensity', residual_variable2='Emissions intensity', font_size=25,y_axis_min_percent_decrease=0.9,AUTO_OPEN=False, hierarchical=False, output_data_folder='output_data', plotting_output_folder='plotting_output'):
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
    if emissions_divisia == False and hierarchical == False:
        
        lmdi_output_additive = pd.read_csv('{}/{}{}_lmdi_output_additive.csv'.format(output_data_folder,data_title, extra_identifier))

        #remove activity data from the dataset
        lmdi_output_additive.drop('Total_{}'.format(activity_variable), axis=1, inplace=True)

        #remove ' effect' where it is at the end of all column names using regex ($ marks the end of the string)
        lmdi_output_additive.columns = lmdi_output_additive.columns.str.replace(' effect$', '', regex=True)
        
        #replace 'Energy intensity' with residual_variable1
        lmdi_output_additive.columns = lmdi_output_additive.columns.str.replace('Energy intensity', residual_variable1)

        #format data for waterfall plot
        #use the latest year, and the energy value for the first year
        beginning_year = lmdi_output_additive[time_variable].min()
        final_year = lmdi_output_additive[time_variable].max()
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

        plotly.offline.plot(fig, filename=plotting_output_folder + data_title + extra_identifier + 'additive_waterfall.html',auto_open=AUTO_OPEN)
        #fig.write_image("./plotting_output/static/" + data_title + extra_identifier + 'additive_waterfall.png')

    elif emissions_divisia  == True and hierarchical == False:
        #this is for emissions plot:
        lmdi_output_additive = pd.read_csv('{}/{}{}_lmdi_output_additive.csv'.format(output_data_folder,data_title, extra_identifier))

        #remove activity data from the dataset
        lmdi_output_additive.drop('Total_{}'.format(activity_variable), axis=1, inplace=True)

        #remove ' effect' where it is at the end of all column names using regex ($ marks the end of the string)
        lmdi_output_additive.columns = lmdi_output_additive.columns.str.replace(' effect$', '', regex=True)

        #replace 'Energy intensity' with residual_variable1
        lmdi_output_additive.columns = lmdi_output_additive.columns.str.replace('Energy intensity', residual_variable1)
        #replace 'Emissions intensity' with residual_variable2
        lmdi_output_additive.columns = lmdi_output_additive.columns.str.replace('Emissions intensity', residual_variable2)
        
        #format data for waterfall plot
        #use the latest year, and the energy value for the first year
        beginning_year = lmdi_output_additive[time_variable].min()
        final_year = lmdi_output_additive[time_variable].max()
        
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

        plotly.offline.plot(fig, filename=plotting_output_folder + data_title + extra_identifier + 'additive_waterfall.html',auto_open=AUTO_OPEN)
        #fig.write_image("./plotting_output/static/" + data_title + extra_identifier + 'additive_waterfall.png')

    elif emissions_divisia == False and hierarchical == True:
        print('Please note that the hierarchical LMDI method only produces a multiplicative output. So the output will be a multiplicative waterfall plot.')
        
        #get data
        lmdi_output_multiplicative = pd.read_csv('{}/{}{}_hierarchical_multiplicative_output.csv'.format(output_data_folder,data_title, extra_identifier))

        #Regardless of the column names, rename data in order of, 'Year', activity_variable, structure_variables_list, residual_variable1, 'Percent change in {}'.format(energy_variable)
        lmdi_output_multiplicative.columns = [time_variable, activity_variable] + structure_variables_list + [residual_variable1, 'Percent change in {}'.format(energy_variable)]

        #filter data to only include the final year
        lmdi_output_multiplicative = lmdi_output_multiplicative[lmdi_output_multiplicative[time_variable] == lmdi_output_multiplicative[time_variable].max()]
        # #create list of driver names in the order we want them to appear in the graph
        # driver_list = [activity_variable] + structure_variables_list + [residual_variable1]

        # #need to make the data in long format so we have a driver column instead fo a column for each driver:
        # mult_plot = pd.melt(lmdi_output_multiplicative, id_vars=[time_variable], var_name='Driver', value_name='Value')

        # #create category based on whether data is driver or change in energy use. because we dont want it to show in the graph we will just make driver a double space, and the change in enegry a singel space
        # mult_plot['Line type'] = mult_plot['Driver'].apply(lambda i: '' if i == 'Percent change in {}'.format(energy_variable) else ' ')
        
        #rename to add_plot to make it easier to copy and paste code
        add_plot = lmdi_output_multiplicative.copy()
        #remove ' effect' where it is at the end of all column names using regex ($ marks the end of the string)
        add_plot.columns = add_plot.columns.str.replace(' effect$', '', regex=True)
        
        #create a 'relative' vlaue  in the list for each driver in the dataset. to count the number of drivers, we can use the number of structure variables + 2 (activity and residual)
        measure_list = ['relative'] * (len(structure_variables_list) + 2) + ['total']

        if graph_title == '':
            title = '{}{} - Multiplicative LMDI'.format(data_title, extra_identifier)
        else:
            title = graph_title + ' - Multiplicative LMDI'

        y = [add_plot[activity_variable].iloc[0]] + add_plot[structure_variables_list].iloc[0].tolist() + [add_plot[residual_variable1].iloc[0],
        add_plot["Percent change in {}".format(energy_variable)].iloc[0]]
        #minus 1 from all values in the list to make them relative to 0
        y = [i-1 for i in y]
        x = [activity_variable] + structure_variables_list + [residual_variable1,'Percent change in {}'.format(energy_variable)]

        fig = go.Figure(go.Bar(
            orientation = "v",
            #measure = measure_list,
            # base = base_amount,

            x = x,

            textposition = "outside",

            #can add text to the waterfall plot here to show the values of the drivers
            # text = [int(add_plot_first_year_energy), 
            # str(int(add_plot["Activity"].round(0).iloc[0])), 
            # str(int(add_plot[structure_variable].round(0).iloc[0])),
            # str(int(add_plot["Energy intensity"].round(0).iloc[0])), 
            # str(int(add_plot["Energy"].round(0).iloc[0]))],

            y = y,

            # decreasing = {"marker":{"color":"#93C0AC"}},
            # increasing = {"marker":{"color":"#EB9C98"}},
            # totals = {"marker":{"color":"#11374A"}}
            #color bars based on their x axis value. if the x axis value is 'Percent change in {}'.format(energy_variable) then make it "#11374A", otherwise if the y axis value is positive make it "#EB9C98" and if its negative make it "#93C0AC"
            marker_color = ["#11374A" if i == 'Percent change in {}'.format(energy_variable) else "#EB9C98" if j > 0 else "#93C0AC" for i,j in zip(x,y)]            

        ))
        dotted_line_index = len(x) - 1.5
        fig.update_layout(
                title = title,
                font=dict(
                size=font_size
            ), waterfallgap = 0.01,
            #create dotted line between residual and percent change in energy use
            shapes = [ dict( type = 'line', x0 = dotted_line_index, y0 = -1, x1 = dotted_line_index, y1 = 1, xref = 'x', yref = 'y', line = dict( color = 'black', width = 1, dash = 'dot' ) ) ]
        )

        plotly.offline.plot(fig, filename=plotting_output_folder + data_title + extra_identifier + 'multiplicative_waterfall.html',auto_open=AUTO_OPEN)
        #fig.write_image("./plotting_output/static/" + data_title + extra_identifier + 'multiplicative_waterfall.png')
##%%

