import pandas as pd
import random
from optparse import OptionParser
from pathlib import Path
import ntpath


def fragment(fpath, fragment_size):
    content = pd.read_csv(fpath, header=0)
    n = len(content)
    s = fragment_size
    skip = sorted(random.sample(range(1, n + 1), n - s))
    df = pd.read_csv(fpath, skiprows=skip)
    return df


parser = OptionParser()

parser.add_option(
    "-p",
    "--prefix",
    dest="prefix",
    default="fragment",
    help="prefix",
    metavar="STRING",
)
parser.add_option(
    "-f",
    "--fragments",
    dest="fragments",
    default=1,
    help="number of fragments",
    metavar="INT",
)
parser.add_option(
    "-s",
    "--size",
    dest="size",
    default=5,
    help="size of fragments",
    metavar="INT",
)
parser.add_option(
    "-o",
    "--outdir",
    dest="outdir",
    default=".",
    help="size of fragments",
    metavar="INT",
)
(options, args) = parser.parse_args()

Path(options.outdir).mkdir(parents=False, exist_ok=True)
for arg in args:
    for i in range(int(options.fragments)):
        df = fragment(arg, int(options.size))
        basename = ntpath.basename(arg)
        df.to_csv(f"{options.outdir}/{basename}.{options.prefix}{i}.csv")
