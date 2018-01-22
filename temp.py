from matplotlib import pyplot as plt
import numpy as np
import matplotlib.transforms as mtransforms

contrastName = 'blaaah'

#Make data into numpy array.
data = np.array([0.89, 0.11])
data = np.kron(data, np.ones((10,30)))

#Add border to data.
data[:, 0] = np.ones(10)
data[:, 30*2-1] = np.ones(10)
data[0, :] = np.ones(30*2)
data[10-1, :] = np.ones(30*2)

#Create figure.
fig=plt.figure(figsize = (3,1))

#Remove axis
ax=fig.add_subplot(1,1,1)
plt.axis('off')

#Add contrast vector to figure
plt.imshow(data, aspect = 'auto', cmap='Greys')

#Check for bording box.
extent = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())

#Save figure (without bording box)
plt.savefig(contrastName + '.png', bbox_inches=extent)



