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
# # Imlementation of the the Exudate detector proposed by our group
from pickletools import uint8
import numpy as np
import matplotlib.pyplot as plt
import cv2
from misc.getFovMask import getFovMask
from misc.kirschEdges import kirschEdges
# from matplotlib.pyplot import plot as plt
from scipy.signal import medfilt2d
from skimage import measure
import pywt
from skimage.transform import resize
from skimage.color import rgb2hsv
import copy
# def imreconstruct2(marker: np.ndarray, mask: np.ndarray, radius: int = 1):
   
#     kernel = np.ones(shape=(radius * 2 + 1,) * 2, dtype=np.uint8)
#     while True:
#         expanded = cv2.dilate(src=marker, kernel=kernel)
#         cv2.bitwise_and(src1=expanded, src2=mask, dst=expanded)

#         # Termination criterion: Expansion didn't change the image at all
#         if (marker == expanded).all():
#             return expanded
#         marker = expanded

    
def imreconstruct(marker, mask):
    kernel = np.ones(shape=(1 * 2 + 1,) * 2, dtype=np.uint8)

    EE = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (6,6))
    # print(marker)
    Imrec = marker
    # Imrec = copy.deepcopy(marker)
    Imresult =np.zeros(mask.shape)
    i = 0
    
    while (Imrec != Imresult).any():
        
        Imresult = Imrec
        # Imresult = copy.deepcopy(Imrec)
        Imdilated = cv2.dilate(Imresult, kernel)
        # Imrec = cv2.bitwise_and(Imdilated, mask,Imdilated)

        
        Imrec = np.minimum(Imdilated, mask)
        if i == 200:
            print('no sale del while')
            break
        i += 1
        
    
    return Imresult
def exDetect(rgbImgOrig = None,removeON = None,onY = None,onX = None): 
    #exDetect: detect exudates
# V. 0.2 - 2010-02-01
# make compatible with Matlab2008
# V. 0.1 - 2010-02-01
#          source: /mnt/data/ornl/lesions/exudatesCpp2/matlab/exudatesCpp3
    
    path='misc'
    #-- Parameters
    showRes = 0
    
    #--
    
    # if no parameters are given use the test image
    if (removeON==None and onY==None and onX==None):
        rgbImgOrig = plt.imread('misc/img_ex_test.jpg')
        removeON = 1
        onY = 905
        onX = 290
        showRes = 1
    
    
    imgProb = getLesions(rgbImgOrig,showRes,removeON,onY,onX)
    return imgProb
    
    
def getLesions(rgbImgOrig,showRes,removeON,onY,onX): 
    # Parameters
    winOnRatio = [1 / 8,1 / 8]
    
    # resize
    origSize = rgbImgOrig.shape
    newSize = 750,(750 * (origSize[1] / origSize[0]))
    #newSize = newSize-mod(newSize,2); # force the size to be even
    newSize = findGoodResolutionForWavelet(newSize)

    imgRGB = resize(rgbImgOrig,newSize)
    # plt.imshow(imgRGB)
    # plt.show()

    imgG = imgRGB[:,:,0]
   
    # change colour plane
    # imgHSV = colorsys.rgb_to_hsv(imgRGB[:,:,0],imgRGB[:,:,1],imgRGB[:,:,2])
    
    imgRGB=np.array(imgRGB, dtype=np.float32)######################################################################
   
    imgHSV = rgb2hsv(imgRGB)
 
    imgV = imgHSV[:,:,2]
    imgV8 = (imgV*255).astype(np.uint8)
 
    #     #--- normalise
#     imgV = [];
#     if( isempty( forBgImg ) )
#         [imgVfor, imgVnorm, forN, forTrimSize] = getForacchiaBg2( imgV, 10, 1 );
#         #create an image with the original size
#         imgVforOs = zeros(newSize);
#         imgVforOs(forTrimSize:newSize(1)-forTrimSize,forTrimSize:newSize(2)-forTrimSize) = imgVfor;
#     else
#         imgVforOs = imresize(forBgImg, newSize);
#     end
#     #---
    
    #--- Remove OD region
    if (removeON):
        # get ON window
        onY = onY * newSize[0] / origSize[0]
        onX = onX * newSize[1] / origSize[1]
        onX = np.round(onX)
        onY = np.round(onY)
        # winOnSize = np.round(np.matmul(winOnRatio,newSize))
        winOnSize = (winOnRatio*newSize)
        # remove ON window from imgTh
        winOnCoordY = ([onY - winOnSize[0],onY + winOnSize[0]])
        winOnCoordX = ([onX - winOnSize[1],onX + winOnSize[1]])
        if (winOnCoordY[0] < 1):
            winOnCoordY[0] = 1
        if (winOnCoordX[0] < 1):
            winOnCoordX[0] = 1
        if (winOnCoordY[1] > newSize[1]):
            winOnCoordY[1] = newSize[1]
        if (winOnCoordX[1] > newSize[1]):
            winOnCoordX[1] = newSize[1]
        #     imgThNoOD = imgTh;
