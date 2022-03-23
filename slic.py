from feature import pixel, voxel
from iod import getpixels, dispixels
from visualisation import cluster_disp
import argparse
import copy
import numpy as np
from tqdm import tqdm
from filters import grad
from datetime import datetime
import json
import os

def parse_args():
    # Function to parse args
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", help="Image to run SLIC on", type=str)
    parser.add_argument("-s", "--S", help="Superpixel Size (s or (sx sy))", nargs='+', default=None, type=int)
    parser.add_argument("-r", "--rect", help="Allow/use rectangular superpixel", action='store_true')
    parser.add_argument("-n", "--num", help="Number of Superpixel", type=int, default=1000)
    parser.add_argument("-t", "--threshold", help="Residual error threshold", type=float, default=0.01)
    parser.add_argument("-o", "--output", help="Path to write outputs", type=str, default=None)
    args = parser.parse_args()
    return args

def min_grad_center(r, c, grad_img):
    # Moved cluster center (c, r) to minimum gradient point in 3x3 window
    min_grad_r = 0
    min_grad_c = 0
    min_grad = np.inf
    for i in range(r-1, r+2):
        for j in range(c-1, c+2):
            if i < 0 or i > grad_img.shape[0]-1 or j < 0 or j > grad_img.shape[1]-1:
                continue
            if grad_img[i][j] < min_grad:
                min_grad_r = i
                min_grad_c = j
                min_grad = grad_img[i][j]
    return min_grad_r, min_grad_c

def L2_dist(pix1, pix2, Sx, Sy):
    m = 25
    dc = np.sqrt((pix1.l-pix2.l)**2 + (pix1.a-pix2.a)**2 + (pix1.b-pix2.b)**2)
    ds = np.sqrt(((pix1.x-pix2.x)/Sx)**2 + ((pix1.y-pix2.y)/Sy)**2)
    D = np.sqrt(dc**2 + m**2 * ds**2)
    return D

def slic(pixels, args):
    rows = len(pixels)
    cols = len(pixels[0])
    N = rows*cols

    # Get the grid intervals (if only the number of superpixels provided)
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

    # Get the image gradients using Sobel filter on the luminance channel
    luminance = np.array([[p.l for p in pixarr] for pixarr in pixels])
    grad_img = grad(luminance)

    # Get the initial cluster centers
    cluster_centers = []
    ri = 0
    while ri < rows:
        ci = 0
        while ci < cols:
            # Recenter to min grad location in 3x3 window (using LAB pixels)
            r, c = min_grad_center(ri, ci, grad_img)
            l, a, b, x, y = pixels[r][c].l, pixels[r][c].a, pixels[r][c].l, pixels[r][c].x, pixels[r][c].y
            cluster_centers.append(pixel(l, a, b, x, y))
            ci += Sx
        ri += Sy

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
            for i in range(max(0, y - 2*Sy), min(rows, y + 2*Sy)):
                for j in range(max(0, x - 2*Sx), min(cols, x + 2*Sx)):
                    pix = pixels[i][j]
                    D = L2_dist(pix, center, Sx, Sy)
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
                ERR += L2_dist(cc, newcc, Sx, Sy)
            else:
                # No pixels assigned to these cluster centers. Assign dummy values
                newcc = pixel(0, 0, 0, -1, -1)
                new_cluster_centers.append(newcc)

        # Get residual error
        ERR = ERR / len(new_cluster_centers)
        iters += 1
        print("Avg. Residual Error after iteration = {} is {}".format(iters, ERR))
        cluster_centers = new_cluster_centers

    # Collect final clusters
    clusters = [[] for k in range(len(cluster_centers))]
    for i in range(rows):
        for j in range(cols):
            pix = pixels[i][j]
            clusters[pix.label].append(pix.__dict__)
    cluster_centers = [cc.__dict__ for cc in cluster_centers]

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
    return cluster_centers, boundary, clusters

def save(cluster_centers, boundary, clusters, args):
    if args.output is None:
        now = datetime.now()
        args.output = os.path.join('results', 'pixel-SLIC_' + now.strftime("%m-%d-%Y_%H-%M-%S"))

    # Make directory
    if not os.path.exists(args.output):
        os.makedirs(args.output)

    # Save image
    cluster_disp(args.path, boundary, os.path.join(args.output, 'out.png'))
    # Save clusters
    with open(os.path.join(args.output, 'cc.json'), "w") as fp:
        json.dump(cluster_centers, fp)
    with open(os.path.join(args.output, 'c.json'), "w") as fp:
        json.dump(clusters, fp)
    with open(os.path.join(args.output, 'args.json'), "w") as fp:
        json.dump(args.__dict__, fp)
    print("Output saved to folder - {}".format(args.output))

def main():
    args = parse_args()
    # Read image and convert to pixels
    pix = getpixels(args.path)
    # Run SLIC
    print("Running image SLIC algorithm on pixels in CIELAB format ...")
    cluster_centers, boundary, clusters = slic(pix, args)
    # Display
    save(cluster_centers, boundary, clusters, args)

if __name__ == "__main__":
    main()