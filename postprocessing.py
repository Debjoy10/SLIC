from feature import pixel, voxel, stereovoxel
from iod import getpixels, dispixels
from visualisation import cluster_disp
from collections import Counter
from statistics import mean
import argparse
from copy import deepcopy
import numpy as np
from tqdm import tqdm
from filters import grad
from datetime import datetime
import json
import os
import cv2

# Utility functions
def inImage(point, rows, cols):
    if point.x <0 or point.x >= cols or point.y <0 or point.y >= rows :
        return False
    else:
        return True

def inVid(point, rows, cols, time):
    if point.x <0 or point.x >= cols or point.y <0 or point.y >= rows or point.t < 0 or point.t >= time:
        return False
    else:
        return True

def my_mode(sample):
    c = Counter(sample)
    mode_list = [k for k, v in c.items() if v == c.most_common(1)[0][1]]
    return mode_list[0]

# Remove disjoint clusters
def PostProcessing(pixels, cluster_centers, boundary, clusters, min_size):
    # Directions for traversing neightbourhood arrays
    directions = 8
    neighbourhood_arrayx = [0,0,1,-1,1, 1, -1, -1]
    neighbourhood_arrayy = [1,-1,0,0,-1, 1, -1, 1]
    new_clusters = []
    small_clusters = []
    rows = len(pixels)
    cols = len(pixels[0])

    # Extract the cluster information for all points:
    cluster_info = np.zeros([rows, cols])
    for i, points in enumerate(clusters):
        for p in points:
            cluster_info[p.y][p.x] = i

    # Get connected components using BFS
    print("Obtaining connected components")
    for i, cluster in tqdm(enumerate(clusters), total = len(clusters)):
        visited_pixel = np.zeros([rows, cols], dtype=bool)
        for j in cluster :
            if visited_pixel[j.y][j.x]:
                continue
            init_point = j
            queue = []
            queue.append(init_point)
            strongly_connected = []
            strongly_connected_mat = np.zeros([rows, cols], dtype=bool)
            cluster_size = 1

            while len(queue)!= 0 :
                point = queue.pop()
                strongly_connected.append(point)
                strongly_connected_mat[point.y][point.x] = True
                visited_pixel[point.y][point.x] = True
                for d in range(directions):
                    neighbourhood_point = pixel(point.l, point.a, point.b, point.x+neighbourhood_arrayx[d] , point.y+neighbourhood_arrayy[d])
                    if inImage(neighbourhood_point, rows, cols) and not strongly_connected_mat[neighbourhood_point.y][neighbourhood_point.x]:
                        if cluster_info[neighbourhood_point.y][neighbourhood_point.x] == i:
                            queue.append(neighbourhood_point)
                            cluster_size+=1
                    else:
                        continue
            if len(strongly_connected) > min_size:
                # Store large clusters
                new_clusters.append(strongly_connected)
            else:
                # Store smaller clusters
                small_clusters.append(strongly_connected)

    # Record the cluster index for each pixel
    new_cluster_indices = np.zeros((rows,cols), dtype = int)
    for ii, nc in enumerate(new_clusters):
        for point in nc:
            new_cluster_indices[point.y][point.x] = ii
            point.label = ii
            pixels[point.y][point.x].label = ii

    print("Incorporating spurious clusters to bigger clusters")
    # For each small cluster, assign that to one of the bigger clusters
    small_cluster_integrated = [False for _ in range(len(small_clusters))]
    for i, small_cluster in tqdm(enumerate(small_clusters), total = len(small_clusters)):
        if small_cluster_integrated[i]:
            continue
        neighbourhood_clusters = []
        for point in small_cluster:
            for d in range(directions):
                inpoint = pixel(point.l, point.a, point.b, point.x+neighbourhood_arrayx[d] , point.y + neighbourhood_arrayy[d])
                if inImage(inpoint, rows, cols):
                    nci = new_cluster_indices[inpoint.y][inpoint.x]
                    if nci != 0:
                        neighbourhood_clusters.append(nci)
        if len(neighbourhood_clusters) == 0:
            continue
        mode_neighbour = my_mode(neighbourhood_clusters)
        for point in small_cluster:
            point.label = mode_neighbour
            pixels[point.y][point.x].label = mode_neighbour
        new_clusters[mode_neighbour].extend(small_cluster)
        small_cluster_integrated[i] = True

    # Obtaining the new cluster centers after adding new points
    new_cluster_centers = []
    for nc in new_clusters:
        l=[]
        a=[]
        b=[]
        x=[]
        y=[]
        for point in nc:
            l.append(point.l)
            a.append(point.a)
            b.append(point.b)
            x.append(point.x)
            y.append(point.y)
        cluster_center = pixel(int(mean(l)), int(mean(a)), int(mean(b)), int(mean(x)), int(mean(y)))
        new_cluster_centers.append(cluster_center)

    # Draw the new boundaries
    new_boundary = []
    for i in range(rows):
        for j in range(cols):
            label = pixels[i][j].label
            if label >= len(new_cluster_centers):
                continue
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
                new_boundary.append((i, j))

    return new_cluster_centers, new_boundary, new_clusters

