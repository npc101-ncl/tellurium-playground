#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 13:27:01 2021

@author: peter
"""

import tellurium as te
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import SBstoat as SBS
import os

antStr="""
model test_model()
    var A
    var B
    
    R1: B->A; k1*B
    R2: A->B; k2*A
    
    A = 0.5;
    B = 0.5;
    
    #k1 := sin(time)+3;
    k1 = 3;
    k2 = 3;

end
"""

duration = 3.14*10

r = te.loada(antStr)
selections = ['time'] + r.getBoundarySpeciesIds() + r.getFloatingSpeciesIds()
r.simulate(0, duration, 100)
r.plot()
r.resetToOrigin()
r.A = 0
r.B = 1
r.simulate(0, duration, 100)
r.plot()
r.A = 1
r.B = 0
r.simulate(0, duration, 100)
r.plot()

"""
dA/dt=k1 B-k2 A=0
dB/dt=k2 A-k1 B=0

k1 B=k2 A
B=k2*A/k1
k2*A-k2*A=0
"""