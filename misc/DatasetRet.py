
import numpy as np
import matplotlib.pyplot as plt
import cv2

class DatasetRet:
    def __init__(self, obj):
        self.obj = obj
    @property
    # @abstractmethod
    def getNumOfImgs(self):
      ...
    def getImg(self,id):
        ...
    def getGT(self,id):
        ...
    def getVesselSeg(self,id,newsize):
        ...
    def getONloc(self,id):
        ...
    def getMacLoc(self,id):
        ...
    def isHealthy(self,id):
        ...

    def display(self):
        imgNum=self.getNumOfImgs()
        # se=np.strel('disk',1)
        se=cv2.getStructuringElement(shape='disk',ksize=1)

        figRes=plt.figure
        figRes2=plt.figure
        for imgIdx in range(1,imgNum):
            plt.figure(figRes)
            plt.imshow(self.getImg(imgIdx))
            input(str(imgIdx)+str(imgNum))
            imgGT,blobInfo=self.getGT(imgIdx)
            imgGTles=imgGT>0
            imgGTlesDil=cv2.dilate(imgGTles,se)
            imgGTlesCont=imgGTlesDil-imgGTles
            r,c=np.where(imgGTlesCont)
            plt.figure(figRes2)
            plt.imshow(self.getImg(imgIdx))
            plt.plot(c,r,'b')
            input(str(imgIdx)+str(imgNum))

           
           
           
            