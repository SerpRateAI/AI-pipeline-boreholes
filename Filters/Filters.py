import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import imageio.v3 as iio
import skimage.color
import skimage.filters
import skimage.measure
from skimage import img_as_float, img_as_ubyte, img_as_uint


mpl.use('TkAgg')


def gaussian(filename, sigma):
    raw_image = "D:/SerpRateAI/Camera/" + filename + ".jpg"
    image = iio.imread(raw_image)
    filtered_image = skimage.filters.gaussian(image, sigma=sigma)
    return filtered_image, image

filtered_image, raw_image = gaussian('CS_5057_5_B_5_1_1', 0.5)

print(filtered_image.dtype,filtered_image.min(), filtered_image.max())
print(raw_image.dtype, raw_image.min(), raw_image.max())



fig, ax = plt.subplots()
plt.imshow(filtered_image)

fig, ax = plt.subplots()
plt.imshow(raw_image)

plt.show()
plt.axis("off");