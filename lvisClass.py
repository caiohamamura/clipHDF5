
'''
A class to hold LVIS data
with methods to read
'''

###################################
import numpy as np
import h5py


###################################

class lvisData(object):
  '''
  LVIS data handler
  '''

  def __init__(self,filename,fields,nRead=-1,sInd=0,setElev=0):
    '''
    Class initialiser. Calls a function
    to read "nRead" waveforms, starting 
    at "sInd" from the file, filename
    setElev=1 converts LVIS's stop and start
    elevations to arrays of elevation.
    '''
    self.fields = fields
    self.ancillary_text = b""
    self.reference_frame = b""
    self.data={}
    # Read fields from LVIS
    self.readLVIS(filename,nRead,sInd)
    if(setElev==1):     # to save time, only read elev if wanted
      self.setElevations()


  ###########################################

  def readLVIS(self,filename,nRead,sInd):
    '''
    Read LVIS data from file
    '''
    # open file for reading
    f=h5py.File(filename,'r')
    # determine number of waveforms so we can decide how many to read
    temp=np.array(f['LFID'])
    if((nRead<0)|(temp.shape[0]<(nRead+sInd))):
      nRead=temp.shape[0]-sInd
    print("Reading",nRead,"waveforms from",filename)
    
    
    # load sliced arrays, to save RAM
    # read fields
    for field in self.fields:
      self.data[field] = f[field][sInd:nRead+sInd]
    # store the array dimensions for ease of access
    self.nWaves = nRead
    print(self.data["RXWAVE"].shape)
    self.nBins = self.data["RXWAVE"].shape[1]
    # close file
    self.ancillary_text = f["ancillary_data"]["ancillary_text"][0]
    self.reference_frame = f["ancillary_data"]["reference_frame"][0]
    f.close()


  ###########################################

  def setElevations(self):
    '''
    Decodes LVIS's RAM efficient elevation
    format and produces an array of
    elevations per waveform bin
    '''
    self.z=np.empty((self.nWaves,self.nBins))
    for i in range(0,self.nWaves):    # loop over waves
      lZ0 = self.data["Z0"][i]
      lZN = self.data["Z1023"][i]
      res = (lZ0 - lZN) / self.nBins
      self.z[i] = np.arange(lZ0, lZN, -1.0 * res)   # returns an array of floats


  ###########################################

  def getOneWave(self,ind):
    '''
    Return a single waveform
    '''
    return(self.z[ind], self.waves[ind])


###########################################

