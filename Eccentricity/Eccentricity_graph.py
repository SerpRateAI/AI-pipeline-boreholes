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

true_depth_list=[0.0, 0.675, 1.35, 2.7, 3.45, 4.2, 4.95, 5.7, 6.45, 7.2, 7.95, 8.7, 9.45, 10.2, 10.95, 11.7, 12.45, 13.2, 14.7, 15.45, 16.95, 17.7, 18.45, 19.2, 20.7, 21.45, 22.2, 22.95, 23.7, 24.45, 25.2, 25.95, 26.7, 27.45, 28.2, 28.95, 29.7, 30.45, 30.82, 31.2, 31.57, 31.95, 32.32, 32.7, 32.87, 33.04, 33.2, 33.825, 34.45, 35.075, 35.7, 36.45, 37.2, 37.95, 38.7, 39.45, 40.2, 40.95, 41.7, 42.7, 43.2, 43.7, 44.7, 45.45, 46.2, 46.95, 47.7, 48.45, 49.2, 49.95, 50.7, 51.45, 52.2, 52.95, 53.7, 54.45, 55.2, 55.95, 56.7, 57.45, 58.2, 58.95, 59.7, 60.45, 61.2, 61.95, 62.7, 63.45, 64.2, 64.95, 65.7, 66.45, 67.2, 67.95, 68.7, 69.45, 70.2, 70.95, 71.7, 72.45, 73.2, 73.95, 74.7, 75.45, 76.2, 76.95, 77.7, 78.45, 79.2, 79.95, 80.7, 81.45, 82.2, 82.95, 83.7, 84.45, 85.2, 85.95, 86.7, 87.45, 88.2, 88.95, 89.7, 90.45, 91.2, 91.95, 92.7, 93.45, 94.2, 94.95, 95.7, 96.45, 97.2, 97.95, 98.7, 99.45, 100.2, 100.95, 101.7, 102.45, 103.2, 103.95, 104.7, 105.45, 106.2, 106.95, 107.7, 108.45, 109.2, 109.95, 110.7, 111.45, 112.2, 112.95, 113.7, 114.45, 115.2, 115.95, 116.7, 117.45, 118.2, 118.95, 119.7, 120.45, 121.2, 121.95, 122.7, 123.45, 124.2, 124.95, 125.7, 126.45, 127.2, 127.95, 128.7, 129.45, 130.2, 130.95, 131.7, 132.45, 133.2, 133.95, 134.7, 135.45, 136.2, 136.95, 137.7, 138.45, 139.2, 139.95, 140.7, 141.45, 142.2, 142.95, 143.7, 144.45, 145.2, 145.95, 146.7, 147.45, 148.2, 148.95, 149.7, 150.45, 151.2, 151.95, 152.7, 153.45, 154.2, 154.95, 155.7, 156.45, 157.2, 157.95, 158.7, 159.45, 160.2, 160.95, 161.7, 162.45, 163.2, 163.95, 164.7, 165.45, 166.2, 166.95, 167.7, 168.45, 169.2, 169.95, 170.7, 171.45, 172.2, 172.95, 173.7, 174.45, 175.2, 175.95, 176.7, 177.45, 178.2, 178.95, 179.7, 180.45, 181.2, 181.95, 182.7, 183.45, 184.2, 184.95, 194.7, 195.45, 196.2, 196.95, 197.7, 198.45, 199.2, 199.95, 200.7, 201.45, 202.2, 202.95, 203.7, 204.45, 205.2, 205.95, 206.7, 207.45, 208.2, 208.95, 209.7, 210.45, 211.2, 211.95, 212.7, 213.45, 214.2, 214.95, 215.7, 216.45, 217.2, 217.95, 218.7, 219.45, 220.2, 220.95, 221.7, 222.45, 223.2, 223.95, 224.7, 225.45, 226.95, 227.7, 228.45, 229.2, 229.95, 230.7, 231.45, 232.2, 232.95, 233.7, 234.45, 235.2, 235.95, 236.7, 237.45, 238.2, 238.95, 239.7, 240.45, 241.2, 241.95, 242.7, 243.45, 244.2, 244.95, 245.7, 246.45, 247.2, 247.95, 248.7, 249.45, 250.2, 250.95, 251.7, 252.45, 253.2, 253.95, 254.7, 255.45, 256.2, 256.95, 257.7, 258.45, 259.2, 259.95, 260.7, 261.45, 262.2, 262.95, 263.7, 264.45, 265.2, 265.95, 266.7, 267.45, 268.2, 268.95, 269.7, 270.45, 271.2, 271.95, 272.7, 273.45, 274.2, 274.95, 275.7, 276.45, 277.2, 277.95, 278.7, 279.45, 280.2, 280.95, 281.7, 282.45, 283.2, 283.95, 284.7, 285.45, 286.2, 286.95, 287.7, 288.45, 289.2, 289.95, 290.7, 291.45, 292.2, 292.95, 293.7, 294.45, 295.2, 295.95, 296.7, 297.45, 298.2, 298.95, 299.7, 300.45, 301.2, 301.95, 302.7, 303.45, 304.2, 304.95, 305.7, 306.45, 307.2, 307.95, 308.7, 309.45, 310.2, 310.95, 311.7, 312.45, 313.2, 313.95, 314.7, 315.45, 316.2, 316.95, 317.7, 318.45, 319.2, 319.95, 320.7, 321.45, 322.2, 322.95, 323.7, 324.45, 325.2, 325.95, 326.7, 327.45, 328.2, 328.95, 329.7, 330.45, 331.2, 331.95, 332.7, 333.45, 334.2, 334.95, 335.7, 336.45, 337.2, 337.95, 338.7, 339.45, 340.2, 340.95, 341.7, 342.45, 343.2, 343.95, 344.7, 345.45, 346.2, 346.95, 347.7, 348.45, 349.2, 349.95, 350.7, 351.45, 352.2, 352.95, 362.7, 363.5, 364.05, 364.6, 365.7, 366.45, 367.2, 367.95, 368.7, 369.45, 370.2, 370.95, 371.7, 372.45, 373.2, 373.95, 374.7, 375.45, 376.2, 376.95, 383.7, 384.45, 385.2, 385.95, 386.7, 387.45, 388.2, 388.95, 389.7, 390.45, 391.2, 391.95, 392.7, 393.45, 394.2, 394.95, 395.7, 396.45, 397.2, 397.95, 398.7, 399.45, 400.2, 400.95]
prop_list=[]

