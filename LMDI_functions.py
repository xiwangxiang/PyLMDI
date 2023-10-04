#The details on the LMDI method which is quite complicated can be found here: https://drive.google.com/file/d/1wCd-S55JVrHoQwRV7w9qZSVxTlfiqGa8/view?usp=sharing
#in all of the following functions we use the term energy but it can also be emissions, as that capacbiltiy has been built into the code.
#also the term driver is used. It represents the effect, such as activity effect, structural effect and energy intensity effect. It can also be emissions intensity effect, as that capacity has been built into the code.
import pandas as pd
import numpy as np
import re


##########################################################################################################################################################


def Mult(driver_input_data, energy_data, drivers_list, structure_variables_list,energy_variable,time_variable,extra_identifier):#driver_input_data, energy):
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
    energy_year_t_sum = energy_year_t.groupby(time_variable).sum(numeric_only=True)
    energy_base_year_sum = energy_base_year.groupby(time_variable).sum(numeric_only=True)
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
    driver_df = driver_df.groupby(time_variable).sum(numeric_only=True)
    #calc the exponential of each new driver value
    for driver in drivers_list:
        driver_df[driver] = np.exp(driver_df[driver])

    #calculate ratio of energy for each year commpared to the base year using the 'Change in energy_top' variable. To do this we need to rejoin the base year data to the driver df to calculate ('change in energy'/base year energy) + 1 (this is equivalent to the ratio between other eyars and base years in total energy)
    driver_df['{}_base_year'.format(energy_variable)] = energy_base_year_sum[energy_variable].values[0]
    driver_df['Multiplicative change in {}'.format(energy_variable)] = (driver_df['Change in {}_top'.format(energy_variable)]/driver_df['{}_base_year'.format(energy_variable)]) + 1

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

    #check that the product of drivers in each year is equal to the percent change in energy
    lmdi_output_multiplicative['product'] = lmdi_output_multiplicative[drivers_list_new].product(axis=1)
    lmdi_output_multiplicative['difference'] = lmdi_output_multiplicative['product'] - lmdi_output_multiplicative['Multiplicative change in {}'.format(energy_variable)]
    total_difference = lmdi_output_multiplicative['difference'].sum().sum()
    if abs(total_difference) > 0.01:
        breakpoint()
        print('WARNING: The product of the multiplicative drivers for {} in each year is not equal to the percent change in energy. This seems to be a result of the input data, probably because the structure is inconsistent (i.e. certain structure variable categories are missing in certain years). The difference is {}'.format(extra_identifier, total_difference))
    #drop the product and difference columns
    lmdi_output_multiplicative = lmdi_output_multiplicative.drop(columns=['product', 'difference'])

    return lmdi_output_multiplicative

############################################### 
###############################################
###############################################

def Add(driver_input_data, energy_data, drivers_list, structure_variables_list,energy_variable,time_variable,extra_identifier):
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
    driver_df = driver_df.groupby(time_variable).sum(numeric_only=True)

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

    #test that the sum of the effects in final year is equal to the change in energy
    #sum the effects
    lmdi_output_additive['sum of effects'] = lmdi_output_additive[drivers_list_new].sum(axis=1)
    #calc difference between sum of effects and change in energy
    lmdi_output_additive['difference'] = lmdi_output_additive['sum of effects'] - lmdi_output_additive['Change in {}'.format(energy_variable)]
    #calcaulte the total difference
    total_difference = lmdi_output_additive['difference'].sum().sum()
    #check that the total difference is less than 0.001
    if abs(total_difference) > 0.001:
        breakpoint()
        print('WARNING: The sum of the additive effects for {} is not equal to the change in energy for one or more years. This seems to be a result of the input data, probably because the structure is inconsistent (i.e. certain structure variable categories are missing in certain years). Please check the input. \nThe total difference is: {}'.format(extra_identifier, total_difference))
    #drop the difference column
    lmdi_output_additive = lmdi_output_additive.drop(columns=['difference','sum of effects'])

    return lmdi_output_additive

##########################################################################################################################################################


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

##########################################################################################################################################################



