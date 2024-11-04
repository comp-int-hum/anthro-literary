import argparse
import gzip
import json
import csv
import pandas as pd
import math

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("verbs_in", help = "csv with bert and roberta score differences")
	parser.add_argument("averaged", help = "csv with mean difference between bert and roberta scores")

	args = parser.parse_args()

	df = pd.read_csv(args.verbs_in)

	df["difference"] = pd.to_numeric(df["difference"], errors="coerce")
	mean_diff = df["difference"].mean()
#	df.reset_index().sort_values("word")
	mean = [mean_diff]
	out_df = pd.DataFrame(mean)
	out_df.to_csv(args.averaged)
