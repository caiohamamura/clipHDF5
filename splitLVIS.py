
'''
Script to split up LVIS files
'''
FIELDS = ["LON0", 
              "LON1023", 
              "LAT0", 
              "LAT1023", 
              "LFID", 
              "SHOTNUMBER", 
              "RXWAVE", 
              "TXWAVE", 
              "INCIDENTANGLE", 
              "Z0", 
              "Z1023", 
              "SIGMEAN", 
              "TIME"]


##################################################

from lvisClass import lvisData
import numpy as np
import argparse
import h5py


##################################################

def readCommands():
  p = argparse.ArgumentParser(description=("Split an LVIS file up"))
  p.add_argument("--input",dest="inName",type=str,default='/Users/dill/data/gedi/lvis/ILVIS1B_GA2016_0220_R1611_045137.h5',help=("Input filename"))
  p.add_argument("--outRoot",dest="outRoot",type=str,default='lvis.split',help=("Input filename"))
  p.add_argument("--nPer", dest ="nPer", type=int, default=1000, help=("Number of waveforms per file"))
  cmdargs = p.parse_args()
  return cmdargs


##################################################

def splitLVIS(l,nPer,outRoot):
  nBlocks=int(l.nWaves/nPer+1)
  # loop over blocks
  for i in range(0,nBlocks):
    sInd=i*nPer
    eInd=sInd+nPer
    if(sInd >= l.nWaves):
      break
    if(eInd>l.nWaves):
      eInd=l.nWaves
    # open file
    print("Splitting %d" % i)
    outName=outRoot+"."+str(i)+".h5"
    f=h5py.File(outName,'w')
    # create datasets
    for field in FIELDS:
      f.create_dataset(field,data=l.data[field][sInd:eInd])

    # Create ancillary_data
    f.create_group("ancillary_data")
    ancillary_data = f["ancillary_data"]
    ancillary_data.create_dataset('HDF5 Version', shape=(1,), data=np.bytes_(h5py.version.hdf5_version))
    ancillary_data.create_dataset('Maximum Latitude', shape=(1,), data=np.bytes_(np.str(np.max(f["LAT1023"]))))
    ancillary_data.create_dataset('Maximum Longitude', shape=(1,), data=np.bytes_(np.str(np.max(f["LON1023"]))))
    ancillary_data.create_dataset('Minimum Latitude', shape=(1,), data=np.bytes_(np.str(np.min(f["LON1023"]))))
    ancillary_data.create_dataset('Minimum Longitude', shape=(1,), data=np.bytes_(np.str(np.min(f["LON1023"]))))
    ancillary_data.create_dataset('ancillary_text', shape=(1,), data=l.ancillary_text)
    ancillary_data.create_dataset('reference_frame', shape=(1,), data=l.reference_frame)
    f.close()
    print("Written to",outName)
  
  return


##################################################

if __name__=="__main__":
  '''
  Main block
  '''
  cmdargs=readCommands()
  # read data
  l=lvisData(cmdargs.inName, FIELDS, setElev=0)
  # split it
  splitLVIS(l, cmdargs.nPer, cmdargs.outRoot)

