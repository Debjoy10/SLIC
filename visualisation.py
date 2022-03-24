import numpy as np
import cv2
from iod import display_image, load_video, load_stereo_images
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
    if opath:
        cv2.imwrite(opath, img)
        print("Output image written to {}".format(opath))

def cluster_disp_vox(path, B, opath):
    # B = [(x, y, z) ...]
    # Load video
    frames = np.array([cv2.cvtColor(f, cv2.COLOR_LAB2BGR) for f in load_video(path, sfidx = 0)])

    # Collect coordinates of each point
    B_dict = {i: [] for i in range(0, 5)}
    for (k, i, j) in B:
        B_dict[k] = [(i, j)]

    # Plot 3D slices of video, 5 frames
    for i, im in enumerate(frames[:5]):
        img = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)/255
        x, y = ogrid[0:img.shape[0], 0:img.shape[1]]
        ax = gca(projection='3d')
        for yi, xi in B_dict[i]:
            img[yi][xi][:] = 0
        ax.plot_surface(x, y, i*np.ones_like(x), rstride=1, cstride=1, facecolors=img, antialiased=True)
    plt.savefig(opath)

def write_cluster_video(path, B, opath):
    # B = [(x, y, z) ...]
    # Load video
    frames = np.array([cv2.cvtColor(f, cv2.COLOR_LAB2BGR) for f in load_video(path, sfidx = 0)])
    width = frames.shape[2]
    height = frames.shape[1]
    if not opath.endswith("mp4"):
        opath = opath.split('.')[0] + '.mp4'
    video = cv2.VideoWriter(opath, cv2.VideoWriter_fourcc('m','p','4','v'), 1, (width, height))
    for boundary in B:
        k, i, j = boundary
        frames[k][i][j][:] = 0
    for frame in frames:
        video.write(frame)
    video.release()
    return

def write_cluster_stereo_video(path, B, opath):
    # B = [(x, y, z) ...]
    # Load video
    frames = load_stereo_images(path)
    camrows, camcols, time, rows, cols, _ = frames.shape
    if not opath.endswith("mp4"):
        opath = opath.split('.')[0] + '.mp4'
    video = cv2.VideoWriter(opath, cv2.VideoWriter_fourcc('m','p','4','v'), 1, (camcols*cols, camrows*rows))
    for boundary in B:
        ci, cj, k, i, j = boundary
        frames[ci][cj][k][i][j][:] = 0
    combined_frames = np.zeros([time, camrows*rows, camcols*cols, 3])
    for ci in range(camrows):
        for cj in range(camcols):
            for k in range(time):
                combined_frames[k, ci*rows: (ci+1)*rows, cj*cols: (cj+1)*cols] = frames[ci][cj][k]
    for frame in combined_frames:
        video.write(np.uint8(frame))
    video.release()
    return