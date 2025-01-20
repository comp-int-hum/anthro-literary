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
		loaded_json = [{"score": json.loads(line)["score"], "word": json.loads(line)["word"]} for line in e_in]
		loaded_df = pd.DataFrame(loaded_json)

		loaded_df["score"] = pd.to_numeric(loaded_df["score"], errors="coerce")
		loaded_df = loaded_df.groupby("word")["score"].mean()
		loaded_df.reset_index().sort_values("word")
		loaded_df.to_csv(args.averaged)
