#############################
#%%

import pandas as pd

def Lfun(yt,y0):
    if yt == y0:
        return 0
    else:
        return (yt-y0)/(np.log(yt) - np.log(y0))#(EiT-Ei0) / LnETi-lnE0i)

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
            

#%%

#insert pre-fomatted data here














#%%
Xt_ = [[200,300],[0.5,0.2],[3,5]]
X0_= [[100,150],[0.25,0.1],[1.5,2.5]]
Vt_= [300,300]
V0_ = [37.5,37.5]
#in the data above: there are two sectors since there are two entries of energy use
#there are therefgore three variables?
#var 1 = act
#var 2 = ?
#var 3 = ?

Xt_ = np.array(Xt_)
X0_= np.array(X0_)
Vt_= np.array(Vt_)
V0_= np.array(V0_)


LMDI = PyLMDI(Vt_,V0_,Xt_,X0_)


ans = LMDI.Add()
print(ans)
# [525.0, 175.0, 175.0, 175.0]

ans1 = LMDI.Mul()
print(ans1)

# [8.0, 2.0, 2.0, 2.0]

# for start, end in zip(X0_, Xt_):
#     print(start, 'end', end)
# [100. 150.] end [200. 300.]
# [0.25 0.1 ] end [0.5 0.2]
# [1.5 2.5] end [3. 5.]    
# %%

#--- Step1: Input
Ct = 794.6119504871361     # Carbon emission from China's commercial buildings in 2018
C0 = 761.984276581356     # Carbon emission from China's commercial buildings in 2017

Pt = 1395.38          # Population size in 2018
P0 = 1390.08          #                 in 2017 
gt = 64.52073987      
g0 = 59.04367375
st = 0.521570193
s0 = 0.51892765
it = 0.002743568
i0 = 0.002876626
et = 3.053397862
e0 = 3.004500526
kt = 2.02
k0 = 2.07


Ct,C0 = [Ct],[C0]

Xt = np.array([Pt,gt,st,it,et,kt]).reshape([-1,1])
X0 = np.array([P0,g0,s0,i0,e0,k0]).reshape([-1,1])

#--- Step2-4: LMDI decomposition analysis

LMDI = PyLMDI(Ct,C0,Xt,X0)
ans = LMDI.Add()


# --- Step 5: Output

print("The change of carbon emission of China's commercial buildings from 2017 to 2018 is: ",ans[0])

print("The various driving forces contribute as follows:")

print("P: ",ans[1])
print("g: ",ans[2])
print("s: ",ans[3])
print("i: ",ans[4])
print("e: ",ans[5])
print("K: ",ans[6])


# The change of carbon emission of China's commercial buildings from 2017 to 2018 is:  32.62767390578017
# The various driving forces contribute as follows:
# P:  2.9613642210015874
# g:  69.03218170760294
# s:  3.9527028782313187
# i:  -36.85387876903687
# e:  12.56275828546528
# K:  -19.027454417484062

# for start, end in zip(X0, Xt):
#     print(start, 'end', end)
# [1390.08] end [1395.38]
# [59.04367375] end [64.52073987]
# [0.51892765] end [0.52157019]
# [0.00287663] end [0.00274357]
# [3.00450053] end [3.05339786]
# [2.07] end [2.02]
# %%

#TEST

Xt_ = [[48+72,48+72],[0.4,0.6],[2.5,0.375]]
X0_= [[20+80, 20+80],[0.2, 0.8],[3,0.5]]
Vt_= [120,27]
V0_ = [60,40]
#in the data above: there are two sectors since there are two entries of energy use
#there are therefgore three variables?
#var 1 = act
#var 2 = ?
#var 3 = ?

Xt_ = np.array(Xt_)
X0_= np.array(X0_)
Vt_= np.array(Vt_)
V0_= np.array(V0_)


LMDI = PyLMDI(Vt_,V0_,Xt_,X0_)


ans = LMDI.Add()
print(ans)
# [525.0, 175.0, 175.0, 175.0]

ans1 = LMDI.Mul()
print(ans1)

# %%
