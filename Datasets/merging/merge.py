import pandas as pd
from scipy.spatial import cKDTree
import numpy as np

# Load "Dataset_VCDs.xlsx" and "Dataset_BA1B_Final.xlsx"
vcds_file_path = 'Dataset_VCDs.xlsx'
ba1b_file_path = 'Dataset_BA1B_Final.xlsx'

# Load all sheets from "Dataset_VCDs.xlsx"
vcds_xls = pd.ExcelFile(vcds_file_path)

# Load 'Sheet1' from "Dataset_BA1B_Final.xlsx"
ba1b_df = pd.read_excel(ba1b_file_path, sheet_name='Sheet1')

# Prepare the BA1B depths for nearest neighbor search
# ba1b_depths = ba1b_df['TOP_DEPTH'].to_numpy()
ba1b_depths = ba1b_df['TOP_DEPTH'].fillna(-9999).to_numpy()
tree = cKDTree(ba1b_depths[:, None])

# Initialize an empty DataFrame for merged sheets
merged_sheets_df = pd.DataFrame()

# Iterate over each sheet in "Dataset_VCDs.xlsx"
for sheet_name in vcds_xls.sheet_names:
    # Load each sheet
    sheet_df = pd.read_excel(vcds_xls, sheet_name=sheet_name)

    # Handling NaN values in the sheet's depth data
    sheet_depths = sheet_df['Top depth (m downhole)'].to_numpy()
    sheet_depths_clean = sheet_depths[~np.isnan(sheet_depths)]

    # Finding nearest neighbors for the cleaned depth data
    _, indices_clean_sheet = tree.query(sheet_depths_clean[:, None])

    # Creating a mapping from sheet depths to nearest BA1B TOP_DEPTH
    nearest_top_depth_mapping_sheet = dict(zip(sheet_depths_clean, ba1b_depths[indices_clean_sheet]))

    # Applying the mapping to the sheet data
    sheet_df['Nearest_TOP_DEPTH'] = sheet_df['Top depth (m downhole)'].map(nearest_top_depth_mapping_sheet)

    # Merging the sheet data with the BA1B data
    merged_sheet_df = sheet_df.merge(ba1b_df, left_on='Nearest_TOP_DEPTH', right_on='TOP_DEPTH', how='left')

    # Combine merged sheet into the final DataFrame
    merged_sheets_df = pd.concat([merged_sheets_df, merged_sheet_df], ignore_index=True)

# Saving the combined merged DataFrame to a new Excel file
all_sheets_merged_file_path = 'Merged_All_Sheets_Dataset.xlsx'
merged_sheets_df.to_excel(all_sheets_merged_file_path, index=False)
