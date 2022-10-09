#The details on the LMDI method which is quite complicated can be found here: https://drive.google.com/file/d/1wCd-S55JVrHoQwRV7w9qZSVxTlfiqGa8/view?usp=sharing
#in all of the following functions we use the term energy but it can also be emissions, as that capacbiltiy has been built into the code.
#also the term driver is used. It represents the effect, such as activity effect, structural effect and energy intensity effect. It can also be emissions intensity effect, as that capacity has been built into the code.
import pandas as pd
import numpy as np
import re
def Mult(driver_input_data, energy_data, drivers_list, structure_variables_list,energy_variable,time_variable,activity_variable):#driver_input_data, energy):
    #This will carry out the LMDI-I formula for the multiplicative case. The formula is: exp(sum((log(energy_t/energy_base_year)/log(sum(energy_t)/sum(energy_base_year))) * log(mean(energy_t/energy_base_year)) * log(driver_t/driver_base_year)))
    #note that where the word energy is used in names, it can be swapped out for emissions. Although any changes to columns names occurs outside this function.
    
    #PREP DATA:
    #prep driver data
    #get base year from data
    base_year = driver_input_data[time_variable].min()
    driver_base_year  =  driver_input_data.loc[driver_input_data[time_variable] == base_year]
    driver_t = driver_input_data.loc[driver_input_data[time_variable] != base_year]
    #merge base year driver value onto non base year data, so we can subtract it from the other years
    driver_df = pd.merge(driver_t, driver_base_year, on=structure_variables_list, how='left', suffixes=('', '_base_year'))
    #drop base year time variable
    driver_df = driver_df.drop(columns=time_variable+'_base_year')

    #prep energy data
    #get base year from data
    base_year = energy_data[time_variable].min()
    #separate data by base year and other years
    energy_base_year = energy_data.loc[energy_data[time_variable] == base_year]
    energy_year_t = energy_data.loc[energy_data[time_variable] != base_year]
    #merge base year energy value onto non base year data, so we can subtract it from the other years
    energy_df_top = pd.merge(energy_year_t, energy_base_year, on=structure_variables_list, how='left', suffixes=('', '_base_year'))
    #drop base year time variable
    energy_df_top = energy_df_top.drop(columns=time_variable+'_base_year')
    #calculate sum of energy for each year for the bottom part of the formula log(sum(energy_t)/sum(energy_base_year)
    energy_year_t_sum = energy_year_t.groupby(time_variable).sum()
    energy_base_year_sum = energy_base_year.groupby(time_variable).sum()
    #since energy_base_year_sum is just one value, create a column of that value for each year in energy_year_t_sum
    energy_df_bot = energy_year_t_sum
    energy_df_bot['{}_base_year'.format(energy_variable)] = energy_base_year_sum[energy_variable].values[0]
    energy_df_bot.reset_index(inplace=True)

    #CALCULATE:
    #calulate ln(d_t/d_0) for the drivers. We will call this the 'log ratio driver value'
    for driver in drivers_list:
        driver_df[driver+'_log_ratio'] = np.log(driver_df[driver]/driver_df[driver+'_base_year'])

        #drop unneeded columns
        driver_df = driver_df.drop(columns=['{}_base_year'.format(driver), driver])

    #find the log means using the log_mean_func()
    log_mean_top = log_mean_func(energy_df_top, energy_variable)
    log_mean_bot = log_mean_func(energy_df_bot, energy_variable)

    #keep only the important cols
    log_mean_top = log_mean_top[structure_variables_list+[time_variable,'log_mean','Change in {}'.format(energy_variable)]]
    log_mean_bot = log_mean_bot[[time_variable,'log_mean','Change in {}'.format(energy_variable)]]
    #merge so we can calculate the weighting factor as log_mean = log_mean_top/log_mean_bot
    log_mean = pd.merge(log_mean_top, log_mean_bot, on=time_variable, how='left', suffixes=('_top', '_bot'))
    log_mean['weighting_factor'] = log_mean['log_mean_top']/log_mean['log_mean_bot']

    ##now times the log mean by the log ratio driver value
    #first get driver data and log mean data in the right shape, merged
    driver_df = driver_df.merge(log_mean, on=[time_variable]+structure_variables_list, how='left')

    #now multiply the log mean by the log ratio driver value for each driver
    for driver in drivers_list:
        driver_df[driver] = driver_df[driver+'_log_ratio'] * driver_df['weighting_factor']
        #drop unneeded columns
        driver_df = driver_df.drop(columns=['{}_log_ratio'.format(driver)])

    #sum up for each year to get total effect per year
    driver_df = driver_df.groupby(time_variable).sum()
    #calc the exponential of each new driver value
    for driver in drivers_list:
        driver_df[driver] = np.exp(driver_df[driver])

    #calculate ratio of energy for each year commpared to the base year from the 'Change in energy_top' variable. To do this we need to rejoin the base year data to the driver df to calculate ('change in energy'/base year energy) + 1
    driver_df['{}_base_year'.format(energy_variable)] = energy_base_year_sum[energy_variable].values[0]
    driver_df['Percent change in {}'.format(energy_variable)] = (driver_df['Change in {}_top'.format(energy_variable)]/driver_df['{}_base_year'.format(energy_variable)]) + 1

    #FINAL FORMATTING:
    #drop unneeded columns
    lmdi_output_multiplicative = driver_df.drop(columns=['weighting_factor', 'log_mean_top', 'log_mean_bot', 'Change in {}_bot'.format(energy_variable), 'Change in {}_top'.format(energy_variable), '{}_base_year'.format(energy_variable)])

    #recreate drivers list by adding effect to the original names 
    drivers_list_new = drivers_list.copy()
    #first remove 'Total_' from activity variable name within the drivers list using regex to ensure Total_ is at the start of the string
    drivers_list_new = [re.sub('^Total_', '', driver) for driver in drivers_list_new]
    #remove _share from the ends of the structure names
    drivers_list_new = [re.sub('_share$', '', x) for x in drivers_list_new]
    #then add 'effect' to the end of each driver name
    drivers_list_new = [x + ' effect' for x in drivers_list_new]

    #replace names in the driver df col
    lmdi_output_multiplicative.rename(columns=dict(zip(drivers_list, drivers_list_new)), inplace=True)

    #add row of zeros for the base year:
    lmdi_output_multiplicative = lmdi_output_multiplicative.reset_index()
    #create new row by creating a pandas series where we only state Year and then concatenate it to the df
    new_row = pd.Series({'{}'.format(time_variable):base_year})
    #add the new row to the df
    lmdi_output_multiplicative = pd.concat([new_row.to_frame().T,lmdi_output_multiplicative])
    #If Year is base year, replace NAs with 1
    lmdi_output_multiplicative = lmdi_output_multiplicative.fillna(1)

    return lmdi_output_multiplicative

