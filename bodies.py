from utils import *
from constants import * 

# reference body defaults for all calculations involving a different body will be bodies[0]
# Also body 0 can't move, again for simplicity and laziness' sake

class system():
    def __init__(self) -> None:
        self.bodies = []
        self.bodies_names = []

    def createBody(self, mass, name = None,
        pos_cart = None, pos_sphr = None,
        vel_cart = None, vel_sphr = None
        ):
        if pos_cart == None and pos_sphr:
            pos_cart = getCart(pos_sphr)
        elif pos_sphr == None and pos_cart:
            pos_sphr = getSphr(pos_cart)
        else:
            pos_cart, pos_sphr = (0,0,0), (0,0,0)

        if vel_cart == None and vel_sphr:
            vel_cart = getCart(vel_sphr)
        elif vel_sphr == None and vel_cart:
            vel_sphr = getSphr(vel_cart)
        else:
            vel_cart, vel_sphr = (0,0,0), (0,0,0)

        acc_cart, acc_sphr = (0,0,0), (0,0,0) # it is just zero. 

        pos_cart = np.array(pos_cart)
        pos_sphr = np.array(pos_sphr)
        vel_cart = np.array(vel_cart)
        vel_sphr = np.array(vel_sphr)
        acc_cart = np.array(acc_cart)
        acc_sphr = np.array(acc_sphr)

        if not name:
            name = "body_"+str(len(self.bodies_names))

        self.bodies_names.append(name.lower())
        self.bodies.append(
            body(
                mass=mass, name=name.lower(),
                pos_cart=pos_cart, vel_cart=vel_cart, acc_cart=acc_cart,
                pos_sphr=pos_sphr, vel_sphr=vel_sphr, acc_sphr=acc_sphr
            )
        )

    # def sim
    def startSim(self, length, interval): 
        self.T = length
        self.dt = interval

        self.bodycount = len(self.bodies)


        self.t = 0
        n_iter = int(self.T / self.dt)
        self.t_arr = np.zeros([n_iter])

        for n in range(n_iter):
            if n == 55566:
                break

            msgMain = f"\nSim iteration {n+1}/{n_iter} | t={self.t}s"
            print(msgMain)

            self.sim()      

    def sim(self):
        self.calcGravAll()

        for body in self.bodies:
            dv = body.acc_cart * self.dt
            ds = body.vel_cart * self.dt

            if body.name == "earth":
                body.printDetailedInfo()
                printSph(getSphr(ds))
            
            body.vel_cart = body.vel_cart + dv
            body.pos_cart = body.pos_cart + ds

            body.vel_sphr = getSphr(body.vel_cart)
            body.pos_sphr = getSphr(body.pos_cart)

            body.pos_cart_arr = np.vstack((body.pos_cart_arr, body.pos_cart))
            body.pos_sphr_arr = np.vstack((body.pos_sphr_arr, body.pos_sphr))
            body.vel_cart_arr = np.vstack((body.vel_cart_arr, body.vel_cart))
            body.vel_sphr_arr = np.vstack((body.vel_sphr_arr, body.vel_sphr))
            body.acc_cart_arr = np.vstack((body.acc_cart_arr, body.acc_cart))
            body.acc_sphr_arr = np.vstack((body.acc_sphr_arr, body.acc_sphr))

        self.t += self.dt

    def calcGravAll(self):
        forces = np.zeros([self.bodycount, self.bodycount])
        
        # this is a thing.
        i, j = np.nested_iters(forces, [[0],[1]], flags=["c_index"])
        for x in i:
            idx = i.index
            for y in j:
                idy = j.index
                if idx < idy:
                    
                    # time to calculate gravitational force
                    a = g_force(
                        G=G, 
                        m_1=self.bodies[idx].mass, m_2=self.bodies[idy].mass, 
                        r=getDistance(self.bodies[idx].pos_cart, self.bodies[idy].pos_cart))
                    forces[idx,idy] = a
                    forces[idy,idx] = a
        

        #summing forces
        force_result = np.zeros([self.bodycount, 3])
        i = np.nditer(forces, flags=["multi_index"], op_flags=[["readwrite"]])
        for f in i:
            # force on x by y
            idx, idy = i.multi_index[0], i.multi_index[1]
            if idx == idy:
                continue
            force_dir = getDir(self.bodies[idx].pos_cart, self.bodies[idy].pos_cart)
            force_cart = getCart((f, force_dir[1], force_dir[2]))

            force_result[idx] += force_cart

        for i, body in enumerate(self.bodies):
            body.acc_cart = force_result[i] / body.mass
            body.acc_sphr = getSphr(force_result[i]) / body.mass

class body():
    def __init__(self, mass, name, pos_cart, pos_sphr, vel_cart, vel_sphr, acc_cart, acc_sphr) -> None:
        """
        cartesian x, y, z
        spherical r, theta, phi

        {scalar params}
        - mass

        {vector params} -> all 6 element arrays
        [x, y, z, r, theta, phi]
        ** Vector operations are done with cartesian.
        - pos
        - vel
        - acc

        {misc}
        """
        self.name = name
        self.mass = mass

        self.pos_cart = pos_cart
        self.pos_sphr = pos_sphr
        self.vel_cart = vel_cart
        self.vel_sphr = vel_sphr
        self.acc_cart = acc_cart
        self.acc_sphr = acc_sphr


        self.pos_cart_arr = np.reshape(pos_cart, (1,3))
        self.pos_sphr_arr = np.reshape(pos_sphr, (1,3))
        self.vel_cart_arr = np.reshape(vel_cart, (1,3))
        self.vel_sphr_arr = np.reshape(vel_sphr, (1,3))
        self.acc_cart_arr = np.reshape(acc_cart, (1,3))
        self.acc_sphr_arr = np.reshape(acc_sphr, (1,3))

    def returnCurrentBodyInfo(self):
        """
        Returns a dict with all info
        Dumb version.
        """

        return {
            "name":self.name, "mass":self.mass, 
            "pos":self.pos_cart+self.pos_sphr, 
            "vel":self.vel_cart+self.vel_sphr, 
            "acc":self.acc_cart+self.acc_sphr, 
        }

    def printDetailedInfo(self):
        msg = f"\nPosition: {self.pos_cart} | distance to sun: {self.pos_sphr[0]}\n"
        msg2 = f"Elevation: {np.degrees(self.pos_sphr[1])}° | Azimuth: {np.degrees(self.pos_sphr[2])}°\n"
        msg3 = f"Speed: {self.vel_sphr[0]}m/s\n"
        
        print(msg + msg2 + msg3)