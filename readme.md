# COVID-19 in Victoria by LGA

## Overview 

This project was conducted in 2020, during the second significant wave of COVID-19 in Victoria, Australia. Its website is located at https://the2ndwave.amanjitgill.com.

## Tasks 

- Wrote Jupyter [notebooks](notebooks/) to scrape daily COVID-19 cases by LGA (local government area) and generate spatial heatmaps for Victoria and Melbourne.

- Once the notebooks were working, I turned them into Python [scripts](scripts/) and invoked them once a day, using a [bash script](daily_update.sh). This script was itself automatically triggered using a cron job.

- To the bash script, I added calls to `ffmpeg` to turn the generated spatial heatmaps into time-lapse videos showing the progression of COVID-19 through Victoria. 

- Created an interactive [Dash visualisation](lga_graphs.py) allowing users to enter the name of any Victorian LGA and see a time-series graph of its COVID-19 cases. This app also allows users to compare multiple LGAs on the same graph. 

- Initially published the Dash app on Heroku, but I'm now using DigitalOcean to serve it, because it offers fast load times (no 'sleep' mode) at a low cost.

- Wrote a website in `html/css` and used this to publish both the time-lapse videos and the Dash app. This is published through GitHub Pages and available at the URL above. 