############################################### 
###############################################
###############################################

def Add(driver_input_data, energy_data, drivers_list, structure_variables_list,energy_variable,time_variable,activity_variable):
    #This will carry out the LMDI-I formula for the additive case. The formula is: sum(log(energy_t/energy_base_year) * log(mean(energy_t/energy_base_year)) * log(driver_t/driver_base_year))
    #note that where the word energy is used in names, it can be swapped out for emissions. Although any changes to columns names occurs outside this function.

    #PREP DATA:
    #prep driver data
    #get base year from data
    base_year = driver_input_data[time_variable].min()
    driver_base_year  =  driver_input_data.loc[driver_input_data[time_variable] == base_year]
    driver_t = driver_input_data.loc[driver_input_data[time_variable] != base_year]
    #merge base year driver value onto non base year data, so we can subtract it from the other years
    driver_df = pd.merge(driver_t, driver_base_year, on=structure_variables_list, how='left', suffixes=('', '_base_year'))
    #drop base year time variable
    driver_df = driver_df.drop(columns='{}_base_year'.format(time_variable))

    #prep energy data
    #get base year from data
    base_year = energy_data[time_variable].min()
    #separate data by base year and other years
    energy_base_year = energy_data.loc[energy_data[time_variable] == base_year]
    energy_year_t = energy_data.loc[energy_data[time_variable] != base_year]
    #merge base year energy value onto non base year data, so we can subtract it from the other years
    energy_df = pd.merge(energy_year_t, energy_base_year, on=structure_variables_list, how='left', suffixes=('', '_base_year'))
    #drop base year time variable
    energy_df = energy_df.drop(columns='{}_base_year'.format(time_variable))

    #CALCULATE:
    #calulate ln(d_t/d_0) for the drivers. We will call this the 'log ratio driver value'
    for driver in drivers_list:
        driver_df[driver+'_log_ratio'] = np.log(driver_df[driver]/driver_df[driver+'_base_year'])

        #drop unneeded columns
        driver_df = driver_df.drop(columns=['{}_base_year'.format(driver), driver])

    #find the log mean which is the weighting factor using the log_mean_func()
    log_mean = log_mean_func(energy_df, energy_variable)

    #keep only the important cols
    log_mean = log_mean[structure_variables_list+[time_variable,'log_mean','Change in {}'.format(energy_variable)]]

    ##now times the log mean by the log ratio driver value
    #first get driver data and log mean data in the right shape, merged
    driver_df = driver_df.merge(log_mean, on=[time_variable]+structure_variables_list, how='left')

    #now multiply the log mean by the log ratio driver value for each driver
    for driver in drivers_list:
        driver_df[driver] = driver_df[driver+'_log_ratio'] * driver_df['log_mean']

        #drop unneeded columns
        driver_df = driver_df.drop(columns=['{}_log_ratio'.format(driver)])

    #sum up for each year to get total effect per year
    driver_df = driver_df.groupby(time_variable).sum()

    #FINAL FORMATTING:
    #drop unneeded columns
    lmdi_output_additive = driver_df.drop(columns=['log_mean'])
    
    #recreate drivers list by adding effect to the original names 
    drivers_list_new = drivers_list.copy()
    #first remove 'Total_' from activity variable name within the drivers list using regex to ensure Total_ is at the start of the string
    drivers_list_new = [re.sub('^Total_', '', driver) for driver in drivers_list_new]
    #remove _share from the ends of the structure names
    drivers_list_new = [re.sub('_share$', '', x) for x in drivers_list_new]
    #then add 'effect' to the end of each driver name
    drivers_list_new = [x + ' effect' for x in drivers_list_new]

    #replace names in the driver df col
    lmdi_output_additive.rename(columns=dict(zip(drivers_list, drivers_list_new)), inplace=True)

    #add row of zeros for the base year:
    lmdi_output_additive = lmdi_output_additive.reset_index()
    #create new row by creating a pandas series where we only state Year and then concatenate it to the df
    new_row = pd.Series({'{}'.format(time_variable):base_year})
    #add the new row to the df
    lmdi_output_additive = pd.concat([new_row.to_frame().T,lmdi_output_additive])
    #If Year is base year, replace NAs with 0
    lmdi_output_additive = lmdi_output_additive.fillna(0)

    return lmdi_output_additive

