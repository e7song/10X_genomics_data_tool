import sys
from datetime import datetime
import os

def log_progress(message): # credits, learned/implemented this from an IBM course
    timestamp_format = '%Y-%h-%d-%H:%M:%S' # Year-Monthname-Day-Hour-Minute-Second 
    now = datetime.now()
    timestamp = now.strftime(timestamp_format)
    log_path = './logs.txt'
    with open(log_path, 'a') as f:
        f.write(timestamp + ' : ' + message + '\n')
    f.close()

def process():
    pass

if __name__ == "__main__":
    # input format:
    # py get_data.py [link?] [save directory?]

    # download, check if download is successful

    # unzip to save directory, if save directory does not exist prompt user to save to the directory specified?

    pass