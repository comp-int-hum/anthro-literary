import argparse
import gzip
import json
import csv
import pandas as pd

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--input", help = "gz.jsonl with verbs")
	parser.add_argument("--output_wv", help = "csv")
	parser.add_argument("--output_avw")

	args = parser.parse_args()

	df = pd.read_json(args.input, lines=True, compression="gzip")

	avgs = []
	auths = []
	for name, group in df.groupby(["verb"]):
		avgs.append({"verb": name[0], "mean": group["score"].mean(), "count": len(group["score"])})
		for auth, g2 in group.groupby(["author"]):
			auths.append({"author": auth[0], "verb": name[0], "mean": g2["score"].mean(), "count": len(g2["score"])})

	avg_df = pd.DataFrame.from_records(avgs)
	print(avg_df)
	auth_df = pd.DataFrame.from_records(auths)
	print(auth_df)
	avg_df.to_csv(args.output_wv)
	auth_df.to_csv(args.output_avw)
        