# Remove disjoint clusters
def PostProcessing_voxels(voxels, cluster_centers, boundary, clusters, min_size):
    # Directions for traversing neightbourhood arrays
    directions = 24
    neighbourhood_arrayx = [0,0,1,-1,1, 1, -1, -1, 0,0,1,-1,1, 1, -1, -1, 0,0,1,-1,1, 1, -1, -1]
    neighbourhood_arrayy = [1,-1,0,0,-1, 1, -1, 1, 1,-1,0,0,-1, 1, -1, 1, 1,-1,0,0,-1, 1, -1, 1]
    neighbourhood_arrayt = [-1,-1,-1,-1,-1,-1,-1,-1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1]
    new_clusters = []
    small_clusters = []
    time = len(voxels)
    rows = len(voxels[0])
    cols = len(voxels[0][0])

    # Extract the cluster information for all points:
    cluster_info = np.zeros([time, rows, cols])
    for i, points in enumerate(clusters):
        for p in points:
            cluster_info[p.t][p.y][p.x] = i

    # Get connected components using BFS
    print("Obtaining connected components")
    for i, cluster in tqdm(enumerate(clusters), total = len(clusters)):
        visited_pixel = np.zeros([time, rows, cols], dtype=bool)
        for j in cluster :
            if visited_pixel[j.t][j.y][j.x]:
                continue
            init_point = j
            queue = []
            queue.append(init_point)
            strongly_connected = []
            strongly_connected_mat = np.zeros([time, rows, cols], dtype=bool)
            cluster_size = 1

            while len(queue)!= 0 :
                point = queue.pop()
                strongly_connected.append(point)
                strongly_connected_mat[point.t][point.y][point.x] = True
                visited_pixel[point.t][point.y][point.x] = True
                for d in range(directions):
                    neighbourhood_point = voxel(point.l, point.a, point.b, point.x+neighbourhood_arrayx[d], point.y+neighbourhood_arrayy[d], point.t+neighbourhood_arrayt[d])
                    if inVid(neighbourhood_point, rows, cols, time) and not strongly_connected_mat[neighbourhood_point.t][neighbourhood_point.y][neighbourhood_point.x]:
                        if cluster_info[neighbourhood_point.t][neighbourhood_point.y][neighbourhood_point.x] == i:
                            queue.append(neighbourhood_point)
                            cluster_size+=1
                    else:
                        continue
            if len(strongly_connected) > min_size:
                # Store large clusters
                new_clusters.append(strongly_connected)
            else:
                # Store smaller clusters
                small_clusters.append(strongly_connected)

    # Record the cluster index for each pixel
    new_cluster_indices = np.zeros((time, rows,cols), dtype = int)
    for ii, nc in enumerate(new_clusters):
        for point in nc:
            new_cluster_indices[point.t][point.y][point.x] = ii
            point.label = ii
            voxels[point.t][point.y][point.x].label = ii

    print("Incorporating spurious clusters to bigger clusters")
    # For each small cluster, assign that to one of the bigger clusters
    small_cluster_integrated = [False for _ in range(len(small_clusters))]
    for i, small_cluster in tqdm(enumerate(small_clusters), total = len(small_clusters)):
        if small_cluster_integrated[i]:
            continue
        neighbourhood_clusters = []
        for point in small_cluster:
            for d in range(directions):
                inpoint = voxel(point.l, point.a, point.b, point.x+neighbourhood_arrayx[d] , point.y + neighbourhood_arrayy[d], point.t + neighbourhood_arrayt[d])
                if inVid(inpoint, rows, cols, time):
                    nci = new_cluster_indices[inpoint.t][inpoint.y][inpoint.x]
                    if nci != 0:
                        neighbourhood_clusters.append(nci)
        if len(neighbourhood_clusters) == 0:
            continue
        mode_neighbour = my_mode(neighbourhood_clusters)
        for point in small_cluster:
            point.label = mode_neighbour
            voxels[point.t][point.y][point.x].label = mode_neighbour
        new_clusters[mode_neighbour].extend(small_cluster)
        small_cluster_integrated[i] = True

    # Obtaining the new cluster centers after adding new points
    new_cluster_centers = []
    for nc in new_clusters:
        l=[]
        a=[]
        b=[]
        x=[]
        y=[]
        t=[]
        for point in nc:
            l.append(point.l)
            a.append(point.a)
            b.append(point.b)
            x.append(point.x)
            y.append(point.y)
            t.append(point.t)
        cluster_center = voxel(int(mean(l)), int(mean(a)), int(mean(b)), int(mean(x)), int(mean(y)), int(mean(t)))
        new_cluster_centers.append(cluster_center)

    # Draw the new boundaries
    new_boundary = []
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
                    new_boundary.append((k, i, j))

    return new_cluster_centers, new_boundary, new_clusters