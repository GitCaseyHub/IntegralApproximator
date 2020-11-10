import matplotlib.pyplot as plt 
import matplotlib
import mpmath
import numpy as np
import sys
  
def figurePlot():
    fig = plt.figure() 
    ax = fig.add_subplot(111) 

    function = input('What function would you like to estimate the integral of?\n')
    typeOfRule = input('\nWhat type of rule would you like to estimate the integral with? Righthand(R), Lefthand(L), Midpoint(M), or Trapezoid(T)?\n')
    num_rect = int(input('\nHow many bins would you like to approximate the integral with?\n'))
    bounds = input('\nInput the lower and upper bounds of the integrable region in the form [a,b]:\n')
    lower_bound = int(bounds.split(',')[0][1:])
    upper_bound = int(bounds.split(',')[1][:-1])
    rect_distance = (upper_bound-lower_bound)/num_rect
    current_x = lower_bound
    counter=0
    coords = []
    leftCoords = []
    rightCoords = []
    sumApprox = 0
    x_points = np.array(list(decimalRange(lower_bound,upper_bound, (upper_bound-lower_bound)/1000)),dtype=float)
    y_points = np.array([eval(cleanup(function)) for x in x_points],dtype=float)

    for i in range(num_rect):
        leftCoords.append(current_x+rect_distance*counter)
        rightCoords.append(current_x + rect_distance*(counter+1))
        coords.append(current_x+rect_distance*counter)
        counter+=1
    
    if typeOfRule == 'R':
        y = rightHandRule(coords,rect_distance,function)
        
    elif typeOfRule=='L':
        y = np.array([eval(cleanup(function)) for x in coords],dtype=float)
        
    elif typeOfRule == 'M':
        y = midPointRule(coords,rect_distance,function)
        
    elif typeOfRule == 'T':
        y = drawTrapezoids(leftCoords,rightCoords,rect_distance,function,ax)
        sumApprox+=y[len(y)-1]
        y = y[:-1]
    else:
        print('You didn\'t input a recognizable rule, so this will be approximated via the left_hand rule.\n')
        
    typeOfRule='Righthand' if typeOfRule=='R' else('Lefthand' if typeOfRule=='L' else ('Midpoint' if typeOfRule=='M' else 'Trapezoid'))
    
    if typeOfRule !='Trapezoid':
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
    repeat = input('Would you like to estimate another function?\n')
    
    if repeat=='yes':
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
    
def rightHandRule(coords,rect_length,function):
    coords = [x+rect_length for x in coords]
    return np.array([eval(cleanup(function)) for x in coords],dtype=float)

def midPointRule(coords,rect_length,function):
    coords = [x+rect_length/2 for x in coords]
    return np.array([eval(cleanup(function)) for x in coords],dtype=float)

def drawTrapezoids(leftCoords,rightCoords,rect_distance,function,ax):
    # Currently only works for all positive functions; issue with negative because left_eval and right_eval need to be reversed when drawing polygon in that situation
    counter=0
    currentSum=0
    y=[]
    for i in leftCoords:
        x=leftCoords[counter]
        left_eval = eval(cleanup(function))
        x=rightCoords[counter]
        right_eval = eval(cleanup(function))
        
        if left_eval > right_eval:
            y.append(left_eval)
            ax.add_patch(matplotlib.patches.Rectangle((rightCoords[counter],0),rect_distance,right_eval,color='red'))
            ax.add_patch(matplotlib.patches.Polygon([[leftCoords[counter],right_eval],[rightCoords[counter],right_eval],[leftCoords[counter],left_eval]],color='red'))
            currentSum+=(rightCoords[counter]-leftCoords[counter])*(right_eval)
        
        else:
            y.append(right_eval)
            ax.add_patch(matplotlib.patches.Rectangle((leftCoords[counter],0),rect_distance,left_eval,color='red'))
            ax.add_patch(matplotlib.patches.Polygon([[leftCoords[counter],left_eval],[rightCoords[counter],left_eval],[rightCoords[counter],right_eval]],color='red'))
            currentSum+=(rightCoords[counter]-leftCoords[counter])*(left_eval)

        currentSum+=(1/2)*abs(rightCoords[counter]-leftCoords[counter])*abs(right_eval-left_eval)
        counter+=1
    y.append(currentSum)
    return y
