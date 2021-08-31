import pandas as pd
import random
from optparse import OptionParser

# TODO: function to get a random subset of rows from a .csv as dataframe
def fragment(fpath, fragment_size):
    content = pd.read_csv(fpath, header=0)
    n = len(content)
    s = fragment_size
    skip = sorted(random.sample(range(1, n+1), n-s))
    df = pd.read_csv(fpath, skiprows=skip)
    return df

#TODO: function to create n random fragments of a file

#TODO: create module entry
    