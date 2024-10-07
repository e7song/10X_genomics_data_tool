import sys
from datetime import datetime
import os
from functions import preprocess
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tifffile
import skimage
from skimage import io
from scipy.stats import zscore
from scipy.ndimage import rotate
from skimage.filters import gaussian
from skimage.transform import resize, radon, rotate

def log_progress(message, log_path): # credits, learned/implemented this from an IBM course
    timestamp_format = '%Y-%h-%d-%H:%M:%S' # Year-Monthname-Day-Hour-Minute-Second 
    now = datetime.now()
    timestamp = now.strftime(timestamp_format)
    log_path = path
    with open(log_path, 'a') as f:
        f.write(timestamp + ' : ' + message + '\n')
    f.close()

def data_eda(cell_boundaries, log_path):
    log_progress("Starting data EDA.", log_path)
    count_points = cell_boundaries.groupby('cell_id').size().reset_index(name = 'count')
    num_point_dct = {}
    pt_name_dct = {}
    for idx, row in count_points.iterrows():
        curr_name = row['cell_id']
        curr_num = row['count']
        num_point_dct[curr_num] = num_point_dct.get(curr_num, 0) + 1
        if pt_name_dct.get(curr_num) is None:
            pt_name_dct[curr_num] = [curr_name]
        else:
            pt_name_dct[curr_num].append(curr_name)
    log_progress("Data EDA done.", log_path)
    return pt_name_dct, num_point_dct

def process(cell_boundaries, pt_name_dct, identifier, log_path):
    log_progress("Starting cell processing.", log_path)
    # iterate through each cell to create all the cell images
    error_dct = {}
    for cell_id in pt_name_dct[25]: # all the complete cells
        current_save_path = f'{save_path}/10x_{identifier}_{cell_id}'
        if not os.path.exists(current_save_path): # if the cell has not been generated, then try and generate it
            current_cell = preprocess(cell_id, cell_boundaries)
            if type(current_cell) == str:
                if error_dct.get(current_cell, None) == None: # if error has not been encountered, create a list for it
                    error_dct[current_cell] = [cell_id]
                else:
                    error_dct[current_cell].append(cell_id) # if error has been encountered, add new instance to the list
            else: # successfully created an image array
                tifffile.imwrite(current_save_path, current_cell)
        else:
            continue # don't try and generate an existing cell

    log_progress("Finished cell processing.", log_path)
    return error_dct

if __name__ == "__main__":
    # input format:
    # py get_data.py [link?] [save directory?]

    # download, check if download is successful

    # unzip to save directory, if save directory does not exist prompt user to save to the directory specified?

    boundary_path = sys.argv[1]

    cell_boundaries = pd.read_csv(boundary_path)

    save_path = sys.argv[2]

    identifier = sys.argv[3]

    log_path = sys.arv[4]

    pt_name_dct, num_point_dct = data_eda(cell_boundaries, log_path)

    saved_files = len(os.listdir(save_path))

    error_dct = process(cell_boundaries, pt_name_dct, identifier, log_path)

    print(f'Percentage of Errors:')
    for key in error_dct.keys():
        error_rate = len(error_dct[key]) / saved_files
        print(f'{key} Error: {error_rate * 100:2f}%')

    log_progress("Writing in cells that caused an error during processing", log_path)

    error_file = f'{identifier}_errors.txt'

    with open(error_file, 'w') as f:
        f.write(str(error_dct) + '\n')
    
    f.close()