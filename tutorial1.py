#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 13:27:01 2021

@author: peter
"""

# hey you over there. This is a comment
# first we need to load the libraries we will use

# this is tellurium the biological model simulation library
# for brevity we tell the code we want to call it just te
import tellurium as te
# this is pandas a library for working with data in tables
# we abbreviate it as pd
import pandas as pd
# this is seaborn a library for plotting graphs of large data sets
# we call it sns
import seaborn as sns
# this is matplotlib a lower level plotting library seaborn is built on
# we can use it to get more fine control over plots, we call it plt
import matplotlib.pyplot as plt
# this is sbstoat, it uses data to estimate the right value for model
# parameters, it's built on tellurium, we abbreviate it as SBS
import SBstoat as SBS
# this is os, a library for interacting with the operating system
# it can interact with the file system, its name is so short it
# doesn't make sense to abbreviate it
import os

# we create a string to define our model. using """ means we can
# get new line characters in the string just by moving to a new line
antStr="""
# comments in antimony look like this too
# so we define our model and give it a name
model test_model()
    # so we define some variables that we want to vary over time
    # this could be the concentration of a particular protein in a cell
    # or of mRNA or anything really
    var A
    var B
    
    # we also define some reactions
    # reactions start with a label then a : then reaction definition 
    # then a ; followed by a rate law
    
    # so the first reaction is called R1. ->A indicates A is created
    # out of nothing (no material is used up in the process). k1 is
    # the rate at which A is created.
    R1: ->A; k1
    
    # reaction R2 describes the destruction of A. A-> implies A is used up
    # but nothing is created. The rate law is k2*A*B which means the more
    # A and B there is the faster the reaction will go. If there is no A
    # no B no A is broken down. You could think about this as protein B
    # finding protein A and breaking it down.
    R2: A->; k2*A*B
    
    # R3 is the creation of B out of nothing. The reaction law is k3*A
    # which is to say all that is required for the creation of B is
    # some A. The more A the faster B is created.
    R3: ->B; k3*A
    
    # R4 is the break down of B which is only dependant on there being
    # some B to break down.
    R4: B->; k4*B
    
    # we need to set the initial values for the variables A and B
    A = 0;
    B = 0;
    
    # and we need to define the parameter values that control the 
    # reaction laws
    k1 = 1;
    k2 = 2;
    k3 = 3;
    k4 = 4;

# lastly we indicate we've finished defining the model
end
"""

# so we are going to simulate the model with tellurium but we need to
# do some setting up

# we define a simulation duration
duration = 2

# we ask tellurium to create a simulator for our model using the string we
# made as a reference
r = te.loada(antStr)
# we get the names of the variables (plus time) from the simulator
selections = ['time'] + r.getBoundarySpeciesIds() + r.getFloatingSpeciesIds()
# we ask the simulator to simulate 100 points between time 0 and the
# duration
r.simulate(0, duration, 100)
# the simulator remembers the points we asked it to simulate and now
# we can ask it to plot them.
r.plot()

# now we're going to do nine simulations looking at what would have
# happened if we stated with different values of A and B

# we ask pandas to make an empty table to hold the results
s = pd.DataFrame()

