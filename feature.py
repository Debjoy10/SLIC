import numpy as np

# Pixel feature class
class pixel: 
    def __init__(self, l, a, b, x, y): 
        self.l = int(l) 
        self.a = int(a)
        self.b = int(b)
        self.x = int(x)
        self.y = int(y)
        self.label = -1
        self.distance = np.inf

# Voxel feature class
class voxel: 
    def __init__(self, l, a, b, x, y, t): 
        self.l = l 
        self.a = a
        self.b = b
        self.x = x
        self.y = y
        self.t = t
        self.label = -1
        self.distance = np.inf

# Stereo Voxel feature class
class stereovoxel: 
    def __init__(self, l, a, b, x, y, t, cx, cy): 
        self.l = l 
        self.a = a
        self.b = b
        self.x = x
        self.y = y
        self.t = t
        self.cx = cx
        self.cy = cy
        self.label = -1
        self.distance = np.inf