#     imgThNoOD(winOnCoordY(1):winOnCoordY(2), winOnCoordX(1):winOnCoordX(2)) = 0;
    
    #---
    
    # Create FOV mask
    imgFovMask = getFovMask(imgV8,1,30)
    x1=int(winOnCoordX[0])
    x2=int(winOnCoordX[1])
    y1=int(winOnCoordY[0])
    y2=int(winOnCoordY[1])
    imgFovMask[y1:y2,x1:x2] = 0
    # imgFovMask[x2,y2] = 0
    #     #--- Calculate threshold using median Background
#     x=0:255;
#     offset=4;
#     subImg = double(imgVforOs) - double(medfilt2(imgVforOs, [round(newSize(1)/30) round(newSize(1)/30)]  ));
#     subImg = subImg .* double(imgFovMask);
#     subImg(subImg < 0) = 0;
#     histImg=hist(subImg(:),x);
#     histImg2 = histImg(offset:end);
#     xPos = x(offset:end);
#     pp = splinefit( xPos, histImg2 );
#     splineHist = ppval( pp, xPos );
# #     figure;plot(xPos,splineHist);
#     splineHistDD = [diff(diff(splineHist)) 0 0];
#     zcList = crossing(splineHistDD);
#     th = xPos(zcList(1));
#     imgThNoOD = subImg >= th;
#     #---
    
    #     #--- fixed threshold using median Background (normal)
#     subImg = double(imgV8) - double(medfilt2(imgV8, [round(newSize(1)/30) round(newSize(1)/30)]  ));
#     subImg = subImg .* double(imgFovMask);
#     subImg(subImg < 0) = 0;
#     imgThNoOD = uint8(subImg) > 10;
#     #---
    # mod = (newSize[0]//30) % 2
    # if mod > 0:
    #     pass
    # else:
    #     newSize=newSize[0]+1

    kernelSize=int(np.round(newSize[0]/30))
    #--- fixed threshold using median Background (with reconstruction)
    medBg = np.double((medfilt2d(imgV8,(kernelSize))))
   
    #reconstruct bg
    maskImg = np.double(imgV8)
    
    pxLbl = maskImg < medBg
   
    maskImg[pxLbl] = medBg[pxLbl]

    medRestored = imreconstruct(medBg,maskImg)
    
    # subtract, remove fovMask and threshold
    subImg = np.double(imgV8) - np.double(medRestored)
    
    subImg = subImg*np.double(imgFovMask)
    
    subImg[(subImg) < 0] = 0
 
    imgThNoOD = np.uint8(subImg) > 0
   
    
    #     #--- create mask to remove fov, on and vessels, hence enhance lesions
#     se = strel('disk', 5);
#     imgVess = imdilate(imgVess,se);
#     imgMask = imgFovMask & ~imgVess;
#     #---
    
    #--- Calculate wavelet background
#     imgWav = preprocessWavelet( imgV8, imgMask );
#     imgWav = preprocessWavelet( imgVforOs, imgMask );
#---
   
    #--- Calculate edge strength of lesions
    imgKirsch = kirschEdges(imgG)
    
    img0 = (imgG*np.uint8(imgThNoOD == 0))
    
    #---
    img0recon = imreconstruct(img0,imgG)
   
    img0Kirsch = kirschEdges(img0recon)
    imgEdgeNoMask = imgKirsch - img0Kirsch
  
    #---
    
# remove mask and ON (leave vessels)
    imgEdge = (np.double(imgFovMask)*imgEdgeNoMask)

 
  
    #     #--- Calculate edge strength for each lesion candidate (Matlab2009)
