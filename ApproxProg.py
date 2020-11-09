import matplotlib.pyplot as plt 
import matplotlib
  
fig = plt.figure() 
ax = fig.add_subplot(111) 
  
num_rect = int(input('Num rects in approx?'))
bounds = input('Input bounds')
lower_bound = int(bounds.split(',')[0][1:])
upper_bound = int(bounds.split(',')[1][:-1])
rect_distance = (upper_bound-lower_bound)/num_rect
current_x = lower_bound
counter=0
coords = []
sumApprox = 0

for i in range(num_rect):
    coords.append(current_x+rect_distance*counter)
    counter+=1
y = [x**2 for x in coords]
coordCount=0
for coord in range(num_rect):
    ax.add_patch(matplotlib.patches.Rectangle((coords[coordCount],0),rect_distance,y[coordCount],color='red'))
    sumApprox+=rect_distance*y[coordCount]
    coordCount+=1
        
plt.xlim([lower_bound-5,upper_bound+5]) 
plt.ylim([min(y)-5,max(y)+5]) 
  
plt.show() 

print('Estimated Sum: '+str(sumApprox))
