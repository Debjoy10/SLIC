# Function for reading and writing images in CIELAB format
import cv2
from feature import pixel, voxel
import numpy as np

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

def RGB_to_XYZ(r, g, b):
    # http://www.easyrgb.com/en/math.php - (If we need to do manually) - Refer for rest of colour conversion functions

    var_R = r / 255
    var_G = g / 255
    var_B = b / 255

    if var_R > 0.04045:
        var_R = (( var_R + 0.055) / 1.055) ^ 2.4
    else:
        var_R = var_R / 12.92
    if var_G > 0.04045:
        var_G = (( var_G + 0.055) / 1.055) ^ 2.4
    else:
        var_G = var_G / 12.92
    if var_B > 0.04045:
        var_B = ((var_B + 0.055) / 1.055 ) ^ 2.4
    else:                   
        var_B = var_B / 12.92

    var_R = var_R * 100
    var_G = var_G * 100
    var_B = var_B * 100

    X = var_R * 0.4124 + var_G * 0.3576 + var_B * 0.1805
    Y = var_R * 0.2126 + var_G * 0.7152 + var_B * 0.0722
    Z = var_R * 0.0193 + var_G * 0.1192 + var_B * 0.9505

    return X, Y, Z

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

def load_video(path):
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
        frames.append(arr)
        idx += 1
    frames = np.asarray(frames)
    print("Loaded")
    return frames