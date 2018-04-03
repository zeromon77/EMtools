import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
import glob
import os

## Convert xml files to cvs
for i in glob.glob('*.xml'):
  name = os.path.splitext(i)[0]
  #bashcommand = "xmltable2csv --input ./%s.xml --output ./%s.csv  --tag Data" %(name)
  bashcommand = 'xmltable2csv --input ./%s.xml --output ./%s.csv  --tag "Data"' %(name, name)
  os.system(bashcommand)


## show ADF image and intensity profile
for filepath in glob.glob('*.png'):
  filename = os.path.splitext(filepath)[0]

  s = np.loadtxt("./%s.csv" %(filename), delimiter=",", skiprows=1)
  im = plt.imread("./%s.png" %(filename))

  (height, width) = im.shape
  print(filename, width, height)
  
  f, (ax1, ax2) = plt.subplots(1,2, figsize=(15,5))
  ax1.imshow(im, cmap=cm.gray)
  ax1.set_axis_off()

  ax2.imshow(im, cmap=cm.gray, extent=[0,width,0,height])
  sc = ax2.scatter(s[:,1], s[:,2], c= s[:,-1], s=20, cmap=cm.viridis,edgecolor='')
  ax2.set_xlim(0, width)
  ax2.set_ylim(0, height)
  ax2.set_axis_off()
  cbar = f.colorbar(sc)
  cbar.set_label("Intensity")

  plt.savefig("Intensity_%s.pdf" %(filename))



