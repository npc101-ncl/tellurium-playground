#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 11:11:23 2021

@author: peter
"""

import tellurium as te
import roadrunner as rr
from random import uniform

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
  piecewise(cubicRootsThreeMax(p, q),4*p^3+27*q^2<0,cubicRootsOnePGZ(p, q),p>0,cubicRootsOnePLZ(p, q),p<0,q^(1/3))
end

model test_model()
    var A
    
    R1: A->; A
    
    p = 1;
    q = 1;
    t = cubicRoots(p, q);
    A = t^3+p*t+q

end
"""

r = te.loada(antStr)

for _ in range(100):
    r.p = uniform(-1,1)
    r.q = uniform(-1,1)
    r.reset()
    print(r["A"])