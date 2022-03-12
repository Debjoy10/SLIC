import numpy as np
import cv2
from iod import display_image

def cluster_disp(path, B, opath):
    img = cv2.imread(path)
    for (r, c) in B:
        img[r][c][:] = 0
    display_image(img)
    if opath:
        cv2.imwrite(opath, img)
        print("Output image written to {}".format(opath))