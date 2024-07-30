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

	df.groupby("verbs")
	df.sort_values("verbs", ascending=False)
	if df["verbs"]>=1:
		df.mean().sort_values()
		df.to_csv(args.verbs_out)
		verb_count = doc["verbs"].countby(token.pos_)
		for token in verb_count:
			if verb_count[0] >1:
				verb_count.to_csv(args.verbs_out)
