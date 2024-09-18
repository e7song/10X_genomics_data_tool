#!/bin/bash

# exit at any error
# set -e 

# get the URL
echo "Insert URL: "
read URL

# get the directory
echo "Insert Directory Location: "
read DIRECTORY

# start the downloading
echo "Starting Script: "$(date)
echo "Downloading from $URL. Are you in the correct directory? [y/n]"
read CONTINUE_DOWNLOAD

if [ "$CONTINUE_DOWNLOAD" != 'y' ]; then
    echo "Early Exit"
    exit 0
fi

if [ -d "DIRECTORY" ]; then
    echo "Downloading to $DIRECTORY"
    DELETE_DIR_ON_ERR=1 # don't delete the users pre-created directory
else
    echo "Creating $DIRECTORY"
    mkdir -p "$DIRECTORY"
    DELETE_DIR_ON_ERR=0 # delete the directory
fi

wget $URL

# additional comments: maybe filter for the size of the directory? need to look more into this

if [ $? -eq 0 ]; then # checking the success of wget
    echo "Download successfully finished at: "$(date)
else
    echo "Something went wrong with the download."
    echo "Exited at: "$(date)
    if [ DELETE_DIR_ON_ERR -eq 0 ]; then
        rm -rf "$DIRECTORY" # dangerous? might delete all the data... maybe query user decision?
        rmdir "$DIRECTORY"
    exit 1
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
