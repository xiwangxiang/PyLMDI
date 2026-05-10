"""
_________________________________________________________

Python-LMDI (PyLMDI) source codes version 1.0 

Developed in Python(3.8)         

Author and programmer: Xiwang Xiang, Xin Ma, Zhili Ma*, and Minda Ma*

e-Mail: mzlmx@cqu.edu.cn; maminda@tsinghua.edu.cn 


Main paper: Python-LMDI: A tool for the index decomposition analysis
_________________________________________________________
"""


import numpy as np
from operation import Lfun

class PyLMDI():
    def __init__(self,Vt,V0,Xt,X0):
        self.V0 = V0
        self.Vt = Vt
        self.X0 = X0
        self.Xt = Xt
        
    def Add(self):
        Delta_V = [sum(self.Vt)-np.sum(self.V0)]
        for start, end in zip(self.X0, self.Xt):
            temp = sum([ Lfun(self.Vt[i], self.V0[i]) * np.log(end[i]/start[i]) 
                        for i in range(len(start))])
            Delta_V.append(temp)       
        return Delta_V

    def Mul(self):
        D_V = [sum(self.Vt) / np.sum(self.V0)]
        for start, end in zip(self.X0,self.Xt):
            temp = sum([Lfun(self.Vt[i], self.V0[i])/Lfun(sum(self.Vt),sum(self.V0))*np.log(end[i]/start[i])
                        for i in range(len(start))])
            D_V.append(np.exp(temp))            
        return D_V
            
        
        
        
# -*- coding: utf-8 -*-
#%%
"""
Created on Wed Oct 20 15:39:16 2021

@author: ASUS
"""
import numpy  as np
def Lfun(yt,y0):
    if yt == y0:
        return 0
    else:
        return (yt-y0)/(np.log(yt) - np.log(y0))
    
#%%
# =============================================================================
# Step1: Input
# =============================================================================
import numpy as np
from PyLMDI import PyLMDI

def Lfun(yt,y0):
    if yt == y0:
        return 0
    else:
        return (yt-y0)/(np.log(yt) - np.log(y0))

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
            temp = sum([ Lfun(Ct[year_index], C0) * np.log(base_year_parameter/current_year_parameter)])
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
            temp = sum([Lfun(Ct[year_index], C0)/Lfun(Ct[year_index],C0)*np.log(base_year_parameter/current_year_parameter)])
            Delta_V.append(np.exp(temp)) 
        Delta_V_list.append(Delta_V)

    return Delta_V_list

#%%

#--- Step1: Input
Dates = [2017, 2018, 2019]
Ct = [794.6119504871361,7]     # Carbon emission from China's commercial buildings in 2018
C0 = 761.984276581356   # Carbon emission from China's commercial buildings in 2017

Pt = [1395.38, 5]       # Population size in 2018
P0 =1390.08         # Population size in 2017 
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
ans_mult = Mult_function(Ct, C0, Xt, X0, Dates)

ans_add = Add_function(Ct, C0, Xt, X0, Dates)
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
#%%

#--- Step1: Input
Dates = [ 2017, 2018]
Ct = [885.7759428080185]  # Carbon emission from US's commercial buildings in 2018
C0 = 866.6410668838769  # Carbon emission from US's commercial buildings in 2017

Pt = [326.687501]  # Population size in 2018
P0 = 324.985538 #                 in 2017 
gt = [62.99647129]
g0 = 60.0622225
st = [0.768904032]
s0 =0.771978857
it = [0.005676565]
i0 =0.005817767
et = [7.392394794]
e0 =7.352421075
kt = [1.333927521]
k0 =1.344564777
    
Xt = np.array([Pt,gt,st,it,et,kt])
X0 = np.array([P0,g0,s0,i0,e0,k0])

ans = Mult_function(Ct, C0, Xt, X0, Dates)
ans = Add_function(Ct, C0, Xt, X0, Dates)

# --- Step 5: Output
print("The change of carbon emission of US's commercial buildings from {0} to {1} is: ".format(Dates[0], Dates[-1]), '???')

print("The various driving forces contribute as follows: ")
print("??energy?: ",ans[-1][0])
print("P: ",ans[-1][1])
print("g: ",ans[-1][2])
print("s: ",ans[-1][3])
print("i: ",ans[-1][4])
print("e: ",ans[-1][5])
print("K: ",ans[-1][6])

#%%
#MULT
print('\n Doing a scripted version of multiplicative function for testing: \n')
Delta_V_list = []#perhaps make this one of tose list dictionaries so we can track the year as well,m but keep it in order too.
for year_index in range(len(Dates)-1):#get the numbert of years, minus the base year
    #now we have the index for the current yuear we are considering cvompatred to the base year
    #we can use this index to get the data for the current year
    Delta_V = [np.sum(Ct[year_index]) / C0]
    for base_year_parameter, current_year_parameter in zip(X0,Xt[:, year_index]):
        temp = sum([Lfun(Ct[year_index], C0)/Lfun(Ct[year_index],C0)*np.log(base_year_parameter/current_year_parameter)])
        Delta_V.append(np.exp(temp)) 
    Delta_V_list.append(Delta_V)

# --- Step 5: Output
ans = Delta_V_list
print("The change of carbon emission of US's commercial buildings from {0} to {1} is: ".format(Dates[0], Dates[-1]), '???')

