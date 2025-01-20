import argparse
import gzip
import json
import csv
import pandas as pd
import math

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("verbs_in", help = "gz.jsonl with verb frequencies")
	parser.add_argument("stats_out", help = "csv with statistics on frequency")

	args = parser.parse_args()

	with gzip.open(args.embed_in, "rt") as e_in:
		loaded_json = [{"score": json.loads(line)["score"]} for line in e_in]
		df = pd.DataFrame(loaded_json)

		df["score"] = pd.to_numeric(df["score"], errors="coerce")
		neg = df[df["score"] < 0]
		print(neg)
		neg_counts = neg.count()
		pos = df[df["score"] > 0]
		pos_counts = pos.count()
		count = df[df.columns[0]].count()
		pos_ratio = pos_counts/count
		neg_ratio = neg_counts/count
		out_df = pd.DataFrame()
		out_df["positive percent"] = pos_ratio
		out_df["negative percent"] = neg_ratio

		out_df.to_csv(args.stats_out)
