#!/bin/bash

# Create Conda environment with specified Python version
echo "$(date +'%Y-%m-%d %H:%M:%S') - Creating Conda environment"
conda create -p ./env python=3.10 -y

# Activate the newly created environment
echo "$(date +'%Y-%m-%d %H:%M:%S') - Activating Conda environment"
source activate ./env

# Install dependencies
echo "$(date +'%Y-%m-%d %H:%M:%S') - Installing dependencies"
pip install -r requirements.txt

# Echo completion message
echo "$(date +'%Y-%m-%d %H:%M:%S') - Setup completed"
