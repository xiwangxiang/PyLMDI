#The details on the LMDI method which is quite complicated can be found here: https://drive.google.com/file/d/1wCd-S55JVrHoQwRV7w9qZSVxTlfiqGa8/view?usp=sharing
#in all of the following functions we use the term energy but it can also be emissions, as that capacbiltiy has been built into the code.
import pandas as pd
import numpy as np

def log_mean_func(energy_year_t, energy_base_year):
    """a part of the divisia method, this is the logarithmic mean function"""
    #have to use function on each row indvidually since we are doing conidtional on each cell, i think. Then we will add each row to the dataframe seqwuentially again
    log_mean = energy_year_t.copy()
    
    for row_i in range(len(energy_year_t)):#for each sector in the dataset, do:
        log_mean.iloc[row_i,:] = energy_year_t.iloc[row_i, :].apply(lambda col: 0 if (col == energy_base_year[row_i]).any() else (col-energy_base_year[row_i])/(np.log(col) - np.log(energy_base_year[row_i])))

    return log_mean

def log_mean_func_vectorised(energy_year_t_sum, energy_base_year_sum):
    """a part of the divisia method, this is the logarithmic mean function"""
    #have to use function on each row indvidually since we are doing conidtional on each cell, i think. Then we will add each row to the dataframe seqwuentially again
    log_mean = energy_year_t_sum.copy()

    log_mean = energy_year_t_sum.apply(lambda col: 0 if (col == energy_base_year_sum).any() else (col-energy_base_year_sum)/(np.log(col) - np.log(energy_base_year_sum)))

    return log_mean

def Add(driver_input_data, energy):
    """this version of the funciton in pylmdi will take in data for multiple years and sectors, but only one driver at a time
    Will assume that base year is the first year in the dataframe
    
    We will also calc enegry change since it is needed for the output. Unfortunately since this funciton is run once for very driver, this step will be needlessly repeated, but it's no harm done to return the smae number for each driver, i think."""
    ##PREP DATA:

    energy_base_year = energy.iloc[:, 0]
    energy_year_t = energy.iloc[:, 0:]
    driver_base_year  =  driver_input_data.iloc[:, 0]
    driver_t = driver_input_data.iloc[:, 0:]

    ##first calc the change in total enegry for each year compared to base year.
    #invovles summing up energy for all sectors, in each year
    change_energy = energy_year_t.apply(lambda col: col - energy_base_year)
    #sum up columns to get total cchange
    change_energy = change_energy.sum(axis=0)
    

    ##now apply divisia funcrtion to the data
    driver = log_mean_func(energy_year_t, energy_base_year) * driver_t.apply(lambda col: np.log(col/driver_base_year))
    driver = driver.sum(axis=0)

    return driver, change_energy

def Mult(driver_input_data, energy):
    ##PREP DATA:

    energy_base_year = energy.iloc[:, 0]
    energy_year_t = energy.iloc[:, 0:]
    driver_base_year  =  driver_input_data.iloc[:, 0]
    driver_t = driver_input_data.iloc[:, 0:]

    ##first calc the MULTIPLICATIVE change in total enegry for each year compared to base year.
    #invovles summing up energy for all sectors, in each year first
    energy_year_t_sum = energy_year_t.apply(lambda col: col.sum())
    energy_base_year_sum = energy_base_year.sum()
    #then do calculation on columns to get MULT cchange
    change_energy = energy_year_t_sum.apply(lambda col: col / energy_base_year_sum)

    ##now apply MULTIPLICATIVE divisia funcrtion to the data
    #one thing to note, is that we use the log_mean_func differently, you will see:
    log_mean_val_x = log_mean_func(energy_year_t, energy_base_year)
    log_mean_val_y = log_mean_func_vectorised(energy_year_t.sum(axis=0), energy_base_year.sum(axis=0))
    log_mean_val = log_mean_val_x.T.apply(lambda col: col / log_mean_val_y).T#transpose to get data in right shape, and then back

    driver = log_mean_val * driver_t.apply(lambda col: np.log(col/driver_base_year))

    driver = np.exp(driver.sum(axis=0))

    return driver, change_energy
