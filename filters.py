import numpy as np

def conv(lum, filt):
    # Convolution operator
    padded_lum = np.zeros([lum.shape[0]+2, lum.shape[1]+2])
    padded_lum[1:padded_lum.shape[0]-1, 1:padded_lum.shape[1]-1] = lum
    grad = np.zeros([lum.shape[0], lum.shape[1]])
    for i in range(1, padded_lum.shape[0]-1):
        for j in range(1, padded_lum.shape[1]-1):
            grad_value = 0
            for m in range(i-1, i+2):
                for n in range(j-1, j+2):
                    grad_value += filt[m+1-i][n+1-j] * padded_lum[m][n]
            grad[i-1][j-1] = grad_value
    return grad
            
def grad(lum):
    # Sobel horizontal filter
    sobel_h = [
        [ 1,  2,  1],
        [ 0,  0,  0],
        [-1, -2, -1]
    ]
    # Sobel vertical filter
    sobel_v = [
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]
    ]
    # Convolution
    grad_h = conv(lum, sobel_h)
    grad_v = conv(lum, sobel_v)
    grad = np.zeros([lum.shape[0], lum.shape[1]])
    for i in range(lum.shape[0]):
        for j in range(lum.shape[1]):
            grad[i][j] = np.sqrt(grad_h[i][j]**2 + grad_v[i][j]**2)
    return grad