def hierarchical_LMDI(energy_data, activity_data, energy_variable, activity_variable, structure_variables_list, time_variable,extra_identifier):
    
    #This is the function for lmdi hierarchical multiple structural effects.

    #There is only one intensity effect, which is for the final structural driver (the lowest on the hierarchy), but to keep things simple we will calculate the intensity effect for all structural variables and remove the ones we dont need at the end.
    #The structural driver for each subsequent structural category down the hierarchy is calculated. The exact formula is complicated. I have put it as a screenshot in the documentation folder.

    #The code for this function is quite long, this is because it is a complicated formula and since I have tried to make it as clear as possible, it is long.

    #The process will be centred around one big_df which we will dip in and out of for variables. We will also have a list of the different structural drivers which we will loop through since there are a lot of different combinations of sectoral calcualtions that need to be done.

    #we will also use a numbering system in case it is useful to reference where soime variables were clacualted or something.

    # 1:
    #In this section we calcualte and sum for:
    #Eijk, Eij, Ei, E : where E is energy and ijk are the sectors in the structural drivers list. 
    #Aijk, Aij, Ai, A : where A is activity
    # intensity for each level of the structural drivers (i.e. Eijk/Aijk, Eij/Aij, Ei/Ai, E/A)
    #ln(intensity_other_years/intensity_base_year) for each level of the structural drivers
    #Aij/Ai, Ai/A, Aijl/Aij : where A is activity. This is the structural share.
    #Intersectoral intensity: Eij/Ai, Eijk/Aij : where E is energy and A is activity. This is what ive called the intersectoral structural intensity. We will calculate a log mean from this in 3, which will also be used to calculate weighting_value_ in 3 too.

    #so treating the order of structure_variables_list as the hierarchical order:
    #calc total activity and energy for each year
    base_year = energy_data[time_variable].min()
    #check base year is the same in both dataframes
    assert base_year == activity_data[time_variable].min()

    big_df = pd.merge(activity_data, energy_data, on=[time_variable]+structure_variables_list)
    big_df = pd.merge(big_df, activity_data.groupby([time_variable])[activity_variable].sum(), on=[time_variable], suffixes=('', '_total'))
    big_df = pd.merge(big_df, energy_data.groupby([time_variable])[energy_variable].sum(), on=[time_variable], suffixes=('', '_total'))

    hierarchy_list = []
    for structure_variable in structure_variables_list:
        hierarchy_list.append(structure_variable)

        energy_sum = energy_data.groupby([time_variable]+hierarchy_list)[energy_variable].sum().reset_index()
        activity_sum = activity_data.groupby([time_variable]+hierarchy_list)[activity_variable].sum().reset_index()
        prev_activity_sum = activity_data.groupby([time_variable]+hierarchy_list[:-1])[activity_variable].sum().reset_index()

        intensity = pd.merge(energy_sum, activity_sum, on=[time_variable]+hierarchy_list)
        intensity = pd.merge(intensity, prev_activity_sum, on=[time_variable]+hierarchy_list[:-1], suffixes=('', '_prev'))
        intensity['intensity_'+structure_variable] = intensity[energy_variable]/intensity[activity_variable]

        if len(hierarchy_list) > 1:
            #intersectoral intensity is only calculated for the second and subsequent levels of hierarchy's structural driver
            # So for example, if we have ['Vehicle Type', 'Drive'], then we have calculated this value for Drive, but not for Vehicle Type. 
            intensity['intersectoral_intensity_'+structure_variable] = intensity[energy_variable]/intensity[activity_variable+'_prev']

        intensity = intensity.drop(columns=[activity_variable, energy_variable, activity_variable+'_prev'])#note that its important we still keep regular intensity values since they are useful later.

        big_df = pd.merge(big_df, intensity, on=[time_variable]+hierarchy_list, how='left')
        ##############

        #while here we can calculate ln(intensity_other_years/intensity_base_year) for each structure variable
        #first create a df which only has the intensity, time variable and hierarchy list
        intensity = intensity[[time_variable, 'intensity_'+structure_variable]+hierarchy_list]
        # separate the base year and other years
        intensity_base_year = intensity[intensity[time_variable]==base_year].drop(columns=[time_variable])
        intensity_other_years = intensity[intensity[time_variable]!=base_year]
        #merge the two together
        intensity_log = pd.merge(intensity_other_years, intensity_base_year, on=hierarchy_list, suffixes=('', '_base_year'))
        #calc the log
        intensity_log['log_intensity_ratio_{}'.format(structure_variable)] = np.log(intensity_log['intensity_{}'.format(structure_variable)]/intensity_log['intensity_{}_base_year'.format(structure_variable)])
        #drop cols
        intensity_log = intensity_log.drop(columns=['intensity_{}'.format(structure_variable), 'intensity_{}_base_year'.format(structure_variable)])

        big_df = pd.merge(big_df, intensity_log, on=[time_variable]+hierarchy_list, how='left')
        ##############

        structural_share = pd.merge(activity_sum, prev_activity_sum, on=[time_variable]+hierarchy_list[:-1], suffixes=('', '_prev'))
        structural_share['structural_share_'+structure_variable] = structural_share[activity_variable]/structural_share[activity_variable+'_prev']
        structural_share = structural_share.drop(columns=[activity_variable, activity_variable+'_prev'])

        #while here we can still calculate ln(structural_share_other_years/structural_share_base_year) for each structure variable
        #first separate the base year and other years
        structural_share_base_year = structural_share[structural_share[time_variable]==base_year].drop(columns=[time_variable])
        structural_share_other_years = structural_share[structural_share[time_variable]!=base_year]
        #merge the two together
        structural_share_log = pd.merge(structural_share_other_years, structural_share_base_year, on=hierarchy_list, suffixes=('', '_base_year'))
        #calc the log
        structural_share_log['log_structural_share_{}'.format(structure_variable)] = np.log(structural_share_log['structural_share_{}'.format(structure_variable)]/structural_share_log['structural_share_{}_base_year'.format(structure_variable)])
        #drop cols
        structural_share_log = structural_share_log.drop(columns=['structural_share_{}'.format(structure_variable), 'structural_share_{}_base_year'.format(structure_variable)])

        big_df = pd.merge(big_df, structural_share_log, on=[time_variable]+hierarchy_list, how='left')

        ##############

    
    ########################################
    #2
    #ln(At/A0) : which is used in claculating the activity driver

    #get data
    activity_log = activity_data.groupby([time_variable])[activity_variable].sum().reset_index()
    #separate the base year and other years
    activity_base_year = activity_log[activity_log[time_variable]==base_year]
    activity_other_years = activity_log[activity_log[time_variable]!=base_year]
    #create a col in other years which is just the data for base year
    activity_log = activity_other_years.copy()
    activity_log['{}_base_year'.format(activity_variable)] = activity_base_year[activity_variable].values[0]
    #calc the log
    activity_log['log_activity'] = np.log(activity_log[activity_variable]/activity_log['{}_base_year'.format(activity_variable)])
    #drop cols
    activity_log = activity_log.drop(columns=[activity_variable, activity_variable+'_base_year'])
    #join to big df
    big_df = pd.merge(big_df, activity_log, on=[time_variable], how='left')

    

    ########################################
    #3.
    #L(EijT/AiT, Eij0/Ai0)
    #L(EiT/AiT, Ei0/Ai0)
    #L(EijT/AiT, Eij0/Ai0) / L(EiT/AiT, Ei0/Ai0) : which is the division of the two above
    big_df_2 = big_df.copy()
    #now is a tricky part. We will calculate a log mean value using the intersectoral intensity which is only calculated for the second and subsequent levels of hierarchy's structural driver. So for example, if we have ['Vehicle Type', 'Drive'], then we have calculated this value for Drive, but not for Vehicle Type. If there were extra sectors, the pattern would continue.
    #the formula for this value for the second level of hierarchy would be: L(EijT/AiT, Eij0/Ai0) / L(EiT/AiT, Ei0/Ai0) where T is the time variable after the base year, 0 is the base year. i is Vehicle type, j is Drive.

    #Calculate top value L(EijT/AiT, Eij0/Ai0)
    hierarchy_list = [structure_variables_list[0]]
    for structure_variable in structure_variables_list[1:]:
        hierarchy_list.append(structure_variable)

        calc_df = big_df_2[[time_variable, 'intersectoral_intensity_'+structure_variable]+hierarchy_list]

        #remove any duplicates in the df since we are reducing the number of cateogircal variables
        calc_df = calc_df.drop_duplicates()

        #sep base year and other years
        base_year_df = calc_df[calc_df[time_variable] == base_year].drop(columns=[time_variable])
        other_years_df = calc_df[calc_df[time_variable] != base_year]
        calc_df = pd.merge(other_years_df, base_year_df, on=hierarchy_list, suffixes=('', '_base_year'))

        #calc log mean
        calc_df = log_mean_func(calc_df, 'intersectoral_intensity_'+structure_variable)

        #name the log mean value column
        calc_df.rename(columns={'log_mean':'intensity_log_mean_top_'+structure_variable}, inplace=True)#NOTE THIS IS CHANGED FROM 'log_mean_'+structure_variable

        #keep the columns we need
        calc_df = calc_df[[time_variable]+hierarchy_list+['intensity_log_mean_top_'+structure_variable]]

        #merge the log mean value back into the big df
        big_df_2 = pd.merge(big_df_2, calc_df, on=[time_variable]+hierarchy_list, how='left')

    ########################################
    #3. 
    #CALCUALTE WEIGHTING VALUES FOR EACH STRUCTURE VARIABLE EXCEPT THE FIRST ONE
    #this will work assuming that the strucutral variables will increase as the structural variable for teh driver does to. 
    #so say, for the intensity and structrual share drivers of drive, the formula is:
    #L(EijT/AiT, Eij0/Ai0)
    #L(EiT/AiT, Ei0/Ai0)
    #L(EijT/AiT, Eij0/Ai0) / L(EiT/AiT, Ei0/Ai0) : which is the division of the two above

    #but then if there was another structural variable, k, then the formula would be:
    #L(EijkT/AijT, Eijk0/Aij0)
    #L(EijT/AijT, Eij0/Aij0)
    #L(EijkT/AijT, Eijk0/Aij0) / L(EijT/AijT, Eij0/Aij0) : which is the division of the two above


    #So since we will skip the first strucutral variable, we will calculate this weighting value using the intersectoral intensity for the second and subsequent levels of hierarchy's structural driver.
    #the formula for this value for the second level of hierarchy would be: L(EijT/AiT, Eij0/Ai0) / L(EiT/AiT, Ei0/Ai0) where T is the time variable after the base year, 0 is the base year. i is Vehicle type, j is Drive.
    
    #Calculate top value eg. L(EijT/AiT, Eij0/Ai0)
    hierarchy_list = [structure_variables_list[0]]
    for structure_variable in structure_variables_list[1:]:
        hierarchy_list.append(structure_variable)

        calc_df = big_df[[time_variable, 'intersectoral_intensity_'+structure_variable]+hierarchy_list]

        #remove any duplicates in the df since we are reducing the number of cateogircal variables
        calc_df = calc_df.drop_duplicates()

        #sep base year and other years
        base_year_df = calc_df[calc_df[time_variable] == base_year].drop(columns=[time_variable])
        other_years_df = calc_df[calc_df[time_variable] != base_year]
        calc_df = pd.merge(other_years_df, base_year_df, on=hierarchy_list, suffixes=('', '_base_year'))

        #calc log mean
        calc_df = log_mean_func(calc_df, 'intersectoral_intensity_'+structure_variable)

        #name the log mean value column
        calc_df.rename(columns={'log_mean':'log_mean_'+structure_variable}, inplace=True)

        #keep only the columns we do need
        calc_df = calc_df[[time_variable, 'log_mean_'+structure_variable]+hierarchy_list]

        #merge the log mean value back into the big df
        big_df = pd.merge(big_df, calc_df, on=[time_variable]+hierarchy_list, how='left')

    #########
    #calculate bottom value L(EiT/AiT, Ei0/Ai0)
    #Note that we can just use intensity as calculated for each structural variable earlier
    hierarchy_list = [structure_variables_list[0]]
    for structure_variable in structure_variables_list[1:]:
        previous_structure_variable = hierarchy_list[-1]
        intensity = big_df[['intensity_'+previous_structure_variable, time_variable]+ hierarchy_list]
        intensity = intensity.drop_duplicates()
        #separate the base year and other year data and make the base year data a col in the other year data
        base_year_df = intensity[intensity[time_variable] == base_year].drop(columns=[time_variable])
        other_years_df = intensity[intensity[time_variable] != base_year]
        #merge the data
        intensity_df_bot = pd.merge(other_years_df, base_year_df, on=hierarchy_list, suffixes=('', '_base_year'))
        #calc log mean
        intensity_df_bot = log_mean_func(intensity_df_bot, 'intensity_'+previous_structure_variable)

        #rename the log mean value column
        intensity_df_bot.rename(columns={'log_mean':'intensity_log_mean_bot_{}'.format(structure_variable)}, inplace=True)
        #keep only the columns we do need
        intensity_df_bot = intensity_df_bot[[time_variable, 'intensity_log_mean_bot_{}'.format(structure_variable)]+hierarchy_list]

        #merge the log mean value back into the big df
        big_df = pd.merge(big_df, intensity_df_bot, on=[time_variable]+hierarchy_list, how='left')

        hierarchy_list.append(structure_variable)#add to the hierarchy list last because we are basing intensity on the previous level of hierarchy

    ##############
    #merge the top and bot values and calculate the ratio between them
    #we will have to do this using a loop since the values in top will change according to the level of hierarchy
    hierarchy_list = [structure_variables_list[0]]
    for structure_variable in structure_variables_list[1:]:
        hierarchy_list.append(structure_variable)
        intersectoral_intensity_df = big_df[['log_mean_'+structure_variable,'intensity_log_mean_bot_{}'.format(structure_variable),  time_variable]+ hierarchy_list]
        intersectoral_intensity_df = intersectoral_intensity_df.drop_duplicates()
        intersectoral_intensity_df['weighting_value_'+structure_variable] = intersectoral_intensity_df['log_mean_'+structure_variable] / intersectoral_intensity_df['intensity_log_mean_bot_{}'.format(structure_variable)]

        #drop the columns we don't need
        intersectoral_intensity_df.drop(columns=['log_mean_'+structure_variable,'intensity_log_mean_bot_{}'.format(structure_variable)], inplace=True)
        
        #merge the weighting value back into the big df
        big_df = pd.merge(big_df, intersectoral_intensity_df, on=[time_variable]+hierarchy_list, how='left')
    
    ########################################
    # 4.
    #L(Eit,Ei0) 
    #L(ET,E0) 
    # First weight for the first structural variable which is the ratio of the two values above

    #TOP
    #grab sum for first structural variable:
    first_structure_variable = structure_variables_list[0]
    energy_sum = energy_data.groupby([time_variable,first_structure_variable])[energy_variable].sum().reset_index()

    #separate the base year and other year data and make the base year data a col in the other year data
    base_year_df = energy_sum[energy_sum[time_variable] == base_year].drop(columns=[time_variable])
    other_years_df = energy_sum[energy_sum[time_variable] != base_year]
    #merge the data
    weighting_df_top = pd.merge(other_years_df, base_year_df, on=[first_structure_variable], suffixes=('', '_base_year'))
    #calc log mean
    weighting_df_top = log_mean_func(weighting_df_top, energy_variable)
    #clean
    weighting_df_top.drop(columns=['log_{}_base_year'.format(energy_variable), 'log_{}'.format(energy_variable), 'log_{}_diff'.format(energy_variable),'Change in {}'.format(energy_variable)], inplace=True)
    weighting_df_top.rename(columns={'log_mean':'weighting_log_mean_top'}, inplace=True)

    #BOT
    #grab Energy by year summed for the first strucutral category and energy summed with no strucutral categorys
    total_energy_sum = big_df[[energy_variable + '_total', time_variable]]
    #remove duplicates
    total_energy_sum = total_energy_sum.drop_duplicates()
    #separate the base year and other year data and make the base year data a col in the other year data
    base_year_df = total_energy_sum[total_energy_sum[time_variable] == base_year]
    other_years_df = total_energy_sum[total_energy_sum[time_variable] != base_year]
    #create a df with the base year data as a column in the other year data
    weighting_df_bot = other_years_df.copy()
    weighting_df_bot[energy_variable + '_total'+'_base_year'] = base_year_df[energy_variable + '_total'].values[0]
    #calc log mean
    weighting_df_bot = log_mean_func(weighting_df_bot, energy_variable + '_total')
    #clean
    weighting_df_bot.drop(columns=['log_{}_base_year'.format(energy_variable + '_total'), 'log_{}'.format(energy_variable + '_total'), 'log_{}_diff'.format(energy_variable + '_total'),'Change in {}'.format(energy_variable + '_total')], inplace=True)
    weighting_df_bot.rename(columns={'log_mean':'weighting_log_mean_bot'}, inplace=True)

    ########
    #merge the top and bot values and claculate the weighting value
    weighting_df = pd.merge(weighting_df_top, weighting_df_bot, on=[time_variable])
    weighting_df['weighting_value_first_str_variable'] = weighting_df['weighting_log_mean_top'] / weighting_df['weighting_log_mean_bot']
    #keep the columns we do need
    weighting_df = weighting_df[[time_variable,first_structure_variable, 'weighting_value_first_str_variable']]
    #merge the weighting value back into the big df
    big_df = pd.merge(big_df, weighting_df, on=[time_variable, first_structure_variable])

    ########################################

    
    #5.
    #CALCULATE ACTIVITY DRIVER
    #PLEASE NOTE THAT WE WILL RENAME ALL DRIVERS AT THE END OF THIS SCRIPT, SO IT IS EASIER TO BUGFIX THIS DATA
    #Activity driver = exp( SUM( Weighting value * Value from step 2 ) )
    activity_driver = big_df[[time_variable, 'log_activity', 'weighting_value_first_str_variable']]
    #remove duplicates
    activity_driver = activity_driver.drop_duplicates()
    #times the weighting value by the log activity
    activity_driver['activity_driver'] = activity_driver['log_activity'] * activity_driver['weighting_value_first_str_variable']
    #sum the activity_driver by year
    activity_driver = activity_driver.groupby([time_variable])['activity_driver'].sum().reset_index()
    #calc the exponential
    activity_driver['activity_driver'] = np.exp(activity_driver['activity_driver'])

    ############################################################################################################

    #7
    #first structural level structural driver = exp( SUM( Weighting value * ln(structural_share_other_years/structural_share__base_year) ) )
    #where structural share is for the first structural level
    first_structural_level_structural_driver = big_df[[time_variable, 'log_structural_share_{}'.format(first_structure_variable), 'weighting_value_first_str_variable']]
    #remove duplicates
    first_structural_level_structural_driver = first_structural_level_structural_driver.drop_duplicates()
    #times the weighting value by the log value
    first_structural_level_structural_driver['first_structural_level_structural_driver'] = first_structural_level_structural_driver['log_structural_share_{}'.format(first_structure_variable)] * first_structural_level_structural_driver['weighting_value_first_str_variable']
    #sum the first_structural_level_structural_driver by year
    first_structural_level_structural_driver = first_structural_level_structural_driver.groupby([time_variable])['first_structural_level_structural_driver'].sum().reset_index()
    #calc the exponential
    first_structural_level_structural_driver['first_structural_level_structural_driver'] = np.exp(first_structural_level_structural_driver['first_structural_level_structural_driver'])

    ############################################################################################################

    #8
    #please note that in the final version of this method we actually remove the intensity drivers for all structural levels except the last. But we have to calcualte the intensity_log_mean_ratio for each structural level anyway so to keep the code simple we jsut calcualte the intensity drivers for all structural levels and remove them afterwwards

    #successive structural level intensity drivers = exp( SUM( Weighting value * SUM( intensity_log_mean_ratio * ln(intensity_other_years/intensity_base_year) ) )
    #where intensity is for the successive structural levels
    #where intensity_log_mean_ratio is for the successive structural levels
    successive_structural_level_drivers_dict = {}
    hierarchy_list = [structure_variables_list[0]]#hierarchy list will have the next structure variable added to it after each iteration
    for structure_variable in structure_variables_list[1:]:
        structure_variable_index = structure_variables_list.index(structure_variable)

        #get the data for this level
        successive_structural_level_drivers = big_df[[time_variable, 'log_structural_share_{}'.format(structure_variable), 'log_intensity_ratio_{}'.format(structure_variable), 'weighting_value_{}'.format(structure_variable),structure_variable]+hierarchy_list]

        #remove duplicates
        successive_structural_level_drivers = successive_structural_level_drivers.drop_duplicates()

        ##NOW DO CALCULATIONS 

        #times the weighting_value_ by the log value for the current level (current level = structure_variable)
        successive_structural_level_drivers['intensity_driver_{}'.format(str(structure_variable_index))] = successive_structural_level_drivers['log_intensity_ratio_{}'.format(structure_variable)] * successive_structural_level_drivers['weighting_value_{}'.format(structure_variable)]

        successive_structural_level_drivers['structural_driver_{}'.format(str(structure_variable_index))] = successive_structural_level_drivers['log_structural_share_{}'.format(structure_variable)] * successive_structural_level_drivers['weighting_value_{}'.format(structure_variable)]


        #sum the successive_structural_level_drivers by year and all the structural levels except the current one
        successive_structural_level_drivers = successive_structural_level_drivers[[time_variable, 'intensity_driver_{}'.format(str(structure_variable_index)), 'structural_driver_{}'.format(str(structure_variable_index))]+hierarchy_list].groupby([time_variable]+hierarchy_list).sum(numeric_only=True).reset_index()

        #NOW do this for each structural vairable in the hierarchy list (except the first one), but going backwards (so the last one is the first one))(i.e. going from j to i if there are 3 structural variables ijk):
        #times the variable successive_structural_level_drivers_{}'.format(str(structure_variable_index) by the previous structural vairables weighting_value_ and sum for each year and all the structural levels up to that one. this will be set as the new value for the successive_structural_level_drivers_{}'.format(str(structure_variable_index) for the next iteration
        
        #note that this only has an effect if there are more than 2 structural variables since hierarchy_list doesn't contain the current structure_variable

        mini_hierarchy_list = hierarchy_list#mini_hierarchy_list will contain all the variables for which we still need to times the weighting_value_ by the successive_structural_level_drivers value

        for hierarchy_variable in hierarchy_list[::-1]:
            if hierarchy_variable != hierarchy_list[0]:#ignore the first one (i) because the calc for that is different.
                
                #this will create a df with the successive_structural_level_drivers_ for the structural variable we have just calculated it for, and the intensity_log_mean_ratio for the current hierarchy variable
                successive_structural_level_drivers = pd.merge(successive_structural_level_drivers, big_df[[time_variable, 'weighting_value_{}'.format(hierarchy_variable)] + mini_hierarchy_list], on=[time_variable]+mini_hierarchy_list)

                #drop duplicates
                successive_structural_level_drivers = successive_structural_level_drivers.drop_duplicates()

                #times the weighting_value_ by the successive_structural_level_drivers_
                successive_structural_level_drivers['intensity_driver_{}'.format(str(structure_variable_index))] = successive_structural_level_drivers['intensity_driver_{}'.format(str(structure_variable_index))] * successive_structural_level_drivers['weighting_value_{}'.format(hierarchy_variable)]

                successive_structural_level_drivers['structural_driver_{}'.format(str(structure_variable_index))] = successive_structural_level_drivers['structural_driver_{}'.format(str(structure_variable_index))] * successive_structural_level_drivers['weighting_value_{}'.format(hierarchy_variable)]
                
                #remove the current hierarchy variable from the mini_hierarchy_list now that we have done the calc for it
                mini_hierarchy_list.remove(hierarchy_variable)

                #sum the new successive_structural_level_drivers by year and mini_hierarchy_list
                successive_structural_level_drivers = successive_structural_level_drivers[[time_variable, 'intensity_driver_{}'.format(str(structure_variable_index)), 'structural_driver_{}'.format(str(structure_variable_index))]+mini_hierarchy_list].groupby([time_variable]+mini_hierarchy_list).sum(numeric_only=True).reset_index()

        #times the weighting value for the first_structure_variable by the newly calculated value
        successive_structural_level_drivers = pd.merge(successive_structural_level_drivers, weighting_df, on=[time_variable, structure_variables_list[0]])

        successive_structural_level_drivers['intensity_driver_{}'.format(str(structure_variable_index))] = successive_structural_level_drivers['intensity_driver_{}'.format(str(structure_variable_index))] * successive_structural_level_drivers['weighting_value_first_str_variable']

        successive_structural_level_drivers['structural_driver_{}'.format(str(structure_variable_index))] = successive_structural_level_drivers['structural_driver_{}'.format(str(structure_variable_index))] * successive_structural_level_drivers['weighting_value_first_str_variable']
        
        #sum the successive_structural_level_drivers by year
        successive_structural_level_drivers = successive_structural_level_drivers[[time_variable, 'intensity_driver_{}'.format(str(structure_variable_index)), 'structural_driver_{}'.format(str(structure_variable_index))]].groupby(time_variable).sum(numeric_only=True).reset_index()

        #calc the exponential
        successive_structural_level_drivers['intensity_driver_{}'.format(str(structure_variable_index))] = np.exp(successive_structural_level_drivers['intensity_driver_{}'.format(str(structure_variable_index))])
        successive_structural_level_drivers['structural_driver_{}'.format(str(structure_variable_index))] = np.exp(successive_structural_level_drivers['structural_driver_{}'.format(str(structure_variable_index))])
        #add to the dictionary using index as key
        successive_structural_level_drivers_dict[structure_variable_index]=successive_structural_level_drivers

        #add structure variable to the hierarchy list
        hierarchy_list.append(structure_variable)

    ######################################################
    #10
    #FORMATTING
    #GREAT GOOD WORK! 
    #we have now calculated all the drivers. We will rename them and put them in one dataframe with a time variable and the ratio between other eyars and base years in total energy,  then we are done!
    drivers_df = activity_driver.copy()
    drivers_df = drivers_df.merge(first_structural_level_structural_driver, on=time_variable)
    for structure_variable in structure_variables_list[1:]:
        structure_variable_index = structure_variables_list.index(structure_variable)
        drivers_df = drivers_df.merge(successive_structural_level_drivers_dict[structure_variable_index], on=time_variable)

    #now calculate the ratio between other eyars and base years in total energy
    mult_change = energy_data.groupby([time_variable])[energy_variable].sum().reset_index()
    #separate the base year and other years
    energy_base_year = mult_change[mult_change[time_variable]==base_year]
    energy_other_years = mult_change[mult_change[time_variable]!=base_year]
    #merge the two together
    mult_change = energy_other_years.copy()
    mult_change['energy_base_year'] = energy_base_year[energy_variable].values[0]
    #calc the ratio
    mult_change['energy_mult_change'] = mult_change[energy_variable]/mult_change['energy_base_year'] 

    #merge the drivers with the ratio
    drivers_df = drivers_df.merge(mult_change[[time_variable, 'energy_mult_change']], on=time_variable)

    #rename the columns
    drivers_df = drivers_df.rename(columns={'activity_driver': '{}'.format(activity_variable), 'first_structural_level_structural_driver': '{}'.format(structure_variables_list[0]),'energy_mult_change': 'Multiplicative change in {}'.format(energy_variable)})

    for structure_variable in structure_variables_list[1:]:
        structure_variable_index = structure_variables_list.index(structure_variable)
        drivers_df = drivers_df.rename(columns={'intensity_driver_{}'.format(str(structure_variable_index)): '{} intensity'.format(structure_variable), 'structural_driver_{}'.format(str(structure_variable_index)): '{}'.format(structure_variable)})

    #add effect to the end of all names except 'Multiplicative change in {}'.format(energy_variable) and Year
    drivers_df.columns = [col + ' effect' if col not in ['Multiplicative change in {}'.format(energy_variable), time_variable] else col for col in drivers_df.columns]

    #for ease of use we didnt remove the intensity drivers for all structural variables except the last one. Now we will remove them.
    for structure_variable in structure_variables_list[1:-1]:
        drivers_df = drivers_df.drop(['{} intensity effect'.format(structure_variable)], axis=1) 
    #and then move the last one to one from the end of the df by popping it then inserting it
    drivers_df.insert(len(drivers_df.columns)-2, '{} intensity effect'.format(structure_variables_list[-1]), drivers_df.pop('{} intensity effect'.format(structure_variables_list[-1])))

    #check that the product of drivers in each year is equal to the percent change in energy
    drivers_list = drivers_df.columns.tolist()
    drivers_list.remove('Multiplicative change in {}'.format(energy_variable))
    drivers_list.remove(time_variable)

    drivers_df['product'] = drivers_df[drivers_list].product(axis=1)
    drivers_df['difference'] = drivers_df['product'] - drivers_df['Multiplicative change in {}'.format(energy_variable)]
    total_difference = drivers_df['difference'].sum().sum()
    if abs(total_difference) > 0.01:
        breakpoint()#this started happening in 25th september. dont know why
        print('WARNING: The product of the hierarchical multiplicative drivers in each year for {} is not equal to the percent change in energy. The difference is {}. This seems to be a result of the input data, probably because the structure is inconsistent (i.e. certain structure variable categories are missing in certain years).'.format(extra_identifier,total_difference))
    #drop the product and difference columns
    drivers_df = drivers_df.drop(columns=['product', 'difference'])
    #now we are done. return drivers_df
    return drivers_df


