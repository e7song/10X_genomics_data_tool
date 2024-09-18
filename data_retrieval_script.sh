#!/bin/bash

# exit at any error
set -e 

# get the URL
echo "Insert URL: "
read URL

# get the directory
echo "Insert Directory Location: "
read DIRECTORY

# start the downloading
echo "Starting Script: "`date`
echo "Downloading from $URL. Are you in the correct directory? [y/n]"
read CONTINUE_DOWNLOAD

if [$CONTINUE_DOWNLOAD != 'y']; then
    
fi



echo "Testing $URL and $DIRECTORY"

# todo:
# py get_data.py $URL $DIRECTORY
#
# Planned Hierarchy:
# DIRECTORY
#  --> LOG FILE (TEXT)
#  --> CELL_ID_SUCCESS? (TEXT)
#  --> CELL_ID_FAILURE (TEXT)
#  --> IMAGES (DIRECTORY)
#  	--> TIFF FILES
# 
#
# du -sh >> LOG FILE (make sure there is a newline separating the existing contents
#
# Planned Outputs:
#   -- time it took to run
#   -- size of image directory
#   -- how many cells threw an error
#   -- what percentage of the cells were converted
#   	-- total number of cells
#
