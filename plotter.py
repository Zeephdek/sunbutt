import matplotlib
import matplotlib.pyplot as plt 
import numpy as np

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

    def plotPaths(self):
        """
        Plots paths in 3d
        """
        self.fig=plt.figure(figsize=(16,9))
        fig = self.fig

        fig.suptitle("<3") 

        ax1=fig.add_subplot(111, projection='3d')
        ax1.set_title("Orbits")

        for i, body in enumerate(self.s.bodies):
            # print(body.pos_cart_arr[:,0])
            if body.name == "sun":
                ax1.plot3D(
                    body.pos_cart_arr[:,0], 
                    body.pos_cart_arr[:,1], 
                    body.pos_cart_arr[:,2], 
                    linewidth=5,
                    marker="o", markersize=5, color="orange"
                )
            elif body.name == "earth":
                ax1.plot3D(
                    body.pos_cart_arr[:,0], 
                    body.pos_cart_arr[:,1], 
                    body.pos_cart_arr[:,2], 
                    linewidth=0.3,
                    marker="o", markersize=0.3, color="blue"
                )

        set_axes_equal(ax1)

        ax1.set_xlabel("X")
        ax1.set_ylabel("Y")
        ax1.set_zlabel("Z")      


        fig.show()
        input()