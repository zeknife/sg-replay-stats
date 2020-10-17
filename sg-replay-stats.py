import glob
import os
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm 

data_filename = 'rndlen.npy'

# Function to get length of replay
def lenFun(filename):
    try:
        with open(filename, "rb") as f:
            b_read = f.read()
            length = b_read[3] + (b_read[4] << 8) # Bytes 3-4, little endian
        return length
    except Exception as e:
        pass
        #print(f"Invalid replay {filename}")

def genLenArr():
    # Get all replays in folder or subfolders
    filepaths = glob.glob(f"./**/*.rnd", recursive=True)
    paths = np.array(filepaths) #Useful for output...
    print(f"Got {len(filepaths)} replay filepaths.")

    # Get array of all replay lengths
    lengths = np.array(list(map(lenFun, tqdm(filepaths))),dtype=float)

    # Remove NaN elements
    paths = paths[~np.isnan(lengths)]
    lengths = lengths[~np.isnan(lengths)]

    # Remove 0 elements
    paths = paths[np.argwhere(lengths)]
    lengths = lengths[np.argwhere(lengths)]
    print(f"Read {len(lengths)} replays")

    return lengths,paths

######################################################################

if __name__ == "__main__":
    try:
        with open(data_filename, 'rb') as f:
            lengths = np.load(f)
            paths = np.load(f)
            print(f"Successfuly read {data_filename}.")
    except FileNotFoundError:
        print(f"File {data_filename} not found. Generating.")
        lengths,paths = genLenArr()
        with open(data_filename, 'wb') as f:
            np.save(f, lengths)
            np.save(f, paths)
            print(f"Successfuly wrote {data_filename}.")


    # Stats time!!
    # Calculate your stuff
    maxlength = np.amax(lengths)
    minlength = np.min(lengths)
    avglength = np.mean(lengths)
    longest = paths[np.argmax(lengths)]
    shortest = paths[np.argmin(lengths)]

    # Print your stuff
    print(f"Max replay length: {maxlength:.0f} frames, ~{maxlength/72:.2f} seconds")
    print(f"Min replay length: {minlength:.0f} frames, ~{minlength/72:.2f} seconds")
    print(f"Avg replay length: {avglength:.2f} frames, ~{avglength/72:.2f} seconds")
    print(f"Longest replay: {longest}")
    print(f"Shortest replay: {shortest}")

    # Blabla... outlier stuff. maybe make a function for this
    # percentile = np.percentile(lengths, 0.01)
    # percentileupper = np.percentile(lengths, 99.9)
    # print(percentile)
    # outliers = lengths[lengths < percentile]
    # outlierpaths = paths[lengths < percentile]
    # print(len(outliers))
    # print(outliers)
    # print(outlierpaths)

    # Time for a plot. Adjust lengths from frames to seconds
    ls = lengths/72
    # Plot histogram
    count, bins, ignored = plt.hist(ls, bins=100, range=(percentile/72, percentileupper/72), density=True)#, weights=np.ones(len(ls)) / len(ls))
    #plt.gca().yaxis.set_major_formatter(PercentFormatter(1))

    # Plot the normal distribution curve
    mu = avglength/72
    sigma = np.std(lengths/72)
    plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (bins - mu)**2 / (2 * sigma**2) ), linewidth=3, color='y')

    plt.title(f"SG2E Match Durations\n mu={mu:.2f}, sigma={sigma:.2f}")
    plt.xlabel('Duration (Seconds)')
    plt.ylabel('Density')

    plt.show()