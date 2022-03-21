# Function for reading and writing images in CIELAB format
import cv2
from feature import pixel, voxel
import numpy as np
from random import randrange

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
        frames.append(cv2.cvtColor(arr, cv2.COLOR_BGR2LAB))
        idx += 1
    if sfidx is not None:
        frames = frames[sfidx:sfidx+5]
        print("Selecting 5 consecutive frames starting from {}".format(sfidx))
    frames = np.asarray(frames)
    print("Loaded")
    return frames

def getpixels_video(path):
    # Read image in path in CIELAB format and convert to pixel-array (l, a, b, x, y)
    vid = load_video(path, 0)
    time = vid.shape[0]
    rows = vid.shape[1]
    cols = vid.shape[2]
    pixels = [[[voxel(vid[t][i][j][0], vid[t][i][j][1], vid[t][i][j][2], j, i, t-2) for j in range(cols)] for i in range(rows)] for t in range(time)]
    return pixels