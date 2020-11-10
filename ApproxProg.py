import matplotlib.pyplot as plt 
import matplotlib
from mpmath import *
import numpy as np
import sys
  
def figurePlot():
    fig = plt.figure() 
    ax = fig.add_subplot(111) 

    function = input('What function would you like to estimate the integral of?\n')
    typeOfRule = input('\nWhat type of rule would you like to estimate the integral with? Righthand(R), Lefthand(L), or Midpoint(M)?\n')
    num_rect = int(input('\nHow many rectangles would you like to approximate the integral with?\n'))
    bounds = input('\nInput the lower and upper bounds of the integrable region in the form [a,b]:\n')
    lower_bound = int(bounds.split(',')[0][1:])
    upper_bound = int(bounds.split(',')[1][:-1])
    rect_distance = (upper_bound-lower_bound)/num_rect
    current_x = lower_bound
    counter=0
    coords = []
    sumApprox = 0
    x_points = np.array(list(decimalRange(lower_bound,upper_bound, (upper_bound-lower_bound)/1000)),dtype=float)

    for i in range(num_rect):
        coords.append(current_x+rect_distance*counter)
        counter+=1
        
    if typeOfRule == 'R':
        coords = rightHandRule(coords,rect_distance)
        
    elif typeOfRule == 'M':
        coords = midPointRule(coords,rect_distance)
        
    else:
        print('You didn\'t input a recognizable rule, so this will be approximated via the left_hand rule.\n')
        
    typeOfRule='Righthand' if typeOfRule=='R' else('Lefthand' if typeOfRule=='L' else 'Midpoint')
    
    y = np.array([eval(cleanup(function)) for x in coords],dtype=float)
    y_points = np.array([eval(cleanup(function)) for x in x_points],dtype=float)
    
    coordCount=0
    for coord in range(num_rect):
        ax.add_patch(matplotlib.patches.Rectangle((coords[coordCount],0),rect_distance,y[coordCount],color='red'))
        sumApprox+=rect_distance*y[coordCount]
        coordCount+=1

    plt.xlim(lower_bound -(0.05)*abs(lower_bound),upper_bound + 0.05*abs(upper_bound)) 
    
    if max(y) + 1 < 0:
        plt.ylim(min(y)-1,0.5)
        
    elif min(y)-1 > 0:
        plt.ylim(-0.5,max(y)+1)
        
    else:
        plt.ylim(min(y)-1,max(y)+1)
        
    plt.ylabel('Y Values')
    plt.xlabel('X Values')
    plt.plot(x_points,y_points)

    plt.show() 

    print('Estimated Sum using '+typeOfRule+' rule: '+str(sumApprox))
    repeat = input('Would you like to estimate another function?')
    
    if repeat==('Yes' or 'Y' or 'y' or 'yes'):
        figurePlot()
        
    else:
        print('Thank you and goodbye.')
        try:
            sys.exit()
        except:
            pass

def cleanup(function):
    if '^' in function:
        function=function.replace('^','**')
        
    return function

def decimalRange(start, stop, step=1.0):
    i = start
    while i < stop:
        yield i
        i += step
    
def rightHandRule(coords,rect_length):
    coords = [x+rect_length for x in coords]
    return coords

def midPointRule(coords,rect_length):
    coords = [x+rect_length/2 for x in coords]
    return coords
