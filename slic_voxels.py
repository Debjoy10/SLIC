from feature import pixel, voxel
from iod import getpixels, dispixels, getpixels_video
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
    parser.add_argument("-c", "--plt_surface", help="(Experimental) If true plot the surface plot of the output", action='store_true')
    args = parser.parse_args()
    return args

def L2_dist(pix1, pix2, Sx, Sy, Sz = 5):
    m = 25
    dc = np.sqrt((pix1.l-pix2.l)**2 + (pix1.a-pix2.a)**2 + (pix1.b-pix2.b)**2)
    ds = np.sqrt(((pix1.x-pix2.x)/Sx)**2 + ((pix1.y-pix2.y)/Sy)**2 + ((pix1.t-pix2.t)/Sz)**2)
    D = np.sqrt(dc**2 + m**2 * ds**2)
    return D

def slic(voxels, args):
    time = len(voxels)
    rows = len(voxels[0])
    cols = len(voxels[0][0])
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

    # Get the image gradients using Sobel filter on the luminance channel - Only need for the middle frame
    luminance = np.array([[v.l for v in voxarr] for voxarr in voxels[int(time/2)]])
    grad_video = grad(luminance)
    
    # Get the initial cluster centers - only on middle frame
    cluster_centers = []
    ti = int(time/2)
    ri = 0
    while ri < rows:
        ci = 0
        while ci < cols:
            # Recenter to min grad location in 3x3 window (using LAB pixels)
            r, c = min_grad_center(ri, ci, grad_video)
            l, a, b, x, y, t = voxels[ti][r][c].l, voxels[ti][r][c].a, voxels[ti][r][c].l, voxels[ti][r][c].x, voxels[ti][r][c].y, voxels[ti][r][c].t 
            cluster_centers.append(voxel(l, a, b, x, y, t))
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
            t = center.t
            if x == -1 or y == -1 or t == -1:
                continue
            for ti in range(max(0, t - 2*Sz), min(time, t + 2*Sz)):        
                for i in range(max(0, y - 2*Sy), min(rows, y + 2*Sy)):
                    for j in range(max(0, x - 2*Sx), min(cols, x + 2*Sx)):
                        vox = voxels[ti][i][j]
                        D = L2_dist(vox, center, Sx, Sy, Sz)
                        if D < vox.distance:
                            vox.distance = D
                            vox.label = k

        # Collect all points in clusters separately
        clusters = [{"l": [], "a": [], "b": [], "x": [], "y": [], "t": []} for k in range(len(cluster_centers))]
        for k in range(time):
            for i in range(rows):
                for j in range(cols):
                    vox = voxels[k][i][j]
                    clusters[vox.label]["l"].append(vox.l)
                    clusters[vox.label]["a"].append(vox.a)
                    clusters[vox.label]["b"].append(vox.b)
                    clusters[vox.label]["x"].append(vox.x)
                    clusters[vox.label]["y"].append(vox.y)
                    clusters[vox.label]["t"].append(vox.t)

        # Assign new centers
        new_cluster_centers = []
        ERR = 0
        for ic in range(len(clusters)):
            c = clusters[ic]
            cc = cluster_centers[ic]
            if len(c["l"]) != 0:
                # Assign the cluster centers as the mean of all pixels in the cluster
                newcc = voxel(np.mean(c["l"]), np.mean(c["a"]), np.mean(c["b"]), np.mean(c["x"]), np.mean(c["y"]), np.mean(c["t"]))
                new_cluster_centers.append(newcc)

                # Add to residual error
                ERR += L2_dist(cc, newcc, Sx, Sy, Sz)
            else:
                # No pixels assigned to these cluster centers. Assign dummy values
                newcc = voxel(0, 0, 0, -1, -1, -1)
                new_cluster_centers.append(newcc)

        # Get residual error
        ERR = ERR / len(new_cluster_centers)
        iters += 1
        print("Avg. Residual Error after iteration = {} is {}".format(iters, ERR))
        cluster_centers = new_cluster_centers

    # Collect final clusters
    clusters = [[] for k in range(len(cluster_centers))]
    for k in range(time):
        for i in range(rows):
            for j in range(cols):
                vox = voxels[k][i][j]
                clusters[vox.label].append(vox.__dict__)
    cluster_centers = [cc.__dict__ for cc in cluster_centers]

    # Draw cluster boundaries for visualisation
    boundary = []
    for k in range(time):
        for i in range(rows):
            for j in range(cols):
                label = voxels[k][i][j].label
                nlabel = []
                if i < rows-1:
                    nlabel.append(voxels[k][i+1][j].label)
                if j < cols-1:    
                    nlabel.append(voxels[k][i][j+1].label)
                if i < rows-1 and j < cols-1:
                    nlabel.append(voxels[k][i+1][j+1].label)
                if i > 0 and j < cols-1:
                    nlabel.append(voxels[k][i-1][j+1].label)
                if len(nlabel) > 0 and sum([n != label for n in nlabel]) != 0:
                    boundary.append((k, i, j))
    return cluster_centers, boundary, clusters

def save(cluster_centers, boundary, clusters, args):
    if args.output is None:
        now = datetime.now()
        args.output = os.path.join('results', 'voxel-SLIC_' + now.strftime("%m-%d-%Y_%H-%M-%S"))

    # Make directory
    if not os.path.exists(args.output):
        os.makedirs(args.output)

    # Save image
    if args.plt_surface:
        cluster_disp_vox(args.path, boundary, os.path.join(args.output, 'out.jpg'))
    write_cluster_video(args.path, boundary, os.path.join(args.output, 'out.mp4'))

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
    pix = getpixels_video(args.path)
    # Run SLIC
    print("Running video SLIC algorithm on pixels in CIELAB format ...")
    cluster_centers, boundary, clusters = slic(pix, args)
    # Display
    save(cluster_centers, boundary, clusters, args)

if __name__ == "__main__":
    main()