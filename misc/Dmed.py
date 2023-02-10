import numpy as np
import os
import matplotlib.pyplot as plt
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
# # Class to access the Diabetic Macular Edema Dataset (DMED)
from .DatasetRet import DatasetRet
import cv2
import gzip
from .ReadGNDFile import ReadGNDFile
import re
from pathlib import Path
import win32com.client
import matplotlib.image as mpimg
def get_file_metadata(path, filename, metadata):
    # Path shouldn't end with backslash, i.e. "E:\Images\Paris"
    # filename must include extension, i.e. "PID manual.pdf"
    # Returns dictionary containing all file metadata.
    sh = win32com.client.gencache.EnsureDispatch('Shell.Application', 0)
    ns = sh.NameSpace(path)

    # Enumeration is necessary because ns.GetDetailsOf only accepts an integer as 2nd argument
    file_metadata = dict()
    item = ns.ParseName(str(filename))
    for ind, attribute in enumerate(metadata):
        attr_value = ns.GetDetailsOf(item, ind)
        if attr_value:
            file_metadata[attribute] = attr_value

    return file_metadata
class Dmed(DatasetRet):
    

        
    def __init__(self,dirIn): 
        #DatasetCSV  constructor
            # self = self@DatasetRet;
    
      
        self.roiExt = '.jpg.ROI'
        self.imgExt = '.jpg'
        self.metaExt = '.meta'
        self.gndExt = '.GND'
        self.mapGzExt = '.map.gz'
        self.mapExt = '.map'
        self.baseDir =dirIn

        # self.data = []
        self.data=dict([])
        idxData = 0

        for file in os.listdir(self.baseDir):
            if file.endswith(self.imgExt):
                dirList=os.path.join(self.baseDir,file)

        for file in os.listdir(self.baseDir):
            if file.endswith(self.imgExt ):
                
                self.data[idxData],ext= os.path.splitext(file)
                # filee,ext= os.path.splitext(file)
                # self.data.append(filee)
                # print(self.data)
                idxData=idxData+1
        # for i in range(0,len(dirList)):
        #     fileName = dirList[i]
        #     checkBad =[]########################
        #     # for file in os.listdir(self.baseDir):
        #     #     if  file.endswith(self.imgExt):
        #     #         pass
        #     #     else:
        #     #         checkBad=os.path.join(self.baseDir,fileName)
        #     # if (len(checkBad)==0):
        #     print("hi")

        #         # self.data[idxData] = fileName[fileName - len(self.imgExt)]#######################
        #     # self.data[idxData] =Path(str(fileName)+self.imgExt).stem
        #     # idxData = idxData + 1
        
        self.origImgNum = len(self.data)
        self.imgNum = self.origImgNum
        self.idMap = np.arange(0,self.imgNum)
        # print(self.data)
            
    def getNumOfImgs(self): 
        imgNum = self.imgNum
        
        return imgNum
        
        
    def getImg(self ,id ): 
        # print(str(id)+"hi")
        if (id < 0 or id > self.imgNum):
            img = []
            raise Exception('Index exceeds dataset size of '+str(self.imgNum))
        else:
            
            imgAddress=os.path.join(self.baseDir,self.data[self.idMap[id]]+self.imgExt)
            print(imgAddress)
            # imgAddress = self.baseDir+'/'+self.data[self.idMap[id]],self.imgExt
            img = plt.imread(imgAddress)
            
        
        return img
        
        
    def getGT(self = None,id = None): 
        if (id < 1 or id > self.imgNum):
            imgGT = []
            raise Exception('Index exceeds dataset size of '+str(self.imgNum))
        else:
            #-- decompress gz file
            mapGzFile = str(self.baseDir)+'/'+str(self.data[self.idMap[id]])+str(self.mapGzExt)
            if (os.path.exist(str(mapGzFile))):
                gzip.open(mapGzFile,self.baseDir)
            gndFile = str(self.baseDir)+'/'+str(self.data[self.idMap(id)])+str(self.gndExt)
            mapFile = str(self.baseDir)+'/'+str(self.data[self.idMap(id)])+str(self.mapExt)
            #--
    # load map info
            fMap = open(mapFile,'r')
            if (fMap > 0):
                resImg = np.fromfile(fMap,3)
                imgGT = np.fromfile(fMap,resImg[2],resImg[3])
                # fMap.close()
                imgGT = np.transpose(imgGT)
                # get description
                blobInfo = ReadGNDFile(gndFile)
            else:
                #if there is not any GND file available consider it as healthy
                blobInfo = np.array()
                img = self.getImg(id)
                imgGT = np.zeros((np.array([img.shape[1-1],img.shape[2-1]]),np.array([img.shape[1-1],img.shape[2-1]])))
            #-- remove decompressed file
            if (os.path.exist(str(mapGzFile))):
                os.delete(mapFile)
            #--
        
        return imgGT,blobInfo
        
        
    def isHealthy(self = None,id = None): 
        healthy = 1
        if (id < 1 or id > self.imgNum):
            raise Exception(np.array(['Index exceeds dataset size of ',str(self.imgNum)]))
        else:
            gndFile = np.array([self.baseDir,'/',self.data[self.idMap(id)],self.gndExt])
            if (os.path.exist(str(gndFile))):
                # get description
                blobInfo = ReadGNDFile(gndFile)
                
                lesList = re.match(blobInfo,'MicroAneurysm|Exudate')
                # lesList = regexpi(blobInfo,'MicroAneurysm|Exudate')
                for i in range(1,len(lesList)):
                    if (not len(lesList[i])==0 ):
                        healthy = 0
                        break
            else:
                healthy = 1
        
        return healthy
        
        
    def hasNoDarkLes(self = None,id = None): 
        healthy = 1
        if (id < 1 or id > self.imgNum):
            raise Exception(np.array(['Index exceeds dataset size of ',str(self.imgNum)]))
        else:
            gndFile = str(self.baseDir)+'/'+str(self.data[self.idMap(id)])+str(self.gndExt)
            if (os.path.exist(str(gndFile))):
                # get description
                blobInfo = ReadGNDFile(gndFile)
                lesList = re.match(blobInfo,'0')
                # lesList = regexpi(blobInfo,'0')
                for i in range(1,len(lesList)):
                    if (not len(lesList[i])==0 ):
                        healthy = 0
                        break
            else:
                healthy = 1
        
        return healthy
        
        
    def hasNoBrightLes(self = None,id = None): 
        healthy = 1
        if (id < 1 or id > self.imgNum):
            raise Exception('Index exceeds dataset size of '+str(self.imgNum))
        else:
            gndFile = str(self.baseDir)+'/'+str(self.data[self.idMap(id)])+str(self.gndExt)
            if (os.path.exist(str(gndFile))):
                # get description
                blobInfo = ReadGNDFile(gndFile)
                lesList = re.match(blobInfo,'1')
                for i in range(1,len(lesList)):
                    if (not len(lesList[i])==0 ):
                        healthy = 0
                        break
            else:
                healthy = 1
        
        return healthy
        
        
    def hasNoExudates(self = None,id = None): 
        healthy = 1
        if (id < 1 or id > self.imgNum):
            raise Exception('Index exceeds dataset size of '+str(self.imgNum))
        else:
            gndFile = str(self.baseDir)+'/'+str(self.data[self.idMap(id)])+str(self.gndExt)
            if (os.path.exist(str(gndFile))):
                # get description
                blobInfo = ReadGNDFile(gndFile)
                lesList = re.match(blobInfo,'Exudate')
                for i in range(1,len(lesList)):
                    if (not len(lesList[i])==0 ):
                        healthy = 0
                        break
            else:
                healthy = 1
        
        return healthy
        
        
    def getQuality(self = None,id = None): 
        if (id < 1 or id > self.imgNum):
            imgVess = []
            raise Exception('Index exceeds dataset size of '+str(self.imgNum))
        else:
            metaFile = str(self.baseDir)+'/'+str(self.data[self.idMap(id)])+str(self.metaExt)
            fMeta = open(metaFile,'r')
            if (fMeta > 0):
                res = chr(np.fromfile(fMeta))
                res = np.transpose(res)
                fMeta.close()
                tok,mat = re.match(res,'QualityValue\W+([0-9\.]+)','tokens')
                if (not len(tok)==0 ):
                    qa = int(tok[0])
                else:
                    qa = - 1
            else:
                qa = - 1
        
        return qa
        
        
    def getEthnicity(self = None,id = None): 
        if (id < 1 or id > self.imgNum):
            ethnicityStr = []
            raise Exception(np.array(['Index exceeds dataset size of ',str(self.imgNum)]))
        else:
            metaFile = np.array([self.baseDir,'/',self.data[self.idMap(id)],self.metaExt])
            fMeta = open(metaFile,'r')
            if (fMeta > 0):
                res = chr(np.fromfile(fMeta))
                res = np.transpose(res)
                fMeta.close()
                tok,mat = re.match(res,'PatientRace\~(\w+)','tokens')
                if (not len(tok)==0 ):
                    ethnicityStr = np.array(tok[0])
                    # ethnicityStr = cell2mat(tok[0])
                else:
                    ethnicityStr = []
            else:
                ethnicityStr = []
        
        return ethnicityStr
        
        #Get other attribute
        
    def getMetaAttr(self = None,id = None,attrIn = None): 
        if (id < 1 or id > self.imgNum):
            attrStr = []
            raise Exception('Index exceeds dataset size of '+str(self.imgNum))
        else:
            metaFile = str(self.baseDir)+'/',str(self.data[self.idMap(id)]),str(self.metaExt)
            fMeta = open(metaFile,'r')
            if (fMeta > 0):
                res = chr(np.fromfile(fMeta))
                res = np.transpose(res)
                fMeta.close()
                tok,mat = re.match(res,np.array([attrIn,'~([a-z\s\.\/\\0-9]+).+']),'tokens')
                if (not len(tok)==0 ):
                    attrStr = (np.array(tok[0])).strip()############ remove white space from string
                else:
                    attrStr = []
            else:
                attrStr = []
        
        return attrStr
        
        
    def getVesselSeg(self = None,id = None,newSize = None): 
        ##getVesselSegRS: get vessels. if newSize is given, it specifies the final size of the image
        imgVess = []
        if (id < 1 or id > self.imgNum):
            raise Exception('Index exceeds dataset size of '+str(self.imgNum))
        else:
            vessAddress = str(self.baseDir)+'/'+str(self.data[self.idMap(id)])+'_vess.png'
            if (os.path.exist(str(vessAddress))):
                if (id==None and newSize==None):
                #################################
                    imgOrig = self.getImg(id)
                    newSize = imgOrig.shape
                imgVess = plt.imread(vessAddress)
                imgVess = cv2.resize(imgVess,newSize(np.arange(1,2+1)))
                # binarise
                imgVess = imgVess > 30
        
        return imgVess
        
        
    def getONloc(self,id): 
        onRow = []
        onCol = []
        if (id < 0 or id > self.imgNum):
            raise Exception('Index exceeds dataset size of '+str(self.imgNum))
        else:
            metadata = ['ONcol', 'ONrow']
            # metaFile=os.path.join(self.baseDir,self.data[self.idMap[id]]+str(self.metaExt))
            metaFile=self.baseDir+'/'+self.data[self.idMap[id]]+self.metaExt
            # metaFile = str(self.baseDir)+'/'+str(self.data[self.idMap(id)])+str(self.metaExt)
            fMeta = open(metaFile,'r')
            if (fMeta):
                # res = str(np.fromfile(fMeta))
                res=fMeta.read()
                # res = np.transpose(res)
                # print(res)
                fMeta.close()
                tokRow = re.search('ONrow\W+([0-9\.]+)',res)
                tokCol = re.search('ONcol\W+([0-9\.]+)',res)
                if (tokRow  and  tokCol):
                    onRow = int(tokRow.group().split('~')[1])
                    onCol = int(tokCol.group().split('~')[1])
        
        return onRow,onCol
        
        
    def getMacLoc(self = None,id = None): 
        if (id < 1 or id > self.imgNum):
            macRow = []
            macCol = []
            raise Exception('Index exceeds dataset size of '+str(self.imgNum))
        else:
            onRow = - 1
            onCol = - 1
        
        return macRow,macCol
        
        
    def setBoundaries(self = None,startIdx = None,endIdx = None): 
        if (startIdx > self.origImgNum or startIdx < 1):
            raise Exception('Wrong boundaries')
        
        if (endIdx > self.origImgNum or endIdx < 1):
            raise Exception('Wrong boundaries')
        
        # set boundary
        self.imgNum = endIdx - startIdx + 1
        self.idMap = np.arange(startIdx,endIdx+1)
        return
        
        
    def resetBoundaries(self = None): 
        self.imgNum = self.origImgNum
        self.idMap = np.arange(1,self.imgNum+1)
        return
        
        
    def getName(self = None,id = None): 
        if (id < 1 or id > self.imgNum):
            img = []
            raise Exception('Index exceeds dataset size of '+str(self.imgNum))
        else:
            imgName = self.data[self.idMap(id)]
            imgExt = self.imgExt
        
        return imgName,imgExt
        
        
    def getMetaFileLoc(self = None,id = None): 
        ##getMetaFileLoc: returns the location of the metafile for the given
    ##id, check if it exist and return the information in isPresent
        if (id < 1 or id > self.imgNum):
            img = []
            raise Exception('Index exceeds dataset size of ',str(self.imgNum))
        else:
            metaFileLoc = str(self.baseDir)+'/'+str(self.data[self.idMap(id)])+str(self.metaExt)
            fMeta = open(metaFileLoc,'r')
            if (fMeta > 0):
                isAvailable = 1
            else:
                isAvailable = 0
        
        return metaFileLoc,isAvailable
        
        
    def showLesions(self = None,id = None): 
        if (id < 1 or id > self.imgNum):
            img = []
            raise Exception('Index exceeds dataset size of '+str(self.imgNum))
        else:
            imgIdx = self.idMap(id)
            se = se=cv2.getStructuringElement(shape='disk',ksize=1)######################
            #------- Show lesions
    # Get and resize ground truth labels
            imgGT,blobInfo = self.getGT(imgIdx)
            #-- find lesion ids and associate a different colour
            lesIdList = np.array([])
            lesColList = np.array([])
            # Find MA
            lesMaList = re.match(blobInfo,'MicroAneurysm')
            tmpIdList = []
            for i in range(1,len(lesMaList)):
                if (not len(lesMaList[i])==0 ):
                    tmpIdList[-1] = i#############################
            lesIdList[0] = tmpIdList
            lesColList[0] = 'r'
            # Find Exudates
            lesExList = re.match(blobInfo,'Exudate')
            tmpIdList = []
            for i in np.arange(1,len(lesExList)+1).reshape(-1):
                if (not len(lesExList[i])==0 ):
                    tmpIdList[len(tmpIdList)+1] = i
            lesIdList[2] = tmpIdList
            lesColList[2] = 'y'
            # Find everything else
            tmpIdList = []
            for i in np.arange(1,len(lesMaList)+1).reshape(-1):
                if (len(lesMaList[i])==0 and len(lesExList[i])==0):
                    tmpIdList[len(tmpIdList)+1] = i
            lesIdList[3] = tmpIdList
            lesColList[3] = 'b'
            #--
    # show image
            plt.imshow(self.getImg(imgIdx))
            # hold('on')
            for idxLesType in range(1,len(lesIdList)):
                tmpLesList = lesIdList[idxLesType]
                imgGTles = np.zeros((imgGT.shape,imgGT.shape))
                for idxLes in np.arange(1,len(tmpLesList)+1).reshape(-1):
                    imgGTles = np.logical_or(imgGTles,(imgGT == tmpLesList(idxLes)))
                imgGTlesDil = cv2.dilate(imgGTles,se)
                imgGTlesCont = imgGTlesDil - imgGTles
                # plot lesions
                r,c = np.where(imgGTlesCont)
                plt.plot(c,r,np.array(['.',lesColList[idxLesType]]))
            # hold('off')
            #-------
        
        return
        
        
    def display(self): 
        imgNum = self.getNumOfImgs()
        figRes = plt.figure
        figRes2 = plt.figure
        for imgIdx in range(0,imgNum):
            plt.figure(figRes)
            plt.imshow(self.getImg(imgIdx))
            input(('Img '+str(imgIdx)+' of '+str(imgNum)+', QA '+str(self.getQuality(imgIdx))+', press enter to show lesions'))
            plt.figure(figRes2)
            self.showLesions(imgIdx)
            input('Img '+str(imgIdx)+' of '+str(imgNum)+', press enter for next image')
        
        return
        
        
    def displayImg(self = None,id = None): 
        if (id < 1 or id > self.imgNum):
            img = []
            raise Exception('Index exceeds dataset size of '+str(self.imgNum))
        else:
            imgIdx = self.idMap(id)
            figRes = plt.figure
            figRes2 = plt.figure
            plt.figure(figRes)
            plt.imshow(self.getImg(imgIdx))
            plt.figure(figRes2)
            self.showLesions(imgIdx)
        
        return
        