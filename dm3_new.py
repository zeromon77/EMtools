import hyperspy.api as hs
import numpy as np
import glob
import os

for filepath in glob.glob('*.dm3'):
  min = img.original_metadata.DocumentObjectList.TagGroup0.ImageDisplayInfo.LowLimit
  max = img.original_metadata.DocumentObjectList.TagGroup0.ImageDisplayInfo.HighLimit
  img = hs.load(filepath)
#  img.align2D()
  filename = img.metadata.General.original_filename
  img.save("%s.png" %(filename))
  print("%s is aligned" %(filename))
