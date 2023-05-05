import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import imageio.v3 as iio
import skimage.color
import skimage.filters
import skimage.measure
from skimage.measure import regionprops_table, label
from skimage.util import map_array
import pandas as pd
import PIL
from skimage import img_as_float, img_as_ubyte, img_as_uint
from os import listdir

mpl.use('TkAgg')

def connected_components(filename, sigma=1.0, t=0.5, connectivity=2):

    # load the image
    segmented_image="D:/SerpRateAI/Results/"+filename+"/"+filename+"_Simple Segmentation_3"+".tif"
    image = iio.imread(segmented_image)

    # convert the image to grayscale
    #gray_image = skimage.color.rgb2gray(image)

    # denoise the image with a Gaussian filter
    blurred_image = skimage.filters.gaussian(image, sigma=sigma)

    # mask the image according to threshold
    binary_mask = blurred_image > t

    # perform connected component analysis
    augm_segm, count = skimage.measure.label(binary_mask,connectivity=connectivity, return_num=True)

    #to return the raw image
    raw_dir="D:/SerpRateAI/Camera/" + filename+'.jpg'
    print(raw_dir)
    raw=iio.imread(raw_dir)

    return augm_segm, count, image, raw


#for file in listdir("D:\SerpRateAI\Camera"):
#name = file[:-4]
name='CS_5057_5_B_9_3_1'
print(name)
augm_segm, count, simple_segm, raw_image = connected_components(filename=name, sigma=0.05, t=0.5, connectivity=2)

    # labeled = label(augm_segm > 0)  # ensure input is binary
    # data = regionprops_table(augm_segm,properties=('label', 'eccentricity'),)
    # table = pd.DataFrame(data)
    # table_sorted_by_ecc = table.sort_values(by='eccentricity', ascending=False)

    # print(table_sorted_by_ecc)

    #compute object features and extract object areas
object_features = skimage.measure.regionprops(augm_segm)

ecc_threshold=0.87

for object_id, objf in enumerate(object_features, start=1):
    if objf["eccentricity"] < ecc_threshold:
        augm_segm[augm_segm == objf["label"]] = 0
    if objf["eccentricity"] >= ecc_threshold:
        augm_segm[augm_segm == objf["label"]] = 65535


augm_segm = img_as_uint(augm_segm)
iio.imwrite('D:/SerpRateAI/Results/'+ name + '/' + name + '_Augmented Segmentation_3_eccentricity_' + str(ecc_threshold) +'.tif', augm_segm)
'''
    fig, ax = plt.subplots()
    plt.imshow(augm_segm)
    plt.show()
'''