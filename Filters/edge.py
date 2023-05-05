import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from skimage import filters
import skimage
import imageio.v3 as iio

mpl.use('TkAgg')

def filters(filename):
    raw_image = "D:/SerpRateAI/Camera/" + filename + ".jpg"
    image = iio.imread(raw_image)
    print(image.shape)
    edge_roberts = skimage.filters.roberts(image)
    edge_sobel = skimage.filters.sobel(image)
    return edge_sobel, edge_roberts

edge_sobel, edge_roberts = filters('CS_5057_5_B_5_1_1')

fig, axes = plt.subplots(ncols=2, sharex=True, sharey=True,
                         figsize=(8, 4))

axes[0].imshow(edge_roberts, cmap=plt.cm.gray)
axes[0].set_title('Roberts Edge Detection')

axes[1].imshow(edge_sobel, cmap=plt.cm.gray)
axes[1].set_title('Sobel Edge Detection')

for ax in axes:
    ax.axis('off')

plt.tight_layout()
plt.show()