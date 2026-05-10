# -*- coding: utf-8 -*-
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
    
    
# def Deltax_x():
    # 