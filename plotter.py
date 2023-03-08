import matplotlib
import matplotlib.pyplot as plt 
import numpy as np

from matplotlib import colors

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

class dataPlot():
    def __init__(self, system) -> None:
        self.s = system
        
        matplotlib.use("TKAgg", force=True)

        # and any other matplotlib configs.

    def plotData(self):
        self.fig=plt.figure(figsize=(16,9))
        fig = self.fig

        fig.suptitle("<3") 
        ax1=fig.add_subplot(121)
        ax2=fig.add_subplot(122)

        # print(self.s.bodies[1].acc_sphr_arr[:,0])
        # print(self.s.t_arr)
        ax1.plot(self.s.t_arr/24/3600, self.s.bodies[2].pos_sphr_arr[:,0])
        ax1.plot(self.s.t_arr/24/3600, self.s.bodies[1].pos_sphr_arr[:,0])
        ax2.plot(self.s.t_arr/24/3600, self.s.bodies[2].acc_sphr_arr[:,0])
        ax2.plot(self.s.t_arr/24/3600, self.s.bodies[1].acc_sphr_arr[:,0])
        # ax1.plot(self.s.bodies[2].pos_sphr_arr[:,0], self.s.bodies[2].acc_sphr_arr[:,0])

        ax1.set_xlabel("Time/Days")
        ax1.set_ylabel("r/m")
        ax2.set_xlabel("Time/Days")
        ax2.set_ylabel("a/ms-2")
        

        fig.show()
        input()

    def plotPaths(self):
        """
        Plots paths in 3d
        """
        with plt.rc_context({'axes.edgecolor':'white',
        'axes.titlecolor':'white',
        'axes.labelcolor':'white',
        'text.color':'white',
        'xtick.color':'white',
        'ytick.color':'white',
        'figure.facecolor':'black',
        }):
            self.fig=plt.figure(figsize=(16,9))
            fig = self.fig

            fig.suptitle("<3") 
            fig.patch.set_facecolor('black')

            ax1=fig.add_subplot(111, projection='3d')
            ax1.set_title("Orbits")
            ax1.set_facecolor('black')

            ax1.xaxis.pane.fill = False
            ax1.yaxis.pane.fill = False
            ax1.zaxis.pane.fill = False

            for i, body in enumerate(self.s.bodies):
                # print(body.pos_cart_arr[:,0])
                if body.name == "sun":
                    ax1.plot3D(
                        body.pos_cart_arr[:,0], 
                        body.pos_cart_arr[:,1], 
                        body.pos_cart_arr[:,2], 
                        linewidth=6,
                        marker="o", markersize=6, color="orange"
                    )
                elif body.name == "earth":
                    ax1.plot3D(
                        body.pos_cart_arr[:,0], 
                        body.pos_cart_arr[:,1], 
                        body.pos_cart_arr[:,2], 
                        linewidth=0.7,
                        marker="o", markersize=0.7, color="blue"
                    )
                else:
                    ax1.plot3D(
                        body.pos_cart_arr[:,0], 
                        body.pos_cart_arr[:,1], 
                        body.pos_cart_arr[:,2], 
                        linewidth=0.45,
                        marker="o", markersize=0.45
                    )

            set_axes_equal(ax1)

            ax1.set_xlabel("X")
            ax1.set_ylabel("Y")
            ax1.set_zlabel("Z")      


            fig.show()
            input()

    def superPlot(self):

        fig=plt.figure(figsize=(12,9))

        fig.suptitle("<3") 

        ax1=fig.add_subplot(221, projection='3d')
        ax2=fig.add_subplot(222)
        ax3=fig.add_subplot(223)

        ax1.set_title("Orbits")
        ax2.set_title("Radii")
        ax3.set_title("Earth-Moon Distances")

        # calc distances
        l_vec = self.s.bodies[1].pos_cart_arr - self.s.bodies[2].pos_cart_arr
        length = np.sqrt(l_vec[:,0]**2+ l_vec[:,1]**2+ l_vec[:,2]**2)

        for i, body in enumerate(self.s.bodies):
            # print(body.pos_cart_arr[:,0])
            if body.name == "sun":
                # continue
                ax1.plot3D(
                    body.pos_cart_arr[:,0], 
                    body.pos_cart_arr[:,1], 
                    body.pos_cart_arr[:,2], 
                    linewidth=0.1,
                    marker="o", markersize=6, color="orange", label=body.name
                )
            elif body.name == "earth":
                ax1.plot3D(
                    body.pos_cart_arr[:,0], 
                    body.pos_cart_arr[:,1], 
                    body.pos_cart_arr[:,2], 
                    linewidth=0.7,
                    marker="o", markersize=0.7, color="blue", label=body.name
                )
            else:
                ax1.plot3D(
                    body.pos_cart_arr[:,0], 
                    body.pos_cart_arr[:,1], 
                    body.pos_cart_arr[:,2], 
                    linewidth=0.45,
                    marker="o", markersize=0.45, label=body.name
                )

            if i != 0:
                radius = np.sqrt(body.pos_cart_arr[:,0]**2+ body.pos_cart_arr[:,1]**2+ body.pos_cart_arr[:,2]**2)
                ax2.plot(self.s.t_arr/24/3600, radius, label=body.name)

                tp = turningPointsIneff(self.s.t_arr/24/3600, radius)
                ax2.scatter(tp[0], tp[1], color='r', zorder=2)

                for i, x in enumerate(tp[0]):
                    ax2.annotate("{:.1f}".format(x), (tp[0][i], tp[1][i]))
        

        ax3.plot(self.s.t_arr/24/3600, length)
        ax3.set_xlabel("n")
        ax3.set_ylabel("Earth-Moon Distance/m")

        tp = turningPointsIneff(self.s.t_arr/24/3600, length)
        ax3.scatter(tp[0], tp[1], color='r', zorder=2)

        for i, x in enumerate(tp[0]):
            ax3.annotate("{:.1f}".format(x), (tp[0][i], tp[1][i]))

        set_axes_equal(ax1)

        ax1.set_xlabel("X")
        ax1.set_ylabel("Y")
        ax1.set_zlabel("Z")    

        ax2.set_xlabel("t/days")  
        ax2.set_ylabel("r/m")  

        ax1.legend()
        ax2.legend()

        ## CALC ADDITIONAL DATA/


        fig.show()
        input()

