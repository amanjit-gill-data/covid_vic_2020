import geopandas as gpd
import matplotlib.cm as cm
import matplotlib.colors as col
import matplotlib.pyplot as plt
import pandas as pd
import math
from datetime import date
import calendar

# load geometry data
vic_geo_df = gpd.read_file('../data/VIC_LOCALITY_POLYGON_shp.geojson')

# load active cases data
df_all_dates = pd.read_csv('../data/all_dates.csv')

# merge geometry with active cases
vic_geo_df = pd.merge(vic_geo_df[['VIC_LGA__3', 'geometry']], df_all_dates, how = 'inner', 
    left_on = 'VIC_LGA__3', right_on = 'lga', sort = True)

# create colour map that will be used for all images
cmap = col.LinearSegmentedColormap.from_list(
    'covid_custom', [(0,'white'), (0.01, '#fffa86'), (0.25, 'yellow'), (0.5, 'red'), (0.75, 'brown'), (1, 'black')])

# create list of dates
date_list = vic_geo_df.columns.tolist()

date_list.remove('VIC_LGA__3')
date_list.remove('geometry')
date_list.remove('lga')

# define paths where image files will be stored
MELB_CASES_PATH = '../data/images/melb/cases_absolute/'
VIC_CASES_PATH = '../data/images/all_vic/cases_absolute/'

# set annotation coordinates
VIC_ANNOT_COORDS = (145.5, -34.205)
MELB_ANNOT_COORDS = (145.5, -37.45)

# define function for visualising one date
def create_image(gdf, col_name, path, img_num, annot_coords):
    
    gdf.plot(figsize = (14,10), column = col_name, cmap = cmap, k = k, 
             vmin = 0, vmax = vmax, edgecolor = 'lightblue')
    
    date_obj = date.fromisoformat(col_name)
    plt.annotate(xy = annot_coords, text = calendar.month_name[date_obj.month] + ' ' + str(date_obj.day), 
                 fontsize = 45, fontweight = 700)
    
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(path + str(img_num).zfill(3) + '.png')
    plt.close()

# create list of melb lgas
melb_lgas = ['Banyule','Bayside','Boroondara','Brimbank','Cardinia','Casey','Darebin','Frankston','Glen Eira',
'Greater Dandenong','Hobsons Bay','Hume','Kingston','Knox','Manningham','Maribyrnong','Maroondah','Melbourne',
'Melton','Monash','Moonee Valley','Moreland','Mornington Peninsula','Nillumbik','Port Phillip','Stonnington',
'Whitehorse','Whittlesea','Wyndham','Yarra','Yarra Ranges']

melb_lgas = [lga.upper() for lga in melb_lgas]

# extract just melb lgas from vic geo df
melb_geo_df = vic_geo_df[vic_geo_df['lga'].isin(melb_lgas)]

# get previous max divided by 100, and today's max divided by 100
max_prev = vic_geo_df[[date_list[i] for i in range(len(date_list)-1)]].max().max()
max_today = vic_geo_df[date_list[-1]].max()
max_prev_hundreds = math.ceil(max_prev/100)
max_today_hundreds = math.ceil(max_today/100)

vmin = 0

# if today's max hasn't beaten any previous value, just stick with the same scale as before
if (max_prev_hundreds >= max_today_hundreds):
    # create maps for just today, and keep all the previous maps
    vmax = max_prev_hundreds * 100
    k = vmax/10 # create bin size of 10
    image_number = len(date_list) - 1
    create_image(melb_geo_df, date_list[-1], MELB_CASES_PATH, image_number, MELB_ANNOT_COORDS)
    create_image(vic_geo_df, date_list[-1], VIC_CASES_PATH, image_number, VIC_ANNOT_COORDS)
    
else:
    # replace all maps with new ones, using the new vmax in the scale
    vmax = max_today_hundreds * 100
    k = vmax/10 # create bin size of 10
    for i in range(len(date_list)):
        create_image(melb_geo_df, date_list[i], MELB_CASES_PATH, i, MELB_ANNOT_COORDS)
        create_image(vic_geo_df, date_list[i], VIC_CASES_PATH, i, VIC_ANNOT_COORDS)
    # replace the old scale image with a new one
    ax = plt.subplot()
    plt.colorbar(cm.ScalarMappable(norm=col.Normalize(0, vmax), cmap=cmap), ax=ax)
    ax.remove()
    plt.savefig('../assets/images/scale.svg', bbox_inches = 'tight')
    plt.close()
