from feature import pixel, voxel
from iod import getpixels, dispixels, getpixels_video, load_stereos
from visualisation import cluster_disp, cluster_disp_vox, write_cluster_video
import argparse
import copy
import numpy as np
from tqdm import tqdm
from filters import grad
from slic import min_grad_center
from datetime import datetime
import json
import os

def parse_args():
    # Function to parse args
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", help="Video to run SLIC on", type=str)
    parser.add_argument("-s", "--S", help="Superpixel Size (s or (sx sy))", nargs='+', default=None, type=int)
    parser.add_argument("-r", "--rect", help="Allow/use rectangular superpixel", action='store_true')
    parser.add_argument("-n", "--num", help="Number of Superpixel", type=int, default=1000)
    parser.add_argument("-t", "--threshold", help="Residual error threshold", type=float, default=0.01)
    parser.add_argument("-o", "--output", help="Path to write outputs", type=str, default=None)
    args = parser.parse_args()
    return args

def L2_dist(pix1, pix2, Sx, Sy, Sz = 5, Scx = 3, Scy = 3):
    m = 25
    n = 10
    dc = np.sqrt((pix1.l-pix2.l)**2 + (pix1.a-pix2.a)**2 + (pix1.b-pix2.b)**2)
    ds = np.sqrt(((pix1.x-pix2.x)/Sx)**2 + ((pix1.y-pix2.y)/Sy)**2 + ((pix1.t-pix2.t)/Sz)**2)
    dz = np.sqrt(((pix1.cx-pix2.cx)/Scx)**2 + ((pix1.cy-pix2.cy)/Scy)**2)
    D = np.sqrt(dc**2 + m**2 * ds**2 + n**2 * dz**2)
    return D

def slic(stvoxels, args):
    camrows, camcols, time, rows, cols = stvoxels.shape
    N = rows*cols
    
    # Get the grid intervals (if only the number of superpixels provided)
    Sz = int(time / 2)
    if args.S == None:
        if args.rect:
            Sx = int(cols / np.sqrt(args.num))
            Sy = int(rows / np.sqrt(args.num))
        else:
            Sx = int(np.sqrt(N / args.num))
            Sy = int(np.sqrt(N / args.num))
    else:
        assert len(args.S) == int(args.rect) + 1
        if not args.rect:
            Sx = args.S[0]
            Sy = args.S[0]
        else:
            Sx = args.S[0]
            Sy = args.S[1]
    print("Running with Super-pixel Size = (Sx, Sy) = ({}, {})".format(Sx, Sy))
    return None, None

def main():
    args = parse_args()
    # Read images and convert to pixels - (cy, cx, t, y, x)
    pix = load_stereos(args.path)
    # Run SLIC
    print("Running video SLIC algorithm on pixels in CIELAB format ...")
    cluster_centers, boundary = slic(pix, args)
    # Display
    # todo

if __name__ == "__main__":
    main()