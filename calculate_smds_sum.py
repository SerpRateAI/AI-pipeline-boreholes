"""

Before running this you should first run two scripts:
1) ROI_selection.py:to crop ROI images of size 512 by 512 and put them in a folder.
2) calculate_smds.py: to calculate smds for each ROI images which saves the dictionaries in an output folder

This script uses the dictionaries to calculate the sum of first 50 points (probability values) of polytope functions.

Output:
It outputs a csv file containing the core image names and sum of each polytope functions.

Usage:

python calculate_smds_sum.py --path_smds D:\Hamed\SerpAIpipeline\smd_outputs --path_output D:\Hamed\SerpAI
pipeline\smd_outputs_test

"""

import os
import joblib
import argparse
import pandas as pd
from tqdm import tqdm

## parsing arguments
def parse_args():
  """Parses arguments."""
  parser = argparse.ArgumentParser()
  parser.add_argument('--path_smds', required= True, type=str,
                       help='Path to the folder containing all dictionaries calculated with calculate_smds.py')
  parser.add_argument('--num_points', type = int, default= 50, help = 'Numnber of points to sum in the smd')

  parser.add_argument('--path_output', type =str, help= 'Path to the output folder to save dictinary containing the SMDs')
  
  return parser.parse_args()

def calculate_sum():

    args = parse_args()
    # if the output path for saving the results is not specified, save it in the Dataset folder
    if args.path_output is None:
        args.path_output =  'Datasets'
        print(f'The results will be saved in {args.path_output}...')

    numpts = args.num_points

    ## I used the same column name as I see in the Dataset excel file you had. Just added a fracture fraction (but maybe you had it already)
    my_data_dict = {
        'image_name': [],
        'fracture_fracton':[],
        'PnS2_sum': [],
        'PnP3H_sum': [],
        'PnP3V_sum': [],
        'PnP4_sum':[],
        'PnP6V_sum':[],
        'PnL_sum':[],
        'FnS2_sum': [],
        'FnP3H_sum': [],
        'FnP3V_sum': [],
        'FnP4_sum': [],
        'FnP6V_sum':[],
        'FnL_sum':[]
            
    }


    for filename in tqdm(os.listdir(args.path_smds)):


    #     print(filename)# 
        # Check if the file is a .pkl file
        if filename.endswith('.pkl'):
        
            smd_dict = joblib.load(os.path.join(args.path_smds, filename))
            
            my_data_dict['image_name'].append(os.path.splitext(filename)[0])
            my_data_dict['fracture_fracton'].append(smd_dict['s2'][0].round(decimals =4))
            
            my_data_dict['PnS2_sum'].append(smd_dict['s2'][:numpts].sum().round(decimals =4))
            my_data_dict['PnP3H_sum'].append(smd_dict['p3h'][:, 1][:numpts].sum().round(decimals =4))
            my_data_dict['PnP3V_sum'].append(smd_dict['p3v'][:, 1][:numpts].sum().round(decimals =4))
            my_data_dict['PnP4_sum'].append(smd_dict['p4'][:, 1][:numpts].sum().round(decimals =4))
            my_data_dict['PnP6V_sum'].append(smd_dict['p6'][:, 1][:numpts].sum().round(decimals =4))
            my_data_dict['PnL_sum'].append(smd_dict['L'][:, 1][:numpts].sum().round(decimals =4))
            
            #Fn sum values
            
            my_data_dict['FnS2_sum'].append(smd_dict['f2'][:numpts].sum().round(decimals =4))
            my_data_dict['FnP3H_sum'].append(smd_dict['f3h'][:, 1][:numpts].sum().round(decimals =4))
            my_data_dict['FnP3V_sum'].append(smd_dict['f3v'][:, 1][:numpts].sum().round(decimals =4))
            my_data_dict['FnP4_sum'].append( smd_dict['f4'][:, 1][:numpts].sum().round(decimals =4))
            my_data_dict['FnP6V_sum'].append(smd_dict['f6'][:, 1][:numpts].sum().round(decimals =4))
            my_data_dict['FnL_sum'].append(smd_dict['fL'][:, 1][:numpts].sum().round(decimals =4))

    df_smd = pd.DataFrame(my_data_dict)
    df_smd.to_csv(os.path.join(args.path_output, 'dataset_smd_sum.csv'), index= False)

    ## check if the sum of smds have been already calculated and the columns exist in the dataset excel file.
    ## then replace the values with new smd calulation results
    path_dataset = r'D:\Hamed\SerpAIpipeline'
    df_data = pd.read_csv(os.path.join(path_dataset, 'Dataset_BA1B.csv')) # update this to read xlsx file

    columns_to_replace = [
        'PnS2_sum',
        'PnP3H_sum',
        'PnP3V_sum',
        'PnP4_sum',
        'PnP6V_sum',
        'PnL_sum',
        'FnS2_sum',
        'FnP3H_sum',
        'FnP3V_sum',
        'FnP4_sum',
        'FnP6V_sum',
        'FnL_sum']
    
    if all(col in df_data.columns for col in columns_to_replace):
        print("All columns exist!")
    else:
        print("Some columns are missing.")

    # make a new column showing the image name that match the core names
    df_data['image_name'] = df_data['SEGMENTATION'].str.extract(r'Results/([^/]+)/')

    #to combine df_data with df_smd based on the image_name column
    # The suffixes is used to handle column name conflicts when the two dataframes being merged have columns with the same name
    # (other than the key column(s) used for the merge).
    merged_df = pd.merge(df_data, df_smd, on='image_name', how='left', suffixes=('', '_smd'))
    for col in columns_to_replace:
        merged_df[col] = merged_df[f"{col}_smd"]
        merged_df.drop(columns=[f"{col}_smd"], inplace=True)

    merged_df.to_csv(os.path.join(args.path_output, 'Dataset_BA1B_updated.csv'))






if __name__=="__main__":
    calculate_sum()