import math
import numpy as np
import warnings as wgs


# Abstract class for a process to be controlled

class Process(object):

    def __init__(self):
        self.reset()

    def update(self, dt):
        # Read the set-point
        self.y = self.set_point(self.t)
        # Measure the process variable
        self.x = self.sense(self.t)
        # Compute error
        self.e = self.y - self.x
        # Perform correction based on error
        self.u = self.correct(self.e, dt)
        # Use the correction to act on process
        self.actuate(self.u, dt)

        self.t += dt

        return self.e

    def reset(self):
        self.t = 0.

    # Loop the process until simulation time is reached;
    # Returns a structured array of intermediate results for each iteration

    def loop(self, t_sim=10, dt=0.01):
        wgs.filterwarnings("ignore")  # To suppress FutureWarning -> dtype
        n = int(math.ceil(t_sim / dt))
        for i in range(n):
            self.update(dt)
            if i == 0:
                fields = [
                    ('y', np.float32, self.y.shape),
                    ('x', np.float32, self.x.shape),
                    ('e', np.float32, self.e.shape),
                    ('u', np.float32, self.u.shape),
                    ('t', np.float32, 1)
                ]
                result = np.zeros(n, dtype=fields)
            result[i] = (self.y, self.x, self.e, self.u, self.t - dt)

        return result