# def convert_multiplicative_to_additive(multiplicative_output, energy_data,energy_variable, time_variable, extra_identifier):
#     #take in the multiplicative output and convert it to additive by timesing the effects by the energy data in the base year:
#     additive_output = multiplicative_output.copy()
#     drivers_list = additive_output.columns.tolist()
#     drivers_list.remove('Multiplicative change in {}'.format(energy_variable))
#     drivers_list.remove(time_variable)
#     base_year = energy_data[time_variable].min()
#     energy_data_sum = energy_data.groupby([time_variable])[energy_variable].sum().reset_index()
#     energy_base_year = energy_data_sum[energy_data_sum[time_variable]==base_year][energy_variable].values[0]
#     additive_output = additive_output.merge(energy_data_sum, on=time_variable)
    
#     for driver in drivers_list:
#         additive_output[driver] = (additive_output[driver] * energy_base_year)  - energy_base_year
#     additive_output['Additive change in {}'.format(energy_variable)] = (additive_output['Multiplicative change in {}'.format(energy_variable)] * energy_base_year) - energy_base_year
    
#     #test whether the sum of the additive effects is equal to the additive change in energy
#     additive_output['sum'] = additive_output[drivers_list].sum(axis=1)
#     additive_output['difference'] = additive_output['sum'] - additive_output['Additive change in {}'.format(energy_variable)]
#     total_difference = additive_output['difference'].sum().sum()
#     if abs(total_difference) > 0.01:
#         breakpoint()#this started happening in 25th september. dont know why
#         print('WARNING: The sum of the hierarchical additive drivers in each year for {} is not equal to the additive change in energy. The differences are {}'.format(extra_identifier,additive_output[[time_variable, 'Additive change in {}'.format(energy_variable), 'difference']].loc[additive_output['difference']!=0]))
#     #test whether the sum of effects plus base year energy is equal to the total energy
#     additive_output['sum'] = additive_output['sum'] + energy_base_year
#     additive_output['difference'] = additive_output['sum'] - additive_output[energy_variable]
#     total_difference = additive_output['difference'].sum().sum()
#     if abs(total_difference) > 0.01:
#         breakpoint()
#         print('WARNING: The sum of the hierarchical additive drivers in each year for {} is not equal to the total energy. The differences are {}'.format(extra_identifier,additive_output[[time_variable, energy_variable, 'difference']].loc[additive_output['difference']!=0]))
#     #drop the sum and difference columns
#     additive_output = additive_output.drop(columns=['sum', 'difference', energy_variable, 'Multiplicative change in {}'.format(energy_variable)])
    
