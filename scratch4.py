#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 11:29:10 2022

@author: peter
"""

import tellurium as te
import roadrunner as rr
import pandas as pd
import sympy as sp

antStr="""
function cubicRootsThree(p, q, k)
  2*(-p/3)^(1/2)*cos(arccos((-3/p)^(1/2)*3*q/(2*p))/3-2*pi*k/3)
end

function cubicRootsOnePGZ(p, q)
  -2*(p/3)^(1/2)*sinh(arcsinh((3/p)^(1/2)*3*q/(2*p))/3)
end

function cubicRootsOnePLZ(p, q)
  -2*(abs(q)/q)*(-p/3)^(1/2)*cosh(arccosh(-3*abs(q)*(-3/p)^(1/2)/(2*p))/3)
end

function cubicRootsThreeMax(p, q)
  piecewise(piecewise(cubicRootsThree(p, q, 2), cubicRootsThree(p, q, 2) > cubicRootsThree(p, q, 1), cubicRootsThree(p, q, 1)), piecewise(cubicRootsThree(p, q, 2), cubicRootsThree(p, q, 2) > cubicRootsThree(p, q, 1), cubicRootsThree(p, q, 1)) > cubicRootsThree(p, q, 0), cubicRootsThree(p, q, 0))
end

function cubicRoots(p, q)
  piecewise(cubicRootsThreeMax(p, q),4*p^3+27*q^2<0,cubicRootsOnePGZ(p, q),p>0,cubicRootsOnePLZ(p, q),p<0,(-q)^(1/3))
end

model test_model()
    var A
    var Ap
    var B
    var Bp
    var C
    var Cp
    
    R1: A->Ap; k1*A
    R1: Ap->A; k2*Ap*Cp
    R3: B->Bp; k3*Cp*B
    R4: Bp->B; k4*Bp
    R5: C->Cp; k5*C/(1+k6*Bp+k7*Ap)+k8*C
    R6: Cp->C; k9*Cp
    
    Atot = 2;
    Bt = 2;
    Ct = 2;
    
    Cp  = 1;
    pk1 = k1*Atot;
    pk2 = k3*Bt;
    Ap  = pk1/(k1+k2*Cp);
    Bp  = pk2*Cp/(k3*Cp+k4);
    A   = Atot-Ap;
    B   = Bt-Bp;
    C   = Ct-Cp;
    
    k1 = 1;
    k2 = 1;
    k3 = 1;
    k4 = 1;
    k5 = 1;
    k6 = 1;
    k7 = 1;
    k8 = 1;
    k9 = 1;
end
"""

k1,k2,k3,k4,k5,k6,k7,k8,k9 = sp.symbols("k1,k2,k3,k4,k5,k6,k7,k8,k9")
pk1,pk2 = sp.symbols("pk1,pk2")
Ap,Bp,Cp = sp.symbols("Ap,Bp,Cp")
At,Bt,Ct = sp.symbols("At,Bt,Ct")
exprAp = pk1/(k1+k2*Cp)
exprBp = pk2*Cp/(k3*Cp+k4)
exprCeq = k5*(Ct-Cp)/(1+k6*Bp+k7*Ap)+k8*(Ct-Cp)-k9*Cp
exprCeq = exprCeq.subs(Ap,exprAp).subs(Bp,exprBp)
exprCeq = sp.together(exprCeq)
exprCeq = exprCeq.func(*[i for i in exprCeq.args 
                         if i.func!=sp.core.power.Pow])
exprCeq = sp.collect(sp.expand(exprCeq),Cp)
print(exprCeq)


r = te.loada(antStr)
r.simulate(0, 100, 100)
r.plot()