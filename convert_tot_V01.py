#!/usr/bin/env python

## This script convert 'dm3' image files from Gatan and 'ser' image files from FEI

## Prerequsits: hyperspy, numpy, matplotlib

# Script information for the file.
__author__ = "Daesung Park"
__email__ = "zeromon.park@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2017 Daesung Park"
__license__ = "GPL v2"


# standard library modules.
import matplotlib.pyplot as plt
import glob
import os
import numpy as np

# hyperspy module
import hyperspy.api as hs
from hyperspy.drawing import widgets

## To generating calibration factor table as csv file
calibration = []

## read all dm3 fils in the folder
for filepath in sorted(glob.glob('*.dm3')):
  img = hs.load(filepath)

  # get information from DM3 metadatas
  min = img.original_metadata.DocumentObjectList.TagGroup0.ImageDisplayInfo.LowLimit
  max = img.original_metadata.DocumentObjectList.TagGroup0.ImageDisplayInfo.HighLimit
  res = float(img.original_metadata.ImageList.TagGroup0.ImageData.Dimensions.Data0)
  cal = img.original_metadata.ImageList.TagGroup0.ImageData.Calibrations.Dimension.TagGroup0.Scale
  unit = img.original_metadata.ImageList.TagGroup0.ImageData.Calibrations.Dimension.TagGroup0.Units

  ### make a table for calibration factor
  item = [filepath, cal]
  calibration.append(item)
  np.savetxt("calibration_dm3.csv", calibration, delimiter=",", fmt='%s')

  ## matplotlib export setting for savefig function
  ## redefine dpi to export the image with the origing image pixel size

  dpx = res*100.0/600
  ## qt backend resolution in matplotlib 2.0 is 800 x 600 px
  ## qt backend resolution in matplotlib 1.x is 680 x 480 px
  ## savefig dpi is 100 dpi

  #fig = plt.figure(figsize=(res/my_dpi, res/my_dpi), dpi=my_dpi)
  fig = plt.figure(figsize=(6,6))
  ax = fig.add_subplot(1,1,1)
  imgplot = ax.imshow(img.data, extent=[0,cal*res,0,cal*res])

  ## correct the cut-off of intensity histogram
  imgplot.set_clim(min, max)

  ## show scale bar using widget from hyperspy
  scalebar = widgets.ScaleBar(ax=ax, units='%s' %(unit), lw=4, color='white', max_size_ratio=0.12)

  ##
  ax.set_frame_on(False)
  ax.axes.get_yaxis().set_visible(False)
  ax.axes.get_xaxis().set_visible(False)

  filename = img.metadata.General.get_item('title')

  ## Greek letters written by Latex
  plt.rcParams['mathtext.fontset'] = "stix"

  ## remove the white space around axes of images
  ## previous options to remove white spaces were  bbox_inches = 'tight', pad_inches = 0. They reducues the image size arbitrarily.
  ## New resolution is using subplots_adjust.

  plt.subplots_adjust(bottom=0, left=0, right=1, top=1)
  plt.savefig("%s.png" %(filename), frameon=False, overwrite=True, dpi=dpx)
  plt.close()
  print("%s is converted" %(filename))


### This part is for converting 'ser' files from FEI company

## To generating calibration table as csv file
calibration = []

## read all ser fils in the folder
for filepath in sorted(glob.glob('*.ser')):
  img = hs.load(filepath)

  # get information from DM3 metadatas
  #min = img.original_metadata.DocumentObjectList.TagGroup0.ImageDisplayInfo.LowLimit
  #max = img.original_metadata.DocumentObjectList.TagGroup0.ImageDisplayInfo.HighLimit
  res = float(img.original_metadata.ser_header_parameters.ArraySizeX)
  cal = img.original_metadata.ser_header_parameters.CalibrationDeltaX * 10**9
  unit = 'nm'

 ### make a table for calibration factor
  item = [filepath, img.original_metadata.ser_header_parameters.CalibrationDeltaX]
  calibration.append(item)
  np.savetxt("calibration_ser.csv", calibration, delimiter=",", fmt='%s')


  dpx = res*100/600
  #image size : 640 x 480 px
  # dpi = 100 dpi
  #value =480

  fig = plt.figure(figsize=(6,6))
  ax = fig.add_subplot(1,1,1)

  imgplot = ax.imshow(img.data, extent=[0,cal*res,0,cal*res])
  #imgplot = ax.imshow(img.data)
  #imgplot.set_clim(min, max)
  scalebar = widgets.ScaleBar(ax=ax, units=unit, lw=4, color='white', max_size_ratio=0.15)

  ax.set_frame_on(False)
  ax.axes.get_yaxis().set_visible(False)
  ax.axes.get_xaxis().set_visible(False)

  filename = img.metadata.General.original_filename

  plt.rcParams['mathtext.fontset'] = "stix"

  plt.subplots_adjust(bottom=0, left=0, right=1, top=1)
  plt.savefig("%s.png" %(filename), frameon=False, overwrite=True, dpi=dpx)
  plt.close()
  print("%s is converted" %(filename))
