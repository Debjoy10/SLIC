from feature import pixel, voxel
from iod import getpixels, dispixels
from visualisation import cluster_disp
import argparse
import copy
import numpy as np
from tqdm import tqdm

def parse_args():
    # Function to parse args
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", help="Image to run SLIC on", type=str)
    parser.add_argument("-s", "--S", help="Superpixel Size", default=None, type=int)
    parser.add_argument("-n", "--num", help="Number of Superpixel", type=int, default=100)
    parser.add_argument("-t", "--threshold", help="Residual error min threshold", type=float, default=0.01)
    args = parser.parse_args()
    return args

def min_grad_center(r, c, pixels):
    return r, c 

def L2_dist(pix1, pix2, S):
    m = 10
    dc = np.sqrt((pix1.l-pix2.l)**2 + (pix1.a-pix2.a)**2 + (pix1.b-pix2.b)**2)
    ds = np.sqrt((pix1.x-pix2.x)**2 + (pix1.y-pix2.y)**2)
    D = np.sqrt(dc**2 + m**2 * (ds/S)**2)
    return D

def slic(pixels, args):
    rows = len(pixels)
    cols = len(pixels[0])
    N = rows*cols

    # Get the grid intervals (if only the number of superpixels provided)
    if args.S == None:
        args.S = int(np.sqrt(N / args.num))
    
    # Get the initial cluster centers
    cluster_centers = []
    ri = 0
    while ri < rows:
        ci = 0
        while ci < cols:
            # Recenter to min grad location in 3x3 window (using LAB pixels)
            r, c = min_grad_center(ri, ci, pixels)
            l, a, b, x, y = pixels[r][c].l, pixels[r][c].a, pixels[r][c].l, pixels[r][c].x, pixels[r][c].y
            cluster_centers.append(pixel(l, a, b, x, y))
            ci += args.S
        ri += args.S

    # SLIC algorithm
    ERR = np.inf
    threshold = args.threshold
    iters = 0
    while ERR > threshold:
        for k, center in tqdm(enumerate(cluster_centers), total = len(cluster_centers)):
            x = center.x
            y = center.y
            if x == -1 or y == -1:
                continue
            for i in range(max(0, y - 2*args.S), min(rows, y + 2*args.S)):
                for j in range(max(0, x - 2*args.S), min(cols, x + 2*args.S)):
                    pix = pixels[i][j]
                    D = L2_dist(pix, center, args.S)
                    if D < pix.distance:
                        pix.distance = D
                        pix.label = k    

        # Collect all points in clusters separately
        clusters = [{"l": [], "a": [], "b": [], "x": [], "y": []} for k in range(len(cluster_centers))]
        for i in range(rows):
            for j in range(cols):
                pix = pixels[i][j]
                clusters[pix.label]["l"].append(pix.l)
                clusters[pix.label]["a"].append(pix.a)
                clusters[pix.label]["b"].append(pix.b)
                clusters[pix.label]["x"].append(pix.x)
                clusters[pix.label]["y"].append(pix.y)

        # Assign new centers
        new_cluster_centers = []
        ERR = 0
        for ic in range(len(clusters)):
            c = clusters[ic]
            cc = cluster_centers[ic]
            if len(c["l"]) != 0:
                # Assign the cluster centers as the mean of all pixels in the cluster
                newcc = pixel(np.mean(c["l"]), np.mean(c["a"]), np.mean(c["b"]), np.mean(c["x"]), np.mean(c["y"]))
                new_cluster_centers.append(newcc)

                # Add to residual error
                ERR += L2_dist(cc, newcc, args.S)
            else:
                # No pixels assigned to these cluster centers. Assign dummy values
                newcc = pixel(0, 0, 0, -1, -1)
                new_cluster_centers.append(newcc)

        # Get residual error
        ERR = ERR / len(new_cluster_centers)
        iters += 1
        print("Avg. Residual Error after iteration = {} is {}".format(iters, ERR))
        cluster_centers = new_cluster_centers

    # Draw cluster boundaries for visualisation
    boundary = []
    for i in range(rows):
        for j in range(cols):
            label = pixels[i][j].label
            nlabel = []
            if i < rows-1:
                nlabel.append(pixels[i+1][j].label)
            if j < cols-1:    
                nlabel.append(pixels[i][j+1].label)
            if i < rows-1 and j < cols-1:
                nlabel.append(pixels[i+1][j+1].label)
            if i > 0 and j < cols-1:
                nlabel.append(pixels[i-1][j+1].label)
            if len(nlabel) > 0 and sum([n != label for n in nlabel]) != 0:
                boundary.append((i, j))
    return cluster_centers, boundary

def main():
    args = parse_args()
    # Read image and convert to pixels
    pix = getpixels(args.path)
    # Run SLIC
    cluster_centers, boundary = slic(pix, args)
    # Display
    cluster_disp(args.path, boundary)

if __name__ == "__main__":
    main()