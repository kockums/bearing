# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Provides Math Utils
===================

...

Examples:
    ...

Attributes:
    ...

Todo:

Links:


"""


# Import | Futures
# […]

# Import | Standard Library
import math
# […]

# Import | Libraries
import numpy
import matplotlib.pyplot as pyplot
# […]

# Import | Local Modules
# […]



def plot(x,y,z,grid):
    """ """
    pyplot.figure()
    pyplot.imshow(grid, extent=(x.min(), x.max(), y.max(), y.min()))
    pyplot.hold(True)
    pyplot.scatter(x,y,c=z)
    pyplot.colorbar()



def map_plotter(maplist, voxel_min_x, voxel_max_x, voxel_min_y, voxel_max_y):
    for i in range(len(maplist)):
        img = Image.open(maplist[i].img_file)
        array = np.asarray(img)
        pyplot.subplot(2,2,i+1)
        pyplot.imshow(array, cmap = cm.Greys_r, extent = [voxel_min_x, voxel_max_x, voxel_min_y, voxel_max_y])
        pyplot.title("plot #: " + str(i))
    pyplot.ion()
    pyplot.show()
    sero_message_definition("maps plotted!")

def map_plotter3d(img_file):
    img = Image.open(img_file).convert('L')
    array = np.asarray(img)

    mydata = array[::1,::1]
    fig = pyplot.figure(facecolor='w')
    ax1 = fig.add_subplot(1,3,1)
    im = ax1.imshow(mydata,interpolation='nearest',cmap=pyplot.cm.jet)
    ax1.set_title('2D')

    ax2 = fig.add_subplot(1,3,2,projection='3d')
    x,y = np.mgrid[:mydata.shape[0],:mydata.shape[1]]
    ax2.plot_surface(x,y,mydata,cmap=pyplot.cm.jet,rstride=1,cstride=1,linewidth=0.,antialiased=False)
    ax2.set_title('3D')
    ax2.set_zlim3d(150,255)

    ax3 = fig.add_subplot(1,3,3,projection='3d')
    x,y = np.mgrid[:mydata.shape[0],:mydata.shape[1]]
    ax3.scatter3D(x,y,mydata, cmap=pyplot.cm.jet)
    ax3.set_title('3D')
    ax3.set_zlim3d(150,255)

    pyplot.show()

