import argparse
import gzip
import json
import pandas as pd
import math

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("verbs_in", help = "csv ")
	parser.add_argument("sorted_out", help = "csv containing verbs sorted by author")

	args = parser.parse_args()

	df = pd.read_json(args.verbs_in, lines=True)

	df.groupby("verbs")
	df.sort_values("verbs", ascending=False)
	author_sort = df.groupby("author")["verbs"]

	df["score"] = df["score"].map(lambda a: pd.to_numeric(a, errors='coerce'))
	df = df.dropna()

	verb_means = df.groupby("authors")["verbs"].mean().sort_values()

	df.to_csv(args.sorted_out)

