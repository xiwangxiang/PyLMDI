#%%
from PyLMDI import PyLMDI
import pandas as pd
import numpy as np
import data_creation_functions 

#load data in

#import gdp data from excel
gdp_data = pd.read_excel('input_data/divisia-test-input-data.xlsx', sheet_name='ind_sectoral_gdp')
energy_data = pd.read_excel('input_data/divisia-test-input-data.xlsx', sheet_name='energy_use')

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

    energy = data_creation_functions.structure(energy_data)

    #remove the weird remnants of pd's annoyuing index system (i should just learn it tbh)
    activity = activity.drop(['Unnamed: 0'], axis=1)
    structure = structure.drop(['Unnamed: 0'], axis=1)
    energy_intensity = energy_intensity.drop(['Unnamed: 0'], axis=1)
    energy = energy.drop(['Unnamed: 0'], axis=1)
    # print(activity, structure, energy_intensity)

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
        

#%%

def Add(driver_input_data):
    

        
def Add(self):
    Delta_V = [sum(self.Vt)-np.sum(self.V0)]
    for start, end in zip(self.X0, self.Xt):
        temp = sum([ Lfun(self.Vt[i], self.V0[i]) * np.log(end[i]/start[i]) 
                    for i in range(len(start))])
        Delta_V.append(temp)       
    return Delta_V

    

    #now join alogehter again to make a dataframe with all the data we need
    #we will use this dataframe to pass to the divisia method
    #but during this we will also spearpatre the base year from the other subsequent years
    #so we will make a new dataframe with the base year 
    #and then a dataframe with the subsequent years

    structure_wide_base = structure_wide.iloc[:, 0]
    structure_wide_t = structure_wide.iloc[:, 1:]

    activity_wide_base = activity_wide.iloc[:, 0]
    activity_wide_t = activity_wide.iloc[:, 1:]

    Energy_intensity_wide_base = Energy_intensity_wide.iloc[:, 0]
    Energy_intensity_wide_t = Energy_intensity_wide.iloc[:, 1:]

    energy_wide_base = energy_wide.iloc[:, 0]
    energy_wide_t = energy_wide.iloc[:, 1:]

    Xt = np.array([activity_wide_t, structure_wide_t, Energy_intensity_wide_t]).T
    X0 = np.array([activity_wide_base, structure_wide_base, Energy_intensity_wide_base]).T

    Vt = np.array([energy_wide_t]).T
    V0 = np.array([energy_wide_base]).T


