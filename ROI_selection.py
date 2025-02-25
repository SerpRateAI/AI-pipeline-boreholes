"""" This script crops Regions of interest (ROIs) from core images which are usually large.
We assume the core images have been already segmented. 
Then, the code goes through the parent folder containing folders whose names shows the core number and sections (e.g.,CS_5057_5_B_1_1_1)
In each folder, you have the segmented images with the name ending with '...Simple Segmentation_3.tif

The images here have a fixed width of 1005 pixels but different height from 1000 to more than 5000 pixels,
with two exceptions with heights around 500 pixels (CS_5057_5_B_12_1_1 and CS_5057_5_B_12_1_2).

This script slide a window of size "image_size" over the images with a stride, and chooses the region with maximum fracture fraction.

Usage:
python ROI_selection.py --path_imgs D:\Hamed\SerpAIpipeline\data\core_
images_all --image_size 512 --stride 128 --path_output D:\Hamed\SerpAIpipeline\data\cropped_test
"""

import os
import joblib
import argparse
import numpy as np
import tifffile

## parsing arguments
def parse_args():
  """Parses arguments."""
  parser = argparse.ArgumentParser()
  parser.add_argument('--path_imgs', required= True, type=str,
                       help='Full path to parent folder containing all the core image folders. ')  
  parser.add_argument('--image_size', type= int, default= 512, help = 'ROI image size')
  parser.add_argument('--stride', type= int, default= 128, help = 'Stride for sliding over the images')
  parser.add_argument('--path_output', type =str, help= 'Path to the output folder to save ROI images')
  
  return parser.parse_args()

def crop_ROIs():
    args = parse_args()

    # image_size = 512
    # stride_x = 256 # 50% overlap in vertical direction
    # stride_y = 200
    # stride = 128
    # width = 1005
    # y_start = (width-image_size)//2 # for image_size of 512, y_start = 245, y is horizontal (width), python convensions
    for folder in os.listdir(args.path_imgs):
    #     print(f'folder: {folder}')
        img = tifffile.imread(os.path.join(args.path_imgs, folder, f'{folder}_Simple Segmentation_3.tif'))
        
        ##----------------------
        # test if there is images with dimensions smaller than image size (e.g., 512)
        ## there are two images in our image data: B_12_1_1 and B_12_1_2 both with size of (503, 1005)
        if img.shape < (args.image_size, args.image_size):
            print(f'In the following folder, the size of the core image ({img.shape}) is smaller than the selected ROI size:')
            print({folder})
            print('------------------------')
        # binarize the images
        img = np.where(img == img.max(), 1, 0).astype(np.uint8) # cause the maximum value (fracture pixel) is 128 instead of 1)
        
        height, width = img.shape
        max_x_start = height - args.image_size + 1 ## determining the lowest x_start in the image so a crop of 512 can be selected
        max_y_start = width - args.image_size + 1
        
        
        best_fracf = -1
        best_coords = (0, 0)
        best_roi_image = None
        for x in range(0, max_x_start, args.stride):
            for y in range(0, max_y_start, args.stride):
                
                ##extract the RIO
                img_roi = img[x: x + args.image_size, y:y + args.image_size]
                
                # compute fracture fraction-> as it is binary can be calcualted by mean
                fracf = np.mean(img_roi)
                
                if fracf > best_fracf:
                    best_fracf = fracf
                    best_coords = (x, y)
                    best_roi_image = img_roi
                    
        ## save the best roi image
        if best_roi_image is not None:
            # save the ROI image in the same folder as the original segmented images
            # tifffile.imwrite(os.path.join(args.path_imgs, folder, f'{folder}_ROI_x{best_coords[0]}_y{best_coords[1]}.tif'), best_roi_image)
            # save the ROI image in a separate output folder
            tifffile.imwrite(os.path.join(args.path_output, f'{folder}_ROI_x{best_coords[0]}_y{best_coords[1]}.tif'), best_roi_image)

if __name__ == "__main__":
    crop_ROIs()

        