for file in listdir("/Camera"):
    name = file[:-4]
    print(name)
    number = int(name[12:-4])
    print(number)
    a = 13 + len(str(number))
    number2 = int(name[a:-2])
    print(number2)
    augm_segm, count, simple_segm, raw_image = connected_components(filename=name, sigma=0.05, t=0.5, connectivity=2)

    #compute object features and extract object areas
    object_features = skimage.measure.regionprops(augm_segm)
    #object_areas = [objf["area"] for objf in object_features]
    #print(object_areas)
    #print(len(object_areas))

    #labeled = label(augm_segm > 0)  # ensure input is binary
    #data = regionprops_table(augm_segm,properties=('label', 'eccentricity'),)
    #table = pd.DataFrame(data)
    #table_sorted_by_ecc = table.sort_values(by='eccentricity', ascending=False)

    #print(table_sorted_by_ecc)


    ecc_threshold=0.90

    eccentric_objects = []
    max_objects_eccentricity = []
    max_objects_eccentricity_area=[]
    for objf in object_features:
        if objf["eccentricity"] > ecc_threshold:
            #eccentric_objects.append(objf["label"])
            #max_objects_eccentricity.append(objf["eccentricity"])
            max_objects_eccentricity_area.append(objf["area"])
    #print(max_objects_eccentricity)
    #print("Found", len(max_objects_eccentricity), "objects!")

    #Calculate % of fractures
    height, width = augm_segm.shape
    print(height, width)
    proportion = np.sum(max_objects_eccentricity_area) / (height * width)  + 100*number + 10*number2
    print(proportion, '% of fractures')

    prop_list.append(proportion)


#Display depth graph
print(prop_list)

sorted_percent1=sorted(prop_list)
print(sorted_percent1)

sorted_percent=[]
for i in range(len(sorted_percent1)):
    sorted_percent.append((sorted_percent1[i]%1)*100)
print(sorted_percent)

plt.figure()
plt.title("Core BA1B with the third Segmentation, ecc > 0.9")
plt.xlabel("Percentage of fractures")
plt.ylabel("Depth")
plt.plot(sorted_percent, true_depth_list)
plt.ylim(max(true_depth_list), min(true_depth_list))
plt.show()

'''
    for object_id, objf in enumerate(object_features, start=1):
        if objf["eccentricity"] < ecc_threshold:
            augm_segm[augm_segm == objf["label"]] = 0
        if objf["eccentricity"] >= ecc_threshold:
            augm_segm[augm_segm == objf["label"]] = 65535


    augm_segm = img_as_uint(augm_segm)
    iio.imwrite('D:/SerpRateAI/testecc2.tif', augm_segm)

    fig, ax = plt.subplots()
    plt.imshow(augm_segm)
    plt.show()
'''