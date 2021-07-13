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
    
    B = A
    
    R1: A->; A
    
    A = 1;
    B = A;

end
"""

r = te.loada(antStr)

r["init(A)"]=2
r.resetAll()
print(r["B"])