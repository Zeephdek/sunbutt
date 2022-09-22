import numpy as np
import random as rand
import matplotlib.pyplot as plt 

"""
Well Reddit convinced me to go back to this old girl 
then gere goes with something where I don't need to care 
about memory architectures and stuff

I guess

     _______. __    __  .__   __. .______    __    __  .___________.___________.
    /       ||  |  |  | |  \ |  | |   _  \  |  |  |  | |           |           |
   |   (----`|  |  |  | |   \|  | |  |_)  | |  |  |  | `---|  |----`---|  |----`
    \   \    |  |  |  | |  . `  | |   _  <  |  |  |  |     |  |        |  |     
.----)   |   |  `--'  | |  |\   | |  |_)  | |  `--'  |     |  |        |  |     
|_______/     \______/  |__| \__| |______/   \______/      |__|        |__|     
                                                                                

"""

## spherical coordinate calculations

# debug mode ?

def getSphere(cart=(0,0,0)):
    """
    https://en.wikipedia.org/wiki/Spherical_coordinate_system#Conventions
    returns r, theta, phi (ISO), the latter 2 referring to elevation and azimuth
    cart should be a tuple (x,y,z)

    https://stackoverflow.com/questions/4116658/faster-numpy-cartesian-to-spherical-coordinate-conversion for non realtime use
    """
    if len(cart) == 2:
        print(cart)
        # and later it shall throw an error when its a np array
        cart.append(0)

    x, y, z = cart[0], cart[1], cart[2]
    r = np.sqrt(x * x + y * y + z * z)
    if r == 0:
        return (0,0,0)

    theta = np.arccos(z / r)
    phi = np.arctan2(y, x)

    return (r, theta, phi)

def getCart(sph=(0,0,0)):
    """
    sph is given in (r, theta, phi)
    returns (x, y, z)
    """

    r, theta, phi = sph[0], sph[1], sph[2]

    x = r * np.cos(phi) * np.sin(theta)
    y = r * np.sin(phi) * np.sin(theta)
    z = r * np.cos(theta)

    return (x, y, z)

def getDistance(a=[0,0,0], b=[0,0,0]):
    """
    distance between points a and b.
    DISTANCE. For simple uses.
    """

    return np.sqrt(
        (a[0]-b[0])**2 +
        (a[1]-b[1])**2 +
        (a[2]-b[2])**2
    )

