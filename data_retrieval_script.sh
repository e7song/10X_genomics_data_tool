#!/bin/bash

# exit at any error
# set -e 

# get the URL
echo "Insert URL: "
read URL

# get the directory
echo "Insert Directory Location: "
read DIRECTORY

# creating log file
log_file="logs_$(date "+%m_%d_%y").txt"
touch $log_file

# start the downloading
curr_date=$(date)
# echo "Starting Script: $curr_date"
echo "Starting Script: $curr_date" >> "$log_file"

echo -e "\n=====\n"

echo "Downloading from $URL. Are you in the correct directory? [y/n]"
read CONTINUE_DOWNLOAD

if [ "$CONTINUE_DOWNLOAD" != 'y' ]; then
    echo "Early Exit"
    rm $log_file
    exit 0
fi

if [ -d "DIRECTORY" ]; then # bad code here <<
    echo -e "\n=====\n"
    echo "Downloading to $DIRECTORY" >> "$log_file"
else
    echo -e "\n=====\n"
    echo "Creating $DIRECTORY" >> "$log_file"
    mkdir -p "$DIRECTORY" # -p flag makes the first if statement redundant
fi

wget -P "$DIRECTORY" "$URL"

# additional comments: maybe filter for the size of the directory? need to look more into this

if [ $? -eq 0 ]; then # checking the success of wget
    echo "Download successfully finished at: "$(date) >> $log_file
else
    echo "Something went wrong with the download."
    echo "Exited at: "$(date) 
    rm "$log_file"
    if [ "$(ls -A "$DIRECTORY")" ]; then
        echo "Directory is not empty; check contents before removing."
    else
        echo "Directory is empty. Removing $DIRECTORY"
        rmdir "$DIRECTORY"
    fi
    exit 1
fi

echo -e "\n=====\n" >> "$log_file"

echo -e "Starting unzip at $(date)" >> "$log_file"

zip_location="$DIRECTORY"/*.zip

unzip -d "$DIRECTORY" "$zip_location"


if [ $? -eq 0 ]; then # checking the success of unzip
    echo "Unzip successfully finished at: "$(date) >> "$log_file"
else
    echo "Something went wrong with the unzip."
    echo "Exited at: "$(date)
    rm "$log_file"
    if [ "$(ls -A "$DIRECTORY")" ]; then
        echo "Directory is not empty; check contents before removing."
    else
        echo "Directory is empty. Removing $DIRECTORY"
        rmdir "$DIRECTORY"
    fi
    exit 1
fi

echo "PAUSED FOR TESTING"
read $end_test

echo "Testing $URL and $DIRECTORY"
echo $(ls -A "$DIRECTORY")

# new note 9/25/24: maybe echo all of the information into a logs file for clarity

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