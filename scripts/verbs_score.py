import argparse
import json
import gzip
import pandas as pd
import math

if __name__ == __"main"__:
	parser = argparse.ArgumentParser()
	parser.add_argument("verbs_in", help = "gz.jsonl containing sentences, metadata, verbs and frequency")
	parser.add_argument("verbs_out", help = "csv containing verb data")

	args, other = parser.parse_known_args()

	df = pd.read_json(args.verbs_in, lines=True)

-	df.groupby("verbs")
	df.sort_values("verbs", ascending=False)
	if df["verbs"]>=1:
		df["score"].mean().sort_values()
		df.mean("score")
		df.to_csv(args.verbs_out)

