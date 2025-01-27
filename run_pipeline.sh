#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -o errexit
# Exit if an undeclared variable is used
set -o nounset
# Catch errors in pipelines
set -o pipefail

# Activate conda environment
conda activate aipipeline

# run SMD
echo "SMD calculation running..."
python calculate_smds_sum.py

# run catboost models
echo "Running catboost models..."
python meow.py

# plot results
echo "Plotting Results..."
python paperplots.py
