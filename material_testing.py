# Test file - reading images and pre-processing

# %% import libs
import numpy as np
import sys
import os
from PIL import Image

import matplotlib
# matplotlib.use('Qt5Agg')
# matplotlib.use('MACOSX')
import matplotlib.pyplot as plt


from skimage import data, filters
from skimage import exposure
from skimage.filters import try_all_threshold, threshold_otsu, threshold_li, threshold_minimum, threshold_isodata
from skimage.restoration import denoise_tv_chambolle
from skimage.filters.rank import entropy, mean_bilateral, median
from skimage.morphology import disk

# local libs
from plot_equalize import plot_img_and_hist
import uumatsci_utils as mat

print(sys.executable)
print(sys.version)

# %%
# %matplotlib --list
# %matplotlib osx

# %config InlineBackend.figure_format = 'svg'

# %% set paths
path = '/Users/ivanvasconcelos/Work/Material/'
input_path = path + 'Data/Suzanne/CT_data/'
cdir = os.getcwd()
print(input_path)
print(cdir)

# %% load image file
image_file = input_path + '6.5_GRO2_004_31MPA_30MPA_10MPA_XZ.tif'
print(image_file)
ct_image = Image.open(image_file)
ct_image.show()


# %% write image to numpy array
# Map PIL mode to numpy dtype (note this may need to be extended)
# imdtype = {'F': np.float32, 'L': np.uint8}[ct_image.mode]

