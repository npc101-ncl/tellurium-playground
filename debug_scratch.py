#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 17:07:22 2021

@author: peter
"""

import tellurium as te
import roadrunner as rr
import pandas as pd

antStr="""
model test_model()
    var A
    var D
    
    B := root(2,A)
    
    R1: A->; k1
    R2: ->D; 1/A
    
    A = 1;
    D = 0
    
    k1 = 1;
    C = 0;
    
    at (A<0): C=1

end
"""

duration = 2

"""
r = te.loada(antStr)
r.setIntegrator('euler')
selections = (['time'] + r.getBoundarySpeciesIds() +
              r.getFloatingSpeciesIds()) + r.getGlobalParameterIds()
outs = r.simulate(0, duration, 100, selections=selections)
r.plot()
r.getGlobalParameterIds()
"""

class modelDebugger:
    def __init__(self, antStr, nonNegVar=[], ceilingVar=[], ceiling=None,
                 errorRetVar="myDebugError", eventPrefix="myDebugEvent"):
        self.antStr = antStr
        self.conditions = []
        self.errorRetVar = errorRetVar
        self.eventPrefix = eventPrefix
        for myVar in nonNegVar:
            self.addCondition(variable=myVar, lessThan=0.0)
        if isinstance(ceiling,float):
            for myVar in ceilingVar:
                self.addCondition(variable=myVar, greaterThan=ceiling)
        
        
    def addCondition(self,variable=None,diferential=None,lessThan=None,
                     greaterThan=None, lessThanOrEqual=None,
                     greaterThanOrEqual=None, isDif=False, value=0,
                     canBeEqual=False, isGreaterThan=True):
        if (variable is not None) == (diferential is not None):
            return None
        elif diferential is not None:
            myVar = diferential
            myDif = True
        else:
            myVar = variable
            myDif = isDif
        myCount = [lessThan,greaterThan,lessThanOrEqual,greaterThanOrEqual]
        myCount = sum([i is not None for i in myCount])
        if myCount>1:
            return None
        elif myCount == 0:
            myValue = value
            myCBE = canBeEqual
            myIGT = isGreaterThan
        elif lessThan is not None:
            myValue = lessThan
            myCBE = False
            myIGT = False
        elif greaterThan is not None:
            myValue = greaterThan
            myCBE = False
            myIGT = True
        elif lessThanOrEqual is not None:
            myValue = lessThanOrEqual
            myCBE = True
            myIGT = False
        else:
            myValue = greaterThanOrEqual
            myCBE = True
            myIGT = True
        self.conditions.append({"var":myVar, "value":myValue,
                                "isDif":myDif,"canBeEqual":myCBE,
                                "isGreaterThan":myIGT})
    
    def genTrigStr(self,myCond):
        if myCond["isGreaterThan"]:
            symb = ">"
        else:
            symb = "<"
        if myCond["canBeEqual"]: 
            symb = symb+"="
        myVar = myCond["var"]
        if myCond["isDif"]: 
            myVar = myVar + "'"
        myStr = ("("+self.errorRetVar+"<=0.0) && " + 
                 "("+myVar+symb+str(myCond["value"])+")")
        return myStr
    
    def genEventLine(self,myCond,i):
        return (self.eventPrefix + str(i) +
                ": at (" + self.genTrigStr(myCond)+"): " +
                self.errorRetVar + "=" + str(i))
    
    def insertLines(self,theLines):
        antLines = self.antStr.splitlines()
        end = [i for i,l in enumerate(antLines) if l.strip()=="end"]
        if len(end)<=0:
            return False
        end = end[-1]
        begining = [i for i,l in enumerate(antLines)
                    if l.strip().startswith("model") and i<end]
        if len(begining)<=0:
            return False
        begining = begining[-1]
        for i in range(begining+1, end):
            if not antLines[i].isspace():
                for j in range(len(antLines[i]), 0, -1):
                    if antLines[i][:j].isspace():
                        break
                myindent = antLines[i][:j]
                break
        else:
            myindent = ""
        indentLines = [myindent+l for l in theLines]
        self.modAntStr = antLines[:end] + indentLines + antLines[end:]
        self.modAntStr = "\n".join(self.modAntStr)
        return True                
    
    def debug(self, start, end, intervals, isEular=False,
              overrides=None):
        newLines = [self.errorRetVar+" = 0"]
        for i, myCond in enumerate(self.conditions):
            newLines.append(self.genEventLine(myCond,i+1))
        if not self.insertLines(newLines):
            return None
        r = te.loada(self.modAntStr)
        """
        r.addParameter(self.errorRetVar, 0.0, True)
        for i, myCond in enumerate(self.conditions):
            r.addEvent(self.eventPrefix+str(i+1), False, 
                       self.genTrigStr(myCond), False)
            r.addEventAssignment(self.eventPrefix+str(i+1),
                                 self.errorRetVar, str(i+1.0), True)
        """
        if isEular:
            r.setIntegrator('euler')
        mySelections = ['time',self.errorRetVar]
        if isinstance(overrides,dict):
            for k,v in overrides.items():
                r[k]=v
        outs = r.simulate(start, end, intervals, selections=mySelections)
        for i in range(outs.shape[0]):
            if outs[i,1]>0:
                myCase = int(outs[i,1])
                if i==0:
                    between = [None,outs[i,0]]
                else:
                    between = [outs[i-1,0],outs[i,0]]
                myCond = self.conditions[myCase-1]
                if myCond["isGreaterThan"]:
                    symb = ">"
                else:
                    symb = "<"
                if myCond["canBeEqual"]: 
                    symb = symb+"="
                myVar = myCond["var"]
                if myCond["isDif"]: 
                    myVar = myVar + "'"
                caseStr = myVar+symb+str(myCond["value"])
                break
        else:
            myCase = 0
            between = [None,None]
            myCond = None
            caseStr = "no error condition detected"
        return {"ID":myCase,"timeFrame":between,
                "condition":myCond, "definition":caseStr}
    
myDebug = modelDebugger(antStr,nonNegVar=["A"], ceilingVar=["D"],
                        ceiling=5.0)

myOut = myDebug.debug(0, duration, 100, isEular=True)
print(myOut)