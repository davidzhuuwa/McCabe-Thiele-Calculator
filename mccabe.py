# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 09:01:42 2019

This script is designed to calculate the minimum number of stages required for
a distillation column separating a binary mixture based on the reflux
ratio, relative volatility, feed and product compositions. A McCabe-Thiele 
figure is output as a result along with the minimum number of stages

Improvements in the future should see calculation of the minimum reflux ratio, 
multi-component distillation facets and use of the Fenske and Underwood equations.
It is assumed that the user has some background knowledge on the function of 
distillation columns.

@author: David Zhu
"""

import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
import debugpy as db 
from matplotlib.ticker import (MultipleLocator,AutoMinorLocator)

# Initial Feed Values
comp = [0.1153, 0.77863338, 0.1039495217, 4, 2.48, 1.1] 

class Composition:
    def __init__(self,feed,distillate,bottoms,reflux,volatility, feedquality):
        self.feed = feed
        self.distillate = distillate
        self.bottoms = bottoms
        self.reflux = reflux
        self.volatility = volatility
        self.feedquality = feedquality
        
    #Need conditional statements to catch 0<x<1, and xf<xd, xb<xf etc.

    def feed_quality_line(self):
         #Need to find where this stops in conjunction with rectifying and 
         # stripping line
        if self.feedquality>1:
            slopeQ = -self.feedquality/(1-self.feedquality)
            interceptQ = (1/(1-self.feedquality))*self.feed
            xQ = np.array(np.arange(self.feed,self.qline_ROL_intersect()[0],0.0001))
            yQ = slopeQ*xQ+interceptQ
        #need a case for q = 1
        elif self.feedquality ==1:
            xQ = [self.feed,self.feed]
            yQ = [self.feed,self.qline_ROL_intersect()[1]]
            
        else:
            slopeQ = -self.feedquality/(1-self.feedquality)
            interceptQ = (1/(1-self.feedquality))*self.feed
            xQ = np.array(np.arange(self.qline_ROL_intersect()[0],self.feed,0.0001))
            yQ = slopeQ*xQ+interceptQ
            
        return (xQ,yQ)
    #Determining the VLE curve
    def VLE(self):
        a = self.volatility
        x = np.array(np.arange(0,1,0.001))
        y = a*x/((a-1)*x+1) 
        return y
    
    def rectifying_line(self):
        slopeR = self.reflux/(self.reflux + 1)
        interceptR = 1/(self.reflux+1)*self.distillate
        x = np.array(np.arange(self.qline_ROL_intersect()[0],self.distillate,0.0001))
        y = slopeR*x + interceptR
        return (x,y)
    
    
    def qline_ROL_intersect(self):
        x2 = -self.reflux/(self.reflux+1)
        c2 = 1/(self.reflux+1)*self.distillate
        if self.feedquality == 1:
            C = [self.feed, -x2*self.feed+c2]
            return C
        else:
            x1 = self.feedquality/(1-self.feedquality)
            
            y1 =1
            y2 =1
            c1 = 1/(1-self.feedquality)*self.feed
            
            A = np.array([[x1,y1],[x2,y2]])
            B = np.array([c1,c2])
            C = np.linalg.solve(A,B)
            return C
    
    def stripping_line(self):
        slope_s = (self.qline_ROL_intersect()[1] - self.bottoms)/(
                self.qline_ROL_intersect()[0]-self.bottoms)
        x_s = np.array(np.arange(self.bottoms,self.qline_ROL_intersect()[0],0.0001))
        y_s = x_s * slope_s + self.bottoms*(1-slope_s)
        return (x_s,y_s)
        
#Calling sample fluid composition and column data
#Setting up the user interface
def extract_entry_fields():
    global comp # makes composition a global variable
    feed = e1.get()
    distillate = e2.get()
    bottoms = e3.get()
    reflux = e4.get()
    volatility = e5.get()
    quality = e6.get()
    result = [feed,distillate,bottoms,reflux,volatility,quality]
    comp = result

master = tk.Tk()


tk.Label(master, text="Feed Composition").grid(row=0)
tk.Label(master, text="Distillate Composition").grid(row=1)
tk.Label(master, text="Bottoms Composition").grid(row=2)
tk.Label(master, text="Reflux Ratio").grid(row=3)
tk.Label(master, text="Relative Volatility").grid(row=4)
tk.Label(master, text="Feed quality").grid(row=5)

e1=tk.Entry(master)
e2=tk.Entry(master)
e3=tk.Entry(master)
e4=tk.Entry(master)
e5=tk.Entry(master)
e6=tk.Entry(master)

# inserts default values for each property
e1.insert(10,comp[0]) #not sure why 10 is needed in first argument
e2.insert(10,comp[1])
e3.insert(10,comp[2])
e4.insert(10,comp[3])
e5.insert(10,comp[4])
e6.insert(10,comp[5])

# defines the location of the textboxes
e1.grid(row=0,column=1)
e2.grid(row=1,column=1)
e3.grid(row=2,column=1)
e4.grid(row=3,column=1)
e5.grid(row=4,column=1)
e6.grid(row=5,column=1)

master.title("McCabe-Thiele Calculator")
master.geometry("600x375")
# terminating the program setup
class HaltException(Exception):
    pass

def close_window_calculate():
    extract_entry_fields()
    master.destroy()

def terminate_program():
    try:
        master.destroy()
        raise HaltException("The program has been closed")
    except HaltException as h:
        print(h)
        exit()
        

tk.Button(master, 
          text='Quit', 
          command=terminate_program).grid(row=6, 
                                    column=0, 
                                    sticky=tk.W, 
                                    pady=4)
tk.Button(master, 
          text='Calculate', command=close_window_calculate).grid(row=6, 
                                                       column=1, 
                                                       sticky=tk.W, 
                                                       pady=4)

master.mainloop()

# Now the code below will set up the plot of the McCabe-Thiele Diagram
data = Composition(float(comp[0]),float(comp[1]),
                   float(comp[2]),float(comp[3]),
                   float(comp[4]),float(comp[5]))

# Todo - rewrite plotting code to be more OOP orientedl. 
fig = plt.figure(num=None, figsize=(12, 10), dpi=200, facecolor='w', edgecolor='k')
#fig,ax = plt.subplots(figsize=(12,10),dpi=80,facecolor='w',edgecolor='k')
# Set plot axes to have major ticks of 0.1, minor ticks of 0.02
#ax.xaxis.set_major_locator(MultipleLocator(0.1))
#ax.yaxis.set_major_locator(MultipleLocator(0.1))
#ax.xaxis.set_minor_locator(MultipleLocator(0.02))
#ax.yaxis.set_minor_locator(MultipleLocator(0.02))

plt.plot([0,1],[0,1]) # y = x line
plt.xlabel('x (liquid mole fraction)')
plt.ylabel('y (vapour mole fraction)')
#plt.plot([data.feed,data.feed +0.1],[data.feed,data.feedquality*
         #(data.feed+0.1)])
         
         
#Plotting the vertical bottoms, feed and distillate lines
plt.plot([data.bottoms,data.bottoms],[0,data.bottoms])
plt.plot([data.feed,data.feed],[0,data.feed])
plt.plot([data.distillate,data.distillate],[0,data.distillate])

# Plotting the VLE curve based on the volatility
plt.plot(np.array(np.arange(0,1,0.001)),data.VLE())

# Plotting the rectifying line
RL = data.rectifying_line()
plt.plot(RL[0],RL[1])

# Plotting the feed quality line
QL = data.feed_quality_line()
plt.plot(QL[0],QL[1])

# Plotting the stripping line
SL = data.stripping_line()
plt.plot(SL[0],SL[1])

# Plotting the number of stages
# Start with horizontal line at x_distillate, until it reaches intersect between
# VLE curve. Then draw vertical line untilit intersects with the ROL or SOL
# for x>x q-ROL intercept, should be ROL
# otherwise, for x<x q-ROL intercept, should be SOL (for vertical lines)

# Initial Horizontal Line
y_ini = data.distillate
x_ini = data.distillate
x_d = data.distillate
RV = data.volatility
x_end = y_ini/(RV*(-y_ini)+RV+y_ini)
plt.hlines(y_ini,x_end,x_ini,colors ="black")

# Initial vertical line
RR = data.reflux #reflux ratio
x_q = data.qline_ROL_intersect()[0] #x fraction where q-line and ROl intersect
y_q = data.qline_ROL_intersect()[1] #same but y-fraction
x_b = data.bottoms

count = 1

# Parameters for stripping line
m_strip = (y_q - x_b)/(x_q-x_b)
int_strip = x_b*(1-m_strip)

if x_end >= x_q: #stops at rectifying operating line
    y_end = ((RR)/(RR+1))*x_end + (1/(RR+1))*x_d
    
else: #stops at stripping line
    y_end = m_strip*x_end + int_strip

plt.vlines(x_end,y_end,y_ini,colors ="black") #syntax (xcoord, ymin, ymax)

# Looping through the remainder of the stages
while(x_end>=x_b):
    # Now plotting horizontal line in loop
    x_ini = x_end
    y_ini = y_end
    x_end = y_ini/(RV*(-y_ini)+RV+y_ini)
    plt.hlines(y_ini,x_end,x_ini, colors="black")

    # Plotting vertical line in loop
    if x_end >= x_q:
        y_end = ((RR)/(RR+1))*x_end + (1/(RR+1))*x_d
    else:
        y_end = m_strip*x_end+int_strip
    plt.vlines(x_end,y_end,y_ini,colors ="black")
    count +=1
plt.title(f'Minimum number of stages is {count}')
#plt.figure(num=None, figsize=(12, 10), dpi=200, facecolor='w', edgecolor='k')

print(f"Minimum number of stages required is {count}")
print("McCabe-Thiele Diagram is saved as 'McCabe.png' in working directory.")
fig.savefig("McCabe.png")
