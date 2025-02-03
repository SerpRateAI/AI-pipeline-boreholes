#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -o errexit
# Exit if an undeclared variable is used
set -o nounset
# Catch errors in pipelines
set -o pipefail

# Activate conda environment
# conda activate aipipeline

# # Check if the CSV file exists
# CSV_FILE="Datasets/dataset_smd_sum.csv"  # Replace this with path to the csv file containing smd sum values if different
# if [ ! -f "$CSV_FILE" ]; then
#     echo "CSV file not found. Running SMD calculation..."
#     # replace --path_smds with the path you've saved the smd pickle files
#     python calculate_smds_sum.py --path_smds "D:/Hamed/SerpAIpipeline/smd_outputs"
# else
#     echo "CSV file exists. Skipping SMD calculation."
# fi


# run catboost models
echo "Running catboost models..."
python meow.py

# plot results
echo "Plotting Results..."
python paperplots.py
