#!/bin/bash

conda activate ag_python
cd ~/Google\ Drive/Data\ Science/Projects/covid19_vic/scripts/

python daily_cases.py
python daily_images.py

ffmpeg -y -r:v 2.5 -i "../data/images/all_vic/cases_absolute/%03d.png" -c:v libx264 -preset veryslow -pix_fmt yuv420p -crf 15 -an "../web/videos/all_vic.mp4"
ffmpeg -y -r:v 2.5 -i "../data/images/melb/cases_absolute/%03d.png" -c:v libx264 -preset veryslow -pix_fmt yuv420p -crf 15 -an "../web/videos/melb.mp4"

git add .
git commit -m "Perform daily update"
git push
