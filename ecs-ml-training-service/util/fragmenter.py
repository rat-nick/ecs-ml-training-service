import pandas as pd
import random
from optparse import OptionParser


def fragment(fpath, fragment_size):
    content = pd.read_csv(fpath, header=0)
    n = len(content)
    s = fragment_size
    skip = sorted(random.sample(range(1, n+1), n-s))
    df = pd.read_csv(fpath, skiprows=skip)
    return df

#TODO: function to create n random fragments of a file

parser = OptionParser()
#parser.add_option("-i", "--input", dest="input", default='stdin', help="input file", metavar="FILE")
parser.add_option("-p", "--prefix", dest="prefix", default="fragment", help="prefix", metavar="STRING")
parser.add_option("-f", "--fragments", dest="fragments",default=1, help="number of fragments", metavar="INT")
parser.add_option("-s", "--size", dest="size",default=5, help="size of fragments", metavar="INT")
parser.add_option("-o", "--outdir", dest="outdir", default='.', help="size of fragments", metavar="INT")
(options, args) = parser.parse_args()

for arg in args:
    for i in range(int(options.fragments)):
        df = fragment(arg, int(options.size))
        df.to_csv(f'{options.outdir}/{arg}.{options.prefix}{i}.csv')