def log_mean_func(energy_df, energy_variable):
    ##Find the weighting for the divisia function using the log mean function on the energy data. This will calcualte the log mean when comparing the base year to the other years
    #fyi the log mean function is this: L(E_t,E_0) = (E_t-E_0)/(ln(E_t)-ln(E_0)) where E_t is the energy in the year t and E_0 is the energy in the base year
    #note that where the word energy is used in names, it can be swapped out for emissions. Although any changes to columns names occurs outside this function.

    #calc the change in energy between the base year and the other years
    #(E_t-E_0)
    energy_df['Change in {}'.format(energy_variable)] = energy_df[energy_variable] - energy_df['{}_base_year'.format(energy_variable)]

    #calc the log of the energy in the base year and the other years
    # (ln(E_t)-ln(E_0)) 
    energy_df['log_{}_base_year'.format(energy_variable)] = np.log(energy_df['{}_base_year'.format(energy_variable)])
    energy_df['log_{}'.format(energy_variable)] = np.log(energy_df[energy_variable])
    #calc the diff between them
    energy_df['log_{}_diff'.format(energy_variable)] = energy_df['log_{}'.format(energy_variable)] - energy_df['log_{}_base_year'.format(energy_variable)]

    #now we can calc the log mean
    #L(E_t,E_0) = (E_t-E_0)/(ln(E_t)-ln(E_0))
    energy_df['log_mean'] = energy_df['Change in {}'.format(energy_variable)]/energy_df['log_{}_diff'.format(energy_variable)]

    return energy_df