#     lesCandImg = zeros( newSize );
#     lesCand = bwconncomp(imgThNoOD,8);
#     for idxLes=1:lesCand.NumObjects
#         pxIdxList = lesCand.PixelIdxList{idxLes};
#         lesCandImg(pxIdxList) = sum(imgEdge(pxIdxList)) / length(pxIdxList);
#     end
#     #---
#--- Calculate edge strength for each lesion candidate (Matlab2008)
    x=int(newSize[0])
    y=int(newSize[1])
    lesCandImg = np.zeros((x,y))
    
    
    lblImg = measure.label(imgThNoOD,connectivity=2)
    
   
    # lblImg = bwlabel(imgThNoOD,8)
    lesCand = measure.regionprops(lblImg)
    
    for idxLes in range(len(lesCand)):
        pxIdxList = lesCand[idxLes].coords
        # pxIdxList=pxIdxList[0]
        pxIdxList=pxIdxList[:,0],pxIdxList[:,1]
        lesCandImg[pxIdxList] = np.sum(imgEdge[pxIdxList])/len(pxIdxList)
        
    # lesCandImg=((lesCandImg-lesCandImg.min())*255)/(lesCandImg.max()-lesCandImg.min())
    
    print(lesCandImg.max())
    print(imgEdge.max())
  

    #---
    ###################################################################################
    #     #--- Calculate edge strength for each lesion candidate (for wavelet)
#     lesCandImg = zeros( newSize );
#     lesCandImg2 = zeros( newSize );
#     lesCand = bwconncomp(imgThNoOD,8);
#     for idxLes=1:lesCand.NumObjects
#         pxIdxList = lesCand.PixelIdxList{idxLes};
#         if( length(pxIdxList) > 4 )
# #             lesCandImg(pxIdxList) = sum(imgWav(pxIdxList)) / length(pxIdxList); #mean
#             lesCandImg(pxIdxList) = std(double(imgWav(pxIdxList))); #std
#             lesCandImg2(pxIdxList) = max(imgWav(pxIdxList))-min(imgWav(pxIdxList));
#         end
#     end
#     #---
    
    # resize back
    lesCandImg = resize(lesCandImg,(origSize[0],origSize[1]))
    plt.imshow(lesCandImg)
    plt.show()
    if (showRes):
        plt.figure(442)
        plt.imshow(rgbImgOrig)
        plt.figure(446)
        plt.imshow(lesCandImg)
    
    return lesCandImg
    
    
def findGoodResolutionForWavelet(sizeIn): 
    # Parameters
    maxWavDecom = 2
    pxToAddC = 2 ** maxWavDecom - np.mod(sizeIn[1],2 ** maxWavDecom)
    pxToAddR = 2 ** maxWavDecom - np.mod(sizeIn[0],2 ** maxWavDecom)
    sizeOut = sizeIn + np.array([pxToAddR,pxToAddC])
    return sizeOut
    
    
def preprocessWavelet(imgIn = None,fovMask = None): 
    # Parameters
    maxWavDecom = 2
    
    #     # add pixel to allow wavelet decomposition
#     pxToAddC = 2^maxWavDecom - mod(size(imgIn,2),2^maxWavDecom);
#     pxToAddR = 2^maxWavDecom - mod(size(imgIn,1),2^maxWavDecom);
#     if(pxToAddC > 0 && pxToAddC <= 2^maxWavDecom)
#         imgIn( :,end+1:end+pxToAddC ) = 0;
#         fovMask( :,end+1:end+pxToAddC ) = 0;
#     end
#     if(pxToAddR > 0 && pxToAddR <= 2^maxWavDecom)
#         imgIn( end+1:end+pxToAddR,: ) = 0;
#         fovMask( end+1:end+pxToAddR,: ) = 0;
#     end
    
    imgA,imgH,imgV,imgD = pywt.swt2(imgIn,maxWavDecom,'haar')
    imgRecon = pywt.iswt2(np.zeros((imgA[:,:,2].shape,imgA[:,:,2].shape)),imgH[:,:,2],imgV[:,:,2],imgD[:,:,2],'haar')
    imgRecon[imgRecon < 0] = 0
    imgRecon = uint8(imgRecon)
    imgRecon = np.matmul(imgRecon,uint8(fovMask))
    imgOut = imgRecon * (255 / np.amax(imgRecon))
    return imgOut
    
    
def gauss1d(x = None,mu = None,sigma = None): 
    f = np.exp(- (x - mu) ** 2 / (2 * sigma ** 2)) / (sigma * np.sqrt(2 * np.pi))
    return f
    
