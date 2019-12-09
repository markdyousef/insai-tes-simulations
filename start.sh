#!/bin/bash

# activate virual environment
# Conda Environment
source activate zen_env
source venv/bin/activate

# export GCP environment credentials
export GOOGLE_APPLICATION_CREDENTIALS='/home/mark/Desktop/Insai/insai-eeg-cognition/service-account.json'
export GCLOUD_PROJECT="insai-zen"

# Start Jupyter Lab
jupyter lab --ip=192.168.0.152