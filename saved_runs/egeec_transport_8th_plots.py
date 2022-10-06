#the plotting code to go with egeec_transport_8th.py
#a copy of additive plotting in plot_output.py
#%%

import pandas as pd
import numpy as np

import plotly.express as px
pd.options.plotting.backend = "plotly"#set pandas backend to plotly plotting instead of matplotlib
import plotly.io as pio
pio.renderers.default = "browser"#allow plotting of graphs in the interactive notebook in vscode #or set to notebook
import plotly.graph_objects as go
import plotly
# %%
#create plotting funtion especailly for the EGEEC conference
#have the option of turning it into a function for emissions as well. 
def plot_additive_EGEEC_transport(data_title, extra_identifier, emissions_divisia, time_variable='Year', structure_variable='Sector', graph_title='', residual_variable1='Energy intensity', residual_variable2='Emissions intensity', font_size=18,y_axis_min=9000,y_axis_max=45000):
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

        base_amount = y_axis_min + 1000

        if graph_title == '':
            title = '{}{} - Additive LMDI'.format(data_title, extra_identifier)
        else:
            title = graph_title + ' - Additive LMDI'

        fig = go.Figure(go.Waterfall(
            orientation = "v",
            measure = ["absolute", "relative", "relative", "relative", "total"],
            base = base_amount,

            x = [str(beginning_year) + ' energy use',
            "Activity", structure_variable,residual_variable1,
            str(final_year)+' energy use'],

            textposition = "outside",

            # text = [int(add_plot_first_year_energy), 
            # str(int(add_plot["Activity"].round(0).iloc[0])), 
            # str(int(add_plot[structure_variable].round(0).iloc[0])),
            # str(int(add_plot["Energy intensity"].round(0).iloc[0])), 
            # str(int(add_plot["Energy"].round(0).iloc[0]))],

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
            ), waterfallgap = 0.01,
            yaxis=dict(range=[y_axis_min, y_axis_max]),
            yaxis_title="PJ",
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
        
        base_amount = add_plot_first_year_emissions/4

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

            # text = [int(add_plot_first_year_emissions), 
            # str(int(add_plot["Activity"].round(0).iloc[0])), 
            # str(int(add_plot[structure_variable].round(0).iloc[0])),
            # str(int(add_plot["Energy intensity"].round(0).iloc[0])), 
            # str(int(add_plot["Emissions intensity"].round(0).iloc[0])), 
            # str(int(add_plot["Emissions"].round(0).iloc[0]))],

            y = [add_plot_first_year_emissions-base_amount, 
            add_plot["Activity"].iloc[0],
            add_plot[structure_variable].iloc[0],
            add_plot["Energy intensity"].iloc[0],
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
            ), waterfallgap = 0.01#,
            #yaxis=dict(range=[y_axis_min, y_axis_max])
        )

        plotly.offline.plot(fig, filename='./plotting_output/' + data_title + extra_identifier + 'additive_waterfall.html')
        fig.write_image("./plotting_output/static/" + data_title + extra_identifier + 'additive_waterfall.png')
