import matplotlib.pyplot as plt 
  
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

for i in range(num_rect):
    coords.append(current_x+rect_distance*counter)
    counter+=1

coordCount=0
for coord in range(num_rect):
    ax.add_patch(matplotlib.patches.Rectangle((coords[coordCount],0),rect_distance,10*(1+0.05*coordCount),color='red'))
    coordCount+=1
    
plt.xlim([0, 100]) 
plt.ylim([-10, 100]) 
  
plt.show() 
