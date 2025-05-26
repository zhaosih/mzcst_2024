import sys

import mzcst_2024 as mz

if __name__ == "__main__":
    # This is a demo script to show how to use mzcst
    for i, p in enumerate(sys.path):
        print(f"{i:2d}: {p}")
    print(mz.__version__)
    print(mz.__file__)   

    pass
