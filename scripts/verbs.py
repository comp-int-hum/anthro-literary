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

	args = parser.parse_args()

	df = pd.read_json(args.verbs_in, lines=True, compression="gzip")

	df.sort_values(["verbs", "word"], ascending=[True, True], inplace=True)
	print(df["verbs"].head(25))
	df["score"] = pd.to_numeric(df["score"], errors="coerce")
#	if (df["verbs"].value_counts() >=1).any():
	df = df[df["score"] >=1]
	df["score"].dropna().mean()
	df.sort_values(["verbs", "word", "score"], ascending=[True, True, False], inplace=True)
	df.to_csv(args.verbs_out)
#		verb_count = doc["verbs"].countby(token.pos_)
#		for token in verb_count:
#			if verb_count[0] >1:
#				verb_count.to_csv(args.verbs_out)
