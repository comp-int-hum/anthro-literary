import argparse
import gzip
import json
import csv
import pandas as pd
import math

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("verbs_in", help = "gzip containing verb frequency output")
	parser.add_argument("sorted_out", help = "csv containing verbs sorted by author")

	args = parser.parse_args()

	df = pd.read_json(args.verbs_in, lines=True, compression="gzip")

	print(df["verbs"].head())
#	df.groupby("verbs")
	df.sort_values(by=["author", "verbs"], ascending=[False, True], inplace=True)
	print(df["verbs"].head(25))

	df["score"] = pd.to_numeric(df["score"], errors="coerce")

	if (df["score"] >=1).any():
		df.groupby("author")["verbs"].mean().sort_values()
		df.to_csv(args.sorted_out)
	elif df["score"].isna().any():
		df.to_csv(args.sorted_out)
