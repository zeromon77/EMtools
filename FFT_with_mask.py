import numpy as np
import matplotlib.pyplot as plt

#img = plt.imread('series_30frame_CL_195mm_05_1.ser_mask_01.png')
#plt.imshow(img, cmap='gray')


### http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_transforms/py_fourier_transform/py_fourier_transform.html

#f = np.fft.fft2(img)
#fshift = np.fft.fftshift(f)
#magnitude_spectrum = 20*np.log(np.abs(fshift))
#plt.imshow(magnitude_spectrum, cmap='gray')


# When FFT of selected rectangle region leads is applied in DM, unwanted vertical and horizontal lines are generated. To remove those unwanted lines, circular mask is applied and FFT of the masked imaged is calculated. 

# In[3]:

## This section is copied from http://stackoverflow.com/questions/18352973/mask-a-circular-sector-in-a-numpy-array
## It is not my code, but I should 

def sector_mask(shape,centre,radius,angle_range):
    """
    Return a boolean mask for a circular sector. The start/stop angles in  
    `angle_range` should be given in clockwise order.
    """

    x,y = np.ogrid[:shape[0],:shape[1]]
    cx,cy = centre
    tmin,tmax = np.deg2rad(angle_range)

    # ensure stop angle > start angle
    if tmax < tmin:
            tmax += 2*np.pi

    # convert cartesian --> polar coordinates
    r2 = (x-cx)*(x-cx) + (y-cy)*(y-cy)
    theta = np.arctan2(x-cx,y-cy) - tmin

    # wrap angles between 0 and 2*pi
    theta %= (2*np.pi)

    # circular mask
    circmask = r2 <= radius*radius

    # angular mask
    anglemask = theta <= (tmax-tmin)

    return circmask*anglemask



import hyperspy.api as hs



img = hs.load('series_30frame_CL_195mm_05_1.ser.png')
img = img.data
(x,y) = img.shape
mask = sector_mask(img.shape,(x/2,y/2),x/2.1,(0,360))
img[~mask] = img.max()/2.5
#print(img.max())




f = np.fft.fft2(img)
fshift = np.fft.fftshift(f)
magnitude_spectrum = 20*np.log(np.abs(fshift))

f, (ax1, ax2) = plt.subplots(1,2)
ax1.imshow(img, cmap='gray')
ax1.set_axis_off()
ax2.imshow(magnitude_spectrum, cmap='gray')
ax2.set_axis_off()

plt.show()





