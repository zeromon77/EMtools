#!/usr/bin/env python

#### The images from XL30 are distroted
#### Autor: Daesung Park
#### desired pixels: x,y = 1067, 1424

import os
import glob
from PIL import Image

os.makedirs('corrected', exist_ok=True)
for filepath in glob.glob('*.TIF'):
    img = Image.open(filepath)
    width, height = img.size
    #print(width, height)
    height_new = int(width*1067/1424)
    #print(width, height_new)
    img = img.resize((width, height_new), Image.ANTIALIAS)
    filename, file_extension = os.path.splitext(filepath)
    os.chdir('corrected')
    img.save("%s.png" %(filename)) ## file format can be selected by changing extension of file name
    os.chdir('../')
    print("%s is corrected" %(filename))
print("XL30 distortion correction is completed")
