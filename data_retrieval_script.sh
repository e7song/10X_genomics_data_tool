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
else
    echo "Creating $DIRECTORY"
    mkdir -p "$DIRECTORY"
fi

wget -P "$DIRECTORY" "$URL"

# additional comments: maybe filter for the size of the directory? need to look more into this

if [ $? -eq 0 ]; then # checking the success of wget
    echo "Download successfully finished at: "$(date)
else
    echo "Something went wrong with the download."
    echo "Exited at: "$(date)
    if [ "$(ls -A "$DIRECTORY")" ]; then
        echo "Directory is not empty; check contents before removing."
    else
        echo "Directory is empty. Removing $DIRECTORY"
        rmdir "$DIRECTORY"
    fi
    exit 1
fi

echo "Starting unzip at $(date)"

zip_location="$DIRECTORY"/*.zip

unzip -d "$DIRECTORY" $zip_location


if [ $? -eq 0 ]; then # checking the success of wget
    echo "Unzip successfully finished at: "$(date)
else
    echo "Something went wrong with the unzip."
    echo "Exited at: "$(date)
    if [ "$(ls -A "$DIRECTORY")" ]; then
        echo "Directory is not empty; check contents before removing."
    else
        echo "Directory is empty. Removing $DIRECTORY"
        rmdir "$DIRECTORY"
    fi
    exit 1
fi


echo "Testing $URL and $DIRECTORY"
echo $(ls -A "$DIRECTORY")

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


# 09/17
# want to test with a zip file