# Load the data into a flat numpy array and reshape
np_ctimg = np.array(ct_image.getdata())
w, h = ct_image.size
np_ctimg.shape = (h, w, np_ctimg.size // (w * h))
print(np_ctimg.shape)
plt.figure()

# %%
plt.imshow(np.squeeze(np_ctimg), cmap=plt.cm.gray)

# %% alternative image read method
img_ct = plt.imread(image_file)
print(img_ct.shape)

plt.figure()
plt.imshow(img_ct, cmap=plt.cm.gray)

# %% extract image subset for microstructure analysis
img_ct_sub = img_ct[1000:1500, 500:1000]

print(img_ct_sub.shape)

plt.figure()
plt.imshow(img_ct_sub, cmap=plt.cm.gray)
plt.savefig('Plots/compactionCT_original.tif', dpi=400)


# %% image equalisation

# Contrast stretching
img_ct_sub_p2, img_ct_sub_p98 = np.percentile(img_ct_sub, (2, 98))
img_ct_sub_cstretch = exposure.rescale_intensity(
    img_ct_sub, in_range=(img_ct_sub_p2, img_ct_sub_p98))

plt.figure()
plt.imshow(img_ct_sub_cstretch, cmap=plt.cm.gray)
plt.colorbar()
plt.savefig('Plots/compactionCT_equalisation_testing_cstrechted.tif', dpi=400)

# Histogram Equalization
img_ct_sub_Heq = exposure.equalize_hist(img_ct_sub)

plt.figure()
plt.imshow(img_ct_sub_Heq, cmap=plt.cm.gray)
plt.colorbar()
plt.savefig('Plots/compactionCT_equalisation_testing_HistEq.tif', dpi=400)

# Adaptive Equalization
img_ct_sub_adHeq = exposure.equalize_adapthist(img_ct_sub, clip_limit=0.03)

plt.figure()
plt.imshow(img_ct_sub_adHeq, cmap=plt.cm.gray)
plt.colorbar()
plt.savefig('Plots/compactionCT_equalisation_testing_adaptHistEq.tif', dpi=400)

# Adaptive equalisation + TV denoising
img_ct_sub_adHeq_dnoise = denoise_tv_chambolle(
    img_ct_sub_adHeq, weight=0.15, eps=0.0002, multichannel=False)
plt.figure()
plt.imshow(img_ct_sub_adHeq_dnoise, cmap=plt.cm.gray)
plt.colorbar()
plt.savefig('Plots/compactionCT_equalisation_testing_adaptHistEq_dnoise.tif', dpi=400)

# Entropy in Adaptive equalisation + TV denoising
img_ct_sub_adHeq_dnoise_ent = entropy(img_ct_sub_adHeq_dnoise, disk(5))
plt.figure()
plt.imshow(img_ct_sub_adHeq_dnoise_ent, cmap=plt.cm.gray)
plt.colorbar()
plt.savefig('Plots/compactionCT_equalisation_testing_adaptHistEq_dnoise_entropy.tif', dpi=400)

# Bilateral Mean:  Adaptive equalisation + TV denoising
img_ct_sub_adHeq_dnoise_bilat = mean_bilateral(img_ct_sub_adHeq_dnoise, disk(50), s0=25, s1=25)
plt.figure()
plt.imshow(img_ct_sub_adHeq_dnoise_bilat, cmap=plt.cm.gray)
plt.colorbar()
plt.savefig('Plots/compactionCT_equalisation_testing_adaptHistEq_dnoise_bilatmean.tif', dpi=400)

# Median:  Adaptive equalisation + TV denoising
img_ct_sub_adHeq_dnoise_median = median(img_ct_sub_adHeq_dnoise, disk(3))
plt.figure()
plt.imshow(img_ct_sub_adHeq_dnoise_median, cmap=plt.cm.gray)
plt.colorbar()
plt.savefig('Plots/compactionCT_equalisation_testing_adaptHistEq_dnoise_median.tif', dpi=400)

# %% plot images and histograms

# Display results
fig = plt.figure(figsize=(10, 5))
axes = np.zeros((2, 4), dtype=np.object)
axes[0, 0] = fig.add_subplot(2, 4, 1)
for i in range(1, 4):
    axes[0, i] = fig.add_subplot(2, 4, 1+i, sharex=axes[0, 0], sharey=axes[0, 0])
for i in range(0, 4):
    axes[1, i] = fig.add_subplot(2, 4, 5+i)

ax_img, ax_hist, ax_cdf = plot_img_and_hist(img_ct_sub, axes[:, 0])
ax_img.set_title('Low contrast image')

y_min, y_max = ax_hist.get_ylim()
ax_hist.set_ylabel('Number of pixels')
ax_hist.set_yticks(np.linspace(0, y_max, 5))

ax_img, ax_hist, ax_cdf = plot_img_and_hist(img_ct_sub_cstretch, axes[:, 1])
ax_img.set_title('Contrast stretching')

ax_img, ax_hist, ax_cdf = plot_img_and_hist(img_ct_sub_Heq, axes[:, 2])
ax_img.set_title('Histogram equalization')

ax_img, ax_hist, ax_cdf = plot_img_and_hist(img_ct_sub_adHeq, axes[:, 3])
ax_img.set_title('Adaptive equalization')

ax_cdf.set_ylabel('Fraction of total intensity')
ax_cdf.set_yticks(np.linspace(0, 1, 5))

# prevent overlap of y-axis labels
fig.tight_layout()
plt.savefig('Plots/compactionCT_equalisation_testing_hist.tif', dpi=400)
plt.show()


# %% Threshold options: contrast strechted image
fig, ax = try_all_threshold(img_ct_sub_cstretch, figsize=(10, 10), verbose=False)
plt.savefig('Plots/compactionCT_cstrecht_thresholds.tif', dpi=400)
plt.show()


# %% Threshold options: adaptive-histogram-equalised image
fig, ax = try_all_threshold(img_ct_sub_adHeq, figsize=(10, 10), verbose=False)
plt.savefig('Plots/compactionCT_adHeq_thresholds.tif', dpi=400)
plt.show()

# %% Threshold options: adaptive-histogram-equalised + TV dnoise image
fig, ax = try_all_threshold(img_ct_sub_adHeq_dnoise, figsize=(10, 10), verbose=False)
plt.savefig('Plots/compactionCT_adHeq_dnoise_thresholds.tif', dpi=400)
plt.show()

# %% Threshold options: adaptive-histogram-equalised + TV dnoise image + median
fig, ax = try_all_threshold(img_ct_sub_adHeq_dnoise_median, figsize=(10, 10), verbose=False)
plt.savefig('Plots/compactionCT_adHeq_dnoise_median_thresholds.tif', dpi=400)
plt.show()

# %% Reproduce specific thresholding options

# Otsu method
thresh_otsu = threshold_otsu(img_ct_sub_adHeq_dnoise)
img_ct_sub_adHeq_dnoise_otsu = img_ct_sub_adHeq_dnoise >= thresh_otsu
plt.figure()
plt.imshow(img_ct_sub_adHeq_dnoise_otsu, cmap=plt.cm.gray)
# plt.colorbar()
plt.savefig('Plots/compactionCT_thresholded_adaptHistEq_dnoise_otsu.tif', dpi=400)

# Isodata method
thresh_isodata = threshold_isodata(img_ct_sub_adHeq_dnoise)
img_ct_sub_adHeq_dnoise_isodata = img_ct_sub_adHeq_dnoise >= thresh_isodata
plt.figure()
plt.imshow(img_ct_sub_adHeq_dnoise_isodata, cmap=plt.cm.gray)
# plt.colorbar()
plt.savefig('Plots/compactionCT_thresholded_adaptHistEq_dnoise_isodata.tif', dpi=400)

# Li method
thresh_li = threshold_li(img_ct_sub_adHeq_dnoise)
img_ct_sub_adHeq_dnoise_li = img_ct_sub_adHeq_dnoise >= thresh_li
plt.figure()
plt.imshow(img_ct_sub_adHeq_dnoise_li, cmap=plt.cm.gray)
# plt.colorbar()
plt.savefig('Plots/compactionCT_thresholded_adaptHistEq_dnoise_li.tif', dpi=400)

# Minimum method
thresh_minimum = threshold_minimum(img_ct_sub_adHeq_dnoise)
img_ct_sub_adHeq_dnoise_minimum = img_ct_sub_adHeq_dnoise >= thresh_minimum
plt.figure()
plt.imshow(img_ct_sub_adHeq_dnoise_minimum, cmap=plt.cm.gray)
# plt.colorbar()
plt.savefig('Plots/compactionCT_thresholded_adaptHistEq_dnoise_minimum.tif', dpi=400)


# %% Testing new libs
sample2_test = mat.Microstructure(3, 251)
print(sample2_test.description())
sample2_struc = sample2_test.structure
print(sample2_struc.shape)
sample2_image = sample2_test.sourceimage
print(sample2_image.shape)
