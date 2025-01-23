"""This script calculates the polytope functions for 2D imgages from a IODP expedition.
Before running this script, you should first crop ROI images of size 512 by 512 and put them in a folder.
Imges should be binary (0 and 1) with 1 for your feature of interest (fractures).
if you have images of different size, you should do some changes in cpp code and recompile it (Cpp_source-> Polytope->Sample_Pn_UU.cpp):

#define MAXX 513 --> change this to your image_size + 1 (e.g., for image size of 256, it should be 257)
#define Nt 256 --> change this to half of you image size (e.g., for image size of 256, it should be 128)

Output:
This script saves a dictionary for each image in the output folder specified by user.
In each dictionary, the polytope functions (s2, p3, p4, ..L, f2, f3, f4, fL) are the keys and values are the probabilities at each distance r.
The name of each dictionary shows the core image name.

Usage:
python calculate_smds.py --path_ROI_imgs D:\Hamed\SerpAIpipeline\data\cropped_ROIs --cpathPn Cpp_source_512\Cpp_source\Polytope --runtimePn C
pp_source_512\runtime --outputPn Cpp_source_512\runtime\output --path_output D:\Hamed\SerpAIpipeline\smd_outputs_test


"""

import os
import joblib
import argparse
from tqdm import tqdm
from src.SMDs import calculate_polytopes, calculate_smd_list

import tifffile


## parsing arguments
def parse_args():
  """Parses arguments."""
  parser = argparse.ArgumentParser()
  parser.add_argument('--path_ROI_imgs', required= True, type=str,
                       help='Path to the folder containing all the ROI images selected with ROI_selection.py.')
  # parser.add_argument('--path_cpp_code', type=str, required= True, help='Path to the folder containing compiled cpp codes for different image sizes')
  parser.add_argument('--image_size', type = int, default= 512, help = 'The size of ROI images')
  parser.add_argument('--cpathPn', type= str, help = 'path to polytope folder in cpp_source')
  parser.add_argument('--runtimePn', type= str, help = 'path to runtime folder in cpp_source')
  parser.add_argument('--outputPn', type= str, help = 'path to output folder in runtime')

  parser.add_argument('--path_output', type =str, help= 'Path to the output folder to save dictinary containing the SMDs')
  
  return parser.parse_args()

def quantify_imgs():
    args = parse_args()


    # path to cpp folders, this works when the full path is provided, not reelative path
    cpathPn = args.cpathPn
    runtimePn = args.runtimePn + '/'
    outputPn = args.outputPn + '/'

    # ##hard coded path for image size of 512 by 512 (path to the folders here in github folder)
    # cpathPn = r'Cpp_source_512\Cpp_source\Polytope'
    # runtimePn = r'Cpp_source_512\runtime/'
    # outputPn = r'Cpp_source_512\runtime\output/'


    par={'name':'polytopes','begx': 0, 'begy': 0, 'nsamp': args.image_size, 'edge_buffer': 0,
    'equalisation': False, 'equal_method': 'adaptive', 'stretch_percentile': 2,
    'clip_limit': 0.03, 'tvdnoise': False, 'tv_weight': 0.15, 'tv_eps': 2e-04,
    'median_filter': False, 'median_filter_length': 3,
    'thresholding_method': 'manual', 'thresholding_weight': 0.85, 'nbins': 256,
    'make_figs': False, 'fig_res': 400, 'fig_path':'./Plots/'}

    list_polytopes = ['p2', 'p3h', 'p3v','p4','p6', 'L']
    # list_polytopes = ['p2']
    

    for filename in tqdm(os.listdir(args.path_ROI_imgs)):
        if filename.endswith(".tif"):
            # Remove the file extension
            name_without_ext = os.path.splitext(filename)[0]  # e.g. CS_5057_5_B_9_4_1_ROI_x1152_y256

            # Split at '_ROI_' and take the first part
            parts = name_without_ext.split("_ROI_")
            prefix = parts[0]  # e.g. CS_5057_5_B_9_4_1

            print(prefix)
            img = tifffile.imread(os.path.join(args.path_ROI_imgs, filename))
    #         print(f'image shape = {img.shape}')
            
            # calculate smds
            poly_dict = {}
            for poly in list_polytopes:
                
                if poly == 'p2':

                    s2, f2 = calculate_smd_list(img)
                    poly_dict['s2'] = s2
                    poly_dict['f2'] = f2
    #                 print(f"S2 shape: {poly_dict['s2'].shape}")
                    
                else:
                    poly1, poly2 = calculate_polytopes(img, par, outputPn, cpathPn, runtimePn, polytope = poly)
                    poly_dict[poly] = poly1
                    # we determine the name of poly stored in the dict as key: f3h, f3v, f4, f6, fL
                    poly2_name = poly.replace('p', 'f') if poly.startswith('p') else 'f' + poly
                    poly_dict[poly2_name] = poly2
    #                 print(f"{poly} shape: {poly_dict[poly][0].shape}")
    #                 print(f'polytope {poly} done!')
                    
            joblib.dump(poly_dict, os.path.join(args.path_output, f'{prefix}.pkl'))


if __name__=="__main__":
    quantify_imgs()