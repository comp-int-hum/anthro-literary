import argparse
import json
import re
import gzip
import csv

def tokenize_segment(segment_text):
	sents = re.split(r" *(?<=[\.\?!]) [\'\"\)\]]* *", segment_text)
	#sents = re.split(r" *[\.\?!][\'\"\)\]]* *", segment_text)
	return sents

if __name__== "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--input", help = "jsonl or csv containing corpus and metadata")
	parser.add_argument("--outputs", help = "jsonl containing sentences with metadata")
	parser.add_argument("--id", help = "field to include as id in output gzjsonl", default="acl_id")
	args = parser.parse_args()

	with open(args.input, "rt") as corpus_in, gzip.open(args.outputs, "wt") as corpus_out:
		if args.input.endswith(".csv"):
			cr = csv.DictReader(corpus_in)
			for line in cr:
				corpus_out.write(json.dumps({"full_text": tokenize_segment(line["abstract"]), "id": line[args.id]}) + "\n")
				
		elif args.input.endswith(".jsonl"):
			n_e = 0
			for line in corpus_in:
				try:
					jl = json.loads(line)
					jl["full_text"] = []
					for segment in jl["segments"].values():
						for segment_text in segment:
							sents = tokenize_segment(segment_text)
							jl["full_text"] += sents
					corpus_out.write(json.dumps(jl)+"\n")
				except json.decoder.JSONDecodeError:
					n_e += 1
					continue
			print(n_e)
