#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 10:28:41 2021

@author: peter
"""

import tellurium as te
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import SBstoat as SBS
import os
import random
import pickle

runName = "tor0"
varName = "fairdomTest"
RS= {}

working_dir = os.path.abspath('')
dataDir = os.path.join(working_dir, 'data', runName)
figDir = os.path.join(working_dir, 'figure', runName)
os.makedirs(dataDir, exist_ok = True)
os.makedirs(figDir, exist_ok = True)

antStr="""
model test_model()
    var A
    var B
    
    R1: ->A; k1
    R2: A->; k2*A*B
    R3: ->B; k3*A
    R4: B->; k4*B
    
    A = 0;
    B = 0;
    
    k1 = 1;
    k2 = 2;
    k3 = 3;
    k4 = 4;

end
"""

duration = 2

r = te.loada(antStr)
selections = ['time'] + r.getBoundarySpeciesIds() + r.getFloatingSpeciesIds()
r.simulate(0, duration, 100)
r.plot()

s = pd.DataFrame()

for A in [0, 0.5, 1]:
    for B in [0, 0.5, 1]:
        r.resetToOrigin()
        r.A = A
        r.B = B
        df = pd.DataFrame(r.simulate(0, duration, 100,
                                     selections=selections))
        df.columns=selections
        df["A0"] = A
        df["B0"] = B
        df["idx"] = str(A)+"-"+str(B)
        s = pd.concat([s,df], ignore_index=True)

df = pd.melt(s[s["B0"]==0], id_vars=['time','A0'], value_vars=['A','B'])

sns.lineplot(x="time", y="value", hue="variable", style="A0",
             data=df, legend=False)

idxCase = "0-0"
PEData = s[s["idx"]==idxCase][["time","A","B"]]
PEData = PEData.iloc[::10]

PEFPath = os.path.join(working_dir, 'PEData.csv')
PEData.to_csv(PEFPath, index=False)

antStrB="""
model test_model()
    var A
    var B
    
    R1: ->A; k1
    R2: A->; k2*A*B
    R3: ->B; k3*A
    R4: B->; k4*B
    
    A = 0;
    B = 0;
    
    k1 = 0;
    k2 = 0;
    k3 = 0;
    k4 = 0;
end
"""

estVar = ["k1", "k2", "k3", "k4"]

params = []
for i in range(3):
    r = te.loada(antStrB)
    for param in estVar:
        r[param] =  random.random()*10
    fitter = SBS.ModelFitter(r, PEFPath, estVar)
    fitter.fitModel()
    fitter.plotFitAll()
    plt.savefig(os.path.join(figDir, runName+"-"+varName+"-TC"+str(i)+".png"))
    r = fitter.getFittedModel()
    temp = {param:r[param] for param in estVar}
    temp['chisqr']=fitter.minimizerResult.chisqr
    temp['redchi']=fitter.minimizerResult.redchi
    temp['aic']=fitter.minimizerResult.aic
    temp['bic']=fitter.minimizerResult.bic
    params.append(temp)
params = pd.DataFrame(params)

f = open(os.path.join(dataDir, runName+"-"+varName+"-params.p") , mode='wb')
pickle.dump(params, f)
f.close()

RS["duration"]=duration
RS["antStr"]=antStr
RS["PEData"]=PEData
RS["idxCase"]=idxCase
RS["runName"]=runName

f = open(os.path.join(dataDir, "runSwitches.p") , mode='wb')
pickle.dump(RS, f)
f.close()