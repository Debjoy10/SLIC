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
        self.l = int(l) 
        self.a = int(a)
        self.b = int(b)
        self.x = int(x)
        self.y = int(y)
        self.t = int(t)
        self.label = -1
        self.distance = np.inf

# Stereo Voxel feature class
class stereovoxel: 
    def __init__(self, l, a, b, x, y, t, cx, cy): 
        self.l = int(l) 
        self.a = int(a)
        self.b = int(b)
        self.x = int(x)
        self.y = int(y)
        self.t = int(t)
        self.cx = int(cx)
        self.cy = int(cy)
        self.label = -1
        self.distance = np.inf