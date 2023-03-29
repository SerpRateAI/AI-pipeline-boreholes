import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import imageio.v3 as iio
import skimage.color
import skimage.filters
import skimage.measure
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

for file in listdir("D:\SerpRateAI\Camera"):
    name = file[:-4]
    print(name)
    augm_segm, count, simple_segm, raw_image = connected_components(filename=name, sigma=0.05, t=0.5, connectivity=2)


    # compute object features and extract object areas
    object_features = skimage.measure.regionprops(augm_segm)
    object_areas = [objf["area"] for objf in object_features]
    print(object_areas)


    #extract only objects with area > min_area
    min_area = 50

    large_objects = []
    large_objects_area = []
    for objf in object_features:
        if objf["area"] > min_area:
            large_objects.append(objf["label"])
            large_objects_area.append(objf["area"])
    print(large_objects_area)
    print("Found", len(large_objects), "objects!")
    
    #Calculate the % of fractures
    height, width = augm_segm.shape
    print(height, width)
    proportion=np.sum(large_objects_area)/(height*width)
    print(proportion*100, '% of fractures')
    
    #change format to shutdown smaller objects easily
    print(simple_segm.dtype, augm_segm.min(), augm_segm.max())
    print(augm_segm.dtype, augm_segm.min(), augm_segm.max())
    augm_segm = img_as_uint(augm_segm)
    print(augm_segm.dtype, augm_segm.min(), augm_segm.max())
    
    #keep only bigger objects
    for object_id, objf in enumerate(object_features, start=1):
        if objf["area"] < min_area:
            augm_segm[augm_segm == objf["label"]] = 0
        if objf["area"] >= min_area:
            augm_segm[augm_segm == objf["label"]] = 65535
    
    print(augm_segm.dtype, augm_segm.min(), augm_segm.max())
    
    
    #save results
    iio.imwrite('D:/SerpRateAI/Results/'+ name + '/' + name + '_Augmented Segmentation_3_' + str(min_area) +'.tif', augm_segm)
    
    '''



#for overlay view
    colored = skimage.color.label2rgb(augm_segm, colors=['yellow'], alpha=0.8, image=raw_image, saturation=1, bg_label=0, bg_color=None)
    print(colored)
    print(colored.shape, augm_segm.shape, raw_image.shape)


    im = PIL.Image.fromarray((colored * 255).astype(np.uint8))

    iio.imwrite('D:/SerpRateAI/Results/'+name+'/'+name+'_overlay_view.png', im)

    
#display results
    fig, ax = plt.subplots()
    plt.imshow(colored)
    
'''
    fig, ax = plt.subplots()
    plt.imshow(raw_image)
    
    fig, ax = plt.subplots()
    plt.imshow(augm_segm)
    
    plt.show()
    plt.axis("off");

