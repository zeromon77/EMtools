import hyperspy.api as hs
import numpy as np
import glob
import os

for filepath in sorted(glob.glob('*.ser')):
  img = hs.load(filepath)
  img.align2D()
  filename = img.metadata.General.original_filename
  img.sum(0).save("%s.png" %(filename))
  print("%s is aligned" %(filename))
