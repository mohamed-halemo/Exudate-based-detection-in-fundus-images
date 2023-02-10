# # # # Disclaimer:
# #  This code is provided "as is". It can be used for research purposes only and all the authors
# #  must be acknowledged.
# # # # Authors:
# # Luca Giancardo
# # # # Date:
# # 2010-03-01
# # # # Version:
# # 1.0
# # # # Description:
# # Test the Exudate segmentation on the DMED dataset

# Add directory contatinig the dataset managing class
import numpy as np
import matplotlib.pyplot as pltt
from exDetect import *
from misc.Dmed import Dmed
import os
path='misc'
# The location of the dataset
DMEDloc = './DMED'
# load the dataset
data = Dmed(os.path.abspath(DMEDloc))
# print(data.getNumOfImgs)
# Show the results of the exudate detection algorithm
for i in range (0,data.getNumOfImgs()):
    rgbImg = data.getImg(i)
    # plt.imshow(rgbImg)
    # plt.show()
    onY,onX = data.getONloc(i)
    imgProb = exDetect(rgbImg,1,onY,onX)
    
    # display results
    # pltt.imshow(rgbImg)
    # pltt.show()
    # pltt.imshow(imgProb)
    # pltt.show()
    # block execution up until an image is closed
    
