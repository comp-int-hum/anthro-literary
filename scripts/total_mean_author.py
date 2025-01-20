import argparse
import gzip
import json
import csv
import pandas as pd
import math

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("embed_in", help = "gz.jsonl with embeddings")
	parser.add_argument("averaged", help = "csv with mean score per author")

	args = parser.parse_args()

	with gzip.open(args.embed_in, "rt") as e_in:
		loaded_json = [{"score": json.loads(line)["score"], "author": json.loads(line)["author"]} for line in e_in]
		df = pd.DataFrame(loaded_json)

		df["score"] = pd.to_numeric(df["score"], errors="coerce")
		df = df.groupby("author")["score"].mean()
		df.reset_index().sort_values("author")
		df.to_csv(args.averaged)
