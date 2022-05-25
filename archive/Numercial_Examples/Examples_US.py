



# =============================================================================
# Step1: Input
# =============================================================================
import numpy as np
from PyLMDI import PyLMDI

if __name__=='__main__':
    
    #--- Step1: Input
    Ct = 885.7759428080185  # Carbon emission from US's commercial buildings in 2018
    C0 = 866.6410668838769  # Carbon emission from US's commercial buildings in 2017
    
    Pt = 326.687501  # Population size in 2018
    P0 = 324.985538  #                 in 2017 
    gt = 62.99647129
    g0 = 60.0622225
    st = 0.768904032
    s0 = 0.771978857
    it = 0.005676565
    i0 = 0.005817767
    et = 7.392394794
    e0 = 7.352421075
    kt = 1.333927521
    k0 = 1.344564777
    
    
    Ct,C0 = [Ct],[C0]
    
    Xt = np.array([Pt,gt,st,it,et,kt]).reshape([-1,1])
    X0 = np.array([P0,g0,s0,i0,e0,k0]).reshape([-1,1])
    
    #--- Step2-4: LMDI decomposition analysis
    
    
    LMDI = PyLMDI(Ct,C0,Xt,X0)
    ans = LMDI.Add()
    
    # --- Step 5: Output
    print("The change of carbon emission of US's commercial buildings from 2017 to 2018 is: ",ans[0])
    
    print("The various driving forces contribute as follows:")
    
    print("P: ",ans[1])
    print("g: ",ans[2])
    print("s: ",ans[3])
    print("i: ",ans[4])
    print("e: ",ans[5])
    print("K: ",ans[6])