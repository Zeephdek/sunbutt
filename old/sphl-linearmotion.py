import numpy as np
import matplotlib.pyplot as plt 

"""
x, y, z (the normal orientation)
"""

class physicsObject():
    def __init__(self, pos, vel, acc, mass) -> None:
        self.pos = np.array(pos)
        self.vel = np.array(vel)
        self.acc = np.array(acc)
        self.mass = mass
        self.ke = 0
        self.p = 0
        self.t = [0]
        self.pos_np = np.array([pos])
        self.vel_np = np.array([vel])
        self.acc_np = np.array([acc])
        self.mass_np = np.array([self.mass])
        self.ke_np = np.array([self.ke])
        self.p_np = np.array([self.p])

    def getStats(self):
        """
        gets you the mass, position, velocity, acceleration
        linear KE, linear momentum 
        """
        return (self.t, self.mass, self.pos, self.vel, self.acc, self.ke, self.p)

    def sim(self, t):
        # acc?
        self.t.append(self.t[-1] + t)
        self.vel = self.vel + self.acc * t
        self.pos = self.pos + self.vel * t
        self.ke = 1/2 * self.mass * self.vel
        self.p = self.mass * self.vel
        self.pos_np = np.append(self.pos_np, [self.pos], axis=0)
        self.vel_np = np.append(self.vel_np, [self.vel], axis=0)
        self.acc_np = np.append(self.acc_np, [self.acc], axis=0)
        self.mass_np = np.append(self.mass_np, self.mass)
        self.ke_np = np.append(self.ke_np, self.ke)
        self.p_np = np.append(self.p_np, self.p)

class simObject():
    def __init__(self, uniformAcc = (0,0)) -> None:
        self.unformAcc = uniformAcc
        self.objects = []
        self.t = [0]

    def setSimParams(self, duration, tick_length, stop_on_collision=False):
        self.duration = duration
        self.tick_length = tick_length
        self.stop_on_collision = stop_on_collision

    def collisionDetect(self, acc = 0.25):
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

    
    def createObject(self, pos=(0,0), vel=(0,0), acc=(0,0), mass=0):
        self.objects.append(physicsObject(pos, vel, (acc[0] + self.unformAcc[0], acc[1] + self.unformAcc[1]), mass))

    def startSim(self):
        for i in range(0, int(self.duration / self.tick_length)):
            self.t.append(self.t[-1] + self.tick_length)

            for obj in self.objects:
                obj.sim(self.tick_length)
                colls = self.collisionDetect()
                if colls:
                    print(colls)

    def plotGraphs(self, objects=[], variable="", split = True):
        fig=plt.figure(figsize=(16,9))

        fig.suptitle("<3") 

        if split:
            ax1=fig.add_subplot(121)
            ax2=fig.add_subplot(122)

            for obj in objects:
                if variable == "position":
                    ax1.plot(self.t, self.objects[obj].pos_np[:,0])
                    ax2.plot(self.t, self.objects[obj].pos_np[:,1])
                elif variable == "velocity":
                    ax1.plot(self.t, self.objects[obj].vel_np[:,0])
                    ax2.plot(self.t, self.objects[obj].vel_np[:,1])

        if not split:
            ax1=fig.add_subplot(111)
            for obj in objects:
                if variable == "position":
                    ax1.set_title("Position")
                    ax1.plot(self.objects[obj].pos_np[:,0], self.objects[obj].pos_np[:,1], marker="o", markersize=1, linewidth=0.5)

        fig.show()
        input()


def main():
    theSimpsons = simObject(uniformAcc = (0,0))
    theSimpsons.setSimParams(duration=2, tick_length=0.02)

    theSimpsons.createObject(pos=(0,0), vel=(3,3), acc=(0,0), mass=4)
    theSimpsons.createObject(pos=(5,5), vel=(-3,-3), acc=(0,0), mass=4)
    theSimpsons.startSim()
    theSimpsons.plotGraphs(objects=[0, 1], variable="position", split=False)

if __name__ == "__main__":
    main()