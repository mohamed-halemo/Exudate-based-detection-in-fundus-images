#This prototype software is experimental in nature.
#UT-Battelle, LLC AND THE GOVERNMENT OF THE UNITED STATES OF AMERICA
#MAKE NO REPRESENTATIONS AND DISCLAIM ALL WARRANTIES, BOTH EXPRESSED AND IMPLIED.
#THERE ARE NO EXPRESS OR IMPLIED WARRANTIES OF MERCHANTABILITY OR FITNESS FOR A
#PARTICULAR PURPOSE, OR THAT THE USE OF THE SOFTWARE WILL NOT INFRINGE ANY PATENT,
#COPYRIGHT, TRADEMARK, OR OTHER PROPRIETARY RIGHTS, OR THAT THE SOFTWARE WILL ACCOMPLISH
#THE INTENDED RESULTS OR THAT THE SOFTWARE OR ITS USE WILL NOT RESULT IN INJURY OR DAMAGE.
#The user assumes responsibility for all liabilities, penalties, fines, claims, causes of
#action, and costs and expenses, caused by, resulting from or arising out of, in whole or in
#part the use, storage or disposal of the SOFTWARE.
#Reads the GND file including the blob IDs and the manifestations / states
# # # # Disclaimer:
# #  This code is provided "as is". It can be used for research purposes only and all the authors
# #  must be acknowledged.
# # # # Authors:
# # Priya Govindasamy
# # # # Date:
# # 2010-03-01
# # # # Version:
# # 1.0
# # # # Description:
# # Class to access the Diabetic Macular Edema Dataset (DMED)
import numpy as np
    
def ReadGNDFile(sF = None): 
    fid = open(sF)
    sLine = fgetl(fid)
    
    bGetNotes = 0
    Notes = '(none)'
    if (strcmpi(sLine,'GNDVERSION2.0 (INCLUDES NOTES AT THE END OF THE FILE)')):
        sLine = fgetl(fid)
        bGetNotes = 1
    
    NumberOfBlobEntries = sscanf(sLine,'%f')
    BlobIDs = cell(NumberOfBlobEntries,1)
    for i in np.arange(1,NumberOfBlobEntries+1).reshape(-1):
        sLine = fgetl(fid)
        BlobIDs[i] = sLine
    
    sLine = fgetl(fid)
    
    NumberOfChosenCharacteristics = sscanf(sLine,'%f')
    Characteristics = cell(NumberOfChosenCharacteristics,1)
    for i in np.arange(1,NumberOfChosenCharacteristics+1).reshape(-1):
        sLine = fgetl(fid)
        Characteristics[i] = sLine
    
    sLine = fgetl(fid)
    NumberOfManifestations = sscanf(sLine,'%f')
    sLine = fgetl(fid)
    MaxNumberOfStates = sscanf(sLine,'%f') - 1
    ManifestationAndStateTypes = cell(NumberOfManifestations,2)
    for i in np.arange(1,NumberOfManifestations+1).reshape(-1):
        Manifestation = fgetl(fid)
        for j in np.arange(1,MaxNumberOfStates+1).reshape(-1):
            sLine = fgetl(fid)
            if (len(sLine)==0):
                pass
            else:
                if (j == 1):
                    States = cell(1,1)
                States[j,1] = sLine
        ManifestationAndStateTypes[i,1] = Manifestation
        ManifestationAndStateTypes[i,2] = States
    
    ActualStates = cell(NumberOfManifestations,1)
    for i in np.arange(1,NumberOfManifestations+1).reshape(-1):
        ActualStates[i] = fgetl(fid)
    
    sLine = fgetl(fid)
    
    sLine = fgetl(fid)
    
    sLine = fgetl(fid)
    
    sLine = fgetl(fid)
    
    CDRatio = sscanf(sLine,'%f')
    if (bGetNotes):
        Notes = fgetl(fid)
    
    fid.close()
    return BlobIDs,ManifestationAndStateTypes,ActualStates,CDRatio,Notes