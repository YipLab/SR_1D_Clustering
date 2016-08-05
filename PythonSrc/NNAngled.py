from numpy import genfromtxt
import numpy as np
import sys
from math import atan2, degrees, pi
import os
import glob
from scipy import stats
import matplotlib.pyplot as plt

plt.ioff()

#'ThunderSTORM results_647_84A_primary_secondary.csv'
#'ThunderSTORM results_647_91E_nanobodies.csv'

FolderName = sys.argv[1]
CfgFile = 'Cfg.tmp' 

os.chdir(FolderName)

f = open(CfgFile, 'r')
FileName = f.readline()
f.close()

os.remove(CfgFile)
print(FileName)

my_data = np.loadtxt(FileName, delimiter=',', skiprows = 1, usecols = (1,2,7))


plt.scatter(my_data[:,0],my_data[:,1], s=3, facecolors='none', edgecolors='b')
##plt.scatter(my_data[0:200,0],my_data[0:200,1], s=80,marker = 'x')
if (my_data.shape[0] == 3):
    my_data = np.transpose(my_data)

DataBase = np.zeros([my_data.shape[0],4])+np.nan 
DataBase[:,0:3] = my_data
DataBase[:,3] = np.arange(my_data.shape[0])
del my_data
#plt.figure()
DminCmin = 50  ## Minimum number of closest points taken to calculate orientation
DminCmax = 4000 ## Maximum number of closest points taken to calculate orientation
MinClusterSize = 200
RelAngLim = 2
RelAngLimRad = np.tan(RelAngLim*np.pi/180)
Dmax = 200
DTransversalMax = 200
DLongitudMax = 400
ClusterNum = 0 
#if 1:
ClusterData = np.zeros([DataBase.shape[0],5])+np.nan 
ClusterData[:,0:4] = DataBase
print "\n//////////////////////////\nAnalysis in Progress\n"
print "\n//////////////////////////\n"
#yadayada 
##plt.clf()
##plt.plot(DataBase[:,0],DataBase[:,1],'o')
for kat in np.arange(len(DataBase)):#range(10):#[0]:#
    if np.isnan(ClusterData[kat,4]):
        ClusterData[kat,4] = ClusterNum
        if len(DataBase[np.isnan(ClusterData[:,4])]) > 1:## at least there is one more point to calculate the distance
            Temp = np.copy(DataBase[np.isnan(ClusterData[:,4]),0:2])
            #print 'available points = ' + str(len(Temp))
            TempIDx = np.copy(DataBase[np.isnan(ClusterData[:,4]),3])
            TempI = DataBase[kat,[0,1]]
            ##Temp[kat,:] = np.zeros(DataBase.shape[1])+np.nan
            ##TempIDx = TempIDx[~np.isnan(Temp[:,1])]
            Dist = Temp - TempI
            Dist = (Dist[:,1]**2 + Dist[:,0]**2)**0.5
            MinDistPos = Dist.argmin()
            
            DefLineCnt = 0
            TempDist = np.zeros([Temp.shape[0],2])+np.nan  ## Array that will hold the localizations that belong to the same group
            TempDistIdx = np.zeros(Temp.shape[0])+np.nan
            ##TempDistSlps = np.zeros([DminCmax,1])+np.nan  ## 
            ##TempDistIntrs = np.zeros([DminCmax,1])+np.nan  ## 
            TempDist[DefLineCnt,:] = DataBase[kat,0:2]## First gets populated with the point of consideration
            TempDistIdx[DefLineCnt] = kat
            DefLineCnt += 1
            ##
            for kat3 in np.arange(DminCmin):
                if Dist.min()<Dmax:
                    #plt.plot(Temp[MinDistPos,0],Temp[MinDistPos,1],'ko')
                    TempDist[DefLineCnt,:] = [Temp[MinDistPos,0],Temp[MinDistPos,1]]
                    TempDistIdx[DefLineCnt] = TempIDx[MinDistPos]
                    DefLineCnt += 1
                    Dist[MinDistPos] = Dist.max()
                    MinDistPos = Dist.argmin()
                    #print('min pos: ',MinDistPos)
                else:
                    break
                    ##fit cloud of poitns to a straight line and compare to the previous cloud until the angle increases more than RelAngLim or the points is more than DminCmax
            if (DefLineCnt>DminCmin/2):
                ##xTemp, yTemp = np.where(~np.isnan(TempDist))
                TempDistTest = TempDist[~np.isnan(TempDist[:,1]),:]##TempDistTest = TempDist[0:DefLineCnt-1,:]
                ##TempDistTest = TempDist[~np.isnan(TempDist)[:,0],0]
                slpO, intrcptO, r_O, p_O, errO = stats.linregress(TempDistTest[:,0],TempDistTest[:,1])
                slpI = slpO
                intrcptI = intrcptO
                ##TempDistSlps [DefLineCnt] = slpI
                ##TempDistIntrs [DefLineCnt] = intrcptI
                DefLine = True
                for kat2 in np.arange(DminCmin,Temp.shape[0]):##DefLine:
                    DistToLine = abs(slpI*Temp[MinDistPos,0]-Temp[MinDistPos,1]+intrcptI)/np.sqrt(slpI**2+1)
                    DistMinLine = TempDistTest-Temp[MinDistPos,0:2]
                    DistAlongLine = np.sqrt(sum(np.transpose(DistMinLine**2))).min()
                    if (DistToLine > DTransversalMax):
                        Dist[MinDistPos] = Dist.max()
                        MinDistPos = Dist.argmin()
                        continue
                    if (DistAlongLine > DLongitudMax):
                        Dist[MinDistPos] = Dist.max()
                        MinDistPos = Dist.argmin()
                        continue
                    #DefLine = False
                    slpO = slpI
                    TempDist[DefLineCnt,:] = [Temp[MinDistPos,0],Temp[MinDistPos,1]]
                    TempDistIdx[DefLineCnt] = TempIDx[MinDistPos]
                    ##TempDistSlps [DefLineCnt] = slpI
                    ##TempDistIntrs [DefLineCnt] = intrcptI
                    TempDistTest = TempDist[~np.isnan(TempDist[:,1]),:]
                    DefLineCnt += 1
                    slpI, intrcptI, r_I, p_I, errI = stats.linregress(TempDistTest[:,0],TempDistTest[:,1])
                    Dist[MinDistPos] = Dist.max()
                    MinDistPos = Dist.argmin()
                    #if (DefLineCnt == DminCmax):
                    #DefLine = False
                    #plt.plot(TempDistTest[:,0],TempDistTest[:,1],'k+')
                    #plt.plot(TempDistTest[1,0],TempDistTest[1,1],'bo')
                    #plt.figure()
                    #plt.plot(TempDistSlps)
                    #plt.plot(TempDistIntrs)
                #TempDistIdx = TempDistIdx[0:DefLineCnt-1,:]
                TempDistIdxTrans=TempDistIdx[~np.isnan(TempDistIdx)].astype(int)
                ClusterData[TempDistIdxTrans,4]=ClusterNum*np.ones(len(TempDistIdxTrans))
                if (len(TempDistTest)>MinClusterSize):
                    plt.scatter(TempDistTest[:,0],TempDistTest[:,1],s=10,marker = 'x',c = [(np.random.rand()),(np.random.rand()),(np.random.rand())], alpha=0.5,cmap = 'rgb')
                    NewVar = TempDistTest-TempDistTest[TempDistTest[:,0].argmin(),:]
                    slpI, intrcptI, r_I, p_I, errI = stats.linregress(NewVar[:,0],NewVar[:,1])
                    NewVarRot = (slpI*NewVar[:,0]-NewVar[:,1]+intrcptI)/np.sqrt(slpI**2+1)
                    NewVarLong = (sum(np.transpose(NewVar**2)))**0.5
                    SortPos=np.argsort(NewVarLong)
                    NewVarRot = NewVarRot[SortPos]
                    NewVarLong = NewVarLong[SortPos]
                    SaveName ='Filament' + str(ClusterNum) + '_' + FileName + '.dat'
                    ##print '\n FilenName = ' + SaveName
                    SaveData = np.zeros([len(NewVarLong),3])
                    SaveData[:,0] = NewVarLong
                    SaveData[:,1] = NewVarRot
                    SaveData[:,2] = DataBase[TempDistIdxTrans,2][SortPos]
                    f = open(SaveName,'w')
                    f.write(" %s , %s, %s  \n" % (" X1 [nm]", "Y1 [nm]", "Uncertainty [nm]"))
                    for item in SaveData:f.write(" %s , %s, %s \n" % (str(item[0]),str(item[1]),str(item[2])))
                    f.close()
                    ##TempDistIdxTrans=TempDistIdx[~np.isnan(TempDistIdx)].astype(int)
                    ##ClusterData[TempDistIdxTrans,4]=ClusterNum*np.ones(len(TempDistIdxTrans))
                ClusterNum += 1
                
            ClusterNum += 1
            
SaveName ='FilamentImg' + FileName + '.png'
plt.savefig(SaveName, dpi = 300) 

