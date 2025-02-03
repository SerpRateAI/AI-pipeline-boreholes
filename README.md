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

to run the pipeline simply run

```
bash run_pipeline.sh
```

Assuming your data is in the folders this should run the pipeline and:

1. calculate the SMD features
2. run the ChatGPT text categorization if you have a provided API key stored in `api-key.txt`
3. assemble the data set
4. run the catboost models
5. generate the figures from the paper
