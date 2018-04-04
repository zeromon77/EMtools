#!/usr/bin/env python3

# This script aligns the drifts of sequantial images and forms a single image (rigid drifit correction)
# Prerequsits: hyperspy, numpy, matplotlib

# Script information for the file.
__author__ = "Daesung Park"
__email__ = "zeromon.park@gmail.com"
__version__ = "0.2"
__copyright__ = "Copyright (c) 2017 Daesung Park"
__license__ = "GPL v2"


import hyperspy.api as hs
import matplotlib.pyplot as plt
import numpy as np
import glob
import os
from hyperspy.drawing import widgets

# change working directory path
wd = os.getcwd()
os.chdir(wd)

os.makedirs('scalebar', exist_ok=True)


# To generate and save calibration table as csv file
calibration = []
for filepath in sorted(glob.glob('*.ser')):
  img = hs.load(filepath)
  ### make a table for calibration factor
  item = [filepath, img.original_metadata.ser_header_parameters.CalibrationDeltaX[0]]
  calibration.append(item)
  np.savetxt("calibration.csv", calibration, delimiter=",", fmt='%s')
  

for filepath in sorted(glob.glob('*.ser')):
  img = hs.load(filepath)
  cal = img.original_metadata.ser_header_parameters.CalibrationDeltaX[0] * 10**9
  unit = 'nm'
  
  ### 2D alignment function from hyperspy (cross-correlation)
  img.align2D()
  resx = float(img.data.shape[2])
  resy = float(img.data.shape[1])
  dpx = resy*100/600
  
  fig = plt.figure(figsize=(6,6))
  ax = fig.add_subplot(1,1,1)

  # save corrected image as png and hdf5. The 'hdf5' file contains original intensity information an can be used for the quantification of intensity.
  filename = img.metadata.General.original_filename
  img.sum(0).save("%s.png" %(filename), overwrite=True)
  img.sum(0).save("%s.hdf5" %(filename), overwrite=True)
  #print("%s is aligned" %(filename))
  
  # Save images with scale bar in a different folder.

  os.chdir('scalebar')
  imgplot = ax.imshow(img.sum(0).data, extent=[0,cal*resx,0,cal*resy])
  #imgplot.set_clim(min, max)
  #scalebar = widgets.Scale_Bar(ax=ax, units='%s' %(unit), lw=4, color='white', max_size_ratio=0.12)
  scalebar = widgets.ScaleBar(ax=ax, units=unit, lw=4, color='white', max_size_ratio=0.15)
  #cbar = fig.colorbar(imgplot)
  
  ax.set_frame_on(False)
  ax.axes.get_yaxis().set_visible(False)
  ax.axes.get_xaxis().set_visible(False)
 
  filename = img.metadata.General.original_filename
  plt.rcParams['mathtext.fontset'] = "stix"
  plt.subplots_adjust(bottom=0, left=0, right=1, top=1)
  plt.savefig("%s.png" %(filename), frameon=False, overwrite=True, dpi=dpx)
  plt.close()
  print("%s is aligned and converted" %(filename))
  os.chdir('../')

print("Batch convert mission is completed")

