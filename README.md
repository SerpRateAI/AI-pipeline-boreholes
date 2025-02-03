<a href="https://zenodo.org/doi/10.5281/zenodo.10226092"><img src="https://zenodo.org/badge/614277711.svg" alt="DOI"></a>

# AI-pipeline-boreholes

These codes are the codes relevant to create the AI enabled pipeline for Oman Drilling Project Multi-borehole Observatory borehole BA1B.

# data availability

The core cuts images can be found here: https://www.icdp-online.org/projects/by-continent/asia/oodp-oman/public-data-2

Go to Public Images and choose BA1B in the Cores row, the zip folder whould be around 180 Mo.

The segmented images are available in the following link. please download the folder "core_images_all" where you can find images for all core images:
https://drive.google.com/drive/folders/1fvtC4qP-yYlxWZGLyOqsKw76l6tssY-c?usp=sharing

In this parent folder, you can find greyscale and segmented images for all the core sections. Tif images with names ending with "_Simple Segmentation_3" are the segmented images used for image analysis and calculation of Statistical microstructure descriptors (SMDs).
# Getting started

The SMDs calculations are already done for the ROI core images selected from core images, and sum of the first 50 values are computed and added as columns in the "Datasets\Dataset_BA1B.xlsx" (see the below if you want to redo SMD calculations from scratch or want to do it on your own images). Therefore, to reproduce the results presented in the manuscript, you can run the pipleline simply by running: 

```
bash run_pipeline.sh
```

Assuming your data is in the folders this should run the pipeline and:

1. run the ChatGPT text categorization if you have a provided API key stored in `api-key.txt`
2. assemble the data set
3. run the catboost models
4. generate the figures from the paper

## SMD calculation on your own images
If you perform SMD calcualtions on your images or similar dataset. Following scripts should be run one by one:

Step 1 : Select region of interest (ROI) from segmented images for each core:

```
python ROI_selection.py --path_imgs D:\Hamed\SerpAIpipeline\data\core_
images_all --image_size 512 --stride 128 --path_output D:\Hamed\SerpAIpipeline\data\cropped_test

This script reads the segmented images from 'path_imgs' which is the path to parent folder 'core_images_all' described above. ROIs are selected by sliding a window of size "image_size" over the images with a stride, and chooses the region with maximum fracture fraction. It saves the ROI images in each folder in "core_images_all" and also in the 'path_output' from user.

```