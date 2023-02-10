import numpy as np
from scipy import ndimage,signal
import matplotlib.pyplot as plt

def kirschEdges(imgIn): 
    ##kirschEdges: Calculate the edge map using the Kirsch's method
#imgIn: image input (single plane)
#imgOut: edge map
    signal.convolve2d
    # Kirsch's Templates
    h1 = np.array([[5,- 3,- 3],[5,0,- 3],[5,- 3,- 3]]) / 15
    h2 = np.array([[- 3,- 3,5],[- 3,0,5],[- 3,- 3,5]]) / 15
    h3 = np.array([[- 3,- 3,- 3],[5,0,- 3],[5,5,- 3]]) / 15
    h4 = np.array([[- 3,5,5],[- 3,0,5],[- 3,- 3,- 3]]) / 15
    h5 = np.array([[- 3,- 3,- 3],[- 3,0,- 3],[5,5,5]]) / 15
    h6 = np.array([[5,5,5],[- 3,0,- 3],[- 3,- 3,- 3]]) / 15
    h7 = np.array([[- 3,- 3,- 3],[- 3,0,5],[- 3,5,5]]) / 15
    h8 = np.array([[5,5,- 3],[5,0,- 3],[- 3,- 3,- 3]]) / 15
    # Spatial Filtering by Kirsch's Templates

    t1 = signal.convolve2d(imgIn,np.rot90(h1),mode='same')
   
    t2 = signal.convolve2d(imgIn,np.rot90(h2),mode='same')
    t3 = signal.convolve2d(imgIn,np.rot90(h3), mode='same')
    t4 = signal.convolve2d(imgIn,np.rot90(h4), mode='same')
    t5 =signal.convolve2d(imgIn,np.rot90(h5), mode='same')
    t6 =signal.convolve2d(imgIn,np.rot90(h6),mode='same')
    t7 = signal.convolve2d(imgIn,np.rot90(h7), mode='same')
    t8 =signal.convolve2d(imgIn,np.rot90(h8), mode='same')
    # Find the maximum edges value
    imgOut = np.maximum(t1,t2)
    # plt.imshow(imgIn)
    # plt.show()
    imgOut = np.maximum(imgOut,t3)

    imgOut = np.maximum(imgOut,t4)
    imgOut = np.maximum(imgOut,t5)
    imgOut = np.maximum(imgOut,t6)
    imgOut = np.maximum(imgOut,t7)
    imgOut = np.maximum(imgOut,t8)
    return imgOut
    
