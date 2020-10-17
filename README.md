# sg-replay-stats
Let's do fun statistics with Skullgirls replays!

Currently it will do the following:
* Show max, min, and mean replay length in frames and seconds
* Display the paths to the longest and shortest replays in your collection
* Display a histogram and normal distribution fit of the replay lengths

HOW TO USE:
Place sg-replay-stats.py in a folder containing Skullgirls 2nd Encore replay files. It will search recursively in any subfolders as well. It generates a file to store the replay durations and associated filepaths so it might take a while on the first run.

REQUIREMENTS:
Python 3.6+
Python packages: numpy, matplotlib, tqdm
