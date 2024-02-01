#############################
#%%
import numpy as np
from PyLMDI import PyLMDI
import pandas as pd

def Lfun(yt,y0):
    if yt == y0:
        return 0
    else:
        return (yt-y0)/(np.log(yt) - np.log(y0))#(EiT-Ei0) / LnETi-lnE0i)

#--- Step2-4: LMDI decomposition analysis
def Add_function(Ct, C0, Xt, X0, Dates):
    """
    # LMDI = PyLMDI(Ct,C0,Xt,X0)
    # ans = LMDI.Add(Ct,C0,Xt,X0)
    """
    Delta_V_list = []#perhaps make this one of tose list dictionaries so we can track the year as well,m but keep it in order too.
    
    for year_index in range(len(Dates)-1):#get the numbert of years, minus the base year
    #now we have the index for the current yuear we are considering cvompatred to the base year
    #we can use this index to get the data for the current year

        Delta_V = [np.sum(Ct[year_index])-C0]
        for base_year_parameter, current_year_parameter in zip(X0, Xt[:, year_index]):
            temp = sum([ Lfun(Ct[year_index], C0) * np.log(current_year_parameter/base_year_parameter)])
            #temp =  ((EiT-Ei0) / LnETi-lnE0i) * (ln(SiT/Si0) #will this work for multiple sectors? I imagine it does, but im not sure how the sum function intercts

            #i think we will just need to make sure that when you feed the data in, this function can handle multiple effects at a time, and also when you give it the activity data you will need the same activity value (total for all sectors in that time period) for each sector. E.g if we have sectors x and y, then the activity data would be Q_x and Q_y, and the energy use would be E_x and E_y. So the input data for calculating activity effect would be Xt = [[Q_x+Q_y, Q_x+Q_y]] Vt=[E_x, E_y]]
            
            #sum? (∑A0T) ? #since we are using i sectors, we sum the results of the above calculation for temp to find the total effect?
            Delta_V.append(temp)  
        Delta_V_list.append(Delta_V)
    return Delta_V_list
    
def Mult_function(Ct, C0, Xt, X0, Dates):
    Delta_V_list = []#perhaps make this one of tose list dictionaries so we can track the year as well,m but keep it in order too.
    for year_index in range(len(Dates)-1):#get the numbert of years, minus the base year
        #now we have the index for the current yuear we are considering cvompatred to the base year
        #we can use this index to get the data for the current year
        Delta_V = [np.sum(Ct[year_index]) / C0]
        for base_year_parameter, current_year_parameter in zip(X0,Xt[:, year_index]):
            temp = sum([Lfun(Ct[year_index], C0)/Lfun(Ct[year_index], C0)*np.log(current_year_parameter/base_year_parameter)])
            Delta_V.append(np.exp(temp)) 
        Delta_V_list.append(Delta_V)

    return Delta_V_list

#%%
##############################################################################
#--- Step1: Input
#testing with data from the transport divisia for REF Freight
#for now i dont think it can handle calcualting the share of 
#im going to first try the ethod with all data for one sector 
#but then after wards i will use all sectors and try make that work

data = pd.read_csv('input_data/divisia_input.csv')

#manage input data
#input data will be a long dataframe with columns representing the variables
#the columns will be as so:
#Year, Emissions(or energy), Variable1, Variable2, ... etc.

years = data['Year']
emissions = data['Emissions']
variables = data[:, 2:]

base_year_emissions = emissions[0]
base_year_variables = variables[0]

other_year_emissions =  emissions[1:]
other_year_variables = variables[1:]

Yt = other_year_emissions
Y0 = base_year_emissions   
Xt = other_year_variables
X0 = base_year_variables

#now how to get data from Xt and X0 best?

#%%

#possible variables for now:
#structure:
#GDPi / GDP in year x eg. [[0.5, 0.5], [0.7, 0.3]] < but this wont go into the functions very well i dont expect?
Xt_all = [[0.5, 0.5], [0.7, 0.3], [0.2, 0.8]]
Xt = Xt_all[1:]
X0 = Xt_all[0]

