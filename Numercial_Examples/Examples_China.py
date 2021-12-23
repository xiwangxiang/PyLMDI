



# =============================================================================
# Step1: Input
# =============================================================================
import numpy as np
from PyLMDI import PyLMDI

if __name__=='__main__':
    
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