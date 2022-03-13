import numpy as np
import cv2
from iod import display_image, load_video
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from pylab import *
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

def cluster_disp(path, B, opath):
    img = cv2.imread(path)
    for (r, c) in B:
        img[r][c][:] = 0
    display_image(img)
    if opath:
        cv2.imwrite(opath, img)
        print("Output image written to {}".format(opath))

def cluster_disp_vox(path, opath):
    # Load video
    frames = load_video(path)
    img = cv2.imread(path)
    for i, im in enumerate(frames[0:10]):
        img = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)/255
        x, y = ogrid[0:img.shape[0], 0:img.shape[1]]
        ax = gca(projection='3d')
        ax.plot_surface(x, y, i*np.ones_like(x), rstride=5, cstride=5, facecolors=img)
    show()