#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 11 16:59:03 2021

@author: peter
"""

import tellurium as te
import roadrunner as rr
import pandas as pd

antStr="""
model test_model()
    var A
    var B
    
    B = A
    
    R1: A->; AB
    R2: ->A; 1
    R3: B->; B
    R4: ->B; A
    # dA/dt=1-AB=0
    # dB/dt=A-B=0
    # A = 1/B
    # B=A
    A = 1/B;
    B = A;

end
"""

r = te.loada(antStr)

#r["init(A)"]=2
#r.resetAll()
print(r["A"])
print(r["B"])