class physicsObject():
    def __init__(self, pos=[0,0,0], vel=[0,0,0], mass=0, acc=[], force=[]) -> None:

        self.pos = np.array(pos + getSphere(pos)).astype("float64")
        self.vel = np.array(vel + getSphere(vel)).astype("float64")

        if acc == ():
            self.force = np.array(force + getSphere(force))
            self.acc = force / mass
        else:
            "acceleration overwrites anyway? Ig so so I dont fuck it up lol"
            self.acc = np.array(acc + getSphere(acc))
            self.force = self.acc * mass

        self.base_acc = np.array([self.acc[0], self.acc[1], self.acc[2]]).astype("float64") # base acceleration

        self.mass = mass
        self.ke = 0
        self.p = 0
        self.t = [0]
        self.gpe = self.calcGravitationalPotential()
        self.elastic_pe = 0 # elastic pe

        self.pos_np = np.array([self.pos]).astype("float64")
        self.vel_np = np.array([self.vel]).astype("float64")
        self.acc_np = np.array([self.acc]).astype("float64")
        self.force_np = np.array([self.force]).astype("float64")
        self.mass_np = np.array([self.mass]).astype("float64")
        self.ke_np = np.array([self.ke]).astype("float64")
        self.p_np = np.array([self.p]).astype("float64")
        self.gpe_np = np.array([self.gpe]).astype("float64")
        self.elastic_pe_np = np.array([self.p]).astype("float64")


        self.springs = []
        ## and other params

    class spring():
        def __init__(self, fixed_pos, unstretched_pos, k) -> None:
            """
            Horizontal / Vertical springs for now because I'm too tired to implement Pythagoras' Theorem 
            over here
            it should just use the spherical coords because that is easy, and the code is there to integrate it.

            k is the constant of proportionality
            fixed_pos is a 3d array giving the position where the spring is fixed.
            unstretched_pos is a 3d array giving the position where the spring connects to this object where its extension is zero
                this is called being lazy.
            """

            self.fixed_pos =  np.array(fixed_pos)
            self.unstretched_pos = np.array(unstretched_pos)
            self.base_length = self.unstretched_pos - self.fixed_pos # which should be correct
            self.k = k

        def simSpring(self, c_position):
            """
            all this needs from the other sim function is the current position of the object, 
            or rather where the spring is connected to it, in this case the exact same position.

            and really this just returns the force due to extension, and the elastic pe
                currently using unstretched_pos TODO
            """
            springDimensions = self.unstretched_pos - c_position[0:3]

            f = self.k * (springDimensions) 
            epe = 1/2 * self.k * getDistance(springDimensions) ** 2
            # print(f)

            return f, epe

    def setupSpring(self, fixed_pos, unstretched_pos, k):
        
        self.springs.append(self.spring(fixed_pos, unstretched_pos, k))

    def calcGravitationalPotential(self):
        # gravitational potential = - GM/r
        # taking the body as earth, with a 6370 km negative offset
        # while using 
        distanceToCore = 6370E3 # km -> m
        planetMass = 5.972E24 # kg
        G = 6.67E-11

        return -1 * G * planetMass / (distanceToCore + self.pos[2])

    def getStats(self):
        """
        gets you the mass, position, velocity, acceleration
        linear KE, linear momentum 
        """
        return (self.t, self.mass, self.pos, self.vel, self.acc, self.ke, self.p)

    def stat(self, variables=[], console=True):
        """
        More comprehensive printout of variables
        NOT COMPLETE
        """
        pout =  f"""Time: {self.t[-1]:.5f}s\n"""
        if "pos" in variables:
            pout += f"Position: ({self.pos[0]:.2f}, {self.pos[1]:.2f}, {self.pos[2]:.2f});  ({self.pos[3]:.2f}, {self.pos[4]:.2f}, {self.pos[5]:.2f})\n"

        if "v" in variables or "vel" in variables:
            pout += f"Velocity: ({self.vel[0]:.2f}, {self.vel[1]:.2f}, {self.vel[2]:.2f});  ({self.vel[3]:.2f}, {self.vel[4]:.2f}, {self.vel[5]:.2f})\n"

        if console:
            print(pout)
        return pout

    def sim(self, t):
        self.t.append(self.t[-1] + t)

        "code to determine changes in force / accleration based on position / time"

        # randomised acceleration
        # self.acc[0:3] = np.random.rand(3) * 20 - 10

        # constant acc directed at the origin
        c_acc = 0
        tgt = (0,0,0)
        a = self.directedVector(c_acc, self.pos[:3], tgt)
        self.acc[:3] = a + self.base_acc[:3]

        "Then spring effects, to get acc even though its actually f, to then get acc"
        f_spring = [0,0,0]
        for spr in self.springs:
            fspr_one, epe = spr.simSpring(c_position=self.pos)
            f_spring += fspr_one
            
        self.acc[0:3] += f_spring / self.mass
        

        # CART -> SPHER
        self.acc[3:] = getSphere(self.acc[0:3]) 
        self.force = self.acc
        self.force[:4] = self.acc[:4] * self.mass # muh f=ma

        # print(self.force[:3], f_spring, self.pos[2])
        ##

        "----------------------------------------------------------------------"
        # vectors, with calculations first done usingcartesion coords
        self.vel[0:3] = self.vel_np[-1][0:3] + self.acc[0:3] * t # use the last element of the array eh
        self.pos[0:3] = self.pos_np[-1][0:3] + self.vel[0:3] * t
        self.vel[3:] = getSphere(self.vel[0:3])
        self.pos[3:] = getSphere(self.pos[0:3])

        # scalars
        self.ke = 1/2 * self.mass * self.vel[3]
        self.p = self.mass * self.vel[3]

        ## appending
        self.pos_np = np.append(self.pos_np, [self.pos], axis=0)
        self.vel_np = np.append(self.vel_np, [self.vel], axis=0)
        self.acc_np = np.append(self.acc_np, [self.acc], axis=0)

        self.mass_np = np.append(self.mass_np, self.mass)
        self.ke_np = np.append(self.ke_np, self.ke)
        self.p_np = np.append(self.p_np, self.p)

        self.gpe_np = np.append(self.gpe_np, self.calcGravitationalPotential())
        self.elastic_pe_np = np.append(self.elastic_pe_np, epe)


    def directedVector(self, magnitude, src, tgt, spherical=False):
        """For a force or acceleration towards a particular point
        src and tgt are cartesian coordinates (otherwise CONVERT THEM)

        magnitude typically is calculated beforehang with another function

        outputs either spherical or cartesion (defaults to cartesian)
        """
        dir_vector = tgt - src

        spherical_form = getSphere(dir_vector)
        if spherical:
            return (magnitude, spherical_form[1], spherical_form[2])
        else:
            return getCart((magnitude, spherical_form[1], spherical_form[2]))

    def gpeFromMinimum(self):
        """
        Changes gpe from the proper value to a number over the minimum

        adds a new array gpe_min_np
        """
        min_gpe = np.amin(self.gpe_np)
        self.gpe_min_np = self.gpe_np - min_gpe

