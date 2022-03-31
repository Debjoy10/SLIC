# Function for reading and writing images in CIELAB format
import cv2
from feature import pixel, voxel, stereovoxel
import numpy as np
from random import randrange
import os
from tqdm import tqdm
import imutils

def read_LAB_img(path):
    # Reads the image
    img = cv2.imread(path)
    # Converts to LAB color space
    img = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    return img

def disp_RGB_img(img):
    # Converts from LAB to RGB color space and displays
    img = cv2.cvtColor(img, cv2.COLOR_LAB2BGR)
    display_image(img)
    return img
    
def display_image(img, winname = 'image'):
    cv2.namedWindow(winname, cv2.WINDOW_NORMAL)
    # Displays RGB image direct
    cv2.imshow(winname, img) 
    cv2.waitKey(0)         
    cv2.destroyAllWindows()

def getpixels(path):
    # Read image in path in CIELAB format and convert to pixel-array (l, a, b, x, y)
    img = read_LAB_img(path)
    rows = img.shape[0]
    cols = img.shape[1]
    pixels = [[pixel(img[i][j][0], img[i][j][1], img[i][j][2], j, i) for j in range(cols)] for i in range(rows)]
    return pixels

def dispixels(pixels):
    # Display RGB image from pixel array in format (l, a, b, x, y)
    rows = len(pixels)
    cols = len(pixels[0])
    lab_img = np.array([[[pixels[i][j].l, pixels[i][j].a, pixels[i][j].b] for j in range(cols)] for i in range(rows)])
    disp_RGB_img(lab_img)

def load_video(path, sfidx = None):
    # Loading video in RGB
    if not os.path.isdir(path):
        vid = cv2.VideoCapture(path)
        print("Loading Video {} ...".format(path))
        frames = []
        frame_jump = 10
        idx = 0
        while True:
            check, arr = vid.read()
            if not check:
                break 
            if idx % frame_jump != 0:
                idx += 1
                continue
            frames.append(imutils.resize(cv2.cvtColor(arr, cv2.COLOR_BGR2LAB), width=512))
            idx += 1
        if sfidx is not None:
            frames = frames[sfidx:sfidx+5]
            print("Selecting 5 consecutive frames starting from {}".format(sfidx))
        frames = np.asarray(frames)
        print("Loaded")
    else:
        print("Loading Video from frames {} ...".format(path))
        imgs = os.listdir(path)
        imgs.sort()
        vid = [imutils.resize(cv2.cvtColor(cv2.imread(os.path.join(path, f)), cv2.COLOR_BGR2LAB), width=512) for f in imgs]
        time = min(5, len(vid))
        frames = np.asarray(vid[:time])
        print("Loaded")
    return frames

def getpixels_video(path):
    # Read image in path in CIELAB format and convert to pixel-array (l, a, b, x, y)
    vid = load_video(path, 0)
    time = vid.shape[0]
    rows = vid.shape[1]
    cols = vid.shape[2]
    pixels = [[[voxel(vid[t][i][j][0], vid[t][i][j][1], vid[t][i][j][2], j, i, t) for j in range(cols)] for i in range(rows)] for t in range(time)]
    pixels = np.array(pixels)
    return pixels

##### Stereo Images
def load_stereo_images(path):
    isframes = ('00_00' in os.listdir(path))
    frames = []
    if isframes:
        print("Loading Stereo Frames {} ...".format(path))
        for y in tqdm(range(3)):
            frames.append([])
            for x in range(3):
                y1 = 3*y
                x1 = 3*x
                dirname = os.path.join(path, '0{}_0{}'.format(y1, x1))
                vid = [imutils.resize(cv2.imread(os.path.join(dirname, f)), width=512) for f in os.listdir(dirname)]
                rows = vid[0].shape[0]
                cols = vid[0].shape[1]
                time = min(5, len(vid))
                frames[y].append(vid[:time])
    else:
        print("Loading Stereo Videos {} ...".format(path))
        for y in tqdm(range(3)):
            frames.append([])
            for x in range(3):
                num = 10*y + 3*x + 1
                vid = str(num) + ".mp4"
                camvid = np.array([cv2.cvtColor(f, cv2.COLOR_LAB2BGR) for f in load_video(os.path.join(path, vid), sfidx = 0)])
                frames[y].append(camvid)
    print("Loaded")
    frames = np.array(frames)
    return frames

def load_stereos(path):
    isframes = ('00_00' in os.listdir(path))
    frames = []
    if isframes:
        print("Loading Stereo Frames {} ...".format(path))
        for y in tqdm(range(3)):
            frames.append([])
            for x in range(3):
                y1 = 3*y
                x1 = 3*x
                dirname = os.path.join(path, '0{}_0{}'.format(y1, x1))
                vid = [imutils.resize(read_LAB_img(os.path.join(dirname, f)), width=512) for f in os.listdir(dirname)]
                rows = vid[0].shape[0]
                cols = vid[0].shape[1]
                time = min(5, len(vid))
                camvid = [[[stereovoxel(vid[t][i][j][0], vid[t][i][j][1], vid[t][i][j][2], j, i, t, x, y) for j in range(cols)] for i in range(rows)] for t in range(time)]
                frames[y].append(camvid)
    else:
        print("Loading Stereo Videos {} ...".format(path))
        for y in tqdm(range(3)):
            frames.append([])
            for x in range(3):
                num = 10*y + 3*x + 1
                vid = str(num) + ".mp4"
                vid = load_video(os.path.join(path, vid))
                rows = vid[0].shape[0]
                cols = vid[0].shape[1]
                time = min(5, len(vid))
                camvid = [[[stereovoxel(vid[t][i][j][0], vid[t][i][j][1], vid[t][i][j][2], j, i, t, x, y) for j in range(cols)] for i in range(rows)] for t in range(time)]
                frames[y].append(camvid)
    print("Loaded")
    frames = np.array(frames)
    return frames