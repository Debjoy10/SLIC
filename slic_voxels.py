from feature import pixel, voxel
from iod import getpixels, dispixels
from visualisation import cluster_disp
import argparse
import copy
import numpy as np
from tqdm import tqdm
from filters import grad
from slic import min_grad_center

def parse_args():
    # Function to parse args
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", help="Video to run SLIC on", type=str)
    parser.add_argument("-s", "--S", help="Superpixel Size (s or (sx sy))", nargs='+', default=None, type=int)
    parser.add_argument("-r", "--rect", help="Allow/use rectangular superpixel", action='store_true')
    parser.add_argument("-n", "--num", help="Number of Superpixel", type=int, default=1000)
    parser.add_argument("-t", "--threshold", help="Residual error threshold", type=float, default=0.01)
    parser.add_argument("-o", "--output", help="Path to write output video", type=str, default='images/out.mp4')
    args = parser.parse_args()
    return args

def L2_dist(pix1, pix2, Sx, Sy, Sz = 5):
    m = 25
    dc = np.sqrt((pix1.l-pix2.l)**2 + (pix1.a-pix2.a)**2 + (pix1.b-pix2.b)**2)
    ds = np.sqrt(((pix1.x-pix2.x)/Sx)**2 + ((pix1.y-pix2.y)/Sy)**2 + ((pix1.t-pix2.t)/Sz)**2)
    D = np.sqrt(dc**2 + m**2 * ds**2)
    return D

def main():
    args = parse_args()
    # Read image and convert to pixels
    pix = getpixels_video(args.path)
    # Run SLIC
    print("Running video SLIC algorithm on pixels in CIELAB format ...")
    cluster_centers, boundary = slic(pix, args)
    # Display
    cluster_disp_vox(args.path, boundary, args.output)

if __name__ == "__main__":
    main()