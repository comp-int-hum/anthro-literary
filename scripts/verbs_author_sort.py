import argparse
import gzip
import json
import csv
import pandas as pd

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("verbs_in", help = "gz.jsonl with verb frequencies")
	parser.add_argument("sorted_out", help = "csv containing verbs sorted by author")

	args = parser.parse_args()

	df = pd.read_json(args.verbs_in, lines=True, compression="gzip")
#	print("data frame loaded")

#	print(df["score"].head())
	df["verbs"].value_counts()
	print(df["verbs"].head(8))
	print(df["score"].head())
	if df["score"].any() == "error":
		print("all error")
	df["score"] = pd.to_numeric(df["score"], errors="coerce")
	print(df["score"].head())
	if df["score"].isna().all():
		print("is na")

#	if (df["score"] >=1).any():
#		if df["verbs"] >=1:
#		df.groupby("verbs")
	df = df[df["score"] >=1]
	df.groupby("verbs")
	df.sort_values("verbs", ascending=False)
	df.groupby("author")["verbs"]
	df.to_csv(args.sorted_out)
#	elif df["score"].isna().any():
#		print("none")
