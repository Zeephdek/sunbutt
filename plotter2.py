import matplotlib
import matplotlib.pyplot as plt 
import numpy as np

import os

import csv

import pandas as pd

from matplotlib import colors

bodynames = ["sun", "earth", "moon"]

def set_axes_equal(ax):
    '''Make axes of 3D plot have equal scale so that spheres appear as spheres,
    cubes as cubes, etc..  This is one possible solution to Matplotlib's
    ax.set_aspect('equal') and ax.axis('equal') not working for 3D.

    Input
      ax: a matplotlib axis, e.g., as output from plt.gca().
    '''

    x_limits = ax.get_xlim3d()
    y_limits = ax.get_ylim3d()
    z_limits = ax.get_zlim3d()

    x_range = abs(x_limits[1] - x_limits[0])
    x_middle = np.mean(x_limits)
    y_range = abs(y_limits[1] - y_limits[0])
    y_middle = np.mean(y_limits)
    z_range = abs(z_limits[1] - z_limits[0])
    z_middle = np.mean(z_limits)

    # The plot bounding box is a sphere in the sense of the infinity
    # norm, hence I call half the max range the plot radius.
    plot_radius = 0.5*max([x_range, y_range, z_range])

    ax.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
    ax.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])
    ax.set_zlim3d([z_middle - plot_radius, z_middle + plot_radius])

def turning_points(x, y, thresh = 1440000):

    dy = np.gradient(y)
    
    idx_thresh = np.argmax(dy > thresh)
    return x[idx_thresh:], y[idx_thresh:]

def turningPointsIneff(x, y):
    " the  shit recursive method "
    i = np.nditer(y, flags=["c_index"], op_flags=[["readwrite"]])
    prev = 0
    up = 1
    prev_up = 1
    
    res_x = []
    res_y = []

    for f in i:
        # force on x by y
        index = i.index
        if index != 0:
            if y[index] < prev:
                up = 0
            else:
                up = 1

            if up != prev_up:
                res_y.append(y[index])
                res_x.append(x[index])

            prev = y[index]
            prev_up = int(up)

    return res_x, res_y

def main():
    matplotlib.use("TKAgg", force=True)
    listoffiles = os.listdir("csv")
    
    listoffiles2 = [os.path.join("csv", a) for a in listoffiles]

    bodies = []

    for file in listoffiles2:
        df = pd.read_csv(file, header=None, index_col=False)
        bodies.append(df.to_numpy())

    # path plotting code
    
    fig=plt.figure(figsize=(12,9))

    fig.suptitle("<3") 

    ax1=fig.add_subplot(221, projection='3d')
    ax2=fig.add_subplot(222)
    ax3=fig.add_subplot(223)

    ax1.set_title("Orbits")
    ax2.set_title("Radii")
    ax3.set_title("Earth-Moon Distances")

    # calc distances
    l_vec = bodies[2] - bodies[1]
    length = np.sqrt(l_vec[:,0]**2+l_vec[:,1]**2+l_vec[:,2]**2)
    

    times = np.arange(0, len(bodies[0]))

    for i, body in enumerate(bodies):
        # print(body.pos_cart_arr[:,0])
        ax1.plot3D(
            body[:,0], 
            body[:,1], 
            body[:,2], 
            linewidth=0.3,
            marker="o", markersize=0.4, label=bodynames[i]
        )

        if i != 0:
            radius = np.sqrt(body[:,0]**2+ body[:,1]**2+ body[:,2]**2)
            ax2.plot(times, radius, label=bodynames[i])
    
    ax3.plot(times, length)
    ax3.set_xlabel("n")
    ax3.set_ylabel("Earth-Moon Distance/m")
    tp = turningPointsIneff(times, length)
    ax3.scatter(tp[0], tp[1], color='r', zorder=2)

    for i, x in enumerate(tp[0]):
        ax3.annotate(x, (tp[0][i], tp[1][i]))

    set_axes_equal(ax1)

    ax1.set_xlabel("X")
    ax1.set_ylabel("Y")
    ax1.set_zlabel("Z")    

    ax2.set_xlabel("n")  
    ax2.set_ylabel("r/m")  

    ax1.legend()
    ax2.legend()

    ## CALC ADDITIONAL DATA/


    fig.show()
    input()


if __name__ == "__main__":
    main()