#     return additive_output
    
def multiplicative_to_additive(base_value, multiplicative_effects):
    additive_effects = []
    current_value = base_value

    for effect in multiplicative_effects:
        new_value = current_value * effect  # Apply multiplicative effect
        additive_effect = new_value - current_value  # Calculate additive effect
        additive_effects.append(additive_effect)
        current_value = new_value  # Update current value for next iteration

    return additive_effects

def convert_multiplicative_to_additive(multiplicative_output, energy_data, activity_data, activity_variable, energy_variable, time_variable, extra_identifier):
    additive_output = multiplicative_output.copy()
    drivers_list = additive_output.columns.tolist()
    drivers_list.remove('Multiplicative change in {}'.format(energy_variable))
    drivers_list.remove(time_variable)
    
    base_year = energy_data[time_variable].min()
    energy_data_sum = energy_data.groupby([time_variable])[energy_variable].sum().reset_index()
    energy_base_year = energy_data_sum[energy_data_sum[time_variable] == base_year][energy_variable].values[0]
    activity_data_sum = activity_data.groupby([time_variable])[activity_variable].sum().reset_index()
    
    additive_output = additive_output.merge(energy_data_sum, on=time_variable, how='outer')
    additive_output = additive_output.merge(activity_data_sum, on=time_variable, how='outer')
    
    for index, row in additive_output.iterrows():
        multiplicative_effects = row[drivers_list].values
        additive_effects = multiplicative_to_additive(energy_base_year, multiplicative_effects)
        for driver, additive_effect in zip(drivers_list, additive_effects):
            additive_output.at[index, driver] = additive_effect
    
    additive_output['Additive change in {}'.format(energy_variable)] = additive_output[drivers_list].sum(axis=1)
    
    additive_output['difference'] = additive_output['Additive change in {}'.format(energy_variable)] - (additive_output[energy_variable] - energy_base_year)
    total_difference = additive_output['difference'].abs().sum()
    
    if total_difference > 0.01:
        print(f'WARNING: The sum of the hierarchical additive drivers in each year for {extra_identifier} is not equal to the total energy. The differences are {additive_output[[time_variable, energy_variable, "difference"]].loc[additive_output["difference"] != 0]}')
    # Drop the unnecessary columns
    additive_output = additive_output.drop(columns=['difference', 'Multiplicative change in {}'.format(energy_variable)])
    # Rename Activity to 'Total_{}'.format(activity_variable) and energy to 'Total {}'.format(energy_variable)
    additive_output.rename(columns={energy_variable: 'Total {}'.format(energy_variable), activity_variable: 'Total_{}'.format(activity_variable)}, inplace=True)
    
    return additive_output





