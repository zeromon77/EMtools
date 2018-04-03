import matplotlib.pyplot as plt
import hyperspy.api as hs
import glob
import os
import numpy as np
from hyperspy.drawing import widgets

## To generating calibration table as csv file
calibration = []
for filepath in sorted(glob.glob('*.dm3')):
  img = hs.load(filepath)
  ### make a table for calibration factor
  item = [filepath, img.original_metadata.ImageList.TagGroup0.ImageData.Calibrations.Dimension.TagGroup0.Scale]
  calibration.append(item)
  np.savetxt("calibration.csv", calibration, delimiter=",", fmt='%s')
  
for filepath in sorted(glob.glob('*.dm3')):
  img = hs.load(filepath)
  
  # get information from DM3 metadatas
  min = img.original_metadata.DocumentObjectList.TagGroup0.ImageDisplayInfo.LowLimit
  max = img.original_metadata.DocumentObjectList.TagGroup0.ImageDisplayInfo.HighLimit
  res = float(img.original_metadata.ImageList.TagGroup0.ImageData.Dimensions.Data0)
  cal = img.original_metadata.ImageList.TagGroup0.ImageData.Calibrations.Dimension.TagGroup0.Scale
  unit = img.original_metadata.ImageList.TagGroup0.ImageData.Calibrations.Dimension.TagGroup0.Units
  dpx = res*100.0/480.0
  
  ## scale bar for 2nm
  #scale = 2/cal/res
  #print scale

  fig = plt.figure()
  ax = fig.add_subplot(1,1,1)

  imgplot = ax.imshow(img.data, extent=[0,cal*res,0,cal*res])
  imgplot.set_clim(min, max)
  scalebar = widgets.ScaleBar(ax=ax, units='%s' %(unit), lw=4, color='white', max_size_ratio=0.12)
  #cbar = fig.colorbar(imgplot)
  
  
  ax.set_frame_on(False)
  ax.axes.get_yaxis().set_visible(False)
  ax.axes.get_xaxis().set_visible(False)
  #plt.axhline(y=res*(1-0.05), xmin=0.05, xmax=0.05+scale, linewidth=4, color='w')
  #ax.set_title("Sample")
  #plt.show()
  filename = img.metadata.General.get_item('title')
  
  plt.rcParams['mathtext.fontset'] = "stix"
  
#  plt.savefig("%s.png" %(filename), frameon=False, overwrite=True, dpi=dpx)
  
  plt.savefig("%s.png" %(filename), frameon=False, bbox_inches='tight', pad_inches=0, overwrite=True, dpi=dpx)
  
  
  plt.close()
  print("%s is converted" %(filename))
