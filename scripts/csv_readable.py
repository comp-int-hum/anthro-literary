import argparse
import json
import re
import gzip
import csv
import pandas as pd


if __name__== "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--input", help = "gzip jsonl")
	parser.add_argument("--outputs", help = "csv for human reading")
	
	args = parser.parse_args()

	with gzip.open(args.input, "rt") as corpus_in:
                lines = [json.loads(line) for line in corpus_in]
                df = pd.DataFrame(lines)
                
                df.to_csv(args.outputs, index=False)