class simObject():
    """
    The sim "environment"
    """
    def __init__(self, uniformAcc = (0,0,0)) -> None:
        self.uniformAcc = uniformAcc
        self.objects = []
        self.t = [0]

    def setSimParams(self, duration, tick_length, stop_on_collision=False):
        self.duration = duration
        self.tick_length = tick_length
        self.stop_on_collision = stop_on_collision

    def collisionDetect(self, acc = 0.25):
        " not really working?"
        colls = []
        for a, obj1 in enumerate(self.objects):
            for b, obj2 in enumerate(self.objects):
                if a != b:
                    # print(obj2.pos, obj1.pos)
                    if obj1.pos[0] - acc <= obj2.pos[0] <= obj1.pos[0] + acc and obj1.pos[1] - acc <= obj2.pos[1] <= obj1.pos[1] + acc:
                        if [a, b] not in colls or [b, a] not in colls:
                            colls.append([a, b])
        if colls == []:
            return None
        else:
            return colls

    def simpleCollisionDetect(self, energy_reten=0.85):
        """ just checks if it reaches any of the boundaries then bounces it back
        energy retention is independent of 

        by the way, a proper method to calculate a reflection line about a plane is in MH_R7b_1 (ASTR)
        """
        for i, obj in enumerate(self.objects):
            if obj.pos[2] < 0: #simplistic idea of hitting the ground
                """
                The proper way to bounce it off a plane is to use a vector method (yadda)
                But

                I am lazy
                And I dont have time.

                So.
                """
                obj.vel[3] = obj.vel[3] * np.sqrt(energy_reten) # using kinetic energy changes

                # I think
                # obj.vel[5] = ( obj.vel[5] + np.pi) % (2* np.pi) # this is wrong lmao
                obj.vel[4] = np.pi - obj.vel[4] # muh dum dum
                
                obj.vel[0:3] = getCart(obj.vel[3:])
                
    def createObject(self, pos, vel, acc, mass, force):
        self.objects.append(physicsObject(pos=pos, vel=vel, acc=(acc[0] + self.uniformAcc[0], acc[1] + self.uniformAcc[1], acc[2] + self.uniformAcc[2]), mass=mass, force=force)) # force should be changed? TODO

    def startSim(self):
        for i in range(0, int(self.duration / self.tick_length)):
            self.t.append(self.t[-1] + self.tick_length)

            for obj in self.objects:
                obj.sim(self.tick_length)
                self.simpleCollisionDetect(energy_reten=1.0)
                # colls = self.collisionDetect() # removed for now
                # if colls:
                #     print(colls)

        for obj in self.objects:
            obj.gpeFromMinimum() # for ease -> gpe_min_np

    ## GRAPHING

    def plotGraphs(self, objects=[], variable="", split = True):
        self.fig=plt.figure(figsize=(16,9))
        fig = self.fig

        fig.suptitle("<3") 

        if split:
            ax1=fig.add_subplot(121)
            ax2=fig.add_subplot(122)

            for obj in objects:
                # change the [:,x], x being the index of [x, y, z], whichever axis is desired.
                if variable == "position":
                    
                    ax1.plot(self.t, self.objects[obj].pos_np[:,2])
                    # ax2.plot(self.t, self.objects[obj].pos_np[:,1])

                elif variable == "velocity":

                    ax1.plot(self.t, self.objects[obj].vel_np[:,0])
                    ax2.plot(self.t, self.objects[obj].vel_np[:,1])

                elif variable == "mah spring energy-x":
                    ax1.plot(self.objects[obj].pos_np[:,2], self.objects[obj].ke_np)
                    ax1.plot(self.objects[obj].pos_np[:,2], self.objects[obj].gpe_min_np)
                    ax1.plot(self.objects[obj].pos_np[:,2], self.objects[obj].elastic_pe_np)
                    ax1.plot(self.objects[obj].pos_np[:,2],
                        self.objects[obj].ke_np + self.objects[obj].gpe_min_np + self.objects[obj].elastic_pe_np
                    )


        if not split:
            for obj in objects:
                

                if variable == "basic":
                    "shows the pos and v/t"

                    ax1=fig.add_subplot(221, projection='3d')
                    ax2 = fig.add_subplot(222) # speed - time

                    ax1.set_title("Position")
                    ax1.plot3D(
                        self.objects[obj].pos_np[:,0], 
                        self.objects[obj].pos_np[:,1], 
                        self.objects[obj].pos_np[:,2], 
                        linewidth=0.5,
                        marker="o", markersize=0.5)
                    ax1.set_xlabel("X")
                    ax1.set_ylabel("Y")
                    ax1.set_zlabel("Z")


                    ax2.set_title("Speed")
                    ax2.plot(self.t, self.objects[obj].vel_np[:,4])

                elif variable == "position":
                    "shows the path, most basic"

                    ax1=fig.add_subplot(111, projection='3d')

                    ax1.set_title("Position")
                    ax1.plot3D(
                        self.objects[obj].pos_np[:,0], 
                        self.objects[obj].pos_np[:,1], 
                        self.objects[obj].pos_np[:,2], 
                        linewidth=0.5,
                        marker="o", markersize=0.5)
                    ax1.set_xlabel("X")
                    ax1.set_ylabel("Y")
                    ax1.set_zlabel("Z")

                

        fig.show()
        input()


def main():
    theSimpsons = simObject(uniformAcc = (0,0,-9.81))
    theSimpsons.setSimParams(duration=25, tick_length=0.05)

    theSimpsons.createObject(mass=5, pos=(0,0,0), vel=(0,0,0), acc=(0,0,0), force=())
    theSimpsons.objects[0].setupSpring(fixed_pos=[0,0,5], unstretched_pos=[0,0,0], k=5)

    theSimpsons.startSim()
    theSimpsons.plotGraphs(objects=[0], variable="mah spring energy-x", split=True)

if __name__ == "__main__":
    main()