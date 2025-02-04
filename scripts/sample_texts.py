import argparse
import json
import re
import gzip
import csv
import random


if __name__== "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--input", help = "jsonl or csv containing corpus and metadata")
	parser.add_argument("--outputs", help = "jsonl containing sentences with metadata")
	parser.add_argument("--nsamp", type=int, default = 0, help = "n texts")
	parser.add_argument("--random_state",type=int,default=29)
	args = parser.parse_args()

	random.seed(args.random_state)

	with gzip.open(args.input, "rt") as corpus_in, gzip.open(args.outputs, "wt") as corpus_out:
		all_texts = []
		for line in corpus_in:
			all_texts.append(json.loads(line))
		all_texts = random.sample(all_texts, args.nsamp) if args.nsamp != 0 else all_texts
		for text in all_texts:
			corpus_out.write(json.dumps(text)+"\n")
