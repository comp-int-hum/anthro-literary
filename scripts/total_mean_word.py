import argparse
import gzip
import json
import csv
import pandas as pd
import math

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("verbs_in", help = "gz.jsonl with verb frequencies")
	parser.add_argument("averaged", help = "csv with mean score per author")

	args = parser.parse_args()

	df = pd.read_json(args.verbs_in, lines=True, compression="gzip")

	df["score"] = pd.to_numeric(df["score"], errors="coerce")
	df = df.groupby("word")["score"].mean()
	df.reset_index().sort_values("word")
	df.to_csv(args.averaged)
