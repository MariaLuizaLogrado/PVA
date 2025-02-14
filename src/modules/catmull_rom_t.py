import numpy as np

class CatmullRomT:
    def __init__(self, control_x, control_y, T):

        self.control_x = control_x
        self.control_y = control_y
        self.T = T
        self.q = self.catmull_rom_t()



    def catmull_rom_t(self):
        def q(t):
            return 1/2 * np.array([t**3, t**2, t, 1]) @ np.array([[-1/self.T, (4*self.T-1)/self.T, (-4*self.T +1)/self.T, 1/self.T], 
                                                                  [2/self.T, (-6*self.T+1)/self.T, (6*self.T-2)/self.T, -1/self.T], 
                                                                  [-1/self.T, 0, 1/self.T, 0], 
                                                                  [0, 2, 0, 0]]) @ np.array([self.control_x, self.control_y]).T
        return q
    
    

