import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
import random
import shutil
from scipy.ndimage import distance_transform_edt
import torch
import torch.nn.functional as F
from scipy.ndimage import binary_erosion
import tifffile
from scipy import stats as st
import skimage
from skimage import io
from scipy.stats import zscore
from scipy.ndimage import rotate
from skimage.filters import gaussian
from skimage.transform import resize, radon, rotate
from skimage.feature import canny
#from datagen_utils import *
import matplotlib.pyplot as plt
import os
import random
import shutil
from scipy.ndimage import zoom
import sys
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
import matplotlib.pyplot as plt
from torch.utils.data import Dataset, DataLoader
import neptune
from sklearn.cluster import KMeans
import umap
from sklearn.manifold import TSNE
import shapely
from sklearn.decomposition import PCA

def find_rotation_angle(cell_image):
    # Convert the image to binary
    binary_image = (cell_image > 0).astype(np.uint8)
    # Find the indices of non-zero pixels in the binary image
    non_zero_indices = np.transpose(np.nonzero(binary_image))
    # Compute the covariance matrix of the non-zero pixel indices
    covariance_matrix = np.cov(non_zero_indices, rowvar=False)
    # Compute the eigenvectors of the covariance matrix
    eigenvalues, eigenvectors = np.linalg.eigh(covariance_matrix)
    # Extract the angle of rotation from the eigenvectors
    angle = np.arctan2(eigenvectors[0, 1], eigenvectors[0, 0]) * 180 / np.pi
    return angle
def add_outline(image, outline_width):
    # Create a larger image with the specified outline width
    padded_image = np.zeros((image.shape[0] + 2 * outline_width, image.shape[1] + 2 * outline_width), dtype=image.dtype)
    padded_image[outline_width:-outline_width, outline_width:-outline_width] = image  # Place the original image in the center
    return padded_image

def preprocess(cell_id, cell_boundaries, resolution = 100, bounds = 128):
    # get the cell
    cell = get_cell(cell_id, cell_boundaries)
    # establish its bounding box
    minx, miny, maxx, maxy = cell.bounds
    # create a meshgrid
    x = np.linspace(minx, maxx, resolution)
    y = np.linspace(miny, maxy, resolution)
    xx, yy = np.meshgrid(x, y)
    # create the polygon
    cell_polygon = np.zeros(xx.shape)
    for i in range(xx.shape[0]):
        for j in range(xx.shape[1]):
            pt = shapely.Point(xx[i, j], yy[i, j])
            if cell.contains(pt):
                cell_polygon[i, j] = 1
    cell_polygon = np.flipud(cell_polygon)
    angle = find_rotation_angle(cell_polygon)
    cell_cropped = rotate(cell_polygon, angle, resize=True)
    # Finding the initial bounding box, not necessarily square
    rows, cols = np.where(cell_cropped > 0)
    # Early exit conditions: cell too small (shouldn't happen anymore) or cell does not exist
    if len(rows) == 0 or len(cols) == 0:
        # Handle the case where there are no non-zero elements
        return "no non-zero"
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    # Too close to the wall
    if min_row - 2 < 0 or max_row + 2 > cell_cropped.shape[0]:
        return "out of bounds, 2 pixel"
    if min_col - 2 < 0 or max_col + 2 > cell_cropped.shape[1]:
        return "out of bounds, 2 pixel"
    # Cell at this point has been isolated with a padding of 2!
    cell_cropped = cell_cropped[min_row-2:max_row+2, min_col-2:max_col+2] # no clipping issues? border cells have been removed, but should still add a manual check!!!!!
    height = cell_cropped.shape[0]
    width = cell_cropped.shape[1]
    # Finding the ratio at which to scale the cell
    if height <= 0 or width <= 0:
        return "Division by Zero"
    if height > width:
        ratio = (bounds - 2)/height
    else:
        ratio = (bounds - 2)/width
    # Scaling the cell to fit in the backdrop
    try:
        cell_scaled = skimage.transform.rescale(cell_cropped, scale = ratio, anti_aliasing=False)
    except:
        return "Error Scaling"
    cell_scaled = np.where(cell_scaled > 0.5, 1, 0)
    # Establishing the backdrop
    background = np.zeros((bounds, bounds)) # backdrop
    # Fitting the scaled cell into the backdrop
    if cell_scaled.shape[0] == bounds - 2:
        if cell_scaled.shape[1] % 2 == 0:
            spacing = (bounds - cell_scaled.shape[1]) // 2
            background[1:-1, spacing:-spacing] = cell_scaled
        else:
            spacing = (bounds - cell_scaled.shape[1]) // 2
            background[1:-1, spacing:-(spacing + 1)] = cell_scaled
    else:
        if cell_scaled.shape[0] % 2 == 0:
            spacing = (bounds - cell_scaled.shape[0]) // 2
            background[spacing:-spacing, 1:-1] = cell_scaled
        else:
            spacing = (bounds - cell_scaled.shape[0]) // 2
            background[spacing:-(spacing + 1), 1:-1] = cell_scaled
    sanity_check = skimage.measure.label(background)
    sanity_check = skimage.morphology.remove_small_objects(sanity_check, min_size=250)
    try:
        assert len(np.unique(sanity_check)) == 2 # should be background + cell
        cell_image_resized = skimage.filters.gaussian(sanity_check, sigma=0.5, preserve_range=True) # getting the final product
        return cell_image_resized
    except:
        # print(f'Error at Cell Index: {cell_index}')
        if max_row - min_row <= 10 or max_col - min_col <= 10:
            return "too small, resulted in multiple cells"
        return "multiple cells"
    return background