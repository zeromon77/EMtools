import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm

s = np.loadtxt("./circ_stat_series_01_1_rot_big_crop.csv", delimiter=",", skiprows=1)
im = plt.imread("./series_01_1_rot_big_crop.png")

f, (ax1, ax2) = plt.subplots(1,2, figsize=(13,5))
#int_max = s[:,-1].max()
#ax1.autoscale(False)
ax1.imshow(im, cmap=cm.gray, extent=[0,788,0,788])
ax1.set_axis_off()

ax2.imshow(im, cmap=cm.gray, extent=[0,788,0,788])
#ax1.autoscale(False)
sc = ax2.scatter(s[:,1], s[:,2], c= s[:,-1], s=20, cmap=cm.jet,edgecolor='')
ax2.set_xlim(0, 788)
ax2.set_ylim(0, 788)
ax2.set_axis_off()
cbar = f.colorbar(sc)
cbar.set_label("Intensity")


#ax2.scatter(s[:,1]-14.0, s[:,2], c= s[:,-1], s=40, cmap=cm.viridis, edgecolor='')
#ax2.set_xlim(0, 922)
#ax2.set_ylim(0, 935)
#sc = plt.scatter(s[:,1], s[:,2], c= s[:,-1], s=70, cmap=cm.viridis, edgecolor='')
#plt.xlim(0,1010)
#plt.ylim(0,1010)
#cb = ax2.colorbar(sc)
#cb.set_label("Intensity")
#plt.savefig('intensity_map.pdf', dpi=300)
plt.tight_layout()
plt.savefig("Intensity_roi_series_M5c1mx_01_1.pdf")