Yt_all = [0.5, 0.6, 0.7]
Yt = Yt_all[1:]
Y0 = Yt_all[0]

Dates = [2017, 2018, 2019]

Delta_V_list = []#perhaps make this one of tose list dictionaries so we can track the year as well,m but keep it in order too.
    
for year_index in range(len(Dates)-1):#get the numbert of years, minus the base year
#now we have the index for the current yuear we are considering cvompatred to the base year
#we can use this index to get the data for the current year

    Delta_V = [np.sum(Yt[year_index])-Y0]
    for base_year_parameter, current_year_parameter in zip(X0, Xt[:, year_index]):
        temp = sum([ Lfun(Yt[year_index], Y0) * np.log(current_year_parameter/base_year_parameter)])
        #temp =  ((EiT-Ei0) / LnETi-lnE0i) * (ln(SiT/Si0) #will this work for multiple sectors? I imagine it does, but im not sure how the sum function intercts
        #sum? (∑A0T) ? #since we are using i sectors, we sum the results of the above calculation for temp to find the total effect?
        Delta_V.append(temp)  
    Delta_V_list.append(Delta_V)

#%%





Ct_all = [930, 970, 996] 
Ct = Ct_all[0:]#?or [1:]?   # Carbon emission from China's commercial buildings in 2018
C0 = Ct_all[0]   # Carbon emission from China's commercial buildings in 2017


Pt = [1395.38, 5]       # Population size in 2018
P0 =          # Population size in 2017 
gt = [64.52073987, 5]      # GDP per capita in 2018
g0 = 59.04367375      # GDP per capita in 2017
st = [0.521570193 , 5]     # industrial structure (G_s / G, which seems to be the proportion of GDP in the buildings industry) in 2018
s0 = 0.51892765       # industrial structure (G_s / G, which seems to be the proportion of GDP in the buildings industry) in 2017
it =[ 0.002743568, 5]      # economic efficiency (E / F, where E is energy use and f seems to be floor area?) in 2018
i0 = 0.002876626     # economic efficiency (E / F, where E is energy use and f seems to be floor area?) in 2017
et =[ 3.053397862, 5]      # energy consumption in 2018
e0 = 3.004500526      # energy consumption in 2017
kt =[ 2.02   , 5]          # total emissions factor in 2018
k0 = 2.07           # total emissions factor in 2017
    
Xt = np.array([Pt,gt,st,it,et,kt])
X0 = np.array([P0,g0,s0,i0,e0,k0])

#%%
#run functions
ans_mult = Mult_function(Yt, Y0, Xt, X0, years)
ans_add = Add_function(Yt, Y0, Xt, X0, years)

#%%
# --- Step 5: Output
print("Multiplicative: \nThe change of carbon emission of US's commercial buildings from {0} to {1} is: ".format(Dates[0], Dates[-1]), '???')

print("The various driving forces contribute as follows: ")
print("??energy?: ",ans_mult[-1][0])
print("P: ",ans_mult[-1][1])
print("g: ",ans_mult[-1][2])
print("s: ",ans_mult[-1][3])
print("i: ",ans_mult[-1][4])
print("e: ",ans_mult[-1][5])
print("K: ",ans_mult[-1][6])

###############################################

print("Additive: \nThe change of carbon emission of US's commercial buildings from {0} to {1} is: ".format(Dates[0], Dates[-1]), '???')

print("The various driving forces contribute as follows: ")
print("??energy?: ",ans_add[-1][0])
print("P: ",ans_add[-1][1])
print("g: ",ans_add[-1][2])
print("s: ",ans_add[-1][3])
print("i: ",ans_add[-1][4])
print("e: ",ans_add[-1][5])
print("K: ",ans_add[-1][6])

#%%
#############################################################
#now check how the time series of multiplicative data output ends up compared to virans spreadsheet:
#So ans_mult[-1][2] should be equal to (ans_add[-1][2] + c0) / c0
x = (ans_add[-1][2] + C0) / C0
y = ans_mult[-1][2]
print('x', x, 'y', y)