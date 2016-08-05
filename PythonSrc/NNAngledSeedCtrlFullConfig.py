import sys
import os
import glob
import time
from subprocess import call

FolderName = sys.argv[1]
CfgFile = 'Cfg.tmp'

os.chdir(FolderName)

CurrentFiles = glob.glob('*.csv')
print "\n//////////////////////////\nSelect File to work on:\n\n"
for kat in range(len(CurrentFiles)):
    print  str(kat) + " : " + CurrentFiles[kat]

WorkFolderNum = raw_input("Enter File to process (i.e. 4):  ")

FileName = CurrentFiles[int(WorkFolderNum)]

print "\n"

DistInit = raw_input("Enter the initial radius of linear fit in nm (i.e. 200):  ")

print "\n"

SlopeErr = raw_input("Enter the acceptable error in the slope \n [0..1],(0 : exact line, 1 : no error filter):  ")

MinClusterSize = raw_input("Enter minimum number of points to be considered a filaments:  ")

DTransversalMax = raw_input("Enter maximum closest neighbour\n distance in the transversal direction in nm (200):  ")

DLongitudMax = raw_input(":Enter maximum closest neighbour\n distance in the longitunal direction in nm (800):  ")

while os.path.exists(CfgFile):
    print 'Configuration file already present \n waiting for clean up ....\n'
    time.sleep(5)

NewDir="Init"+str(DistInit)+"_SErr"+str(SlopeErr)+"_MinFil"+str(MinClusterSize)+"_MaxTrans"+str(DTransversalMax)+"_MaxLong"+str(DLongitudMax)

if os.path.isdir(NewDir):
    print NewDir
    var = raw_input("Data already processed with this settings,\n do you wish to conitnue? Y/N [N]: ")
    if (var == 'Y' or var == 'y'):
        print "Starting Analysis..."
        ##cleans up tempfolder
        shellAct = "rm -r " + NewDir + "/*"
        call(shellAct,shell = 'True')
    else:
        sys.exit("\n\n//////////////////////////////////////////////////////////\nProcessed Folder duplicated please rename your data folder (MM)\n//////////////////////////////////////////////////////////\n")
else:
    os.mkdir(NewDir)
 


CfgData = FileName+";"+str(DistInit)+";"+str(SlopeErr)+";"+str(MinClusterSize)+";"+str(DTransversalMax)+";"+str(DLongitudMax)
f = open(CfgFile, 'w')
f.write(CfgData)
f.close()

##execfile('NNAngled.py')
