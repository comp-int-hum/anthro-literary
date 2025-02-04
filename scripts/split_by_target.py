import argparse
import gzip
import json
import csv
import pandas as pd
import math

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--input", help = "gz.jsonl with verb frequencies")
	parser.add_argument("--outputs", help = "")
	parser.add_argument("--col")

	args = parser.parse_args()

	with gzip.open(args.input, "rt") as e_in, gzip.open(args.outputs, "wt") as i_out:
		for line in e_in:
			jline = json.loads(line)
			if jline["word"] == args.col:
				i_out.write(json.dumps(jline)+"\n")
