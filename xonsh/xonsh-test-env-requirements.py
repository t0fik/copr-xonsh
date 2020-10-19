import sys
import argparse
from pkg_resources import get_distribution, DistributionNotFound

parser = argparse.ArgumentParser()
parser.add_argument("--output", type=str, nargs="?", required=True)
parser.add_argument("deps", nargs=argparse.REMAINDER)
parsed = parser.parse_args(sys.argv[1:])

with open(parsed.output, "w") as fp:
    for dep in parsed.deps:
        try:
            version = get_distribution(dep).version
            print(f"{dep}=={version}", file=fp)
        except DistributionNotFound:
            pass
    print("pytest>=5.4", file=fp)