# def convert_multiplicative_to_additive(multiplicative_output, energy_data,activity_data,activity_variable, energy_variable, time_variable, extra_identifier):
#     # Deep copy to ensure the original dataframe is not modified
#     additive_output = multiplicative_output.copy()

#     # Identify the drivers
#     drivers_list = additive_output.columns.tolist()
#     drivers_list.remove('Multiplicative change in {}'.format(energy_variable))
#     drivers_list.remove(time_variable)

#     # Get the base year and the energy sum for the base year
#     base_year = energy_data[time_variable].min()
#     energy_data_sum = energy_data.groupby([time_variable])[energy_variable].sum().reset_index()
#     energy_base_year = energy_data_sum[energy_data_sum[time_variable] == base_year][energy_variable].values[0]
#     activity_data_sum = activity_data.groupby([time_variable])[activity_variable].sum().reset_index()

#     # Merge to get the energy_variable for each year
#     additive_output = additive_output.merge(energy_data_sum, on=time_variable)
#     additive_output = additive_output.merge(activity_data_sum, on=time_variable)
#     # Convert multiplicative effects to logarithmic scale
#     for driver in drivers_list:
#         additive_output[driver] = np.log(additive_output[driver])
#     additive_output['Log change in {}'.format(energy_variable)] = np.log(additive_output['Multiplicative change in {}'.format(energy_variable)])

