# Testing simlation of generating random points 
from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA

def create_random_point(x0,y0,distance):
    """
            Utility method for simulation of the points
    """   
    r = distance/ 111300
    u = np.random.uniform(0,1)
    v = np.random.uniform(0,1)
    w = r * np.sqrt(u)
    t = 2 * np.pi * v
    x = w * np.cos(t)
    x1 = x / np.cos(y0)
    y = w * np.sin(t)
    return (x0+x1, y0 +y)







fig = plt.figure()
ax = host_subplot(111, axes_class=AA.Axes)

#ax.set_ylim(76,78)
#ax.set_xlim(13,13.1)
ax.set_autoscale_on(True)

latitude1,longitude1 =-25.28646, -57.647
ax.plot(latitude1,longitude1,'ro')

for i in range(1,200):
    x,y = create_random_point(latitude1,longitude1 ,500 )
    ax.plot(x,y,'bo')
    


plt.show()