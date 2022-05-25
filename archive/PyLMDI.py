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
            
        
        
        
        
        
        