print("The various driving forces contribute as follows: ")
print("??energy?: ",ans[-1][0])
print("P: ",ans[-1][1])
print("g: ",ans[-1][2])
print("s: ",ans[-1][3])
print("i: ",ans[-1][4])
print("e: ",ans[-1][5])
print("K: ",ans[-1][6])



#ADD
Delta_V_list = []#perhaps make this one of tose list dictionaries so we can track the year as well,m but keep it in order too.

print('\n Doing a scripted version of multiplicative function for testing: \n')
for year_index in range(len(Dates)-1):#get the numbert of years, minus the base year
    #now we have the index for the current yuear we are considering cvompatred to the base year
    #we can use this index to get the data for the current year

    Delta_V = [np.sum(Ct[year_index])-C0]
    for base_year_parameter, current_year_parameter in zip(X0, Xt[:, year_index]):
        temp = sum([ Lfun(Ct[year_index], C0) * np.log(base_year_parameter/current_year_parameter)])
        Delta_V.append(temp)  
    Delta_V_list.append(Delta_V)

# --- Step 5: Output
ans=Delta_V_list
print("The change of carbon emission of US's commercial buildings from {0} to {1} is: ".format(Dates[0], Dates[-1]), '???')

print("The various driving forces contribute as follows: ")
print("??energy?: ",ans[-1][0])
print("P: ",ans[-1][1])
print("g: ",ans[-1][2])
print("s: ",ans[-1][3])
print("i: ",ans[-1][4])
print("e: ",ans[-1][5])
print("K: ",ans[-1][6])

#%%

run = False
if run:
        Delta_V = [sum(self.Vt)-np.sum(self.V0)]
    for start, end in zip(self.X0, self.Xt):
        temp = sum([ Lfun(self.Vt[i], self.V0[i]) * np.log(end[i]/start[i]) 
                    for i in range(len(start))])
        Delta_V.append(temp)  

    def Add(self):
        Delta_V = [sum(self.Vt)-np.sum(self.V0)]
        for start, end in zip(self.X0, self.Xt):
            temp = sum([ Lfun(self.Vt[i], self.V0[i]) * np.log(end[i]/start[i]) 
                        for i in range(len(start))])
            Delta_V.append(temp)       
        return Delta_V
    # def Add_func(Ct,C0,Xt,X0):
    #     Delta_V = [sum(Ct)-np.sum(C0)]
    #     for start, end in zip(X0, Xt):
    #         temp = sum([ Lfun(Ct[i], C0[i]) * np.log(end[i]/start[i]) 
    #                     for i in range(len(start))])
    #         Delta_V.append(temp)       
    #     return Delta_V

    Add_func(Ct,C0,Xt,X0)

    # --- Step 5: Output

    print("The change of carbon emission of China's commercial buildings from 2017 to 2018 is: ",ans[0])

    print("The various driving forces contribute as follows:")

    print("P: ",ans[1])
    print("g: ",ans[2])
    print("s: ",ans[3])
    print("i: ",ans[4])
    print("e: ",ans[5])
    print("K: ",ans[6])                                                 


    #try mult
    ans = LMDI.Mul()


    # --- Step 5: Output

    print("The change of carbon emission of China's commercial buildings from 2017 to 2018 is: ",ans[0])

    print("The various driving forces contribute as follows:")

    print("P: ",ans[1])
    print("g: ",ans[2])
    print("s: ",ans[3])
    print("i: ",ans[4])
    print("e: ",ans[5])
    print("K: ",ans[6])
    # %%

"""

import numpy as np
from operation import Lfun

class PyLMDI():
    # import numpy  as np
    #     def Lfun(yt,y0):
    #         if yt == y0:
    #             return 0
    #         else:
    #             return (yt-y0)/(np.log(yt) - np.log(y0))

    def __init__(self,Vt,V0,Xt,X0):
        self.V0 = V0
        self.Vt = Vt
        self.X0 = X0
        self.Xt = Xt
        
    def Add(self):
        Delta_V = [sum(self.Vt)-np.sum(self.V0)]
        for start, end in zip(self.X0, self.Xt):
            temp = sum([ Lfun(self.Vt[i], self.V0[i]) * np.log(end[i]/start[i]) 
                        for i in range(len(start))])
            Delta_V.append(temp)       
        return Delta_V

    def Mul(self):
        D_V = [sum(self.Vt) / np.sum(self.V0)]
        for start, end in zip(self.X0,self.Xt):
            temp = sum([Lfun(self.Vt[i], self.V0[i])/Lfun(sum(self.Vt),sum(self.V0))*np.log(end[i]/start[i])
                        for i in range(len(start))])
            D_V.append(np.exp(temp))            
        return D_V
"""
"""
for start, end in zip(X0, Xt):
    print('START: ', start, ', END: ', end)

Delta_V = [sum(Ct)-np.sum(C0)]
for start, end in zip(X0, Xt):
    temp1 = (Ct[i]-C0[i])/(np.log(Ct[i]) - np.log(C0[i]))
    temp2 = np.log(end[i]/start[i])

    temp = sum([ Lfun(Ct[i], C0[i]) * np.log(end[i]/start[i]) 
                for i in range(len(start))])
    Delta_V.append(temp)       

def Lfun(yt,y0):
    if yt == y0:
        return 0
    else:
        return (yt-y0)/(np.log(yt) - np.log(y0))
    
    """