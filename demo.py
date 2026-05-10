# -*- coding: utf-8 -*-
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
from PyLMDI import PyLMDI

Vt = [100,100]
V0 = [50,50]

Xt = [[200,300],[0.5,0.2],[3,5]]
X0 = [[100,150],[0.25,0.1],[1.5,2.5]]
Vt = [300,300]
V0 = [37.5,37.5]


Xt = np.array(Xt)
X0 = np.array(X0)
Vt = np.array(Vt)
V0 = np.array(V0)


LMDI = PyLMDI(Vt,V0,Xt,X0)


ans = LMDI.Add()
print(ans)


ans1 = LMDI.Mul()
print(ans1)