#     # Sum the log effects
#     additive_output['sum'] = additive_output[drivers_list].sum(axis=1)
    
#     # Check the equality by comparing the sum of log effects to the log change in energy_variable
#     additive_output['difference'] = additive_output['sum'] - additive_output['Log change in {}'.format(energy_variable)]
#     total_difference = additive_output['difference'].abs().sum()
    
#     if total_difference > 0.01:
#         breakpoint()
#         print(f'WARNING: The sum of the hierarchical additive drivers in each year for {extra_identifier} is not equal to the additive change in energy. The differences are {additive_output[[time_variable, f"Log change in {energy_variable}", "difference"]].loc[additive_output["difference"] != 0]}')
    
#     # Convert the sum of log effects and the log change in energy_variable back to the original scale
#     additive_output['sum'] = np.exp(additive_output['sum']) * energy_base_year
#     additive_output['Additive change in {}'.format(energy_variable)] = np.exp(additive_output['Log change in {}'.format(energy_variable)]) * energy_base_year - energy_base_year
    
#     # Check the equality in the original scale
#     additive_output['difference'] = additive_output['sum'] - additive_output[energy_variable]
#     total_difference = additive_output['difference'].abs().sum()
    
#     if total_difference > 0.01:
#         breakpoint()
#         print(f'WARNING: The sum of the hierarchical additive drivers in each year for {extra_identifier} is not equal to the total energy. The differences are {additive_output[[time_variable, energy_variable, "difference"]].loc[additive_output["difference"] != 0]}')
    
#     breakpoint()
#     # Drop the unnecessary columns
#     additive_output = additive_output.drop(columns=['sum', 'difference', 'Multiplicative change in {}'.format(energy_variable), f'Log change in {energy_variable}'])
#     #rename Activity to 'Total_{}'.format(activity_variable) and energy to 'Total {}'.format(energy_variable)
#     additive_output.rename(columns={energy_variable: 'Total {}'.format(energy_variable), activity_variable: 'Total_{}'.format(activity_variable)}, inplace=True)
#     breakpoint()
#     return additive_output