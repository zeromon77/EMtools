#### The images from XL30 are distroted  
#### Autor: Daesung Park
#### desired pixels: x,y = 1067, 1424 

#import matplotlib.pyplot as plt
#import numpy as np
import os
import glob
from PIL import Image

try: 
    os.makedirs('corrected')
except OSError:
    if not os.path.isdir('corrected'):
        raise

for filepath in glob.glob('*.TIF'):
    img = Image.open(filepath)
    width, height = img.size
    print(width, height)
    height_new = width*1067/1424
    print(width, height_new)
    img = img.resize((width, height_new), Image.ANTIALIAS)
    filename, file_extension = os.path.splitext(filepath)
    os.chdir('corrected')
    img.save("%s.png" %(filename))
    os.chdir('../')
    print "%s is corrected" %(filename)
print "XL30 distortion c is completed"
   
          

