#!/bin/bash
echo "Insert URL: "
read URL

echo "Insert Directory Location: "
read DIRECTORY

echo "Starting Script: "`date`

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
