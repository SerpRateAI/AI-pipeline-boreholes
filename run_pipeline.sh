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
python smd.py

# run GPT analysis
if [[ -f "api-key.txt" ]]; then
    echo "api-key.txt found. Running GPT summarizer..."
    python GPT_extraction/gpt-summarizer.py
else
    echo "api-key.txt not found. Skipping GPT summarizer."
fi


# run catboost models
echo "Running catboost models..."
python meow.py

# plot results
echo "Plotting Results..."
python paperplots.py