# this is a loop, actually it's a loop inside a loop.
# the outside loop goes through 3 steps and in each step the value of A
# will change to be 0, 0.5, 1 etc.
for A in [0, 0.5, 1]:
    # the inside loop will go round 3 times for each step of the outside
    # loop and the value of B will chance with each step of the inside
    # loop. from 0, 0.5 to 1. So 9 cases looked at in all, each with
    # a different combination of A&B. We have to tab in the code that
    # belongs to each loop because the computer assumes the loop ends
    # when the indentation ends.
    for B in [0, 0.5, 1]:
        # first we need to reset the simulator because it tends to
        # remember the state it was in at the end of the last simulation
        r.resetToOrigin()
        # we set the values of A and B in the simulator to match the values
        # of A and B defined in the loops.
        r.A = A
        r.B = B
        # we ask the simulator to simulate the model starting at the new
        # A and B values and output the points as an array (like a grid)
        # of numbers with the columns in the order the variables (and time)
        # appear in selections. We also ask pandas to convert the grid to
        # a table
        df = pd.DataFrame(r.simulate(0, duration, 100,
                                     selections=selections))
        # tables can have their columns and rows named so we name the
        # variable columns using selections
        df.columns=selections
        # columns can be addressed by using the [] notation. If you set a
        # column that doesn't exist yet it’s created. If you try to set a 
        # column with a single value it's copied into every entry in the
        # column. So basically here we're just making a record of what the
        # starting A and B values were
        df["A0"] = A
        df["B0"] = B
        # you can turn a number into a string with str() and join strings
        # together with +
        df["idx"] = str(A)+"-"+str(B)
        # we now join the new table of simulations to the s table that
        # we're going to use to keep track of all the simulation results
        # we set ignore_index to true to ensure the rows get renumbered
        s = pd.concat([s,df], ignore_index=True)
    # exiting the inner loop
# exiting the outer loop

# We're going to take the A and B columns and merge them into one column
# spread over twice as many rows. Pandas melt function will create a
# variable column containing A or B and a value column containsing the
# values that used to be in the A and B columns. We keep the time and
# A0 columns but the rest are removed. we only pass to melt rows where
# B0 is 0. When you put a column in an equality expression you get a
# collection of true or false values which when you feed them back into
# the table using [] filters out the rows where the equality expression
# is false
df = pd.melt(s[s["B0"]==0], id_vars=['time','A0'], value_vars=['A','B'])

# The lineplot function will add new curves from our new simulations over
# the previous plot. We have to tell seaborn which columns to use for the
# x and y axis but we also tell it to colure the curves based on the A or 
# B value in the variable column and vary the line style based on the
# initial A value
sns.lineplot(x="time", y="value", hue="variable", style="A0",
             data=df, legend=False)

# now we're going to try and take the data from the simulation data in s
# and try to use sbstoat to refind the values of k1, k2, k3 and k4.
# originally I intended to use all 9 simulations but it looks like
# sbstoat can only work with one time series at a time.

# we need to filter the data down to a single simulation and a more
# realistic number of points. we select only the first A=B=0 simulation
# rows and only the time, A and B columns
PEData = s[s["idx"]=="0-0"][["time","A","B"]]
# iloc allows is to select certain rows by number, ::10 indicates that 
# we want only every 10th row (2:40:10 would indicate every 10th row
# between 2 and 39)
PEData = PEData.iloc[::10]

# since we are going to write this data to a file we need to creat a path to 
# the file, since we'd like to put it in the same directory as our code we
# need to know where the file is the os library has a function to find this
# out at runtime
working_dir = os.path.abspath('')
# we need to add the file name on to the end of the directory path but the
# separator can vary between operating systems. The os library has a
# function that will add on a file name in an appropriate way.
PEFPath = os.path.join(working_dir, 'PEData.csv')
# we save the simulation data to a csv file with out including the row numbers
PEData.to_csv(PEFPath, index=False)

# if we start with a model where k1, k2, k3 and k4 are already set to the
# right values it wouldn't be very impressive. so we create a version where
# they're all set to 0.
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

# we ask sbstoat to give us a fitter set up to fit our revised model to the
# data in our csv file for the parameters k1 through k4.
fitter = SBS.ModelFitter(antStrB, PEFPath, ["k1", "k2", "k3", "k4"])
# we ask the fitter to actually try and fit the data and it saves its best
# guess internally
fitter.fitModel()

# we can get a report on how the fit went using the reportFit() function on
# the fitter. Putting it inside the print function makes sure it gets
# displayed on the console
print(fitter.reportFit())
# lastly we create a new set of plots based on simulating using the new
# values the fit has found.
fitter.plotFitAll()