import argparse
import gzip
import json
import csv
import pandas as pd

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("verbs_in", help = "gz.jsonl with verbs")
	parser.add_argument("neg_out", help = "csv negative score lines")
	parser.add_argument("--thresh", type=int, default=0, help="Pull below this threshold")

	args = parser.parse_args()

	df = pd.read_json(args.verbs_in, lines=True, compression="gzip")

	df["score"] = pd.to_numeric(df["score"], errors="coerce")
	df = df[df["score"] <= args.thresh]

	df.to_csv(args.neg_out)
