import matplotlib.pyplot as plt 
import matplotlib
from mpmath import *
import numpy as np
import sys
  
def figurePlot():
    # Creation of figure and subfigure for graphing the function and drawing rectangles/triangles
    fig = plt.figure() 
    ax = fig.add_subplot(111)
    function=''
    typeOfRule=''
    num_rect=''
    bounds=''
    try:
        # Getting input from user to approximate integrals
        while function=='':
            function = input('What function would you like to estimate the integral of?\n')
            if function=='':
                print('You entered nothing. Type in an actual function.\n')

        while typeOfRule=='':
            typeOfRule = input('\nWhat type of rule would you like to estimate the integral with? Righthand(R), Lefthand(L), Midpoint(M), or Trapezoid(T)?\n')
            if typeOfRule=='':
                print('You entered nothing. Type in an approximation technique.\n')

        while num_rect=='':
            num_rect = input('\nHow many bins would you like to approximate the integral with?\n')
            if num_rect=='':
                print('You entered nothing. Type in an appropriate number of bins to approximate with.\n')
        num_rect=int(num_rect)

        while bounds=='':
            bounds = input('\nInput the lower and upper bounds of the integrable region in the form [a,b]:\n')
            if bounds=='':
                print('You entered nothing. Type in appropriate bounds to approximate an integral over.\n')

        # Variables and calculations of variables to be used later
        lower_bound = float(bounds.split(',')[0][1:])
        upper_bound = float(bounds.split(',')[1][:-1])
        rect_distance = (upper_bound-lower_bound)/num_rect
        counter=0
        coords = []
        leftCoords = []
        rightCoords = []
        sumApprox = 0
        x_points = np.array(list(decimalRange(lower_bound,upper_bound, (upper_bound-lower_bound)/1000)),dtype=float)
        y_points = np.array([eval(cleanup(function)) for x in x_points],dtype=float)

        # Generating the x-coords for our rectangles
        for i in range(num_rect):
            leftCoords.append(lower_bound+rect_distance*counter)
            rightCoords.append(lower_bound + rect_distance*(counter+1))
            coords.append(lower_bound+rect_distance*counter)
            counter+=1

        # Modifying the y-values given the type of approx technique you want to use
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
            y = np.array(y,dtype=float)

        else:
            print('You didn\'t input a recognizable rule, so this will be approximated via the left_hand rule.\n')

        typeOfRule='Righthand' if typeOfRule=='R' else('Lefthand' if typeOfRule=='L' else ('Midpoint' if typeOfRule=='M' else 'Trapezoid'))
        print('\nPerfect. Now we will estimate the integral of '+function+' over the interval ['+str(lower_bound)+', '+str(upper_bound)+'] with '+str(num_rect)+' bins using the '+typeOfRule+' Rule.')

        # Plots the standard rectangles for left,right,mid rules
        if typeOfRule !='Trapezoid':
            coordCount=0
            for coord in range(num_rect):
                ax.add_patch(matplotlib.patches.Rectangle((coords[coordCount],0),rect_distance,y[coordCount],color='red'))
                sumApprox+=rect_distance*y[coordCount]
                coordCount+=1

        # Creates the bounds for the graph so all the important parts are visible
        plt.xlim(lower_bound -(0.05)*abs(lower_bound),upper_bound + 0.05*abs(upper_bound)) 

        if max(y) + 1 < 0:
            plt.ylim(min(y)-1,0.5)

        elif min(y)-1 > 0:
            plt.ylim(-0.5,max(y)+1)

        else:
            plt.ylim(min(y)-1,max(y)+1)

        # 'Beautifies' the graph
        plt.ylabel('y Values')
        plt.xlabel('x Values')
        plt.plot(x_points,y_points)
        plt.title('Graph of \''+function+'\'')
        plt.show() 

        print('Estimated Sum: '+str(sumApprox))
        repeat = input('Would you like to estimate another function?\n')

        if repeat=='yes':
            figurePlot()

        else:
            print('Thank you and goodbye.')
            try:
                sys.exit()
            except:
                pass
    except:
        try:
            print('An error has occurred and the program will be shutting down.')
            fig.clear()
            sys.exit()
        except:
            pass

# Def used to cleanup user input so the modules imported recognize the functions that are to be used
def cleanup(function):
    if '^' in function:
        function=function.replace('^','**')\
    
    types = ['arcsin','arccos','arctan','arcsec','arccsc','arccot']
    for item in types:
        if item in function:
            function = function.replace(item,'a'+item[3:])
    return function

# Used to create a LOT of points to graph the actual function so rectangles are visible next to a line function
def decimalRange(start, stop, step=1.0):
    i = start
    while i < stop:
        yield i
        i += step

# Creates x,y coords for right-hand rule
def rightHandRule(coords,rect_length,function):
    coords = [x+rect_length for x in coords]
    return np.array([eval(cleanup(function)) for x in coords],dtype=float)

# Creates x,y coords for mid-point rule
def midPointRule(coords,rect_length,function):
    coords = [x+rect_length/2 for x in coords]
    return np.array([eval(cleanup(function)) for x in coords],dtype=float)

# Creates the trapezoids used for estimation if the user wants to not use the first three rules
def drawTrapezoids(leftCoords,rightCoords,rect_distance,function,ax):
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
            if right_eval < 0:
                ax.add_patch(matplotlib.patches.Rectangle((leftCoords[counter],0),rect_distance,left_eval,color='red'))
                ax.add_patch(matplotlib.patches.Polygon([[leftCoords[counter],left_eval],[rightCoords[counter],left_eval],[rightCoords[counter],right_eval]],color='red'))
            
            else:
                ax.add_patch(matplotlib.patches.Rectangle((leftCoords[counter],0),rect_distance,right_eval,color='red'))
                ax.add_patch(matplotlib.patches.Polygon([[leftCoords[counter],right_eval],[rightCoords[counter],right_eval],[leftCoords[counter],left_eval]],color='red'))
            currentSum+=(rightCoords[counter]-leftCoords[counter])*(right_eval)
        
        else:
            y.append(right_eval)
            if left_eval < 0:
                ax.add_patch(matplotlib.patches.Rectangle((leftCoords[counter],0),rect_distance,right_eval,color='red'))
                ax.add_patch(matplotlib.patches.Polygon([[leftCoords[counter],right_eval],[rightCoords[counter],right_eval],[leftCoords[counter],left_eval]],color='red'))
            else:
                ax.add_patch(matplotlib.patches.Rectangle((leftCoords[counter],0),rect_distance,left_eval,color='red'))
                ax.add_patch(matplotlib.patches.Polygon([[leftCoords[counter],left_eval],[rightCoords[counter],left_eval],[rightCoords[counter],right_eval]],color='red'))
            currentSum+=(rightCoords[counter]-leftCoords[counter])*(left_eval)

        currentSum+=(1/2)*abs(rightCoords[counter]-leftCoords[counter])*abs(right_eval-left_eval)
        counter+=1
    y.append(currentSum)
    return y
