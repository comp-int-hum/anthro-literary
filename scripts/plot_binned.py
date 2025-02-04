import argparse
import gzip
import json
import csv
import pandas as pd
import math
import matplotlib.pyplot as plt


if __name__ == "__main__":
        parser = argparse.ArgumentParser()
        parser.add_argument("--inputs", nargs="+")
        parser.add_argument("--row", default="percent")
        parser.add_argument("--indices", nargs="+")
        parser.add_argument("--output")

        rows = []
        args = parser.parse_args()
        for i in args.inputs:
                df = pd.read_csv(i, index_col=[0])
                rows.append(df.loc["percent"])
        out_df = pd.concat(rows, axis=1).T
        print(out_df)
        print(args.indices)
        out_df.index = args.indices
        ax = out_df.T.plot(kind="bar",rot=0)
        plt.xlabel("Score")
        plt.ylabel("Percent")
        plt.tight_layout()
        plt.savefig(args.output)
        print(out_df)
