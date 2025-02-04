import argparse
import json
import gzip
import csv
import pandas as pd
import math

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("verbs_in", help = "gz.jsonl containing sentences, metadata, verbs and frequency")
	parser.add_argument("verbs_out", help = "csv containing verb data")
	parser.add_argument("--thresh", type=int, default=1, help="AS threshold")

	args = parser.parse_args()

	df = pd.read_json(args.verbs_in, lines=True, compression="gzip")

#	df.groupby("verbs")
	df.sort_values("verbs", ascending=True)
	df["score"] = pd.to_numeric(df["score"], errors="coerce")
	print(df["verbs"].value_counts())
	df = df[df["verbs"].map(df["verbs"].value_counts()) > args.thresh]
#	df = df[df["score"] >=1]
#			df["score"].dropna().mean()
	df.sort_values(["verbs", "word", "score"], ascending=[True, True, False], inplace=True)
	print(df)
	#df.to_csv(args.verbs_out)

