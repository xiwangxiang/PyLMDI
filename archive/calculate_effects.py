#here we will calculate the effects of the different parameters
#so we will take in the data we created in the grooming_code
#and then insert it into the divisia method to get the effects out'
#%%
from PyLMDI import PyLMDI
import pandas as pd
import numpy as np

emissions_divisia = False
#load data in


#%%
if emissions_divisia:
    print('to do')
    #we will take in six diff data sets to insert into the divisia method
    #energy, activity, sturcture, energy intensity,fuel mix, emissions factor
else:
    #we are just taking in energy, activity, sturcture, energy intensity
    activity = pd.read_csv('intermediate_data/industry_activity.csv')
    structure = pd.read_csv('intermediate_data/industry_structure.csv')
    energy_intensity = pd.read_csv('intermediate_data/industry_energy_intensity.csv')

    energy = pd.read_csv('intermediate_data/industry_energy.csv')

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
    #     Xt.shape, X0.shape,  Yt.shape, Y0.shape (not transposed)
    # ((3, 11, 14), (3, 11), (1, 11, 14), (1, 11))

#%%
#TEST
#lets remove all years except two in the t dataframes
Xt = np.array([activity_wide_t.iloc[:,:2], structure_wide_t.iloc[:,:2], Energy_intensity_wide_t.iloc[:,:2]]).T
X0 = np.array([activity_wide_base, structure_wide_base, Energy_intensity_wide_base]).T
Vt = np.array([energy_wide_t.iloc[:,:2]]).T
V0 = np.array([energy_wide_base]).T

#TEST
#lets remove all years except one in the t dataframes
Xt = np.array([activity_wide_t.iloc[:,:1], structure_wide_t.iloc[:,:1], Energy_intensity_wide_t.iloc[:,:1]])
X0 = np.array([activity_wide_base, structure_wide_base, Energy_intensity_wide_base])
Vt = np.array([energy_wide_t.iloc[:,:1]])
V0 = np.array([energy_wide_base])


#%%
#now run divisia using whatever data we created as input (energy or emissions)

LMDI = PyLMDI(Vt, V0, Xt, X0)

#format output data by attaching our original indexes for year and sector to it, as well as labelling the effects

def Lfun(yt,y0):
    if yt == y0:
        return 0
    else:
        return (yt-y0)/(np.log(yt) - np.log(y0))#(EiT-Ei0) / LnETi-lnE0i)

def Add(self):
    Delta_V = [sum(Vt)-np.sum(V0)]#total change in energy for each year in t (so sum of energy in year t -  sum of enegry in year 0)
    for start, end in zip(X0, Xt):#this is going by year and zipping ?.. so each year is output as 
        temp = sum([ Lfun(Vt[i], V0[i]) * np.log(end[i]/start[i]) 
                    for i in range(len(start))])#this is going by sector
        Delta_V.append(temp)       
    return Delta_V

def Add_new(Vt, V0, Xt, X0):
    #data should have shape (YEAR_len, MEASURE_len,  SECTOR_len)
    #the aim of this function is to overhaul the one used in the original code so that it works for multiple years and sectors
    #first calculate change in total enegry for each year in t  
    for year_t_index in len(Vt):
        
        Delta_V = [np.sum(Vt)-np.sum(V0)]

ans = LMDI.Add()
print(ans)
# [525.0, 175.0, 175.0, 175.0]

ans1 = LMDI.Mul()
print(ans1)

# %%
 