#!/bin/bash

# activate environment
source ~/miniconda3/etc/profile.d/conda.sh
conda activate ag_python

# navigate to python scripts and execute
cd ~/Google\ Drive/Data\ Science/Projects/covid19_vic/scripts
python daily_cases.py
python daily_images.py

# navigate to project root as upcoming git commands need to be executed in repo root
cd ..

# create videos
ffmpeg -y -r:v 2.5 -i "data/images/all_vic/cases_absolute/%03d.png" -c:v libx264 -preset veryslow -pix_fmt yuv420p -crf 15 -an "web/videos/all_vic.mp4"
ffmpeg -y -r:v 2.5 -i "data/images/melb/cases_absolute/%03d.png" -c:v libx264 -preset veryslow -pix_fmt yuv420p -crf 15 -an "web/videos/melb.mp4"

# stage, commit and push changes
git add .
git commit -m "Perform auto-update of daily cases."
git push
